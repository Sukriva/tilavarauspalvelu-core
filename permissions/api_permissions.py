from rest_framework import permissions

from spaces.models import Unit

from .helpers import can_manage_units_reservation_units, can_modify_reservation_unit


class ReservationUnitPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, reservation_unit):
        if request.method in permissions.SAFE_METHODS:
            return True
        return can_modify_reservation_unit(request.user, reservation_unit)

    def has_permission(self, request, view):
        if request.method == "POST":
            unit_id = request.data.get("unit_id")
            unit = Unit.objects.get(pk=unit_id)
            return can_manage_units_reservation_units(request.user, unit)
        return request.method in permissions.SAFE_METHODS


class ApplicationPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, reservation_unit):
        if request.method in permissions.SAFE_METHODS:
            return True
        return can_modify_reservation_unit(request.user, reservation_unit)

    def has_permission(self, request, view):
        if request.method == "POST":
            unit_id = request.data.get("unit_id")
            unit = Unit.objects.get(pk=unit_id)
            return can_manage_units_reservation_units(request.user, unit)
        return request.method in permissions.SAFE_METHODS
