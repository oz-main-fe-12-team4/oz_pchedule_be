from rest_framework.permissions import BasePermission


class IsCustomAdmin(BasePermission):
    """
    ✅ 사용자에게 is_admin=True 권한이 있는지 확인
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "is_admin", False))
