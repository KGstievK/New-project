from rest_framework import permissions


class CanEditOrDeleteUserExceptSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем только аутентифицированным пользователям
        if request.user and request.user.is_authenticated:
            # Разрешаем суперпользователю всегда
            if request.user.is_superuser:
                return True
            # Разрешаем редактировать или удалять пользователей, но не суперпользователя
            return not obj.is_superuser
        return False
