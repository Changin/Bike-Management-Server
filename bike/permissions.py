# bike/permissions.py
from rest_framework import permissions
from bike.models import Component


class CustomReadOnly(permissions.BasePermission):
    # GET : 누구나, PUT&PATCH : 해당 유저만
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.bike.user == request.user


class CustomBikeReadOnly(permissions.BasePermission):
    # GET : 누구나, PUT&PATCH : 해당 유저만
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user