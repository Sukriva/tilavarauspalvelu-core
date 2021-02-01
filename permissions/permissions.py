from django.utils.translation import gettext_lazy as _

from .models import ServiceSectorRole, UnitRole

PERMISSIONS = (
    (
        "can_manage_units_reservation_units",
        _("Can create, edit and delete reservation units in certain unit"),
    ),
    ("can_modify_reservation_unit", _("Can modify reservation unit")),
    ("can_modify_unit_roles", _("Can modify unit roles")),
    ("can_modify_service_sector_roles", _("Can modify service sector roles")),
    ("can_handle_application", _("Can handle application")),
)

ROLE_PERMISSIONS = {
    "can_modify_service_sector_roles": [ServiceSectorRole.ROLE_ADMIN],
    "can_modify_unit_roles": [UnitRole.ROLE_ADMIN],
    "can_manage_units_reservation_units": [UnitRole.ROLE_ADMIN, UnitRole.ROLE_MANAGER],
    "can_modify_reservation_unit": [UnitRole.ROLE_ADMIN, UnitRole.ROLE_MANAGER],
    "can_handle_application": [
        ServiceSectorRole.ROLE_ADMIN,
        ServiceSectorRole.ROLE_APPLICATION_MANAGER,
    ],
}
