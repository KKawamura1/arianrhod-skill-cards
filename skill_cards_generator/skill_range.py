from __future__ import annotations

import enum
import re
import mojimoji


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
    string = enum.auto()


class SkillRange:
    kind_table = [
        [SkillRangeKind.weapon, ('武器', '武', 'weapon', 'wp', 'w')],
        [SkillRangeKind.sight, ('視界', '視', 'sight', 'st')],
        [SkillRangeKind.scene, ('シーン', 'シ', 'scene', 'scn', 'sn')],
        [SkillRangeKind.nothing, ('', '-')],
    ]
    metre = re.compile(r'^\s*([0-9]+)\s*m?$', re.IGNORECASE)
    square = re.compile(r'^\s*([0-9]+)\s*sq$', re.IGNORECASE)

    def __init__(
        self,
        kind: SkillRangeKind,
        value: int = None,
        unit: RangeUnit = RangeUnit.m,
        string: str = None
    ) -> None:
        if kind is SkillRangeKind.with_unit:
            assert value is not None
        elif kind is SkillRangeKind.string:
            assert string is not None
        self._kind = kind
        self._value = value
        self._unit = unit
        self._string = string

    @staticmethod
    def from_text(text: str) -> SkillRange:
        for kind, candidates in SkillRange.kind_table:
            for candidate in candidates:
                if (mojimoji.zen_to_han(text).lower()
                        == mojimoji.zen_to_han(candidate).lower()):
                    return SkillRange(kind)
        if mojimoji.zen_to_han(text).lower() in ('至近', '至'):
            return SkillRange(SkillRangeKind.with_unit, 0)
        if SkillRange.metre.match(text) is not None:
            return SkillRange(
                SkillRangeKind.with_unit,
                int(SkillRange.metre.match(text).group(1)),
                RangeUnit.m
            )
        if SkillRange.square.match(text) is not None:
            return SkillRange(
                SkillRangeKind.with_unit,
                int(SkillRange.square.match(text).group(1)),
                RangeUnit.sq
            )

        return SkillRange(SkillRangeKind.string, string=text)

    def __str__(self):
        if self._kind is SkillRangeKind.nothing:
            return 'ー'
        elif self._kind is SkillRangeKind.weapon:
            return '武器'
        elif self._kind is SkillRangeKind.sight:
            return '視界'
        elif self._kind is SkillRangeKind.scene:
            return 'シーン'
        elif self._kind is SkillRangeKind.with_unit:
            assert self._value is not None
            if self._unit == RangeUnit.m and self._value == 0:
                return '至近'
            return str(self._value) + str(self._unit)
        else:
            assert self._kind is SkillRangeKind.string
            assert self._string is not None
            return self._string
