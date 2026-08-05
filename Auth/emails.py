# from django.utils import timezone
# import datetime
# import random
# import uuid

# from django.conf import settings
# from django.core.mail import send_mail, EmailMessage
# from django.template.loader import get_template
# from rest_framework import status
# from rest_framework.response import Response

# from App.settings import TEMPLATES_BASE_URL
# from Auth.models import PasswordResetToken


# def new_token():
#     token = uuid.uuid1().hex
#     return token


# def send_password_reset_email(user):
#     token = new_token()
#     exp_time = timezone.now() + datetime.timedelta(minutes=30)
#     PasswordResetToken.objects.update_or_create(user=user,
#                                                 defaults={'user': user, 'token': token, 'validity': exp_time})
#     email_data = {
#         "token": token,
#         "email": user.email,
#         "base_url": TEMPLATES_BASE_URL,
#     }
#     message = get_template("email/password_reset.html").render(email_data)
#     msg = EmailMessage('Reset Password', body=message, to=[user.email])
#     msg.content_subtype = 'html'

#     try:
#         msg.send()
#     except:
#         pass
#     return Response({'message': 'rest password sent successfully'}, status=status.HTTP_200_OK)


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_custom_email(subject, template_name, context, recipient_list, from_email=None):
    """
    Send a custom email to a list of recipients.
    
    :param subject: Email subject
    :param template_name: Template to render (located in templates directory)
    :param context: Context variables for the template
    :param recipient_list: List of email addresses to send to
    :param from_email: Sender's email address
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)




