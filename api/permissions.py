
from rest_framework.permissions import BasePermission

from accounts.models import CustomerProfile
from technicians.models import Technician


class IsCustomer(BasePermission):
    """
    Allow only authenticated customer accounts
    to access customer-specific API endpoints.
    """

    message = "Access denied. Only customers can access this API."

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_staff or user.is_superuser:
            return False

        return CustomerProfile.objects.filter(
            user=user,
            role="customer"
        ).exists()


class IsTechnician(BasePermission):
    """
    Allow only authenticated registered technicians
    to access technician-specific API endpoints.
    """

    message = "Access denied. Only registered technicians can access this API."

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_staff or user.is_superuser:
            return False

        return Technician.objects.filter(
            user=user,
            user__is_active=True
        ).exists()
