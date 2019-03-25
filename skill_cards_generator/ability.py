from __future__ import annotations

import enum
from typing import Optional


class Ability(enum.Enum):
    strength = enum.auto()
    dexterity = enum.auto()
    agility = enum.auto()
    inteligence = enum.auto()
    sense = enum.auto()
    mental = enum.auto()
    luck = enum.auto()

    def __str__(self) -> str:
        if self is Ability.strength:
            return '筋力'
        elif self is Ability.dexterity:
            return '器用'
        elif self is Ability.agility:
            return '敏捷'
        elif self is Ability.inteligence:
            return '知力'
        elif self is Ability.sense:
            return '感知'
        elif self is Ability.mental:
            return '精神'
        else:
            return '幸運'

    @staticmethod
    def from_text(text: str) -> Optional[Ability]:
        for abi in Ability:
            if str(abi) == text:
                return abi
        return None
