from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from spaces.models import ServiceSector, Unit, UnitGroup

from .base_models import BaseRole


PERMISSIONS = (
    ("can_modify_service_sector_roles", _("Can modify service sector roles")),
    ("can_modify_unit_roles", _("Can modify unit roles")),
    (
        "can_manage_units_reservation_units",
        _("Can create, edit and delete reservation units in certain unit"),
    ),
    ("can_modify_reservation_unit", _("Can modify reservation unit")),
    ("can_handle_application", _("Can handle application")),
)


class ServiceSectorRolePermission(models.Model):
    role = models.CharField(verbose_name=_("Role"), max_length=50, db_index=True)
    permission = models.CharField(verbose_name=_("Permission"), max_length=255, choices=PERMISSIONS)


class UnitRolePermission(models.Model):
    role = models.CharField(verbose_name=_("Role"), max_length=50, db_index=True)
    permission = models.CharField(verbose_name=_("Permission"), max_length=255, choices=PERMISSIONS)


class UnitRole(BaseRole):
    role = models.CharField(verbose_name=_("Role"), max_length=50)

    unit_group = models.ForeignKey(
        UnitGroup,
        verbose_name=_("Unit group"),
        related_name="roles",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    unit = models.ForeignKey(
        Unit,
        verbose_name=_("Unit"),
        related_name="roles",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        related_name="unit_roles",
        on_delete=models.CASCADE,
    )


class ServiceSectorRole(BaseRole):
    role = models.CharField(verbose_name=_("Role"), max_length=50)

    service_sector = models.ForeignKey(
        ServiceSector,
        verbose_name=_("Service sector"),
        related_name="roles",
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        related_name="service_sector_roles",
        on_delete=models.CASCADE,
    )
