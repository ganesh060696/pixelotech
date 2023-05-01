from django.contrib.auth.models import AbstractUser
from django.db import models

from .encryption import AESCipher


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True  # this is an abstract model


class User(AbstractUser, BaseModel):
    username = models.CharField(max_length=50, unique=True)
    hashed_phone_number = models.CharField(max_length=100, unique=True)
    is_profile_complete = models.BooleanField(default=False, null=False)

    @property
    def phone_number(self):
        decrypted_pn = AESCipher().decrypt(self.hashed_phone_number)
        return decrypted_pn

    @classmethod
    def fetch_user_with_phone_number(cls, phone_no):
        encrypted_pn = AESCipher().encrypt(phone_no)
        obj = User.objects.filter(hashed_phone_number=encrypted_pn).first()
        return obj

    def save(self, *args, **kwargs):
        if self.id is None:
            self.hashed_phone_number = AESCipher().encrypt(self.hashed_phone_number)
        super(User, self).save(*args, **kwargs)
