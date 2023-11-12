from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, DateWidget

from users.models.employee import Employee
from common.models import UzCard

from .models import DailyReport


class DailyReportResource(resources.ModelResource):
    date_of_daily_report = Field(attribute="date_of_daily_report", column_name="Sana", readonly=True,
                                 widget=DateWidget(format='%d.%m.%Y'))
    counter_amount_of_gass = Field(attribute="counter_amount_of_gass", column_name="Xisoblagich")
    uzcard = Field(attribute="one", column_name="UzCard", widget=ForeignKeyWidget(UzCard, field="money_quantity"),
                   readonly=True)
    xumo = Field(attribute="xumo", column_name="Xumo")
    daily_report_of_company = Field(attribute="daily_report_of_company", column_name="Shartnoma")
    cash = Field(attribute="cash", column_name="Sotish")
    gas_price = Field(attribute="gas_price", column_name="Gaz narxi")
    employee = Field(
        attribute="Employee", column_name="Kassir", widget=ForeignKeyWidget(Employee, field="phone_number"),
        readonly=True
    )

    class Meta:
        model = DailyReport
        fields = [
            "date_of_daily_report",
            "counter_amount_of_gass",
            "uzcard__date",
            "xumo__amount_of_money",
            "daily_report_of_company",
            "cash",
            "gas_price",
            "employee",
        ]
        widgets = {
            'date_of_daily_report': {'format': '%d.%m.%Y'},
        }
