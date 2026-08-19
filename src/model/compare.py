from dataclasses import dataclass, field

from src.model.dashboard import Cell
from src.model.training import Training

@dataclass
class ValueDifference:
    value: int
    text_value: str
    less_is_best: bool = True
    color_class: str = ""

    def __post_init__(self) -> None:
        if self.value == 0:
            self.color_class = "neutral"

        if self.less_is_best:
            if self.value < 0:
                self.color_class = "positive"
            elif self.value > 0:
                self.color_class = "negative"
        else:
            if self.value < 0:
                self.color_class = "negative"
            elif self.value > 0:
                self.color_class = "positive"


@dataclass
class CompareObj:
    date_1: str
    date_2: str
    differences: dict[str, ValueDifference] = field(default_factory=dict)
    sections: list[str] = field(default_factory=list)
    aggregations: list[str] = field(default_factory=list)
    training_1: dict[str, Cell] = field(default_factory=dict)
    training_2: dict[str, Cell] = field(default_factory=dict)


@dataclass
class Difference:
    training_1: Training
    training_2: Training
    differences: dict[str, ValueDifference] = field(default_factory=dict)

    def _get_all_sections(self) -> list[str]:
        sections: set[str] = set()
        for section in list(self.training_1.sections.keys()) + list(self.training_2.sections.keys()):
            sections.add(section)
        return list(sections)

    def _get_all_aggregations(self) -> list[str]:
        aggregations: set[str] = set()
        for aggregation in list(self.training_1.aggregations.keys()) + list(self.training_2.aggregations.keys()):
            aggregations.add(aggregation)
        return list(aggregations)

    def calculate(self) -> CompareObj:
        self.differences = {}
        sections: list[str] = self._get_all_sections()
        aggregations: list[str] = self._get_all_aggregations()

        for section in sections:
            cell_1: Cell | None = self.training_1.sections.get(section)
            cell_2: Cell | None = self.training_2.sections.get(section)
            if cell_1 and cell_2:
                diff = cell_2.time - cell_1.time
                self.differences[section] = ValueDifference(value=diff, text_value=f"+{diff}" if diff > 0 else f"{diff}")

        for aggregation in aggregations:
            cell_1: Cell | None = self.training_1.aggregations.get(aggregation)
            cell_2: Cell | None = self.training_2.aggregations.get(aggregation)
            if cell_1 and cell_2:
                diff = cell_2.time - cell_1.time
                self.differences[aggregation] = ValueDifference(value=diff, text_value=f"+{diff}" if diff > 0 else f"{diff}",
                                                                less_is_best=cell_1.less_is_best)

        training_1 = self.training_1.sections.copy()
        training_1.update(self.training_1.aggregations)
        training_2 = self.training_2.sections.copy()
        training_2.update(self.training_2.aggregations)
        sections = sorted(sections, key=lambda x: int(x.split(".")[0]))
        return CompareObj(differences=self.differences, sections=sections, aggregations=sorted(aggregations),
                          training_1=training_1 , training_2=training_2, date_1=self.training_1.date,
                          date_2=self.training_2.date)
