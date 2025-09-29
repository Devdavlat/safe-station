from django.urls import path

from .views import (
    XumoCreateAPIView,
    UzCardCreateAPIView,
    UzCardDetailAPIView,
    XumoDetailAPIView,
)

urlpatterns = [
    path("xumo/", XumoCreateAPIView.as_view(), name="xumo-create"),
    path("xumo/<int:pk>/", XumoDetailAPIView.as_view(), name="uzcard-detail"),
    path("uzcard/", UzCardCreateAPIView.as_view(), name="uzcard-create"),
    path("uzcard/<int:pk>/", UzCardDetailAPIView.as_view(), name="uzcard-detail"),
]
