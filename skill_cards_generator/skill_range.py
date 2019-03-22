import enum
from dataclasses import dataclass, field


class RangeUnit(enum.Enum):
    sq = enum.auto()
    m = enum.auto()

    def __str__(self):
        if self is sq:
            return 'sq'
        else:
            return 'm'


@dataclass
class SkillRange:
    value: int
    unit: RangeUnit = field(default=RangeUnit.m)

    def __str__(self):
        if self.unit == RangeUnit.m and self.value == 0:
            return '至近'
        return str(self.value) + self.unit
