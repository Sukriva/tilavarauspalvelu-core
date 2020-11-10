from rest_framework import viewsets
from reservation_units.models import ReservationUnit
from api.base import BaseNestedSerializer
from api.space_api import SpaceSerializer
from api.resources_api import ResourceSerializer
from api.services_api import ServiceSerializer


class ReservationUnitSerializer(BaseNestedSerializer):
    spaces = SpaceSerializer(read_only=True, many=True, exclude_detail_fields=True)
    resources = ResourceSerializer(
        read_only=True, many=True, exclude_detail_fields=True
    )
    services = ServiceSerializer(read_only=True, many=True, exclude_detail_fields=True)

    class Meta:
        model = ReservationUnit
        fields = [
            "id",
            "name",
            "spaces",
            "resources",
            "services",
            "require_introduction",
        ]
        detail_only_fields = ["spaces", "resources", "services", "require_introduction"]


class ReservationUnitViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationUnitSerializer

    def get_queryset(self):
        qs = ReservationUnit.objects.all().prefetch_related(
            "spaces", "resources", "services"
        )
        return qs