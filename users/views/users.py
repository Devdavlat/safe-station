from rest_framework import generics, permissions, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from users.models import Employee, User
from users.serializers import (
    TokenObtainPairSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
    UserSerializer,
    EmployeeSerializer,
    EmployeeCreateSerializer,
    EmployeeProfileSerializer
)
from permissons import IsCashier, IsManager


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class TokenObtainView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except AuthenticationFailed as e:
            e.status_code = status.HTTP_400_BAD_REQUEST
            raise e
        else:
            data = serializer.validated_data
        return Response(data, status=status.HTTP_200_OK)


class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):

    def get(self, request, *args, **kwargs):
        employee = Employee.objects.filter(user_id=request.user.pk).first()
        serializer_data = EmployeeProfileSerializer(employee, context={"request": request})
        return Response(serializer_data.data)


class EmployeesAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsManager]

    def get(self, request, *args, **kwargs):
        users = User.objects.exclude(employee_user__isnull=False)
        serializer = UserSerializer(users, many=True).data

        return Response(data=serializer)


class EmployeeCreateAPIView(APIView):

    @swagger_auto_schema(request_body=EmployeeCreateSerializer)
    def post(self, request, pk, *args, **kwargs):
        data = request.data
        data["user"] = pk
        serializer = EmployeeCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors)
