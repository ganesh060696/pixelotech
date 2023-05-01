from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import User


@receiver(post_save, sender=User)
def post_save_for_user(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
