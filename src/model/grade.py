from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal

from libRunning import GradeModel

from src.model.dashboard import to_time


@dataclass
class Grade:
    grade: int
    start: str
    end: str

    @staticmethod
    def can_convert_to_int(value: Decimal) -> bool:
        return value == int(value)

    @staticmethod
    def convert(grades: list[GradeModel]) -> dict[int, Grade]:
        grade_dict: dict[int, Grade] = {}
        for g in grades:
            if g.time_convertible:
                int_from = int(g.from_)
                int_to = int(g.to_)

                start = to_time(int_from)
                end = to_time(int_to)
            else:
                start = str(g.from_)
                if Grade.can_convert_to_int(g.from_):
                    start = str(int(g.from_))

                end = str(g.to_)
                if Grade.can_convert_to_int(g.to_):
                    end = str(int(g.to_))

            grade = Grade(
                g.grade,
                start=start,
                end=end,
            )
            grade_dict[g.grade] = grade
        return grade_dict