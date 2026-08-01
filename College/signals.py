# # signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags

# from .models import CollegeApplication

# @receiver(post_save, sender=CollegeApplication)
# def send_status_email(sender, instance, **kwargs):
#     if instance.status in ['Accepted', 'Rejected']:
#         subject = f'College Application Status Update for {instance.student}'
#         context = {'application': instance}
#         html_message = render_to_string('email_templates/application_status.html', context)
#         plain_message = strip_tags(html_message)
#         to_email = instance.student.email

#         send_mail(subject, plain_message, None, [to_email], html_message=html_message)
