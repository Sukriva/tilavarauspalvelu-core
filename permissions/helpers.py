from django.contrib.auth.models import User
from django.db.models import Q

from applications.models import Application
from reservation_units.models import ReservationUnit
from spaces.models import ServiceSector, Unit

from .permissions import get_allowed_service_sector_roles, get_allowed_unit_roles


def is_admin(user: User):
    return user.is_superuser


def has_unit_role(user: User, unit: Unit, allowed_roles: list) -> bool:
    if not unit:
        return False
    unit_groups = unit.unit_groups.all()
    return user.unit_roles.filter(
        Q(unit=unit) | Q(unit_group__in=unit_groups), role__in=allowed_roles
    ).exists()


def has_service_sector_role(
    user: User, service_sector: ServiceSector, allowed_roles: list
) -> bool:
    return user.service_sector_roles.filter(
        service_sector=service_sector, role__in=allowed_roles
    ).exists()


def can_modify_service_sector_roles(user: User, service_sector: ServiceSector) -> bool:
    service_sector_roles = get_allowed_service_sector_roles("can_modify_unit_roles")
    return has_service_sector_role(
        user, service_sector, service_sector_roles
    ) or is_admin(user)


def can_modify_unit_roles(user: User, unit: Unit) -> bool:
    unit_roles = get_allowed_unit_roles("can_modify_unit_roles")
    service_sector_roles = get_allowed_service_sector_roles("can_modify_unit_roles")
    return (
        has_unit_role(user, unit, unit_roles)
        or has_service_sector_role(user, unit.secvice_sector, service_sector_roles)
        or is_admin(user)
    )


def can_manage_units_reservation_units(user: User, unit: Unit) -> bool:
    unit_roles = get_allowed_unit_roles("can_manage_units_reservation_units")
    service_sector_roles = get_allowed_service_sector_roles("can_manage_units_reservation_units")
    return (
        has_unit_role(user, unit, unit_roles)
        or has_service_sector_role(user, unit.secvice_sector, service_sector_roles)
        or is_admin(user)
    )


def can_modify_reservation_unit(user: User, reservation_unit: ReservationUnit) -> bool:
    unit_roles = get_allowed_unit_roles("can_modify_reservation_unit")
    service_sector_roles = get_allowed_service_sector_roles("can_modify_reservation_unit")
    return (
        has_unit_role(user, reservation_unit.unit, unit_roles)
        or has_service_sector_role(user, reservation_unit.unit.secvice_sector, service_sector_roles)
        or is_admin(user)
    )


def can_handle_application(user: User, application: Application) -> bool:
    service_sector_roles = get_allowed_service_sector_roles("can_handle_application")
    return has_service_sector_role(
        user, application.application_period.service_sector, service_sector_roles
    )
