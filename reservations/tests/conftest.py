import datetime
from typing import Dict

import pytest

from applications.models import (
    Application,
    ApplicationEvent,
    ApplicationEventSchedule,
    ApplicationRound,
    EventReservationUnit,
)
from reservation_units.models import ReservationUnit
from spaces.models import Space


@pytest.fixture(autouse=True)
def setup_audit_log(settings):
    settings.AUDIT_LOGGING_ENABLED = False


def get_default_start() -> datetime.date:
    return datetime.date(year=2020, month=1, day=1)


def get_default_end() -> datetime.date:
    return datetime.date(year=2020, month=1, day=31)


@pytest.fixture
def default_application_round() -> ApplicationRound:
    return ApplicationRound.objects.create(
        application_period_begin=get_default_start(),
        application_period_end=get_default_end(),
        reservation_period_begin=get_default_start(),
        reservation_period_end=get_default_end(),
        public_display_begin=get_default_start(),
        public_display_end=get_default_end(),
    )


@pytest.fixture
def space_for_15_persons():
    return Space.objects.create(name="Space", max_persons=15)


@pytest.fixture
def space_for_5_persons():
    return Space.objects.create(name="Space", max_persons=5)


@pytest.fixture
def reservation_unit(space_for_15_persons) -> ReservationUnit:
    reservation_unit = ReservationUnit.objects.create(
        name_en="Test reservation unit", require_introduction=False
    )
    reservation_unit.spaces.set([space_for_15_persons])
    return reservation_unit


@pytest.fixture
def second_reservation_unit(space_for_5_persons):
    reservation_unit = ReservationUnit.objects.create(
        name_en="Second test reservation unit",
        require_introduction=False,
    )
    reservation_unit.spaces.set([space_for_5_persons])
    return reservation_unit


@pytest.fixture
def application_round_with_reservation_units(
    reservation_unit, default_application_round
) -> ApplicationRound:
    default_application_round.reservation_units.set([reservation_unit])
    return default_application_round


@pytest.fixture
def minimal_application(default_application_round) -> Application:
    return Application.objects.create(application_round_id=default_application_round.id)


@pytest.fixture
def application_with_reservation_units(
    application_round_with_reservation_units,
) -> Application:
    return Application.objects.create(
        application_round_id=application_round_with_reservation_units.id
    )


@pytest.fixture
def application_with_application_events(
    application_with_reservation_units,
) -> Application:
    return Application.objects.create(
        application_round_id=application_with_reservation_units.id
    )


@pytest.fixture
def recurring_application_event(application_with_reservation_units) -> ApplicationEvent:
    return ApplicationEvent.objects.create(
        application=application_with_reservation_units,
        num_persons=10,
        min_duration=datetime.timedelta(hours=1),
        max_duration=datetime.timedelta(hours=2),
        name="Football",
        events_per_week=2,
        begin=datetime.date(year=2020, month=1, day=1),
        end=datetime.date(year=2020, month=2, day=28),
        biweekly=False,
    )


@pytest.fixture
def scheduled_for_monday(recurring_application_event) -> ApplicationEventSchedule:
    return ApplicationEventSchedule.objects.create(
        day=0, begin="10:00", end="12:00", application_event=recurring_application_event
    )


@pytest.fixture
def matching_event_reservation_unit(
    recurring_application_event, reservation_unit
) -> EventReservationUnit:
    return EventReservationUnit.objects.create(
        priority=100,
        application_event=recurring_application_event,
        reservation_unit=reservation_unit,
    )


@pytest.fixture
def not_matching_event_reservation_unit(
    recurring_application_event, second_reservation_unit
) -> EventReservationUnit:
    return EventReservationUnit.objects.create(
        priority=100,
        application_event=recurring_application_event,
        reservation_unit=second_reservation_unit,
    )


@pytest.fixture
def multiple_applications(
    application_round_with_reservation_units, request, reservation_unit
) -> Dict[str, list]:
    applications = []
    created_events = []
    schedules = []

    for application in request.param["applications"]:
        created_application = Application.objects.create(
            application_round_id=application_round_with_reservation_units.id
        )
        applications.append(created_application)
        for event in application["events"]:
            created_event = ApplicationEvent.objects.create(
                application=created_application,
                num_persons=15,
                min_duration=datetime.timedelta(minutes=event["duration"]),
                max_duration=datetime.timedelta(minutes=event["duration"]),
                name="Football",
                events_per_week=event["events_per_week"],
                begin=datetime.date(year=2020, month=1, day=1),
                end=datetime.date(year=2020, month=2, day=28),
                biweekly=False,
            )
            for schedule in event["schedules"]:
                created_schedule = ApplicationEventSchedule.objects.create(
                    day=schedule["day"],
                    begin=schedule["start"] if "start" in schedule else "10:00",
                    end=schedule["end"] if "end" in schedule else "22:00",
                    application_event=created_event,
                )

                schedules.append(created_schedule)
            created_events.append(created_event)

            EventReservationUnit.objects.create(
                priority=100,
                application_event=created_event,
                reservation_unit=reservation_unit,
            )

    return {
        "applications": applications,
        "created_events": created_events,
        "schedules": schedules,
    }
