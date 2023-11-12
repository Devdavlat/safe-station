from rest_framework import serializers
from .models import Driver, DriveGasUsage, DailReportOfAllCompany, Company


class DriverCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ("full_name", "phone_number", "car_number", "company")


class DriverGasUsageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriveGasUsage
        fields = ("gas_quantity", "date", "driver")


class DriverGasUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriveGasUsage
        fields = ("gas_quantity", "date", "driver", "updated_at", "created_at", "created_at")


class DailyReportOfAllCompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriveGasUsage
        fields = ("date",)


class DailyReportOfAllCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = DriveGasUsage
        fields = ("date", "gas_quantity")


class AllCompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name", "drivers", "contact_number", "gas_station")


class AllDriversSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ("id", "full_name", "phone_number", "car_number", "company")
