from django.contrib import admin

from .models import (
    ServiceSectorRoleChoice,
    ServiceSectorRolePermission,
    UnitRoleChoice,
    UnitRolePermission,
    UnitRole,
    ServiceSectorRole,
)


class UnitRolePermissionInline(admin.TabularInline):
    model = UnitRolePermission


class ServiceSectorRolePermissionInline(admin.TabularInline):
    model = ServiceSectorRolePermission


@admin.register(UnitRoleChoice)
class UnitRoleChoiceAdmin(admin.ModelAdmin):
    model = UnitRoleChoice
    inlines = [UnitRolePermissionInline]


@admin.register(ServiceSectorRoleChoice)
class ServiceSectorRoleChoiceAdmin(admin.ModelAdmin):
    model = ServiceSectorRoleChoice
    inlines = [ServiceSectorRolePermissionInline]


@admin.register(UnitRole)
class UnitRoleAdmin(admin.ModelAdmin):
    model = UnitRole


@admin.register(ServiceSectorRole)
class ServiceSectorRoleAdmin(admin.ModelAdmin):
    model = ServiceSectorRole