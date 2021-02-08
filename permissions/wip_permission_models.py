from django.db import models
from django.utils.translation import gettext_lazy as _

from reservation_units.models import ReservationUnit


features = {
    "managing_reservation_units": {
        "permissions": [can_manage_units_reservation_units, can_modify_reservation_unit]
    },
    "handling_applications": {
        "permissions": [can_approve_application, can_deny_application, can_save_application]
    },
    "creating_application_for_organisation": {
        "permissions": [can_save_application, can_create_application_for_organisation]
    }
}

class Feature(models.Model):

    name = models.CharField(verbose_name=_("Name"), max_length=50)

    def save(self):
        pass

class Role(models.Model):

    role = models.CharField(verbose_name=_("Role"), max_length=50)

    features = models.ManyToManyField(Feature)

class User(models.Model):
    roles = models.ManyToManyField(Role)

class UserReservationUnit(models.Model):

    user = models.ForeignKey(User)
    units = models.ManyToManyField(ReservationUnit)

def has_permission(user: User, permission: str):
    next(feature for feature in role.features.all() for role in user.roles.all() if feature.name == permission)


class ReservationUnitPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, reservation_unit):
        return has_permission(request.user, can_modify_reservation_unit) and can_modify_reservation_unit(request.user, reservation_unit)
