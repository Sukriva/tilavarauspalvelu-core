from django.contrib.auth.models import User
from django.db.models import Q

from applications.models import Application
from reservation_units.models import ReservationUnit
from spaces.models import ServiceSector, Unit


def is_admin(user: User):
    return user.is_superuser


def has_unit_permission(user: User, unit: Unit, required_permission: str) -> bool:
    if not unit:
        return False
    unit_groups = unit.unit_groups.all()
    return user.unit_roles.filter(
        Q(unit=unit) | Q(unit_group__in=unit_groups), role__permissions__permission=required_permission
    ).exists()


def has_service_sector_permission(
    user: User, service_sector: ServiceSector, required_permission: str
) -> bool:
    return user.service_sector_roles.filter(
        service_sector=service_sector, role__permissions__permission=required_permission
    ).exists()


def has_general_permission(
    user: User, required_permission: str
) -> bool:
    return user.general_roles.filter(role__permissions__permission=required_permission
    ).exists()


def can_modify_service_sector_roles(user: User, service_sector: ServiceSector) -> bool:
    permission = "can_modify_service_sector_roles"
    return has_service_sector_permission(
        user, service_sector, permission
    ) or is_admin(user)


def can_modify_unit_roles(user: User, unit: Unit) -> bool:
    permission = "can_modify_unit_roles"
    return (
        has_unit_permission(user, unit, permission)
        or has_service_sector_permission(user, unit.service_sector, permission)
        or is_admin(user)
    )


def can_manage_units_reservation_units(user: User, unit: Unit) -> bool:
    permission = "can_manage_units_reservation_units"
    return (
        has_unit_permission(user, unit, permission)
        or has_service_sector_permission(user, unit.service_sector, permission)
        or is_admin(user)
    )


def can_modify_reservation_unit(user: User, reservation_unit: ReservationUnit) -> bool:
    return can_manage_units_reservation_units(user, reservation_unit.unit)


def can_handle_application(user: User, application: Application) -> bool:
    permission = "can_handle_application"
    return has_service_sector_permission(
        user, application.application_period.service_sector, permission
    )
