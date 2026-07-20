from dataclasses import dataclass, field

from src.model.dashboard import Cell

from libRunning import SectionModel


@dataclass
class SectionDates:
    dates_values: dict[str, Cell] = field(default_factory=dict)
    output: list[tuple[str, Cell]] = field(default_factory=list)

    def add_date(self, date: str, model: SectionModel) -> None:
        self.dates_values[date] = Cell.create_instance(model)

    def prepare(self) -> None:
        self.output = []
        sorted_dict = dict(sorted(self.dates_values.items(), key=lambda item: item[1].order))
        for date, cell in sorted_dict.items():
            self.output.append((date, cell))


