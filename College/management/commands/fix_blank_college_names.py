"""Fill blank College.name from College User display name (… Admin)."""
from django.core.management.base import BaseCommand

from College.models import College


class Command(BaseCommand):
    help = "Set College.name from linked College User when name is blank."

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            action="store_true",
            help="Write changes (default dry-run).",
        )

    def handle(self, *args, **options):
        commit = options["commit"]
        blanks = [
            c
            for c in College.objects.select_related("college_user").all()
            if not (c.name or "").strip()
        ]

        self.stdout.write(self.style.WARNING("DRY-RUN" if not commit else "COMMIT"))
        fixed = 0
        for c in blanks:
            uname = ""
            if c.college_user_id:
                uname = (getattr(c.college_user, "name", None) or "").strip()
            if uname.lower().endswith(" admin"):
                uname = uname[:-6].strip()
            if not uname:
                self.stderr.write(self.style.ERROR(f"id={c.id} rank={c.rank}: no user name"))
                continue
            uname = uname[:255]
            # unique-ish if clash
            final = uname
            if College.objects.filter(name__iexact=final).exclude(pk=c.pk).exists():
                final = f"{uname} ({c.city or c.rank})"[:255]
            self.stdout.write(f"  id={c.id} rank={c.rank} → '{final}'")
            if commit:
                c.name = final
                c.save(update_fields=["name"])
            fixed += 1

        self.stdout.write(self.style.SUCCESS(f"{'Would fix' if not commit else 'Fixed'}: {fixed}"))
        if not commit and fixed:
            self.stdout.write("Run again with --commit to save.")
