from django.db import models
from users.models.base_model import BaseModel
from regex import phone_regex


class Company(BaseModel):
    name = models.CharField(max_length=1024, unique=True)
    drivers = models.PositiveIntegerField(default=0)
    contact_number = models.CharField(max_length=12, validators=[phone_regex], unique=True)
    gas_station = models.ManyToManyField("stations.Station",
                                         related_name="gas_station_company")

    def __str__(self):
        return self.name


class Driver(BaseModel):
    full_name = models.CharField(max_length=64, unique=True)
    phone_number = models.CharField(max_length=15, unique=True, validators=[phone_regex])
    car_number = models.CharField(max_length=8, unique=True)
    company = models.ForeignKey("Company", on_delete=models.CASCADE, related_name="employee")

    def __str__(self):
        return f"{self.full_name} {self.company}"


class DriveGasUsage(BaseModel):
    gas_quantity = models.FloatField()
    date = models.DateField()
    driver = models.ForeignKey("Driver", on_delete=models.CASCADE, related_name="gas")
    station = models.ForeignKey('stations.Station', on_delete=models.CASCADE, related_name='driver_station')

    def __str__(self):
        return f"{self.driver} {self.gas_quantity} {self.station}"


class DailReportOfAllCompany(BaseModel):
    gas_quantity = models.FloatField(default=0)
    date = models.DateField(unique=True)
    employee = models.ForeignKey("users.Employee", on_delete=models.CASCADE, related_name='all_company_report_employee')

    def __str__(self):
        return f"{self.gas_quantity} {self.date}"

    class Meta:
        unique_together = ["date", 'employee']
