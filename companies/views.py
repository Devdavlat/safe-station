from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from permissons import IsCashier, IsManager

from .models import DailReportOfAllCompany, Driver, DriveGasUsage, Company
from .serializers import (
    DriverGasUsageCreateSerializer,
    DriverGasUsageSerializer,
    DriverCreateSerializer,
    DailyReportOfAllCompanyCreateSerializer,
    DailyReportOfAllCompanySerializer,
    AllCompaniesSerializer,
    AllDriversSerializer
)


class DriverGasUsageCreateAPIView(APIView):
    permission_classes = [IsCashier]

    def get(self, request, *args, **kwargs):
        reports_data = DriveGasUsage.objects.all()
        serialized_data = DriverGasUsageSerializer(reports_data, many=True).data
        return Response(serialized_data)

    @swagger_auto_schema(request_body=DriverGasUsageCreateSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data
        data['user'] = self.request.user.pk
        serializer = DriverGasUsageCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DailyReportAllCompanyCreateAPIView(APIView):
    permission_classes = [IsCashier]

    def get(self, request, *args, **kwargs):
        reports_data = DriveGasUsage.objects.all()
        serialized_data = DailyReportOfAllCompanySerializer(reports_data, many=True).data
        return Response(serialized_data)

    @swagger_auto_schema(request_body=DailyReportOfAllCompanyCreateSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data
        data['user'] = self.request.user.pk
        serializer = DailyReportOfAllCompanyCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllCompaniesAPIView(APIView):
    # permission_classes = []

    def get(self, request, *args, **kwargs):
        companies_data = Company.objects.all()
        serializer = AllCompaniesSerializer(companies_data, many=True)
        return Response(data=serializer.data)


class AllDriversAPIView(APIView):
    # permission_classes = []

    def get(self, request, *args, **kwargs):
        drivers_data = Driver.objects.all()
        serializer = AllDriversSerializer(drivers_data, many=True)
        return Response(data=serializer.data)
