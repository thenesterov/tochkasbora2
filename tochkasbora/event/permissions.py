from rest_framework.permissions import BasePermission

from event.models import Event
from user_profile.models import UserProfile


class IsOrganizer(BasePermission):
    def has_object_permission(self, request, view, obj: UserProfile):
        if obj.is_organizer:
            return True

        return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj: Event):
        ...
