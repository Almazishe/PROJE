from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.http import  urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.core.mail import send_mail
from rest_framework import serializers
from apps.accounts.api.serializers import User

from config.settings import SITE_URL


from .tokens import account_activation_token


def activate_account(uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_verification = True
        user.is_active = True
        user.save()

        send_confirmation_email(user)

    else:
        raise serializers.ValidationError('uidb64 or token is not correct.')



def send_confirmation_email(user):
    subject = 'Account confirmed'

    CONFIRMATION_TEXT = f'''
Heey  {user.first_name} {user.last_name}! Your account is activated, now you can freely login!

{settings.SITE_URL}

Team CLAY
'''
    send_mail(
        subject=subject,
        message=CONFIRMATION_TEXT,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=True
    )

def send_activation_email(user):
    subject = 'Account activation'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    ACTIVATION_TEXT = f'''
Hello! To activate your account please press the link below:

{settings.SITE_URL}/account/activate/{uid}/{token}

Team CLAY
'''
    send_mail(
        subject=subject,
        message=ACTIVATION_TEXT,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=True
    )