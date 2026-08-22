"""
Hardened College Excel/CSV import.

Required columns:
  college_user, name, organization_type, college_type, rank, established_year, overview, city

Optional:
  user_name, user_mobile, user_password  (auto-create College User if email missing)
  affiliation, rating, primary_mobile, email, website, meta_title, slug
  course_categories  (pipe-separated: Medical|Engineering)
"""
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from PIL import Image

from Auth.models import CollegeAdmin
from General.models import CollegeType, CourseCategory, OrganizationType
from Main.models import Country, State

from .models import College


def _placeholder(name: str, size=(400, 300), color=(30, 90, 160)) -> ContentFile:
    buf = BytesIO()
    Image.new("RGB", size, color=color).save(buf, format="WEBP", quality=70)
    return ContentFile(buf.getvalue(), name=name)


def _unique_mobile(seed: str) -> str:
    digits = "".join(c for c in seed if c.isdigit())
    if len(digits) >= 10:
        base = digits[-10:]
    else:
        h = abs(hash(seed)) % 10_000_000_000
        base = f"{h:010d}"
    if not base.startswith("9"):
        base = "9" + base[1:]
    mobile = base
    n = 0
    while CollegeAdmin.objects.filter(mobile=mobile).exists():
        n += 1
        mobile = f"{(int(base) + n) % 10_000_000_000:010d}"
        if not mobile.startswith("9"):
            mobile = "9" + mobile[1:]
    return mobile


class CaseInsensitiveFKWidget(ForeignKeyWidget):
    def clean(self, value, row=None, **kwargs):
        if value in (None, ""):
            return None
        val = str(value).strip()
        if self.field == "email":
            val = val.lower()
        try:
            return self.get_queryset(value, row, **kwargs).get(**{f"{self.field}__iexact": val})
        except self.model.DoesNotExist as exc:
            label = self.model._meta.verbose_name
            if self.model is CollegeAdmin:
                raise ValidationError(
                    f"College User email '{val}' not found. "
                    "Add columns user_name + user_mobile (auto-create), "
                    "or pehle Admin → College Users me account banao."
                ) from exc
            raise ValidationError(
                f"{label} not found for {self.field}='{val}'. "
                "Exact master name use karo (seed_masters / General Settings)."
            ) from exc
        except self.model.MultipleObjectsReturned as exc:
            raise ValidationError(
                f"Multiple {self.model._meta.verbose_name} for {self.field}='{val}'."
            ) from exc


class CollegeResource(resources.ModelResource):
    college_user = fields.Field(
        column_name="college_user",
        attribute="college_user",
        widget=CaseInsensitiveFKWidget(CollegeAdmin, "email"),
    )
    organization_type = fields.Field(
        column_name="organization_type",
        attribute="organization_type",
        widget=CaseInsensitiveFKWidget(OrganizationType, "name"),
    )
    college_type = fields.Field(
        column_name="college_type",
        attribute="college_type",
        widget=CaseInsensitiveFKWidget(CollegeType, "name"),
    )
    course_categories = fields.Field(
        column_name="course_categories",
        attribute="course_category",
        widget=ManyToManyWidget(CourseCategory, field="name", separator="|"),
        saves_null_values=False,
    )

    class Meta:
        model = College
        import_id_fields = ("name",)
        skip_unchanged = True
        report_skipped = True
        fields = (
            "college_user",
            "name",
            "affiliation",
            "organization_type",
            "college_type",
            "course_categories",
            "rank",
            "rating",
            "established_year",
            "overview",
            "city",
            "primary_mobile",
            "email",
            "website",
            "meta_title",
            "slug",
        )
        export_order = fields

    def before_import_row(self, row, row_number=None, **kwargs):
        # Normalize headers
        for key in list(row.keys()):
            if key is None:
                continue
            nk = str(key).strip().lower()
            if nk != key:
                row[nk] = row.pop(key)

        email = str(row.get("college_user") or "").strip().lower()
        if not email or "@" not in email:
            raise ValidationError(
                "Column 'college_user' me valid email likho "
                "(example: amaltas.college@admissionsbazaar.com)."
            )
        row["college_user"] = email

        for col in ("name", "organization_type", "college_type", "overview", "city"):
            if not str(row.get(col) or "").strip():
                raise ValidationError(f"Required column empty: {col}")

        if row.get("rank") in (None, ""):
            raise ValidationError("Required column empty: rank (must be unique number)")
        if row.get("established_year") in (None, ""):
            raise ValidationError("Required column empty: established_year")

        cats = str(row.get("course_categories") or "").strip()
        if not cats:
            row.pop("course_categories", None)

        # Auto-create College User (rolled back on dry_run when transactions=True)
        if not CollegeAdmin.objects.filter(email__iexact=email).exists():
            name = str(row.get("user_name") or row.get("name") or email.split("@")[0]).strip()
            mobile_raw = str(row.get("user_mobile") or row.get("primary_mobile") or "").strip()
            mobile = "".join(c for c in mobile_raw if c.isdigit())
            if len(mobile) >= 10:
                mobile = mobile[-10:]
            else:
                mobile = _unique_mobile(email)
            if CollegeAdmin.objects.filter(mobile=mobile).exists():
                mobile = _unique_mobile(email + mobile)

            country = Country.objects.filter(name__iexact="India").first()
            state = State.objects.filter(country=country).first() if country else None
            city = str(row.get("city") or "India").strip()[:70]
            password = str(row.get("user_password") or "College@12345").strip() or "College@12345"

            user = CollegeAdmin(
                email=email,
                name=name[:200],
                mobile=mobile[:15],
                department="Admissions",
                designation="Admin",
                city=city,
                country=country,
                state=state,
                is_staff=True,
                is_college=True,
                is_active=True,
            )
            user.set_password(password)
            user.save()

        existing_user = CollegeAdmin.objects.filter(email__iexact=email).first()
        if existing_user:
            college_name = str(row.get("name") or "").strip()
            linked = College.objects.filter(college_user=existing_user).first()
            if linked is not None and linked.name != college_name:
                raise ValidationError(
                    f"college_user '{email}' already linked to '{linked.name}'. "
                    "Har college ke liye alag College User email use karo."
                )

    def before_save_instance(self, instance, using_transactions, dry_run):
        if dry_run:
            return
        safe = "".join(c if c.isalnum() else "-" for c in (instance.name or "college"))[:40] or "college"
        if not instance.pk or not instance.logo:
            if not instance.logo:
                instance.logo.save(f"{safe}-logo.webp", _placeholder(f"{safe}-logo.webp"), save=False)
        if not instance.image:
            instance.image.save(
                f"{safe}-image.webp",
                _placeholder(f"{safe}-image.webp", size=(800, 450), color=(40, 110, 90)),
                save=False,
            )
