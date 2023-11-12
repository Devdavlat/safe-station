import pandas as pd
from datetime import datetime
from django.utils import timezone
from io import BytesIO
from django.http import FileResponse
from rest_framework import status, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from permissons import IsCashier
from .serializers import (
    DailyReportCreateSerializer,
    DailyReportDetailSerializer,
    DailyReportUpdateSerializer,
    ExpenseCreateSerializer,
    ExpenseDetailSerializer,
    ExpenseSerializer,
    CollectorSerializer,
    CollectorCreateSerializer,
)
from .models import DailyReport, Expense, Collector


class DailyReportExportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        columns = {
            "counter_amount_of_gas": "Xisoblagich",
            "date_of_daily_report": "Sana",
            "uzcard": "UzCard",
            "xumo": "Batafsil ma'lumot",
            "daily_report_of_company": "Shartnoma",
            "cash": "Naqt pulga sotilgan gaz",
            "gas_price": "Narxi",
            "user": "Kassir telefon raqami",
        }
        df = pd.DataFrame(
            list(
                DailyReport.objects.values(
                    "counter_amount_of_gas",
                    "date_of_daily_report",
                    "uzcard",
                    "xumo",
                    "daily_report_of_company",
                    "cash",
                    "gas_price",
                    "user__phone_number",
                )
            ),
            columns=list(columns.keys()),
        )
        df.rename(columns=columns, inplace=True)

        file_like_object = BytesIO()
        df.to_excel(file_like_object, index=False)
        file_like_object.seek(0)  # move to the beginning of file
        response = FileResponse(file_like_object)
        filename = f"DailyReport_{datetime.now().strftime('%Y%m%d_%H%M')}"
        response["Content-Disposition"] = f'attachment; filename="{filename}.xlsx"'

        return response


class DailyReportListAPIView(APIView):
    permission_classes = [IsCashier]

    def get(self, request, *args, **kwargs):
        reports_data = DailyReport.objects.all()
        serialized_data = DailyReportDetailSerializer(reports_data, many=True).data
        return Response(serialized_data)

    @swagger_auto_schema(request_body=DailyReportCreateSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data
        data['user'] = self.request.user.pk
        serializer = DailyReportCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DailyReportUpdateView(generics.UpdateAPIView):
    queryset = DailyReport.objects.all()
    serializer_class = DailyReportUpdateSerializer

    def update(self, request, *args, **kwargs):
        user_id = request.user.pk
        last_update_time = DailyReport.objects.filter(user_id=user_id, pk=kwargs["pk"]).values("created_at")
        difference = (timezone.now() - last_update_time[0]["created_at"]).total_seconds() / 60
        if not difference < 10:
            return super().update(request, *args, **kwargs)


class ExpenseDetailAPIView(APIView):
    permission_classes = [IsCashier]

    def get(self, request, pk, *args, **kwargs):
        expense_data = Expense.objects.filter(pk=pk).first()
        serializer_data = ExpenseDetailSerializer(expense_data).data
        return Response(data=serializer_data)


class ExpenseCreateAPIView(APIView):

    @swagger_auto_schema(request_body=ExpenseCreateSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data
        data['user'] = self.request.user.pk
        serializer = ExpenseCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseAPIView(APIView):

    def get(self, *args, **kwargs):
        expenses = Expense.objects.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(data=serializer.data)


class CollectorCreateAPIView(APIView):

    @swagger_auto_schema(request_body=CollectorCreateSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data
        data['user'] = self.request.user.pk
        serializer = CollectorCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectorAPIView(APIView):

    def get(self, *args, **kwargs):
        collectors = Collector.objects.all()
        serializer = CollectorSerializer(collectors, many=True)
        return Response(data=serializer.data)
