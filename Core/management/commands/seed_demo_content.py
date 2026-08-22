"""
Seed demo content: blogs, exams, testimonials, about, feedback, slider.

Requires masters first:
  python manage.py seed_masters

Then:
  python manage.py seed_demo_content
"""
from datetime import date, timedelta
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from PIL import Image

from Auth.models import User
from Blog.models import Blog, Tag
from Core.models import About, Feedback, PrivacyPolicy, TermsAndCondition, Testimonial
from Exam.models import Exam, UpcomingExam
from General.models import CourseCategory


def _img(name: str, color=(20, 90, 160), size=(800, 450)) -> ContentFile:
    buf = BytesIO()
    Image.new("RGB", size, color=color).save(buf, format="WEBP", quality=70)
    return ContentFile(buf.getvalue(), name=name)


class Command(BaseCommand):
    help = "Seed blogs, exams, testimonials, about/privacy/terms, feedback (idempotent)."

    def handle(self, *args, **options):
        categories = {
            c.name.lower(): c
            for c in CourseCategory.objects.all()
        }
        medical = categories.get("medical") or CourseCategory.objects.first()
        engineering = categories.get("engineering") or medical
        management = categories.get("management") or medical
        law = categories.get("law") or medical

        if not medical:
            self.stderr.write(
                self.style.ERROR("Pehle run karein: python manage.py seed_masters")
            )
            return

        author = User.objects.filter(is_superuser=True).first() or User.objects.filter(is_staff=True).first()
        if not author:
            self.stderr.write(self.style.ERROR("Koi staff/superuser nahi mila (blog author ke liye)."))
            return

        created = {"blog": 0, "exam": 0, "upcoming": 0, "testimonial": 0, "feedback": 0, "about": 0, "legal": 0}

        with transaction.atomic():
            # ---- About / Legal ----
            if not About.objects.exists():
                About.objects.create(
                    title="About Admission Bazaar",
                    description=(
                        "<p><strong>Admission Bazaar</strong> helps students discover colleges, "
                        "courses, exams and counselling guidance — Dream • Discover • Succeed.</p>"
                        "<p>We connect aspirants with verified college information for Medical, "
                        "Engineering, Management, Law and Paramedical streams.</p>"
                    ),
                    meta_title="About Admission Bazaar",
                    meta_description="Learn about Admission Bazaar — college & admission guidance platform.",
                )
                created["about"] += 1
                self.stdout.write(" + About Us")

            if not PrivacyPolicy.objects.exists():
                PrivacyPolicy.objects.create(
                    title="Privacy Policy",
                    description=(
                        "<p>Admission Bazaar respects your privacy. We collect only information "
                        "needed to provide counselling and admission support.</p>"
                        "<p>We do not sell personal data to third parties. Contact "
                        "Admissionsbazaar@gmail.com for privacy requests.</p>"
                    ),
                    meta_title="Privacy Policy | Admission Bazaar",
                )
                created["legal"] += 1
                self.stdout.write(" + Privacy Policy")

            if not TermsAndCondition.objects.exists():
                TermsAndCondition.objects.create(
                    title="Terms & Conditions",
                    description=(
                        "<p>By using Admission Bazaar you agree to use the platform for lawful "
                        "education and admission purposes only.</p>"
                        "<p>College fees, seats and dates may change — always verify with the "
                        "official college or exam authority.</p>"
                    ),
                    meta_title="Terms & Conditions | Admission Bazaar",
                )
                created["legal"] += 1
                self.stdout.write(" + Terms & Conditions")

            # ---- Blogs ----
            blogs = [
                {
                    "title": "NEET UG 2026: Complete Preparation Guide for MBBS Aspirants",
                    "category": medical,
                    "post": (
                        "<h2>Why NEET matters</h2>"
                        "<p>NEET UG is the gateway to MBBS, BDS, BAMS and related medical courses "
                        "in India. A clear plan covering Physics, Chemistry and Biology is essential.</p>"
                        "<h3>Study tips</h3>"
                        "<ul><li>Finish NCERT thoroughly</li><li>Take weekly mock tests</li>"
                        "<li>Revise high-yield topics monthly</li></ul>"
                        "<p>Admission Bazaar helps you shortlist medical colleges by state, fees and ranking.</p>"
                    ),
                    "tags": ["NEET", "MBBS", "Medical"],
                    "color": (180, 40, 60),
                },
                {
                    "title": "How to Choose the Right B.Tech College in India",
                    "category": engineering,
                    "post": (
                        "<p>Choosing an engineering college depends on branch preference, placement "
                        "record, location, fees and accreditation.</p>"
                        "<p>Compare NIRF/rankings, visit campuses when possible, and check "
                        "alumni outcomes for CSE, ECE, Mechanical and Civil.</p>"
                        "<p>Use Admission Bazaar filters for Engineering colleges and course fees.</p>"
                    ),
                    "tags": ["BTECH", "Engineering", "JEE"],
                    "color": (30, 90, 160),
                },
                {
                    "title": "MBA vs PGDM: Which Management Course Should You Pick?",
                    "category": management,
                    "post": (
                        "<p><strong>MBA</strong> is usually university-affiliated; "
                        "<strong>PGDM</strong> is often AICTE-approved autonomous.</p>"
                        "<p>Look at ROI, specializations (Marketing, Finance, HR, Analytics), "
                        "and average packages before you decide.</p>"
                    ),
                    "tags": ["MBA", "PGDM", "CAT"],
                    "color": (40, 120, 80),
                },
                {
                    "title": "CLAT & Law Admissions: Roadmap for LLB Aspirants",
                    "category": law,
                    "post": (
                        "<p>CLAT opens doors to NLUs and top law schools. Build reading speed, "
                        "legal aptitude and current affairs early.</p>"
                        "<p>Admission Bazaar lists Law colleges offering LLB and LLM programs.</p>"
                    ),
                    "tags": ["CLAT", "LLB", "Law"],
                    "color": (90, 60, 140),
                },
            ]

            for b in blogs:
                if Blog.objects.filter(title=b["title"]).exists():
                    continue
                blog = Blog(
                    author=author,
                    category=b["category"],
                    title=b["title"],
                    post=b["post"],
                    status="PUBLIC",
                    published_date=timezone.now(),
                    meta_title=b["title"][:200],
                    meta_description=b["title"][:150],
                )
                blog.image = _img(f"blog-{created['blog']}.webp", b["color"])
                blog.save()
                for t in b["tags"]:
                    Tag.objects.create(tags=t, blog=blog)
                created["blog"] += 1
                self.stdout.write(f" + Blog: {blog.title[:60]}")

            # ---- Exams ----
            exams_data = [
                {
                    "title": "NEET UG",
                    "full_form": "National Eligibility cum Entrance Test (Undergraduate)",
                    "category": medical,
                    "description": (
                        "<p>NEET UG is conducted for admission to MBBS, BDS, BAMS, BUMS, "
                        "BHMS and related courses across India.</p>"
                    ),
                    "upcoming_title": "NEET UG 2026",
                    "url": "https://neet.nta.nic.in/",
                },
                {
                    "title": "JEE Main",
                    "full_form": "Joint Entrance Examination Main",
                    "category": engineering,
                    "description": (
                        "<p>JEE Main is the national engineering entrance for NITs, IIITs "
                        "and other Centrally Funded Technical Institutions.</p>"
                    ),
                    "upcoming_title": "JEE Main 2026 Session 1",
                    "url": "https://jeemain.nta.nic.in/",
                },
                {
                    "title": "CAT",
                    "full_form": "Common Admission Test",
                    "category": management,
                    "description": (
                        "<p>CAT is the premier MBA entrance exam for IIMs and top B-schools.</p>"
                    ),
                    "upcoming_title": "CAT 2026",
                    "url": "https://iimcat.ac.in/",
                },
                {
                    "title": "CLAT",
                    "full_form": "Common Law Admission Test",
                    "category": law,
                    "description": (
                        "<p>CLAT is for admission to undergraduate and postgraduate law "
                        "programs at National Law Universities.</p>"
                    ),
                    "upcoming_title": "CLAT 2027",
                    "url": "https://consortiumofnlus.ac.in/",
                },
                {
                    "title": "NEET PG",
                    "full_form": "National Eligibility cum Entrance Test (Postgraduate)",
                    "category": medical,
                    "description": (
                        "<p>NEET PG is required for MD/MS and related postgraduate medical seats.</p>"
                    ),
                    "upcoming_title": "NEET PG 2026",
                    "url": "https://nbe.edu.in/",
                },
            ]

            today = date.today()
            for i, e in enumerate(exams_data):
                exam = Exam.objects.filter(title=e["title"]).first()
                if not exam:
                    exam = Exam(
                        title=e["title"],
                        full_form=e["full_form"],
                        description=e["description"],
                        course_category=e["category"],
                        meta_title=e["title"],
                        meta_description=e["full_form"],
                    )
                    exam.image = _img(f"exam-{i}.webp", (50 + i * 30, 80, 120), (600, 400))
                    exam.save()
                    created["exam"] += 1
                    self.stdout.write(f" + Exam: {exam.title}")

                if not UpcomingExam.objects.filter(title=e["upcoming_title"]).exists():
                    UpcomingExam.objects.create(
                        exam=exam,
                        title=e["upcoming_title"],
                        exam_mode="Offline" if "NEET" in e["title"] or "CLAT" in e["title"] else "Online",
                        description=e["description"],
                        application_start_date=today + timedelta(days=30 + i * 7),
                        application_end_date=today + timedelta(days=60 + i * 7),
                        exam_start_date=today + timedelta(days=90 + i * 10),
                        exam_end_date=today + timedelta(days=91 + i * 10),
                        result=today + timedelta(days=120 + i * 10),
                        url=e["url"],
                        meta_title=e["upcoming_title"],
                    )
                    created["upcoming"] += 1
                    self.stdout.write(f" + Upcoming: {e['upcoming_title']}")

            # ---- Feedback (simple testimonials-style entries) ----
            feedbacks = [
                ("Riya Sharma", "+919876500001", "riya.demo@admissionsbazaar.com",
                 "Admission Bazaar helped me shortlist MBBS colleges in Madhya Pradesh. Clear fees and counselling tips!", 5),
                ("Aman Verma", "+919876500002", "aman.demo@admissionsbazaar.com",
                 "Great guidance for B.Tech colleges after JEE. The course list is easy to understand.", 5),
                ("Sneha Patel", "+919876500003", "sneha.demo@admissionsbazaar.com",
                 "MBA college comparison and exam dates in one place — very useful for working professionals.", 4),
                ("Rahul Mehta", "+919876500004", "rahul.demo@admissionsbazaar.com",
                 "CLAT preparation roadmap and law college info saved me a lot of time.", 5),
            ]
            for name, phone, email, message, rating in feedbacks:
                if Feedback.objects.filter(email=email).exists():
                    continue
                Feedback.objects.create(
                    name=name, phone=phone, email=email, message=message, rating=rating
                )
                created["feedback"] += 1
                self.stdout.write(f" + Feedback: {name}")

            # ---- Core Testimonial (needs User, OneToOne) ----
            demo_users = [
                ("Priya Singh", "priya.testimonial@admissionsbazaar.com", "9876500011",
                 "Got admission guidance for BDS. Support team was responsive and honest about fees."),
                ("Karan Joshi", "karan.testimonial@admissionsbazaar.com", "9876500012",
                 "Found the right Engineering college match for my rank. Highly recommend Admission Bazaar."),
                ("Ananya Gupta", "ananya.testimonial@admissionsbazaar.com", "9876500013",
                 "Clear information on MBA vs PGDM helped me decide confidently."),
            ]
            for name, email, mobile, text in demo_users:
                user, user_created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        "name": name,
                        "mobile": mobile,
                        "city": "Indore",
                        "is_active": True,
                        "is_student": True,
                    },
                )
                if user_created:
                    user.set_password("Demo@Student123")
                    user.save()
                if Testimonial.objects.filter(user=user).exists():
                    continue
                Testimonial.objects.create(user=user, description=text, rating=5)
                created["testimonial"] += 1
                self.stdout.write(f" + Testimonial: {name}")

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("seed_demo_content complete"))
        self.stdout.write(
            f"  blogs={created['blog']} exams={created['exam']} upcoming={created['upcoming']} "
            f"testimonials={created['testimonial']} feedback={created['feedback']} "
            f"about={created['about']} legal={created['legal']}"
        )
