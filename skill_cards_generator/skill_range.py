import enum
from dataclasses import dataclass


class RangeUnit(enum.Enum):
    sq = enum.auto()
    m = enum.auto()


@dataclass
class SkillRange:
    unit: RangeUnit
    value: int
