from django.contrib import admin
from .models import Company, DriveGasUsage, Driver, DailReportOfAllCompany


@admin.register(Company)
class AdminCompany(admin.ModelAdmin):
    readonly_fields = ('drivers',)


@admin.register(Driver)
class AdminDriver(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "phone_number",
        "car_number",
        "company",
        "created_at",
        "updated_at",
    )


@admin.register(DriveGasUsage)
class AdminDriverGasUsage(admin.ModelAdmin):
    list_display = (
        "id",
        "gas_quantity",
        "date",
        "driver",
        "station",
        "created_at",
        "updated_at",
    )


@admin.register(DailReportOfAllCompany)
class AdminDailReportOfAllCompany(admin.ModelAdmin):
    list_display = (
        "id",
        "gas_quantity",
        "date",
        "employee",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        'gas_quantity',
    )
