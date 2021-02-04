from django.contrib import admin

from .models import (
    UnitRole,
    ServiceSectorRole,
)


@admin.register(UnitRole)
class UnitRoleAdmin(admin.ModelAdmin):
    model = UnitRole


@admin.register(ServiceSectorRole)
class ServiceSectorRoleAdmin(admin.ModelAdmin):
    model = ServiceSectorRole