import datetime

import pytest


@pytest.mark.django_db
def test_getting_occurrences(recurring_application_event, scheduled_for_tuesday):
    occurrences = recurring_application_event.get_all_occurrences()
    dates = []
    start = datetime.datetime(2020, 1, 7, 10, 0)
    delta = datetime.timedelta(days=7)
    while start <= datetime.datetime(2020, 2, 25, 10, 0):
        dates.append(start)
        start += delta
    assert occurrences[scheduled_for_tuesday.id].occurrences == dates
    assert occurrences[scheduled_for_tuesday.id].weekday == scheduled_for_tuesday.day


@pytest.mark.django_db
def test_getting_occurreces_between(recurring_application_event, scheduled_for_tuesday):
    start = datetime.datetime(year=2020, month=1, day=12, hour=0, minute=0)
    end = datetime.datetime(year=2020, month=1, day=23, hour=0, minute=0)
    occurrences = recurring_application_event.get_occurrences_between(start, end)
    assert occurrences[scheduled_for_tuesday.id].occurrences == [datetime.datetime(2020, 1, 14, 10, 0), datetime.datetime(2020, 1, 21, 10, 0)]
    assert occurrences[scheduled_for_tuesday.id].weekday == scheduled_for_tuesday.day

