from rest_framework.permissions import BasePermission
from users.models import Employee
from utils.get_object import get_or_none


class IsCashier(BasePermission):
    def has_permission(self, request, view):
        employee = get_or_none(Employee, user__phone_number=request.user.phone_number)
        return bool(employee.user.is_superuser or employee.position.lower() == "developer")


class IsManager(BasePermission):
    def has_object_permission(self, request, view, obj):
        employee = get_or_none(Employee, user__phone_number=request.user.phone_number)
        return bool(employee.user.is_superuser or employee.position.lower() == "manager")


class IsEmployee(BasePermission):
    def has_object_permission(self, request, view, obj):
        employee = get_or_none(Employee, user__phone_number=request.user.phone_number)
        return bool(employee.user.is_superuser or employee.position.lower() == "manager")
