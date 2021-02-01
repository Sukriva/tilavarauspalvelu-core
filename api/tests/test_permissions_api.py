import pytest
from django.urls import reverse

from permissions.models import ServiceSectorRole, UnitRole


@pytest.mark.django_db
def test_role_create(
    user,
    user_2,
    user_api_client,
    service_sector,
    valid_service_sector_application_manager_role_data,
):
    assert ServiceSectorRole.objects.count() == 0

    # Test without permissions
    response = user_api_client.post(
        reverse("service_sector_role-list"),
        data=valid_service_sector_application_manager_role_data,
        format="json",
    )
    assert response.status_code == 403

    # Test with service sector admin role
    user.service_sector_roles.create(
        service_sector=service_sector, user=user, role=ServiceSectorRole.ROLE_ADMIN
    )
    response = user_api_client.post(
        reverse("service_sector_role-list"),
        data=valid_service_sector_application_manager_role_data,
        format="json",
    )

    assert response.status_code == 201

    assert user_2.service_sector_roles.filter(
        service_sector=service_sector, role=ServiceSectorRole.ROLE_APPLICATION_MANAGER
    ).exists()
