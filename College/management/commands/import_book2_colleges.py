"""
Import Book2 college Excel into DB with mapping + dry-run.

Excel has swapped-ish semantics vs portal masters:
  organization_type column = 'Medical' (course area)
  college_type column = 'Private Medical College' / Trust / Society

Portal needs:
  organization_type = Private / Government
  college_type = Medical
  course_categories = Medical

Usage:
  python manage.py import_book2_colleges Book2_Arranged_According_to_College_Template.xlsx
  python manage.py import_book2_colleges Book2....xlsx --commit
  python manage.py import_book2_colleges Book2....xlsx --limit 5 --commit
"""
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from openpyxl import load_workbook

from Auth.models import CollegeAdmin
from College.models import College
from College.resources import _placeholder, _unique_mobile, ensure_college_user
from General.models import CollegeType, CourseCategory, OrganizationType
from Main.models import Country, State


STATE_ALIASES = {
    "pondicherry": "Puducherry",
    "orissa": "Odisha",
    "uttaranchal": "Uttarakhand",
    "delhi": "Delhi",
    "nct of delhi": "Delhi",
    "jammu & kashmir": "Jammu and Kashmir",
    "jammu and kashmir": "Jammu and Kashmir",
    "andaman & nicobar islands": "Andaman and Nicobar Islands",
    "dadra & nagar haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "daman & diu": "Dadra and Nagar Haveli and Daman and Diu",
}


def _first_token(value):
    if value is None:
        return ""
    text = str(value).strip()
    if not text:
        return ""
    # split multi contact "a, b" or "a / b"
    for sep in [",", "/", ";", "|"]:
        if sep in text:
            text = text.split(sep)[0].strip()
            break
    return text


def _map_org_type(college_type_cell: str) -> str:
    t = (college_type_cell or "").lower()
    if "gov" in t or "government" in t:
        return "Government"
    return "Private"


