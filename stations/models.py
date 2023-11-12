from django.db import models
from users.models.base_model import BaseModel


class Station(BaseModel):
    class StationType(models.TextChoices):
        GAS = "Metan"
        PROPANE = "Propan"
        Petrol = "Benzin"

    name = models.CharField(unique=True, max_length=128)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    type = models.CharField(choices=StationType.choices, max_length=16)
    employees = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name} {self.type}'


class DailyReport(BaseModel):
    counter_amount_of_gas = models.FloatField(help_text="Hisoblagichdagi ko'rsatilgan gaz miqdori.")
    loss_of_gas = models.FloatField(default=1.2, help_text="Yo'qotilgan gaz foizda.")
    gas_price = models.PositiveIntegerField(default=3250)
    cash = models.FloatField(help_text="Naqtga sotilgan gas qiymati.", default=0)
    profit = models.IntegerField(help_text="Naqtga sotilgan gas qiymati summasi.", default=0)
    date_of_daily_report = models.DateField()
    xumo = models.ForeignKey("common.Xumo", on_delete=models.CASCADE, related_name="daily_report_xumo", null=True,
                             blank=True)
    uzcard = models.ForeignKey("common.UzCard", on_delete=models.CASCADE, related_name="daily_report_uzcard", null=True,
                               blank=True)
    employee = models.ForeignKey("users.Employee", on_delete=models.CASCADE, related_name="report_user")
    station = models.ForeignKey("Station", on_delete=models.CASCADE, related_name="station")
    daily_report_of_company = models.ForeignKey(
        "companies.DailReportOfAllCompany", on_delete=models.CASCADE, related_name="daily_report_all_company"
    )

    def __str__(self):
        return str(self.date_of_daily_report)


class Expense(BaseModel):
    date = models.DateField()
    about = models.CharField(max_length=1024)
    amount_of_money = models.PositiveIntegerField()
    station = models.ForeignKey('stations.Station', on_delete=models.CASCADE, related_name="station_expense", default=1)

    def __str__(self):
        return F"{self.pk} {self.date} {self.amount_of_money}"


class Collector(BaseModel):
    gas_quantity_from_gres = models.FloatField()
    date = models.DateField()
    station = models.ManyToManyField('stations.Station')
    profit = models.FloatField(default=1)

    def __str__(self):
        return F"{self.pk} {self.date} {self.gas_quantity_from_gres} {self.station.name}"
