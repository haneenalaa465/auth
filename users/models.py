from django.db import models
from django.contrib.auth.models import AbstractUser

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings


from django.utils.encoding import force_bytes 
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string

# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=30, blank=True)
    is_verified = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        subject = "Account Verification"
        html_message = f"""
        <p>Hi {instance.first_name},</p>
        <p>Please confirm your email address by clicking the link below:</p>
        <a href="http://127.0.0.1:8000/activate/{uid}/{token}">Verify Email</a>
        <p>Thank you!</p>
        """
        try:
            send_mail(
                subject,
                '',
                settings.EMAIL_HOST_USER,  # Use sender email from settings
                [instance.email],
                fail_silently=False,
                html_message=html_message
            )
        except BadHeaderError:
            pass
