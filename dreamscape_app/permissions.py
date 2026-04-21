from rest_framework import permissions

class UserAccessPermission(permissions.BasePermission):
    message = 'Adding user not allowed.'
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user