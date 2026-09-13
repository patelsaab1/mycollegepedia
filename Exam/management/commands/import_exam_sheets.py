"""
Import research-style exam Excel sheets into Exam model.

Sheets have title rows + headers like:
  Exam Name | Exam Category | Conducting Authority | Official Website | ...

Portal Exam needs: title, course_category, full_form, description, meta_*.

Usage:
  python manage.py import_exam_sheets docs/Medical_Examinations_India.xlsx
  python manage.py import_exam_sheets docs/*.xlsx --commit
  python manage.py import_exam_sheets --docs-dir docs --commit
"""
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from openpyxl import load_workbook

from Exam.models import Exam
from General.models import CourseCategory


# filename keyword → CourseCategory.name
FILE_CATEGORY = {
    "engineering": "Engineering",
    "medical": "Medical",
    "management": "Management",
    "law": "Law",
}

# Alternate header labels → normalized key
HEADER_ALIASES = {
    "exam name": "exam_name",
    "exam category": "exam_category",
    "state / coverage": "coverage",
    "coverage": "coverage",
    "conducting authority": "authority",
    "admission level": "level",
    "level": "level",
    "main courses": "courses",
    "main course(s)": "courses",
    "main course / purpose": "courses",
    "institute type": "institute_type",
    "institution type": "institute_type",
    "primary admission coverage": "admission_coverage",
    "admission route": "admission_route",
    "counselling / admission authority": "counselling",
    "official website": "website",
    "notes": "notes",
    "status / notes": "notes",
}


def _clip(value, max_len):
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return text[:max_len]


def _cell(row, idx, key):
    i = idx.get(key)
    if i is None or i >= len(row):
        return ""
    v = row[i]
    return str(v).strip() if v is not None else ""


def _category_from_path(path: Path) -> str:
    name = path.name.lower()
    for key, cat in FILE_CATEGORY.items():
        if key in name:
            return cat
    raise CommandError(
        f"Cannot detect course category from filename: {path.name}. "
        "Expected Engineering/Medical/Management/Law in the name."
    )


def _find_header_row(ws):
    for i, row in enumerate(ws.iter_rows(min_row=1, max_row=15, values_only=True), start=1):
        if not row or not row[0]:
            continue
        if str(row[0]).strip().lower() == "exam name":
            return i, [c for c in row]
    raise CommandError("Header row with 'Exam Name' not found (expected around row 4).")


def _build_description(data: dict) -> str:
    lines = []
    mapping = [
        ("Exam category", "exam_category"),
        ("Level", "level"),
        ("Coverage", "coverage"),
        ("Conducting authority", "authority"),
        ("Main courses / purpose", "courses"),
        ("Admission route", "admission_route"),
        ("Admission coverage", "admission_coverage"),
        ("Institute type", "institute_type"),
        ("Counselling", "counselling"),
        ("Official website", "website"),
        ("Notes", "notes"),
    ]
    for label, key in mapping:
        val = (data.get(key) or "").strip()
        if val:
            lines.append(f"<li><strong>{label}:</strong> {val}</li>")
    if not lines:
        return ""
    return "<ul>\n" + "\n".join(lines) + "\n</ul>"


