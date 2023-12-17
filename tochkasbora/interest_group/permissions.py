from rest_framework.permissions import BasePermission

from user_profile.models import UserProfile


class IsOrganizer(BasePermission):
    def has_object_permission(self, request, view, obj: UserProfile):
        if obj.is_organizer:
            return True

        return False
