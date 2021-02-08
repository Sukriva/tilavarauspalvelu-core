import datetime
import logging
import math
from typing import Dict

from ortools.sat.python import cp_model

from reservations.allocation_models import (
    ALLOCATION_PRECISION,
    AllocationData,
    AllocationEvent,
    AllocationSpace,
)

logger = logging.getLogger(__name__)


def suitable_spaces_for_event(
    allocation_event: AllocationEvent, spaces: Dict[int, AllocationSpace]
) -> Dict[int, AllocationSpace]:
    suitable_spaces = {}
    for space_id, space in spaces.items():
        if space_id in allocation_event.space_ids:
            suitable_spaces[space_id] = space
    return suitable_spaces


class AllocatedEvent(object):
    def __init__(
        self,
        space: AllocationSpace,
        event: AllocationEvent,
        duration: int,
        occurrence_id: int,
        start: int,
        end: int,
    ):
        self.space_id = space.id
        self.event_id = event.id
        self.duration = datetime.timedelta(minutes=duration * ALLOCATION_PRECISION)
        self.occurrence_id = occurrence_id
        self.begin = start
        self.end = end


class AllocationSolutionPrinter(object):
    def __init__(
        self,
        model: cp_model.CpModel,
        spaces,
        allocation_events,
        starts,
        ends,
        selected={},
    ):
        self.model = model
        self.selected = selected
        self.spaces = spaces
        self.allocation_events = allocation_events
        self.starts = starts
        self.ends = ends

    def print_solution(self):
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)
        solution = []
        if status == cp_model.OPTIMAL:
            logger.info("Total cost = %i" % solver.ObjectiveValue())

            for event in self.allocation_events:
                for occurrence_id, occurrence in event.occurrences.items():
                    for space_id, space in suitable_spaces_for_event(
                        event, self.spaces
                    ).items():
                        if solver.BooleanValue(
                            self.selected[(space.id, event.id, occurrence_id)]
                        ):
                            logger.info(
                                "Space ",
                                space.id,
                                " assigned to application event ",
                                event.id,
                                "  Duration = ",
                                event.min_duration,
                            )
                            start_delta = datetime.timedelta(
                                minutes=solver.Value(self.starts[occurrence_id])
                                * ALLOCATION_PRECISION
                            )
                            end_delta = datetime.timedelta(
                                minutes=solver.Value(self.ends[occurrence_id])
                                * ALLOCATION_PRECISION
                            )
                            solution.append(
                                AllocatedEvent(
                                    space=space,
                                    event=event,
                                    duration=event.min_duration,
                                    occurrence_id=occurrence_id,
                                    start=(datetime.datetime.min + start_delta).time(),
                                    end=(datetime.datetime.min + end_delta).time(),
                                )
                            )

        logger.info("Statistics")
        logger.info("  - conflicts : %i" % solver.NumConflicts())
        logger.info("  - branches  : %i" % solver.NumBranches())
        logger.info("  - wall time : %f s" % solver.WallTime())
        return solution


