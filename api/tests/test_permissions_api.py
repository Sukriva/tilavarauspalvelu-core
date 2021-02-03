@pytest.mark.django_db
def test_role_create(user, user_api_client, equipment_hammer, valid_service_sector_role_admin_data):
    assert ReservationUnit.objects.count() == 0

    # Test without permissions
    response = user_api_client.post(
        reverse("service_sector_role-list"), data=valid_reservation_unit_data, format="json"
    )
    assert response.status_code == 403

    # Test with unit manager role
    user.unit_roles.create(unit_id=valid_reservation_unit_data["unit_id"], user=user, role="manager")
    response = user_api_client.post(
        reverse("reservationunit-list"), data=valid_reservation_unit_data, format="json"
    )
    assert response.status_code == 201

    assert ReservationUnit.objects.count() == 1
    unit = ReservationUnit.objects.all()[0]
    assert unit.name_en == "New reservation unit"
    assert list(map(lambda x: x.id, unit.equipments.all())) == [equipment_hammer.id]
