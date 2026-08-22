"""
Create 2 demo college users + colleges for testing / client demos.

Usage (on server):
  python manage.py seed_demo_colleges

Safe to re-run: skips if demo emails / college names already exist.
"""
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image

from Auth.models import CollegeAdmin
from College.models import College
from General.models import CollegeType, CourseCategory, OrganizationType
from Main.models import Country, State


def _placeholder_image(name: str) -> ContentFile:
    buf = BytesIO()
    Image.new("RGB", (400, 300), color=(30, 90, 160)).save(buf, format="WEBP", quality=70)
    return ContentFile(buf.getvalue(), name=name)


class Command(BaseCommand):
    help = "Seed 2 demo College Users and Colleges (idempotent)."

    def handle(self, *args, **options):
        org = OrganizationType.objects.first()
        ctype = CollegeType.objects.first()
        category = CourseCategory.objects.first()
        country = Country.objects.first()
        state = State.objects.filter(country=country).first() if country else State.objects.first()

        missing = []
        if not org:
            missing.append("Organization Type")
        if not ctype:
            missing.append("College Type")
        if not category:
            missing.append("Course Category")
        if not country:
            missing.append("Country")
        if missing:
            self.stderr.write(
                self.style.ERROR(
                    "Pehle admin me ye master data add karein: " + ", ".join(missing)
                )
            )
            return

        demos = [
            {
                "user_email": "demo1.college@admissionsbazaar.com",
                "user_name": "Demo College Admin 1",
                "mobile": "9100000001",
                "department": "Admissions",
                "designation": "Admin",
                "college_name": "Demo Institute of Technology",
                "rank": 9001,
                "city": "Indore",
                "year": 2005,
                "overview": (
                    "<p><strong>Demo Institute of Technology</strong> is a sample college "
                    "created for Admission Bazaar training. Replace this content with real "
                    "college details before going live with students.</p>"
                ),
            },
            {
                "user_email": "demo2.college@admissionsbazaar.com",
                "user_name": "Demo College Admin 2",
                "mobile": "9100000002",
                "department": "Admissions",
                "designation": "Admin",
                "college_name": "Demo Academy of Medical Sciences",
                "rank": 9002,
                "city": "Bhopal",
                "year": 1998,
                "overview": (
                    "<p><strong>Demo Academy of Medical Sciences</strong> is a sample college "
                    "for client walkthrough. Update logo, fees, and overview with real data.</p>"
                ),
            },
        ]

        created = 0
        skipped = 0

        with transaction.atomic():
            for d in demos:
                if College.objects.filter(name=d["college_name"]).exists():
                    self.stdout.write(f"Skip (exists): {d['college_name']}")
                    skipped += 1
                    continue

                user, user_created = CollegeAdmin.objects.get_or_create(
                    email=d["user_email"],
                    defaults={
                        "name": d["user_name"],
                        "mobile": d["mobile"],
                        "department": d["department"],
                        "designation": d["designation"],
                        "is_staff": True,
                        "is_college": True,
                        "is_active": True,
                        "city": d["city"],
                        "country": country,
                        "state": state,
                    },
                )
                if user_created:
                    user.set_password("Demo@College123")
                    user.save()
                    self.stdout.write(f"Created College User: {user.email}")
                else:
                    # Ensure flags if user already existed
                    changed = False
                    if not user.is_college:
                        user.is_college = True
                        changed = True
                    if not user.is_staff:
                        user.is_staff = True
                        changed = True
                    if changed:
                        user.save()
                    if hasattr(user, "college"):
                        self.stdout.write(
                            f"Skip user already linked to a college: {user.email}"
                        )
                        skipped += 1
                        continue

                # Find free rank if 9001/9002 taken
                rank = d["rank"]
                while College.objects.filter(rank=rank).exists():
                    rank += 1

                college = College(
                    college_user=user,
                    name=d["college_name"],
                    affiliation="Demo Affiliation",
                    organization_type=org,
                    college_type=ctype,
                    rank=rank,
                    rating=4.0,
                    established_year=d["year"],
                    overview=d["overview"],
                    city=d["city"],
                    country=country,
                    state=state,
                    primary_mobile=d["mobile"],
                    email=d["user_email"],
                    meta_title=d["college_name"],
                )
                college.logo = _placeholder_image(f"{rank}-logo.webp")
                college.image = _placeholder_image(f"{rank}-image.webp")
                college.save()
                college.course_category.add(category)
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created college: {college.name}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. created={created}, skipped={skipped}. "
                f"Demo login password (new users only): Demo@College123"
            )
        )