class AllocationSolver(object):
    def __init__(self, allocation_data: AllocationData):
        self.spaces: Dict[int, AllocationSpace] = allocation_data.spaces
        self.allocation_events = allocation_data.allocation_events
        self.starts = {}
        self.ends = {}
        self.model = cp_model.CpModel()
        self.selected = {}

    def solve(self):

        for allocation_event in self.allocation_events:
            for occurrence_id, occurrence in allocation_event.occurrences.items():
                for space_id, space in suitable_spaces_for_event(
                    allocation_event, self.spaces
                ).items():
                    self.selected[
                        (space.id, allocation_event.id, occurrence_id)
                    ] = self.model.NewBoolVar("x[%i,%i]" % (space_id, occurrence_id))

        self.constraint_allocation()

        self.contraint_by_events_per_week()
        self.constraint_by_capacity()
        self.constraint_by_event_time_limits()
        self.maximize()

        printer = AllocationSolutionPrinter(
            model=self.model,
            spaces=self.spaces,
            allocation_events=self.allocation_events,
            selected=self.selected,
            starts=self.starts,
            ends=self.ends,
        )
        return printer.print_solution()

    def constaint_by_opening_hours(self, duration:int, allocation_event_id:int, occurrence_id:int, space: AllocationSpace):
        # TODO: When we have opening times from hauki and/or model structure in place, replace with opening hours
        # Now this is hard coded to each space being open from 10 to 22 daily
        open_start = math.ceil(10 * 60 / ALLOCATION_PRECISION)
        open_end = math.ceil(22 * 60 / ALLOCATION_PRECISION)
        name_suffix = "_%i" % occurrence_id
        start = self.model.Add(open_start, open_end, "open_start" + name_suffix)
        end = self.model.NewIntVar(open_start, open_end, "open_end" + name_suffix)
        performed = self.selected[
            (space.id, allocation_event_id, occurrence_id)
        ]
        interval = self.model.NewOptionalIntervalVar(
            start,
            duration,
            end,
            performed,
            "interval_%i_on_s%i" % (occurrence_id, space.id),
        )

    def constraint_by_event_time_limits(self):

        for space_id, space in self.spaces.items():
            intervals = []
            for allocation_event in self.allocation_events:
                for occurrence_id, occurrence in allocation_event.occurrences.items():
                    if (space_id, allocation_event.id, occurrence_id) in self.selected:
                        duration = allocation_event.min_duration
                        min_start = occurrence.begin
                        max_end = occurrence.end
                        name_suffix = "_%i" % occurrence_id
                        start = self.model.NewIntVar(min_start, max_end, "s" + name_suffix)
                        end = self.model.NewIntVar(min_start, max_end, "e" + name_suffix)
                        self.model.Add(start < math.ceil(22*60*ALLOCATION_PRECISION) and start < math.ceil(22*60*ALLOCATION_PRECISION))
                        performed = self.selected[
                            (space_id, allocation_event.id, occurrence_id)
                        ]
                        interval = self.model.NewOptionalIntervalVar(
                            start,
                            duration,
                            end,
                            performed,
                            "interval_%i_on_s%i" % (occurrence_id, space_id),
                        )
                        self.starts[occurrence_id] = start
                        self.ends[occurrence_id] = end
                        #duration:int, allocation_event_id:int, occurrence_id:int, space: AllocationSpace)
                        #self.constaint_by_opening_hours(duration=duration, allocation_event_id=allocation_event.id, occurrence_id=occurrence_id, space=space)
                        intervals.append(interval)
            self.model.AddNoOverlap(intervals)

    def constraint_by_capacity(self):
        # Event durations in each space do not exceed the capacity
        self.model.Add(
            sum(
                self.selected[(space_id, event.id, event_occurrence_id)] * event.min_duration
                for event in self.allocation_events
                for event_occurrence_id, occurrence in event.occurrences.items()
                for space_id, space in suitable_spaces_for_event(
                    event, self.spaces
                ).items()
            )
            # TODO: When we have opening times from hauki and/or model structure in place, replace with opening hours
            # Now this is hard coded to each space being open for 10 hours daily
            <= math.ceil(10 * 60 / ALLOCATION_PRECISION)
        )

    def contraint_by_events_per_week(self):
        # No more than requested events per week is allocated
        for event in self.allocation_events:
            for space_id, space in suitable_spaces_for_event(
                event, self.spaces
            ).items():
                self.model.Add(
                    sum(
                        self.selected[(space_id, event.id, occurrence_id)]
                        for occurrence_id, occurrence in event.occurrences.items()
                    )
                    <= event.events_per_week
                )

    def constraint_allocation(self):
        # Each event is assigned to at most one space.
        for event in self.allocation_events:
            for occurrence_id, occurrence in event.occurrences.items():
                self.model.Add(
                    sum(
                        self.selected[(space_id, event.id, occurrence_id)]
                        for space_id, space in suitable_spaces_for_event(
                            event, self.spaces
                        ).items()
                    )
                    <= 1
                )

    # Objective
    def maximize(self):
        self.model.Maximize(
            sum(
                self.selected[(space_id, event.id, event_occurrence_id)] * event.min_duration
                for event in self.allocation_events
                for event_occurrence_id, occurrence in event.occurrences.items()
                for space_id, space in suitable_spaces_for_event(
                    event, self.spaces
                ).items()
            )
        )
