from __future__ import annotations

import enum
from typing import Sequence, Optional, List, Tuple, Set
from .element import Element
from .normalized_check import normalize_and_check


class ClassifierKind(enum.Enum):
    spell = enum.auto()
    song = enum.auto()
    alchemy = enum.auto()
    role = enum.auto()
    style = enum.auto()
    string = enum.auto()


unify_classifier_table: List[Tuple[ClassifierKind, Set[str]]] = [
    (ClassifierKind.spell, {'魔', '魔術', 'spell', 'spl', 'sp',
                            'magic', 'mag', 'mg'}),
    (ClassifierKind.song, {'呪', '歌', '呪歌', 'song', 'sg'}),
    (ClassifierKind.alchemy, {'錬', '錬金', '錬金術', 'alchemy',
                              'alc', 'ac', 'acm'}),
    (ClassifierKind.role, {'ロ', 'ロール', 'role', 'rl'}),
    (ClassifierKind.style, {'ス', 'スタイル', '流', '流派',
                            'style', 'sty', 'stl', 'st', 'sy'}),
]

ignored_symbols = {',', '.', '<', '〈', '《', '[', '{', '「', '【', '『',
                   '>', '〉', '》', ']', '}', '」', '】', '』'}


class Classifier:
    def __init__(
        self,
        kind: ClassifierKind,
        elements: Sequence[Element] = None,
        string: str = None,
    ) -> None:
        self._kind = kind
        if self._kind is ClassifierKind.spell:
            self._elements: List[Element]
            if elements is None:
                self._elements = []
            else:
                self._elements = list(elements)
        if self._kind is ClassifierKind.string:
            assert string is not None
            self._string = string

    def __str__(self) -> str:
        if self._kind is ClassifierKind.spell:
            if self._elements:
                return '魔術〈' + '／'.join([str(elem) for elem in self._elements]) + '〉'
            return '魔術'
        elif self._kind is ClassifierKind.song:
            return '呪歌'
        elif self._kind is ClassifierKind.alchemy:
            return '錬金術'
        elif self._kind is ClassifierKind.role:
            return 'ロール'
        elif self._kind is ClassifierKind.style:
            return '流派'
        else:
            assert self._kind is ClassifierKind.string and self._string is not None
            return self._string

    @staticmethod
    def from_text(text: str) -> Optional[Classifier]:
        kind = normalize_and_check(text, unify_classifier_table)
        if kind is not None:
            return Classifier(kind)
        if text[:2] == '魔術':
            elements: List[Element] = []
            for char in text[2:]:
                symbol = normalize_and_check(
                    char, [(smb, set([smb])) for smb in ignored_symbols])
                if symbol is not None:
                    continue
                elem = Element.from_text(char)
                if elem is not None:
                    elements.append(elem)
                    continue
                return None
            if elements:
                return Classifier(ClassifierKind.spell, elements)
        return None
