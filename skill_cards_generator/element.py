from __future__ import annotations

import enum
from typing import Optional


class Element(enum.Enum):
    fire = enum.auto()
    water = enum.auto()
    earth = enum.auto()
    wind = enum.auto()
    light = enum.auto()
    dark = enum.auto()

    def __str__(self) -> str:
        if self is Element.fire:
            return '火'
        elif self is Element.water:
            return '水'
        elif self is Element.earth:
            return '地'
        elif self is Element.wind:
            return '風'
        elif self is Element.light:
            return '光'
        else:
            assert self is Element.dark
            return '闇'

    @staticmethod
    def from_text(text: str) -> Optional[Element]:
        for elem in Element:
            if text == str(elem):
                return elem
        return None
