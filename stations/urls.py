from django.urls import path
from .views import (
    DailyReportExportView,
    DailyReportListAPIView,
    DailyReportUpdateView,
    ExpenseDetailAPIView,
    ExpenseCreateAPIView,
    ExpenseAPIView,
    CollectorAPIView,
    CollectorCreateAPIView
)

# import_export_urlpatterns = [
# path("export/", DailyReportExportView.as_view(), name="export"),
#     path("import/", CourseImportView.as_view(), name="import"),
# ]

urlpatterns = [
    path('daily-report/', DailyReportListAPIView.as_view(), name="dily_report"),
    path('daily-report/<int:pk>/', DailyReportUpdateView.as_view(), name="update"),
    path("expense/", ExpenseCreateAPIView.as_view(), name="expense-detail"),
    path("expense/<int:pk>/", ExpenseDetailAPIView.as_view(), name="expense-create"),
    path("expenses/", ExpenseAPIView.as_view(), name="expense-create"),
    path("collector/", CollectorCreateAPIView.as_view(), name="expense-create"),
    path("collectors/", CollectorAPIView.as_view(), name="expense-create"),
]

# urlpatterns += import_export_urlpatterns
