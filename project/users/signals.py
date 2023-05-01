from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import User


# Post save for user, Called when ever a User is created or updated
@receiver(post_save, sender=User)
def post_save_for_user(sender, instance, created, **kwargs):
    if created:
        # Create Token when User is created
        Token.objects.create(user=instance)
