from rest_framework import permissions

from spaces.models import ServiceSector, Unit

from .helpers import (
    can_manage_units_reservation_units,
    can_modify_reservation_unit,
    can_modify_service_sector_roles,
    can_modify_unit_roles
)


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


class UnitRolePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, reservation_unit):
        if request.method in permissions.SAFE_METHODS:
            return True
        return can_modify_reservation_unit(request.user, reservation_unit)

    def has_permission(self, request, view):
        if request.method == "POST":
            unit_id = request.data.get("unit_id", None)
            unit_group_id = request.data.get("unit_group_id", None)
            unit = Unit.objects.get(pk=unit_id)
            return can_modify_unit_roles(request.user, unit)
        return request.method in permissions.SAFE_METHODS


class ServiceSectorRolePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, service_sector):
        if request.method in permissions.SAFE_METHODS:
            return True
        return can_modify_service_sector_roles(request.user, service_sector)

    def has_permission(self, request, view):
        if request.method == "POST":
            service_sector_id = request.data.get("service_sector_id")
            try:
                service_sector = ServiceSector.objects.get(pk=service_sector_id)
                return can_modify_service_sector_roles(request.user, service_sector)
            except ServiceSector.DoesNotExist:
                return False
        return request.method in permissions.SAFE_METHODS
