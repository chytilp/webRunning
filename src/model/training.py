from __future__ import annotations
from dataclasses import dataclass, field

from src.model.dashboard import Cell

from libRunning import SectionModel, TrainingModel

@dataclass
class Training:
    date: str
    note: str = ""
    sections: dict[str, Cell] = field(default_factory=dict)
    aggregations: dict[str, Cell] = field(default_factory=dict)

    def add_section(self, name: str, model: SectionModel) -> None:
        self.sections[name] = Cell.create_instance(model)

    def add_aggregation(self, name: str, model: SectionModel) -> None:
        self.aggregations[name] = Cell.create_instance(model)

    @staticmethod
    def convert(model: TrainingModel) -> Training:
        note = model.note if model.note else ""
        training = Training(date=model.date, note=note)
        for section in model.sections:
            training.add_section(section.name, section)
        for aggregation in model.aggregations:
            training.add_aggregation(aggregation.name, aggregation)
        return training
