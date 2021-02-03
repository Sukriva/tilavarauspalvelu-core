from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from spaces.models import ServiceSector, Unit, UnitGroup

from .base_models import BaseRole


class UnitRole(BaseRole):
    ROLE_ADMIN = "admin"
    ROLE_MANAGER = "manager"
    ROLE_VIEWER = "viewer"

    ROLE_CHOICES = (
        (ROLE_ADMIN, _("Admin")),
        (ROLE_MANAGER, _("Manager")),
        (ROLE_VIEWER, _("Viewer")),
    )

    role = models.CharField(verbose_name=_("Role"), max_length=50, choices=ROLE_CHOICES)

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
    ROLE_ADMIN = "admin"
    ROLE_APPLICATION_MANAGER = "application_manager"

    ROLE_CHOICES = (
        (ROLE_ADMIN, _("Admin")),
        (ROLE_APPLICATION_MANAGER, _("Application manager")),
    )

    role = models.CharField(verbose_name=_("Role"), max_length=50, choices=ROLE_CHOICES)

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
