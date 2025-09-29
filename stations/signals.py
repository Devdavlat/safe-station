from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DailyReport, Expense, Collector
from users.models import Employee


@receiver(post_save, sender=DailyReport)
def save_cash(sender, instance, **kwargs):  # noqa
    gas = round(
        instance.counter_amount_of_gas - round(instance.counter_amount_of_gas * instance.loss_of_gas / 100, 1), 1
    )
    companies_and_cards_in_gas = (
                                         (
                                                 instance.xumo.money_quantity + instance.uzcard.money_quantity) / instance.gas_price
                                 ) + instance.daily_report_of_company.gas_quantity
    gas -= round(companies_and_cards_in_gas, 1)

    DailyReport.objects.filter(pk=instance.pk).update(sales_gas=round(gas, 1), cash=round(gas * instance.gas_price, 1))


@receiver(post_save, sender=Expense)
def save_station(sender, instance, **kwargs):  # noqa
    import inspect  # noqa
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None
    employee = Employee.objects.filter(user=request.user)
    Expense.objects.filter(pk=instance.pk).update(station=employee.values('station')[0]['station'])


@receiver(post_save, sender=Collector)
def save_profit(sender, instance, **kwargs):  # noqa
    profit = instance.gas_quantity_from_gres

    collector_instance = Collector.objects.get(pk=instance.pk)
    station_pks = list(collector_instance.station.values_list('pk', flat=True))
    station_usage_gas = 0
    for pk in station_pks:
        station = DailyReport.objects.get(date_of_daily_report=instance.date, station=pk)
        print(station.counter_amount_of_gas)
