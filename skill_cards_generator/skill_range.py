from __future__ import annotations

import enum
from dataclasses import dataclass


class RangeUnit(enum.Enum):
    sq = enum.auto()
    m = enum.auto()

    def __str__(self):
        if self is RangeUnit.sq:
            return 'sq'
        else:
            return 'm'


class SkillRangeKind(enum.Enum):
    nothing = enum.auto()
    weapon = enum.auto()
    sight = enum.auto()
    scene = enum.auto()
    with_unit = enum.auto()


@dataclass
class SkillRange:
    def __init__(
        self,
        kind: SkillRangeKind,
        value: int = None,
        unit: RangeUnit = RangeUnit.m
    ) -> None:
        if kind is SkillRangeKind.with_unit:
            assert value is not None
        self._kind = kind
        self._value = value
        self._unit = unit

    @staticmethod
    def from_text(text: str) -> SkillRange:
        return SkillRange(SkillRangeKind.with_unit, 0)

    def __str__(self):
        if self._kind is SkillRangeKind.nothing:
            return 'ー'
        elif self._kind is SkillRangeKind.weapon:
            return '武器'
        elif self._kind is SkillRangeKind.sight:
            return '視界'
        elif self._kind is SkillRangeKind.scene:
            return 'シーン'
        else:
            assert (self._kind is SkillRangeKind.with_unit
                    and self._value is not None)
            if self._unit == RangeUnit.m and self._value == 0:
                return '至近'
            return str(self._value) + str(self._unit)