class Command(BaseCommand):
    help = "Import Engineering/Medical/Law/Management exam Excel sheets (dry-run by default)."

    def add_arguments(self, parser):
        parser.add_argument(
            "xlsx",
            nargs="*",
            type=str,
            help="One or more exam xlsx paths",
        )
        parser.add_argument(
            "--docs-dir",
            type=str,
            default=None,
            help="Import all *Examinations*.xlsx / *Examination*.xlsx from this folder",
        )
        parser.add_argument(
            "--commit",
            action="store_true",
            help="Write to DB (default is dry-run).",
        )
        parser.add_argument("--limit", type=int, default=0, help="Max rows per file")
        parser.add_argument(
            "--category",
            type=str,
            default=None,
            help="Force course_category name (overrides filename detection)",
        )

    def handle(self, *args, **options):
        paths = [Path(p) for p in options["xlsx"]]
        docs_dir = options["docs_dir"]
        if docs_dir:
            d = Path(docs_dir)
            if not d.is_dir():
                raise CommandError(f"Not a directory: {d}")
            found = sorted(
                set(d.glob("*Examinations*.xlsx")) | set(d.glob("*Examination*.xlsx"))
            )
            paths.extend(found)
        if not paths:
            raise CommandError(
                "Pass xlsx path(s) or --docs-dir docs"
            )

        commit = options["commit"]
        limit = options["limit"]
        force_cat = options["category"]

        self.stdout.write(self.style.WARNING(
            "DRY-RUN" if not commit else "COMMIT MODE — writing to DB"
        ))

        total_created = total_updated = total_skipped = total_errors = 0

        for path in paths:
            if not path.exists():
                raise CommandError(f"File not found: {path}")
            cat_name = force_cat or _category_from_path(path)
            category, _ = CourseCategory.objects.get_or_create(name=cat_name)
            self.stdout.write(self.style.NOTICE(f"\n=== {path.name} → {cat_name}"))

            c, u, s, e = self._import_file(path, category, commit=commit, limit=limit)
            total_created += c
            total_updated += u
            total_skipped += s
            total_errors += e

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Done. created={total_created} updated={total_updated} "
            f"skipped={total_skipped} errors={total_errors}"
        ))
        if not commit:
            self.stdout.write(self.style.WARNING(
                "Dry-run only — DB me kuch save nahi hua. "
                "OK lage to: python manage.py import_exam_sheets --docs-dir docs --commit"
            ))

    def _import_file(self, path: Path, category, commit=False, limit=0):
        wb = load_workbook(path, data_only=True)
        ws = wb.active
        header_row_no, raw_headers = _find_header_row(ws)

        idx = {}
        for i, h in enumerate(raw_headers):
            if not h:
                continue
            key = HEADER_ALIASES.get(str(h).strip().lower())
            if key:
                idx[key] = i
        if "exam_name" not in idx:
            raise CommandError(f"{path.name}: 'Exam Name' column missing")

        created = updated = skipped = errors = 0
        report = []

        rows = list(ws.iter_rows(min_row=header_row_no + 1, values_only=True))
        if limit and limit > 0:
            rows = rows[:limit]

        for row_no, row in enumerate(rows, start=header_row_no + 1):
            if not row or not row[idx["exam_name"]]:
                skipped += 1
                continue
            title = _clip(_cell(row, idx, "exam_name"), 255)
            if not title:
                skipped += 1
                continue

            data = {k: _cell(row, idx, k) for k in idx}
            description = _build_description(data)
            meta_title = _clip(title, 200)
            extra = (data.get("authority") or data.get("courses") or "").strip()
            meta_description = _clip(f"{title}. {extra}".strip(". "), 300)

            # Store conducting authority in full_form when empty (useful short label)
            authority = _clip(data.get("authority"), 200)

            try:
                with transaction.atomic():
                    existing = Exam.objects.filter(title__iexact=title).first()
                    fields = dict(
                        title=title,
                        course_category=category,
                        description=description or None,
                        full_form=authority,
                        meta_title=meta_title,
                        meta_description=meta_description,
                        meta_keyword=_clip(
                            f"{title}, {category.name}, entrance exam, India", 200
                        ),
                    )
                    # Prefer keeping existing full_form if already set to something else
                    if existing and existing.full_form and authority and existing.full_form != authority:
                        fields["full_form"] = existing.full_form

                    if existing:
                        for k, v in fields.items():
                            if k == "title":
                                # keep canonical casing from Excel on update
                                setattr(existing, k, v)
                                continue
                            setattr(existing, k, v)
                        existing.save()
                        updated += 1
                        report.append((row_no, "UPDATE", title))
                    else:
                        Exam.objects.create(**fields)
                        created += 1
                        report.append((row_no, "CREATE", title))

                    if not commit:
                        transaction.set_rollback(True)
            except Exception as exc:
                errors += 1
                report.append((row_no, "ERROR", f"{title}: {exc}"))
                self.stderr.write(self.style.ERROR(f"Row {row_no}: {exc}"))

        self.stdout.write(
            f"  created={created} updated={updated} skipped={skipped} errors={errors}"
        )
        for item in report[:8]:
            self.stdout.write(f"    {item}")
        if len(report) > 8:
            self.stdout.write(f"    ... +{len(report) - 8} more")
        return created, updated, skipped, errors
