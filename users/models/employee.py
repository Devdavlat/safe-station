from django.db import models
from users.models.base_model import BaseModel

from django.utils.translation import gettext_lazy as _


class Employee(BaseModel):
    class Position(models.TextChoices):
        DIRECTOR = ('director', _("DIRECTOR", ))
        ACCOUNTANT = ('accountant', _("ACCOUNTANT", ))
        MANAGER = ('manager', _("MANAGER", ))
        CASHIER = ('cashier', _("CASHIER", ))
        DEVELOPER = ('developer', _("DEVELOPER", ))
        MODERATOR = ('moderator', _("MODERATOR", ))
        EMPLOYEE = ('employee', _("EMPLOYEE", ))

    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name='employee_user', unique=True)
    position = models.CharField(choices=Position.choices, max_length=64)
    salary = models.PositiveIntegerField()
    station = models.ManyToManyField('stations.Station', related_name='user_station')
    date_out = models.DateField(null=True, blank=True)
    date_in = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.pk} {self.user.full_name} {self.position}"
