from __future__ import annotations
from dataclasses import dataclass

from libRunning import GradeModel

from src.model.dashboard import to_time


@dataclass
class Grade:
    grade: int
    start: str
    end: str

    @staticmethod
    def convert(grades: list[GradeModel]) -> dict[int, Grade]:
        grade_dict: dict[int, Grade] = {}
        for g in grades:
            if g.time_convertible:
                start = to_time(g.from_)
                end = to_time(g.to_)
            else:
                start = str(g.from_)
                end = str(g.to_)

            grade = Grade(
                g.grade,
                start=start,
                end=end,
            )
            grade_dict[g.grade] = grade
        return grade_dict