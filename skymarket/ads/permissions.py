from rest_framework.permissions import BasePermission
from users.models import UserRoles


class IsAdmin(BasePermission):
    """
        Права доступа для админа.
        Пользователи с ролью ADMIN имеют доступ ко всем объектам.
    """

    def has_permission(self, request, view):
        if not request.user.role == UserRoles.ADMIN:
            return False
        return True


class IsOwner(BasePermission):
    """
    Права доступа для пользователя.
    Пользователь имеет доступ к редактированию и удалению только своих объектов.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
