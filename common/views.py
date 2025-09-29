from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from permissons import IsCashier

from .models import Xumo, UzCard
from .serializers import (
    XumoCardCreateSerializer,
    XumoDetailSerializer,
    UzCardCreateSerializer,
    UzCardDetailSerializer
)


class XumoCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCashier]

    def get(self, request, *args, **kwargs):
        reports_data = Xumo.objects.all()
        serialized_data = XumoDetailSerializer(reports_data, many=True).data
        return Response(serialized_data)

    @swagger_auto_schema(request_body=XumoCardCreateSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data
        data['user'] = self.request.user.pk
        serializer = XumoCardCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UzCardCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCashier]

    def get(self, request, *args, **kwargs):
        reports_data = UzCard.objects.all()
        serialized_data = UzCardDetailSerializer(reports_data, many=True).data
        return Response(serialized_data)

    @swagger_auto_schema(request_body=XumoCardCreateSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data
        data['user'] = self.request.user.pk
        serializer = UzCardCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UzCardDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCashier]

    def get(self, request, pk, *args, **kwargs):
        uzcard_data = UzCard.objects.filter(pk=pk).first()
        serializer_data = UzCardDetailSerializer(uzcard_data).data
        return Response(data=serializer_data)

    def put(self, request, pk, *args, **kwargs):
        uzcard_data = UzCard.objects.filter(pk=pk).first()

        pass


class XumoDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCashier]

    def get(self, request, pk, *args, **kwargs):
        xumo_data = Xumo.objects.filter(pk=pk).first()
        serializer_data = XumoDetailSerializer(xumo_data).data
        return Response(data=serializer_data)
