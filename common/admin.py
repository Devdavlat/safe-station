from django.contrib import admin
from .models import Xumo, UzCard


@admin.register(Xumo)
class AdminXumoModel(admin.ModelAdmin):
    list_display = (
        "id",
        "amount_of_money",
        "picture_of_bill",
        "date",
        "station",
        "created_at",
        "updated_at",
    )


@admin.register(UzCard)
class AdminUzcardModel(admin.ModelAdmin):
    list_display = (
        "id",
        "amount_of_money",
        "picture_of_bill",
        "date",
        "station",
        "created_at",
        "updated_at",
    )
