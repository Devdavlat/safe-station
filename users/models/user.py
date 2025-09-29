from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from ..manager import UserManager
from regex import phone_regex


class User(AbstractUser):
    phone_number = models.CharField(unique=True, max_length=15, validators=[phone_regex])
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    username = models.CharField(null=True, blank=True)
    USERNAME_FIELD = "phone_number"

    objects = UserManager()

    def __str__(self):
        return f"{self.pk} {self.phone_number} {self.full_name}"

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name).strip()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}
