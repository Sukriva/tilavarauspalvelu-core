import datetime
import time
from typing import Union

from applications.models import ApplicationEvent, ApplicationPeriod
from reservation_units.models import ReservationUnit

from ortools.sat.python import cp_model

class OpenTime(object):
    def __init__(self, date: datetime, begin: time ,end: time):
        self.date = date
        self.begin = begin
        self.end = end

def random_times():
    times = []
    for i in range(10):
        times.append(
            OpenTime(
                date=datetime.datetime(year=2021, month=1, day = i+1, hour=1, minute=0),
                begin=datetime.datetime(year=2021, month=1, day=i+1, hour=1, minute=0),
                end=datetime.datetime(year=2021, month=1, day=i+1, hour=23, minute=0),
            )
        )

    return times
class Unit(object):

    def __init__(self, times_open: [OpenTime]):
        self.times_open = {x.date.date(): x for x in times_open}

def random_units():
    return Unit(
                times_open=random_times()
            )

class EventRequest(object):
    def __init__(self, start: datetime, end: datetime, min_duration: int, max_duration: Union[int, None]):
        self.min_duration = min_duration
        self.max_duration = min_duration if max_duration is None else min_duration
        self.start_date = start.date()
        self.end_date = end.date()
        self.start_time = start.time()
        self.end_time = end.time()
        self.time_set = start.time()

def random_events():
    events = []
    for i in range(10):
        print("fuck this")
        print(i)
        events.append(EventRequest(
            start= datetime.datetime(year=2021, month=1, day = i+1, hour=10 + i, minute=0),
            end = datetime.datetime(year=2021, month=1, day=i+1, hour=10 + i + 3, minute=0),
            min_duration=1,
            max_duration=1
        ))
    return events

class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, shifts, num_nurses, num_days, num_shifts, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._num_nurses = num_nurses
        self._num_days = num_days
        self._num_shifts = num_shifts
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            print('Solution %i' % self._solution_count)
            for d in range(self._num_days):
                print('Day %i' % d)
                for n in range(self._num_nurses):
                    is_working = False
                    for s in range(self._num_shifts):
                        if self.Value(self._shifts[(n, d, s)]):
                            is_working = True
                            print('  Nurse %i works shift %i' % (n, s))
                    if not is_working:
                        print('  Nurse {} does not work'.format(n))
            print()
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count



class AllocationSolver(object):


    def __init__(self):
        self.events = random_events()
        self.unit = random_units()
        self.model = cp_model.CpModel()

    def initialize(self):
        print("init")
    def event_rules(self):
        print("rules")

    def solve(self):
        for event in self.events:
            self.model.Add(event.start_date in self.unit.times_open)

        solver = cp_model.CpSolver()
        solver.SearchForAllSolutions(self.model)
        print("solver")






