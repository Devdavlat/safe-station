from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Employee
from regex import phone_regex
from utils.verification import check_verification_code
from utils.verification.verification_type import get_verification_type


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "user_id", "position", "salary")


class EmployeeProfileSerializer(serializers.ModelSerializer):
    date_out = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Employee
        fields = ("id", "position", "station", "salary", "date_in", "date_out")

    def to_representation(self, instance):
        user_data = UserSerializer(instance.user).data
        data = super().to_representation(instance)
        data["user_data"] = user_data
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "phone_number")


class EmployeeCreateSerializer(serializers.ModelSerializer):
    date_out = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Employee
        fields = ('user', 'position', "salary", "station", 'date_in', 'date_out')


class TokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = UserSerializer(self.user, context={"request": self.context["request"]}).data

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "phone_number"]

    def to_representation(self, instance):
        data = instance.tokens
        data["user"] = UserSerializer(instance, context={"request": self.context["request"]}).data
        return data


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=6)

    def create(self, validated_data):
        phone_number = validated_data.get("phone_number")
        code = validated_data.get("code")
        verification_type = get_verification_type(phone_number)

        if not check_verification_code(phone_number, verification_type, code):
            raise ValidationError("Incorrect verification code.")

        user = User.objects.filter(phone_number=phone_number).first()

        if not user:
            raise ValidationError("User with this phone number does not exist.")

        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        tokens_and_user_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user_serializer.data,
        }
        return tokens_and_user_data


class SendVerificationCodeSerializer(serializers.Serializer):  # noqa
    phone_number = serializers.CharField(validators=[phone_regex])


class PhoneVerifySerializer(serializers.Serializer):  # noqa
    phone_number = serializers.CharField(validators=[phone_regex])
    code = serializers.CharField(min_length=6, max_length=6)
