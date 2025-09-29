from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views.users import LoginView, UserRegisterView, UserProfileView, EmployeesAPIView, EmployeeCreateAPIView
from .views.verification import PhoneVerifyView, SendVerificationCodeView

urlpatterns = [
    path("auth/token/", LoginView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", UserRegisterView.as_view(), name="register"),
    path("send/verification-code/", SendVerificationCodeView.as_view(), name="send_code"),
    path("verify/phone-number/", PhoneVerifyView.as_view(), name="verify_phone"),
    path("profile/", UserProfileView.as_view(), name="verify_phone"),
    path("employees/", EmployeesAPIView.as_view(), name="employees"),
    path("employees/<int:pk>/", EmployeeCreateAPIView.as_view(), name="employee_create"),
]
