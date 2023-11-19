from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class IsUserOneself(BasePermission):
    def has_object_permission(self, request: Request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.id == request.user.id


class IsUserProfileOneself(BasePermission):
    def has_object_permission(self, request: Request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user_id.id == request.user.id
