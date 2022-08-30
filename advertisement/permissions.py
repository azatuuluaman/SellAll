from rest_framework import permissions


class IsOwnerOrSuperUser(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.owner == request.user
