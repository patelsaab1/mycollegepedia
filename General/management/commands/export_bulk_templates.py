"""
Generate Excel templates for bulk import (College / Exam / Upcoming Exam).

  python manage.py export_bulk_templates
  python manage.py export_bulk_templates --out media/import_templates
"""
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from openpyxl import Workbook


COLLEGE_HEADERS = [
    "college_user",
    "user_name",
    "user_mobile",
    "user_password",
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
]

COLLEGE_SAMPLE = [
    "amaltas.college@admissionsbazaar.com",
    "Amaltas Admin",
    "9876500101",
    "College@12345",
    "Amaltas Institute of Medical Sciences",
    "MPMSU",
    "Private",
    "Medical",
    "Medical",
    "101",
    "4.2",
    "2008",
    "Amaltas Institute offers medical education with modern facilities.",
    "Dewas",
    "9876500101",
    "info@amaltas.example",
    "https://example.com",
    "Amaltas Institute of Medical Sciences Dewas",
    "amaltas-institute-of-medical-sciences",
]

EXAM_HEADERS = [
    "title",
    "full_form",
    "course_category",
    "description",
    "meta_title",
    "meta_keyword",
    "meta_description",
    "slug",
]

EXAM_SAMPLE = [
    "NEET UG",
    "National Eligibility cum Entrance Test Undergraduate",
    "Medical",
    "Entrance exam for MBBS BDS and related courses.",
    "NEET UG Exam",
    "NEET, MBBS, Medical",
    "NEET UG information and dates",
    "neet-ug",
]

UPCOMING_HEADERS = [
    "exam",
    "title",
    "exam_mode",
    "description",
    "application_start_date",
    "application_end_date",
    "exam_start_date",
    "exam_end_date",
    "result",
    "url",
    "meta_title",
    "slug",
]

UPCOMING_SAMPLE = [
    "NEET UG",
    "NEET UG 2026",
    "Offline",
    "NEET UG 2026 session",
    "2026-02-01",
    "2026-03-15",
    "2026-05-03",
    "2026-05-03",
    "2026-06-15",
    "https://neet.nta.nic.in/",
    "NEET UG 2026",
    "neet-ug-2026",
]


def _write_sheet(path: Path, headers, sample, guide_rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"
    ws.append(headers)
    ws.append(sample)
    guide = wb.create_sheet("HOW_TO_FILL")
    for row in guide_rows:
        guide.append([row])
    wb.save(path)


class Command(BaseCommand):
    help = "Write Excel templates for College / Exam / Upcoming Exam bulk import."

    def add_arguments(self, parser):
        parser.add_argument(
            "--out",
            default=None,
            help="Output folder (default: media/import_templates)",
        )

    def handle(self, *args, **options):
        out = Path(options["out"] or Path(settings.MEDIA_ROOT) / "import_templates")
        out.mkdir(parents=True, exist_ok=True)

        _write_sheet(
            out / "college_bulk_template.xlsx",
            COLLEGE_HEADERS,
            COLLEGE_SAMPLE,
            [
                "COLLEGE BULK UPLOAD — kaise bharein",
                "1) Sirf Data sheet use karo. Header row mat badlo.",
                "2) college_user = unique email (har college alag). Agar naya email hai to user auto-create hoga.",
                "3) user_name + user_mobile naye user ke liye recommend. user_password default College@12345.",
                "4) organization_type = Private ya Government (exact).",
                "5) college_type = Medical / Engineering / Management / Law / Paramedical (exact).",
                "6) course_categories = Medical|Engineering (optional, pipe |).",
                "7) rank UNIQUE number hona chahiye (do colleges same rank nahi).",
                "8) overview required (plain text OK). Logo/image Excel se nahi — system placeholder lagata hai.",
                "9) Admin → COLLEGE SETTINGS → Colleges → Import → ye file upload.",
                "10) Pehle seed_masters chala lo taaki Private/Medical etc. exist karen.",
            ],
        )

        _write_sheet(
            out / "exam_bulk_template.xlsx",
            EXAM_HEADERS,
            EXAM_SAMPLE,
            [
                "EXAM BULK UPLOAD",
                "1) title unique rakho (NEET UG, JEE Main…).",
                "2) course_category exact: Medical, Engineering, Management, Law, Paramedical.",
                "3) Admin → Exams → Import.",
                "4) Upcoming Exam alag file se baad me import karo.",
            ],
        )

        _write_sheet(
            out / "upcoming_exam_bulk_template.xlsx",
            UPCOMING_HEADERS,
            UPCOMING_SAMPLE,
            [
                "UPCOMING EXAM BULK UPLOAD",
                "1) Pehle Exam list me exam title exist kare (column exam = exact Exam title).",
                "2) Dates format: YYYY-MM-DD (2026-05-03).",
                "3) exam_mode = Online ya Offline.",
                "4) Admin → Upcoming Exams → Import.",
            ],
        )

        self.stdout.write(self.style.SUCCESS(f"Templates written to: {out}"))
        for name in (
            "college_bulk_template.xlsx",
            "exam_bulk_template.xlsx",
            "upcoming_exam_bulk_template.xlsx",
        ):
            self.stdout.write(f"  - {out / name}")
