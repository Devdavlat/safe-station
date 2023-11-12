from django.contrib import admin

from users.models import Employee, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass
