from rest_framework import permissions


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsCollege(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

class IsCounsellor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_counsellor