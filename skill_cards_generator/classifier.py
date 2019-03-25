from __future__ import annotations

import enum
from typing import Sequence, Optional
import mojimoji
from .element import Element


class ClassifierKind(enum.Enum):
    spell = enum.auto()
    song = enum.auto()
    alchemy = enum.auto()
    role = enum.auto()
    style = enum.auto()
    string = enum.auto()

    def __str__(self) -> str:
        if self is ClassifierKind.spell:
            return '魔術'
        elif self is ClassifierKind.song:
            return '呪歌'
        elif self is ClassifierKind.alchemy:
            return '錬金術'
        elif self is ClassifierKind.role:
            return 'ロール'
        elif self is ClassifierKind.style:
            return '流派'
        else:
            pass


unify_classifier_table = [
    [ClassifierKind.spell, ('魔', '魔術', 'spell', 'spl', 'sp',
                            'magic', 'mag', 'mg')],
    [ClassifierKind.song, ('呪', '歌', '呪歌', 'song', 'sg')],
    [ClassifierKind.alchemy, ('錬', '錬金', '錬金術', 'alchemy',
                              'alc', 'ac', 'acm')],
    [ClassifierKind.role, ('ロ', 'ロール', 'role', 'rl')],
    [ClassifierKind.style, ('ス', 'スタイル', '流', '流派',
                            'style', 'sty', 'stl', 'st', 'sy')],
]


class Classifier:
    def __init__(
        self,
        kind: ClassifierKind,
        elements: Sequence[Element] = None
    ) -> None:
        self._kind = kind
        if self._kind is ClassifierKind.spell:
            assert elements is not None
            self._elements = list(elements)

    @staticmethod
    def from_text(text: str) -> Optional[Classifier]:
        for kind, candidates in unify_classifier_table:
            for candidate in candidates:
                if (mojimoji.zen_to_han(text).lower()
                        == mojimoji.zen_to_han(candidate).lower()):
                    return Classifier(kind)
