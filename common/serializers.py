from rest_framework import serializers
from .models import Xumo, UzCard


class XumoCardCreateSerializer(serializers.ModelSerializer):
    picture_of_bill = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Xumo
        fields = ("amount_of_money", "picture_of_bill", "date")


class UzCardCreateSerializer(serializers.ModelSerializer):
    picture_of_bill = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = UzCard
        fields = ("amount_of_money", "picture_of_bill", "date")


class UzCardDetailSerializer(serializers.ModelSerializer):
    picture_of_bill = serializers.FileField(required=False, allow_null=True)
    update_at = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = UzCard
        fields = ("amount_of_money", "station", "picture_of_bill", "date", "update_at", "created_at")


class UzCardUpdateSerializer(serializers.ModelSerializer):
    picture_of_bill = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = UzCard
        fields = ("amount_of_money", "station", "picture_of_bill", "date")


class XumoDetailSerializer(serializers.ModelSerializer):
    picture_of_bill = serializers.FileField(required=False, allow_null=True)
    update_at = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Xumo
        fields = ("id", "amount_of_money", "station", "picture_of_bill", "date", "update_at", "created_at")
