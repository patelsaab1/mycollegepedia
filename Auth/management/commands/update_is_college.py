from django.core.management.base import BaseCommand
from Auth.models import User,CollegeAdmin


class Command(BaseCommand):
    help = 'Update is_college field to False for all users'

    def handle(self, *args, **options):
        CollegeAdmin.objects.all().update(is_college=True)
        self.stdout.write(self.style.SUCCESS('Successfully updated is_college to False for all users.'))