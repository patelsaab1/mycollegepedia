"""Shared Excel bulk-import templates (admin download + manage.py)."""
from io import BytesIO

from openpyxl import Workbook


def _workbook_bytes(headers, sample, guide_lines):
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"
    ws.append(headers)
    ws.append(sample)
    guide = wb.create_sheet("HOW_TO_FILL")
    for line in guide_lines:
        guide.append([line])
    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.getvalue()


COLLEGE = {
    "filename": "college_bulk_template.xlsx",
    "headers": [
        "college_user", "user_name", "user_mobile", "user_password", "name",
        "affiliation", "organization_type", "college_type", "course_categories",
        "rank", "rating", "established_year", "overview", "city",
        "primary_mobile", "email", "website", "meta_title", "slug",
    ],
    "sample": [
        "amaltas.college@admissionsbazaar.com", "Amaltas Admin", "9876500101",
        "College@12345", "Amaltas Institute of Medical Sciences", "MPMSU",
        "Private", "Medical", "Medical", "101", "4.2", "2008",
        "Amaltas Institute offers medical education with modern facilities.",
        "Dewas", "9876500101", "info@amaltas.example", "https://example.com",
        "Amaltas Institute of Medical Sciences Dewas",
        "amaltas-institute-of-medical-sciences",
    ],
    "guide": [
        "College bulk upload — header row mat badlo.",
        "college_user = unique email (har college alag).",
        "Naya email → user_name + user_mobile bharo (auto user).",
        "organization_type: Private / Government",
        "college_type: Medical / Engineering / Management / Law / Paramedical",
        "rank unique number. Logo Excel se nahi — baad me admin se.",
        "Admin → Colleges → Import",
    ],
}

EXAM = {
    "filename": "exam_bulk_template.xlsx",
    "headers": [
        "title", "full_form", "course_category", "description",
        "meta_title", "meta_keyword", "meta_description", "slug",
    ],
    "sample": [
        "NEET UG", "National Eligibility cum Entrance Test Undergraduate",
        "Medical", "Entrance exam for MBBS BDS and related courses.",
        "NEET UG Exam", "NEET, MBBS, Medical", "NEET UG information and dates", "neet-ug",
    ],
    "guide": [
        "Exam bulk upload — easy steps:",
        "1) Data sheet me rows add karo (header mat badlo).",
        "2) title unique: NEET UG, JEE Main, CAT, CLAT…",
        "3) course_category exact: Medical / Engineering / Management / Law / Paramedical",
        "4) description plain text OK.",
        "5) Admin → Exams → Import → ye file upload → Confirm.",
        "6) Phir Upcoming Exams alag template se import karo.",
    ],
}

UPCOMING_EXAM = {
    "filename": "upcoming_exam_bulk_template.xlsx",
    "headers": [
        "exam", "title", "exam_mode", "description",
        "application_start_date", "application_end_date",
        "exam_start_date", "exam_end_date", "result", "url",
        "meta_title", "slug",
    ],
    "sample": [
        "NEET UG", "NEET UG 2026", "Offline", "NEET UG 2026 session",
        "2026-02-01", "2026-03-15", "2026-05-03", "2026-05-03", "2026-06-15",
        "https://neet.nta.nic.in/", "NEET UG 2026", "neet-ug-2026",
    ],
    "guide": [
        "Upcoming Exam bulk upload:",
        "1) Pehle Exams me exam title exist kare (e.g. NEET UG).",
        "2) Column exam = wahi exact title.",
        "3) Dates YYYY-MM-DD format (2026-05-03).",
        "4) exam_mode: Online ya Offline.",
        "5) Admin → Upcoming Exams → Import.",
    ],
}

TEMPLATES = {
    "college": COLLEGE,
    "exam": EXAM,
    "upcoming_exam": UPCOMING_EXAM,
}


def build_template_bytes(key: str) -> tuple[str, bytes]:
    cfg = TEMPLATES[key]
    data = _workbook_bytes(cfg["headers"], cfg["sample"], cfg["guide"])
    return cfg["filename"], data
