from rest_framework import permissions

class IsCreatorOrReadOnly(permissions.BasePermission):
    """Custom permission: Only allow creators to modify their books"""
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for creator
        return obj.creator == request.user