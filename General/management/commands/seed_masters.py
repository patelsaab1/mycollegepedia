"""
One-time master data for college forms (local + live).

Seeds:
  - Country: India
  - All Indian States & UTs
  - Organization Type: Private, Government
  - College Type: Medical, Engineering, Management, Law, Paramedical
  - Course Category: same 5 categories
  - Course Type: UG, PG, Diploma
  - Courses (Course Subcategory): MBBS, BTECH, MBA, ...
  - Active Academic Year: 2025-26

Usage:
  python manage.py seed_masters
  python manage.py seed_masters --dry-run
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from General.models import (
    AcademicYear,
    CollegeType,
    CourseCategory,
    CourseSubcategory,
    CourseType,
    OrganizationType,
)
from Main.models import Country, State

# Official states + union territories (India)
INDIA_STATES = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
    # Union Territories
    "Andaman and Nicobar Islands",
    "Chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi",
    "Jammu and Kashmir",
    "Ladakh",
    "Lakshadweep",
    "Puducherry",
]

ORGANIZATION_TYPES = ["Private", "Government"]

# Used as College Type dropdown when adding a college
COLLEGE_TYPES = [
    "Medical",
    "Engineering",
    "Management",
    "Law",
    "Paramedical",
]

COURSE_CATEGORIES = [
    "Medical",
    "Engineering",
    "Management",
    "Law",
    "Paramedical",
]

COURSE_TYPES = ["UG", "PG", "Diploma"]

# (course_name, category, course_type, exam_type '1' semester / '2' yearly, duration_years)
COURSES = [
    ("MBBS", "Medical", "UG", "2", 5),
    ("BDS", "Medical", "UG", "2", 5),
    ("BAMS", "Medical", "UG", "2", 5),
    ("BUMS", "Medical", "UG", "2", 5),
    ("MD/MS", "Medical", "PG", "2", 3),
    ("MDS", "Medical", "PG", "2", 3),
    ("DM", "Medical", "PG", "2", 3),
    ("MCH", "Medical", "PG", "2", 3),
    ("AYURVEDA PG", "Medical", "PG", "2", 3),
    ("HOMEOPATHY PG", "Medical", "PG", "2", 3),
    ("BTECH", "Engineering", "UG", "1", 4),
    ("MTECH", "Engineering", "PG", "1", 2),
    ("MBA", "Management", "PG", "1", 2),
    ("PGDM", "Management", "PG", "1", 2),
    ("LLB", "Law", "UG", "1", 3),
    ("LLM", "Law", "PG", "1", 2),
    ("PHYSIOTHERAPY", "Paramedical", "UG", "2", 4),
    ("BSC NURSING", "Paramedical", "UG", "2", 4),
    ("GNM", "Paramedical", "Diploma", "2", 3),
    ("ANM", "Paramedical", "Diploma", "2", 2),
]

ACADEMIC_YEAR = "2025-26"


class Command(BaseCommand):
    help = "Seed India, states, org/college types, categories, and courses (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without writing to DB.",
        )

    def handle(self, *args, **options):
        dry = options["dry_run"]
        if dry:
            self.stdout.write(self.style.WARNING("DRY RUN — no DB writes"))

        stats = {
            "country": 0,
            "states": 0,
            "org": 0,
            "college_type": 0,
            "category": 0,
            "course_type": 0,
            "courses": 0,
            "academic_year": 0,
            "skipped": 0,
        }

        def create_name(model, name, key):
            obj = model.objects.filter(name__iexact=name).first()
            if obj:
                stats["skipped"] += 1
                return obj, False
            if dry:
                stats[key] += 1
                return None, True
            obj = model.objects.create(name=name)
            stats[key] += 1
            return obj, True

        with transaction.atomic():
            # Country
            india = Country.objects.filter(name__iexact="India").first()
            if not india:
                if not dry:
                    india = Country.objects.create(name="India")
                stats["country"] += 1
                self.stdout.write(" + Country: India")
            else:
                stats["skipped"] += 1
                self.stdout.write(" = Country: India (exists)")

            # States
            for state_name in INDIA_STATES:
                if india is None and dry:
                    stats["states"] += 1
                    continue
                existing = State.objects.filter(
                    country=india, name__iexact=state_name
                ).first()
                if existing:
                    stats["skipped"] += 1
                    continue
                if not dry:
                    State.objects.create(name=state_name, country=india)
                stats["states"] += 1
            self.stdout.write(f" + States/UTs added: {stats['states']}")

            # Organization types (Private / Government)
            for name in ORGANIZATION_TYPES:
                _, created = create_name(OrganizationType, name, "org")
                if created:
                    self.stdout.write(f" + Organization Type: {name}")

            # College types
            for name in COLLEGE_TYPES:
                _, created = create_name(CollegeType, name, "college_type")
                if created:
                    self.stdout.write(f" + College Type: {name}")

            # Course categories
            categories = {}
            for name in COURSE_CATEGORIES:
                obj, created = create_name(CourseCategory, name, "category")
                if created:
                    self.stdout.write(f" + Course Category: {name}")
                if obj:
                    categories[name] = obj
                elif not dry:
                    categories[name] = CourseCategory.objects.get(name__iexact=name)
                else:
                    categories[name] = None

            # Course types UG/PG/Diploma
            types = {}
            for name in COURSE_TYPES:
                obj, created = create_name(CourseType, name, "course_type")
                if created:
                    self.stdout.write(f" + Course Type: {name}")
                if obj:
                    types[name] = obj
                elif not dry:
                    types[name] = CourseType.objects.get(name__iexact=name)
                else:
                    types[name] = None

            # Courses (subcategories)
            for course_name, cat_name, type_name, exam_type, duration in COURSES:
                if dry:
                    exists = CourseSubcategory.objects.filter(
                        course_name__iexact=course_name
                    ).exists()
                    if exists:
                        stats["skipped"] += 1
                    else:
                        stats["courses"] += 1
                    continue

                category = categories[cat_name]
                ctype = types[type_name]
                existing = CourseSubcategory.objects.filter(
                    course_name__iexact=course_name,
                    course_category=category,
                ).first()
                if existing:
                    stats["skipped"] += 1
                    continue

                CourseSubcategory.objects.create(
                    course_category=category,
                    type=ctype,
                    course_name=course_name,
                    exam_type=exam_type,
                    duration=duration,
                    description=f"{course_name} under {cat_name}",
                )
                stats["courses"] += 1
                self.stdout.write(f" + Course: {course_name} ({cat_name}/{type_name})")

            # Academic year — only one can be status=True
            year = AcademicYear.objects.filter(year=ACADEMIC_YEAR).first()
            if not year:
                if not dry:
                    # Deactivate others first if we will activate this one
                    AcademicYear.objects.filter(status=True).update(status=False)
                    AcademicYear.objects.create(year=ACADEMIC_YEAR, status=True)
                stats["academic_year"] += 1
                self.stdout.write(f" + Academic Year: {ACADEMIC_YEAR} (active)")
            else:
                if not dry and not year.status:
                    AcademicYear.objects.filter(status=True).update(status=False)
                    year.status = True
                    year.save(update_fields=["status"])
                    self.stdout.write(f" = Academic Year: {ACADEMIC_YEAR} set active")
                else:
                    stats["skipped"] += 1
                    self.stdout.write(f" = Academic Year: {ACADEMIC_YEAR} (exists)")

            if dry:
                transaction.set_rollback(True)

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("seed_masters complete"))
        self.stdout.write(
            f"  country={stats['country']} states={stats['states']} "
            f"org={stats['org']} college_type={stats['college_type']} "
            f"category={stats['category']} course_type={stats['course_type']} "
            f"courses={stats['courses']} academic_year={stats['academic_year']} "
            f"skipped={stats['skipped']}"
        )
        self.stdout.write(
            self.style.NOTICE(
                "College add ke liye ab dropdowns ready: "
                "Private/Government, Medical/Engineering/..., courses, India + states."
            )
        )
