from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UzCard, Xumo
from users.models.employee import Employee


@receiver(post_save, sender=Xumo)
def save_station_xumo(sender, instance, **kwargs):  # noqa
    import inspect  # noqa
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None
    employee = Employee.objects.filter(user=request.user)
    if not request.user.is_superuser:
        Xumo.objects.filter(pk=instance.pk).update(station=employee.values('station')[0]['station'])


@receiver(post_save, sender=UzCard)
def save_station_uzcard(sender, instance, **kwargs):  # noqa
    import inspect  # noqa
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None
    employee = Employee.objects.filter(user=request.user)
    if not request.user.is_superuser:
        UzCard.objects.filter(pk=instance.pk).update(station=employee.values('station')[0]['station'])
