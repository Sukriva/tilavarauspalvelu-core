from rest_framework import mixins, viewsets

from api.base import TranslatedModelSerializer
from services.models import Service
from permissions.models import UnitRole, ServiceSectorRole


class UnitRoleSerializer(TranslatedModelSerializer):
    class Meta:
        model = UnitRole


class ServiceSectorRoleSerializer(TranslatedModelSerializer):
    class Meta:
        model = ServiceSectorRole


class UnitRoleViewSet(viewsets.ModelViewSet):
    serializer_class = UnitRoleSerializer
    queryset = UnitRole.objects.all()


class ServiceSectorRoleViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSectorRoleSerializer
    queryset = ServiceSectorRole.objects.all()
