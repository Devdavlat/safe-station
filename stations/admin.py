from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Station, DailyReport, Expense, Collector
from .recources import DailyReportResource


@admin.register(Station)
class AdminStation(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "type",
        "employees"
    )
    readonly_fields = ('employees',)


@admin.register(DailyReport)
class AdminDailyReport(ImportExportModelAdmin):
    resource_class = DailyReportResource
    list_display = (
        "id",
        "counter_amount_of_gas",
        "loss_of_gas",
        "gas_price",
        "cash",
        "xumo",
        "uzcard",
        "employee",
        'profit',
        'station',
        "date_of_daily_report",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "cash",
        "loss_of_gas",
    )


@admin.register(Expense)
class AdminExpense(admin.ModelAdmin):
    list_display = (
        "id",
        "date",
        "about",
        "amount_of_money",
        "station",
        "created_at",
        "updated_at",
    )


@admin.register(Collector)
class AdminCollector(admin.ModelAdmin):
    list_display = (
        "id",
        "gas_quantity_from_gres",
        "date",
        "profit",
        "created_at",
        "updated_at",
    )
