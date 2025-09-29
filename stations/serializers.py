from rest_framework import serializers
from .models import DailyReport, Expense, Collector


class DailyReportCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = DailyReport
        fields = (
            "counter_amount_of_gas",
            "gas_price",
            "date_of_daily_report",
            "xumo",
            "uzcard",
            "daily_report_of_company",
            "user"
        )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)


class DailyReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReport
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data


class DailyReportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReport
        fields = ("id", "counter_amount_of_gas", "gas_price", "xumo", "uzcard", "daily_report_of_company")


class ExpenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("date", "about", "amount_of_money")


class ExpenseDetailSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(allow_null=True, required=False)

    class Meta:
        model = Expense
        fields = ("id", "date", "about", "station", "created_at", "updated_at")


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("id", "about", "station", "date")


class CollectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collector
        fields = ("id", "gas_quantity_from_gres", "date", "station", "profit")

    def to_representation(self, instance):
        print(instance.station.name)
        return super().to_representation(instance)


class CollectorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collector
        fields = ("gas_quantity_from_gres", "date", "station")
