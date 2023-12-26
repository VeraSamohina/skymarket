from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Отображение пользователей в админ-панели Django.

    """
    list_display = ('email', 'first_name', 'phone', 'is_active', 'role', 'pk')
