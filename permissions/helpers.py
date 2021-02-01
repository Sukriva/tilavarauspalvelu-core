from django.db.models import Q
from django.contrib.auth.models import User

from applications.models import Application
from reservation_units.models import ReservationUnit
from spaces.models import ServiceSector, Unit

from .permissions import ROLE_PERMISSIONS


def can_modify_service_sector_roles(user: User, service_sector: ServiceSector) -> bool:
    allowed_roles = ROLE_PERMISSIONS["can_modify_service_sector_roles"]
    return user.service_sector_roles.filter(
        service_sector=service_sector, role__in=allowed_roles
    ).exists()


def can_modify_unit_roles(user: User, unit: Unit) -> bool:
    allowed_roles = ROLE_PERMISSIONS["can_modify_unit_roles"]
    unit_groups = unit.unit_groups.all()
    return user.unit_roles.filter(
        Q(unit=unit) | Q(unit_group__in=unit_groups), role__in=allowed_roles
    ).exists()


def can_manage_units_reservation_units(user: User, unit: Unit) -> bool:
    allowed_roles = ROLE_PERMISSIONS["can_manage_units_reservation_units"]
    unit_groups = unit.unit_groups.all()
    return user.unit_roles.filter(
        Q(unit=unit) | Q(unit_group__in=unit_groups), role__in=allowed_roles
    ).exists()


def can_modify_reservation_unit(user: User, reservation_unit: ReservationUnit) -> bool:
    allowed_roles = ROLE_PERMISSIONS["can_modify_reservation_unit"]
    unit_groups = reservation_unit.unit.unit_groups.all()
    return user.unit_roles.filter(
        Q(unit=reservation_unit.unit) | Q(unit_group__in=unit_groups),
        role__in=allowed_roles,
    ).exists()


def can_handle_application(user: User, application: Application) -> bool:
    allowed_roles = ROLE_PERMISSIONS["can_handle_application"]
    return user.service_sector_roles.filter(
        service_sector=application.application_period.service_sector,
        role__in=allowed_roles,
    ).exists()
