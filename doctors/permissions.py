from rest_framework.permissions import BasePermission

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Doctor'

class IsApproved(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_approved == True