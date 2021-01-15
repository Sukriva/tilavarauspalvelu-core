from applications.models import ApplicationEvent, ApplicationPeriod
from reservation_units.models import ReservationUnit

from ortools.sat.python import cp_model


class AllocationSolver(object):

    def __init__(self, application_events: [ApplicationEvent], reservation_unit: ReservationUnit,
                 application_period: ApplicationPeriod):
        self.__reservation_unit = reservation_unit
        self.__application_events = application_events
        self.__application_period = application_period

        self.__model = cp_model.CpModel()

    def initialize(self):

    def event_rules(self):
        
        for application_event in self.__application_events:
            self.__model.add

    def solver(self):