class Command(BaseCommand):
    help = "Import Book2 arranged college Excel (dry-run by default)."

    def add_arguments(self, parser):
        parser.add_argument("xlsx", type=str, help="Path to Book2 xlsx")
        parser.add_argument(
            "--commit",
            action="store_true",
            help="Actually write to DB (default is dry-run).",
        )
        parser.add_argument("--limit", type=int, default=0, help="Import only first N rows")
        parser.add_argument("--sheet", type=str, default=None, help="Sheet name (optional)")

    def handle(self, *args, **options):
        path = Path(options["xlsx"])
        if not path.exists():
            raise CommandError(f"File not found: {path}")

        commit = options["commit"]
        limit = options["limit"]

        org_private, _ = OrganizationType.objects.get_or_create(name="Private")
        org_govt, _ = OrganizationType.objects.get_or_create(name="Government")
        college_type, _ = CollegeType.objects.get_or_create(name="Medical")
        category, _ = CourseCategory.objects.get_or_create(name="Medical")
        country = Country.objects.filter(name__iexact="India").first()
        if not country:
            country = Country.objects.create(name="India")

        wb = load_workbook(path, data_only=True)
        ws = wb[options["sheet"]] if options["sheet"] else wb.active
        headers = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
        idx = {h: i for i, h in enumerate(headers) if h}

        required = [
            "college_user", "name", "organization_type", "college_type",
            "rank", "established_year", "overview", "city",
        ]
        missing_cols = [c for c in required if c not in idx]
        if missing_cols:
            raise CommandError(f"Missing columns: {missing_cols}")

        self.stdout.write(self.style.WARNING(
            "DRY-RUN" if not commit else "COMMIT MODE — writing to DB"
        ))

        created = updated = skipped = errors = 0
        email_seen = {}
        report = []

        rows = list(ws.iter_rows(min_row=2, values_only=True))
        if limit and limit > 0:
            rows = rows[:limit]

        def process_all():
            nonlocal created, updated, skipped, errors
            for row_no, row in enumerate(rows, start=2):
                if not row or not row[idx["name"]]:
                    skipped += 1
                    continue
                try:
                    name = str(row[idx["name"]]).strip()
                    email = str(row[idx["college_user"]] or "").strip().lower()
                    rank = int(row[idx["rank"]])
                    year = int(float(row[idx["established_year"]]))
                    city = str(row[idx["city"]] or "").strip()
                    overview = str(row[idx["overview"]] or "").strip()
                    affiliation = str(row[idx.get("affiliation", -1)] or "").strip() if "affiliation" in idx else ""
                    rating = row[idx["rating"]] if "rating" in idx else 4
                    slug = str(row[idx["slug"]] or "").strip() if "slug" in idx else ""
                    meta_title = str(row[idx["meta_title"]] or "").strip() if "meta_title" in idx else name
                    website = str(row[idx["website"]] or "").strip() if "website" in idx else ""
                    contact_email = _first_token(row[idx["email"]]) if "email" in idx else ""
                    mobile = _first_token(row[idx["primary_mobile"]]) if "primary_mobile" in idx else ""
                    mobile = "".join(c for c in mobile if c.isdigit())[-10:] if mobile else ""
                    state_name = str(row[idx["state"]] or "").strip() if "state" in idx else ""
                    address = str(row[idx["address"]] or "").strip() if "address" in idx else ""
                    ctype_cell = str(row[idx["college_type"]] or "").strip()

                    if not email or "@" not in email:
                        raise ValueError("invalid college_user email")
                    # Fix duplicate emails only within this Excel file
                    if email in email_seen:
                        base_local, domain = email.split("@", 1)
                        suffix = 2
                        candidate = f"{base_local}-{suffix}@{domain}"
                        while candidate in email_seen:
                            suffix += 1
                            candidate = f"{base_local}-{suffix}@{domain}"
                        self.stdout.write(
                            self.style.WARNING(
                                f"Row {row_no}: duplicate email '{email}' → '{candidate}'"
                            )
                        )
                        email = candidate
                    email_seen[email] = row_no

                    org_name = _map_org_type(ctype_cell)
                    org = org_govt if org_name == "Government" else org_private

                    state = None
                    if state_name:
                        alias = STATE_ALIASES.get(state_name.lower(), state_name)
                        state = State.objects.filter(name__iexact=alias, country=country).first()
                        if not state:
                            state = State.objects.create(name=alias, country=country)

                    # Build fake row for ensure_college_user helpers
                    fake_row = {
                        "college_user": email,
                        "user_name": f"{name} Admin",
                        "user_mobile": mobile or _unique_mobile(email),
                        "user_password": "College@12345",
                        "name": name,
                        "city": city,
                    }
                    user = ensure_college_user(email, row=fake_row)

                    linked = College.objects.filter(college_user=user).first()
                    existing = College.objects.filter(name=name).first()
                    if linked and existing and linked.id != existing.id:
                        raise ValueError(
                            f"email already linked to other college '{linked.name}'"
                        )
                    if linked and not existing:
                        # update that college instead of creating second
                        existing = linked

                    if College.objects.filter(rank=rank).exclude(name=name).exists():
                        # find free rank
                        new_rank = rank
                        while College.objects.filter(rank=new_rank).exists():
                            new_rank += 1
                        rank = new_rank

                    defaults = dict(
                        college_user=user,
                        affiliation=affiliation or None,
                        organization_type=org,
                        college_type=college_type,
                        rank=rank,
                        rating=rating or 4,
                        established_year=year,
                        overview=overview,
                        city=city,
                        country=country,
                        state=state,
                        current_address=address,
                        primary_mobile=mobile or None,
                        email=contact_email or None,
                        website=website or None,
                        meta_title=meta_title[:200] if meta_title else name[:200],
                        slug=slug or None,
                    )

                    if existing:
                        for k, v in defaults.items():
                            if k == "college_user":
                                continue
                            setattr(existing, k, v)
                        if not existing.logo:
                            safe = "".join(c if c.isalnum() else "-" for c in name)[:40] or "college"
                            existing.logo.save(f"{safe}-logo.webp", _placeholder(f"{safe}-logo.webp"), save=False)
                        if not existing.image:
                            safe = "".join(c if c.isalnum() else "-" for c in name)[:40] or "college"
                            existing.image.save(
                                f"{safe}-image.webp",
                                _placeholder(f"{safe}-image.webp", size=(800, 450)),
                                save=False,
                            )
                        existing.save()
                        existing.course_category.add(category)
                        updated += 1
                        report.append((row_no, "UPDATE", name))
                    else:
                        obj = College(**defaults)
                        safe = "".join(c if c.isalnum() else "-" for c in name)[:40] or "college"
                        obj.logo.save(f"{safe}-logo.webp", _placeholder(f"{safe}-logo.webp"), save=False)
                        obj.image.save(
                            f"{safe}-image.webp",
                            _placeholder(f"{safe}-image.webp", size=(800, 450)),
                            save=False,
                        )
                        obj.save()
                        obj.course_category.add(category)
                        created += 1
                        report.append((row_no, "CREATE", name))
                except Exception as exc:
                    errors += 1
                    report.append((row_no, "ERROR", f"{row[idx['name']]}: {exc}"))
                    self.stderr.write(self.style.ERROR(f"Row {row_no}: {exc}"))

        if commit:
            with transaction.atomic():
                process_all()
        else:
            # dry-run still uses atomic + rollback so no lasting writes
            with transaction.atomic():
                process_all()
                transaction.set_rollback(True)

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Done. created={created} updated={updated} skipped={skipped} errors={errors}"
        ))
        if not commit:
            self.stdout.write(self.style.WARNING(
                "Dry-run only — DB me kuch save nahi hua. "
                "OK lage to: python manage.py import_book2_colleges <file> --commit"
            ))
        # show first few report lines
        for item in report[:20]:
            self.stdout.write(f"  {item}")
        if len(report) > 20:
            self.stdout.write(f"  ... +{len(report) - 20} more")
