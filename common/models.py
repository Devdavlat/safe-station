from django.db import models
from users.models.base_model import BaseModel


class UzCard(BaseModel):
    amount_of_money = models.PositiveIntegerField()
    picture_of_bill = models.FileField(null=True, blank=True)
    date = models.DateField()
    station = models.ForeignKey("stations.Station", on_delete=models.CASCADE, related_name="station_uzcard",
                                default=1)

    class Meta:
        unique_together = ('station', 'date')
        ordering = ["date"]
        verbose_name = "Uzcard"
        verbose_name_plural = "Uzcard kartalari"

    def __str__(self):
        return f"{self.pk} {self.date}da {self.amount_of_money} s'om."


class Xumo(BaseModel):
    amount_of_money = models.PositiveIntegerField()
    picture_of_bill = models.FileField(null=True, blank=True)
    date = models.DateField()
    station = models.ForeignKey("stations.Station", on_delete=models.CASCADE, related_name="station_xumocard",
                                default=1)

    class Meta:
        unique_together = ('station', 'date')
        ordering = ["date"]
        verbose_name = "Xumo"
        verbose_name_plural = "Xumo kartalari"

    def __str__(self):
        return f"{self.pk} {self.date}da {self.amount_of_money} s'om."


