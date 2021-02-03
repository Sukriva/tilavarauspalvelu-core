from rest_framework import mixins, viewsets, permissions, serializers

from api.base import TranslatedModelSerializer
from services.models import Service
from permissions.models import UnitRole, ServiceSectorRole
from permissions.api_permissions import ServiceSectorRolePermission


class UnitRoleSerializer(TranslatedModelSerializer):
    class Meta:
        model = UnitRole


class ServiceSectorRoleSerializer(TranslatedModelSerializer):
    service_sector_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceSectorRole.objects.all(), source="service_sector"
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceSectorRole.objects.all(), source="service_sector"
    )
    class Meta:
        model = ServiceSectorRole
        fields = ['service_sector_id', 'user_id', 'role']


class UnitRoleViewSet(viewsets.ModelViewSet):
    serializer_class = UnitRoleSerializer
    permission_classes = [permissions.IsAuthenticated & ReservationUnitPermission]
    queryset = UnitRole.objects.all()


class ServiceSectorRoleViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSectorRoleSerializer
    permission_classes = [permissions.IsAuthenticated & ServiceSectorRolePermission]
    queryset = ServiceSectorRole.objects.all()
