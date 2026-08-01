from django.utils import timezone
import datetime
import uuid
from django.conf import settings
from twilio.rest import Client
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from App.settings import TEMPLATES_BASE_URL
from Auth.models import PasswordResetToken


def new_token():
    token = uuid.uuid1().hex
    return token


def send_approve_counsellor_sms(counsellor):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    sms_body = render_to_string("sms/counsellor_approve.txt", {
        "user": counsellor.name,
    })
    message = client.messages.create(
        body=sms_body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=counsellor.mobile
    )


def send_password_reset_sms(user):
    # Initialize Twilio client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    token = new_token()
    exp_time = timezone.now() + datetime.timedelta(minutes=30)
    PasswordResetToken.objects.update_or_create(user=user,
                                                defaults={'user': user, 'token': token, 'validity': exp_time})

    # Compose SMS message
    sms_body = render_to_string("sms/password_reset.txt", {
        "token": token,
        "email": user.email,
        "user": user.name,
        "base_url": TEMPLATES_BASE_URL,
    })

    # Send SMS via Twilio
    try:
        message = client.messages.create(
            body=sms_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=user.mobile  # assuming user has a phone_number field
        )
        print("SMS Sent successfully:", message.sid)
        return Response({'message': 'Reset password SMS sent successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        print("Error sending SMS:", str(e))
        return Response({'message': 'Failed to send reset password SMS'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
