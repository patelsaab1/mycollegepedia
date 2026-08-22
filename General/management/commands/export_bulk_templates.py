"""
Generate Excel templates for bulk import.

  python manage.py export_bulk_templates
"""
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from General.bulk_templates import TEMPLATES, build_template_bytes


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
        for key in TEMPLATES:
            filename, data = build_template_bytes(key)
            path = out / filename
            path.write_bytes(data)
            self.stdout.write(f"  - {path}")
        self.stdout.write(self.style.SUCCESS(f"Templates written to: {out}"))
