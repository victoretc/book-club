from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = [*(DjangoUserAdmin.fieldsets or []), ("Reading list", {"fields": ("is_reading_list_public",)})]
