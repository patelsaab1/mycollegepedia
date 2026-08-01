# yourapp/management/commands/update_is_student.py
from django.core.management.base import BaseCommand
from Auth.models import User,Student

class Command(BaseCommand):
    help = 'Update is_student field to True for all users'

    def handle(self, *args, **options):
        # Update is_student to False for all users
        Student.objects.all().update(is_student=True)
        self.stdout.write(self.style.SUCCESS('Successfully updated is_student to True for all users.'))
