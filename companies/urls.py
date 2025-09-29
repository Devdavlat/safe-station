from django.urls import path

from .views import (
    DriverGasUsageCreateAPIView,
    DailyReportAllCompanyCreateAPIView,
    AllDriversAPIView,
    AllCompaniesAPIView
)

urlpatterns = [
    path("driver-gas-usage/", DriverGasUsageCreateAPIView.as_view(), name="driver-gas-usage"),
    path("daily-report-companies/", DailyReportAllCompanyCreateAPIView.as_view(), name="daily-report"),
    path("companies/", AllCompaniesAPIView.as_view(), name="companies"),
    path("drivers/", AllDriversAPIView.as_view(), name="drivers"),
]
