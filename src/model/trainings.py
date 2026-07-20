from dataclasses import dataclass, field

@dataclass
class EnumerationItem:
    value: str
    gap_before: bool = False


def is_month_change(previous: str, current: str) -> bool:
    pre_parts = [int(part) for part in previous.split("-")]
    current_parts = [int(part) for part in current.split("-")]
    return (current_parts[0], current_parts[1]) != (pre_parts[0], pre_parts[1])

@dataclass
class Trainings:
    dates: list[str] = field(default_factory=list)
    current: str | None = None

    def get_items_history(self) -> list[EnumerationItem]:
        output = []
        self.current = None
        while (next := self.get_next()) is not None:
            output.append(next)
        return output

    def get_next(self) -> EnumerationItem | None:
        if self.current is None:
            self.current = self.dates[0]
            return EnumerationItem(value=self.current)
        else:
            index = self.dates.index(self.current)
            if index + 1 > len(self.dates) - 1:
                return None
            gap = is_month_change(self.current, self.dates[index + 1])
            self.current = self.dates[index + 1]
            return EnumerationItem(value=self.current, gap_before=gap)
