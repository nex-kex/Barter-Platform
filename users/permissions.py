from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj
