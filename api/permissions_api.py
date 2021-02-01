from django.contrib.auth.models import User
from rest_framework import mixins, permissions, serializers, viewsets

from api.base import TranslatedModelSerializer
from permissions.api_permissions import ServiceSectorRolePermission, UnitRolePermission
from permissions.models import ServiceSectorRole, UnitRole
from services.models import Service
from spaces.models import ServiceSector


class UnitRoleSerializer(TranslatedModelSerializer):
    class Meta:
        model = UnitRole


class ServiceSectorRoleSerializer(TranslatedModelSerializer):
    service_sector_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceSector.objects.all(), source="service_sector"
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user"
    )

    class Meta:
        model = ServiceSectorRole
        fields = ["service_sector_id", "user_id", "role"]


class UnitRoleViewSet(viewsets.ModelViewSet):
    serializer_class = UnitRoleSerializer
    permission_classes = [permissions.IsAuthenticated & UnitRolePermission]
    queryset = UnitRole.objects.all()


class ServiceSectorRoleViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSectorRoleSerializer
    permission_classes = [permissions.IsAuthenticated & ServiceSectorRolePermission]
    queryset = ServiceSectorRole.objects.all()
