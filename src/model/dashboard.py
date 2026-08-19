from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from libRunning import DashboardModel, SectionModel

from src.model.trainings import EnumerationItem, Trainings

EMPTY_CELL: int = -1

def to_time(sec: int) -> str:
    mins: int = sec // 60
    secs = sec % 60
    ssecs = str(secs).zfill(2)
    return f"{mins}:{ssecs}"

@dataclass
class Cell:
    time: int
    order: int = 0
    grade: int = 0
    lost: int = 0
    time_convertible: bool = True
    less_is_best: bool = True

    @property
    def get_grade_class(self) -> str:
        return f"grade-{self.grade}"

    @property
    def time_converted(self) -> str:
        if not self.time_convertible:
            return str(self.time)
        return to_time(self.time)

    @property
    def str_order(self) -> str:
        return str(self.order).rjust(2, " ")

    @property
    def str_lost(self) -> str:
        return str(self.lost)

    @staticmethod
    def create_instance(obj: SectionModel) -> Cell:
        return Cell(
            time=obj.value,
            order=obj.order,
            grade=obj.grade,
            lost=obj.lost,
            time_convertible=obj.time_convertible,
            less_is_best=obj.less_is_best,
        )

    @property
    def is_empty(self) -> bool:
        return self.time == EMPTY_CELL


@dataclass
class Dashboard:
    sections: list[str] = field(default_factory=list)
    aggregations: list[str] = field(default_factory=list)
    dates: list[EnumerationItem] = field(default_factory=list)
    data: dict[tuple[str, str], Cell] = field(default_factory=dict)

    @staticmethod
    def create_instance(dashboard: DashboardModel) -> Dashboard:
        dates = dashboard.get_dates()
        trainings = Trainings(dates=dates)
        trainings_history = trainings.get_items_history()
        d = Dashboard(
            sections=dashboard.sections,
            aggregations=dashboard.aggregations,
            dates=trainings_history,
        )
        for date in dates:
            for section in dashboard.sections + dashboard.aggregations:
                cell = dashboard.get_data(date, section)
                if cell is not None:
                    d.data[(date, section)] = Cell.create_instance(cell)
        return d


def get_cell(dashboard: Dashboard, date: str, section: str) -> Cell:
    cell = dashboard.data.get((date, section))
    if cell is None:
        return Cell(time=EMPTY_CELL)
    return cell