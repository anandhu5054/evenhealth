from rest_framework.permissions import BasePermission

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Patient'

class IsApproved(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_approved == True

class IsVerified(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_verified == True