from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import DailReportOfAllCompany, DriveGasUsage
from users.models import Employee


@receiver(post_save, sender=DailReportOfAllCompany)
def save_employee_and_sum_of_gas_quantity(sender, instance, **kwargs):  # noqa
    import inspect  # noqa
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None
    employee = Employee.objects.filter(user=request.user)
    gas_quantity = DriveGasUsage.objects.filter(date=instance.date, station=employee.values('station')).aggregate(
        models.Sum("gas_quantity"))[
        "gas_quantity__sum"
    ]
    DailReportOfAllCompany.objects.filter(pk=instance.pk).update(gas_quantity=gas_quantity,
                                                                 employee=employee.values('pk'))
