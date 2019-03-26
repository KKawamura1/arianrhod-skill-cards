from __future__ import annotations

import enum
from typing import List, Tuple, Set
from .normalized_check import normalize_and_check


class TargetKind(enum.Enum):
    myself = enum.auto()
    single = enum.auto()
    force_single = enum.auto()
    multiple = enum.auto()
    engage = enum.auto()
    engage_selectable = enum.auto()
    field = enum.auto()
    field_selectable = enum.auto()


single_set = {'単', '単体', '1', '一', '1体', '一体', 'one', 'single'}
engage_set = {'範', '範囲', 'eg', 'e', 'engage', 'エンゲージ'}
field_set = {'場', '場面', 'field', 'scene', 's', 'シーン'}
selectable_set = {'（選択）', '（選）', '選択', '選', 'c', 'choice', ' choice'}
unify_target_table: List[Tuple[TargetKind, Set[str]]] = [
    (TargetKind.myself, {'', '-', '自', '自身', '0', 'self', 'u', '自分'}),
    (TargetKind.single, single_set),
    (TargetKind.force_single, {single + '※' for single in single_set}),
    (TargetKind.engage, engage_set),
    (TargetKind.engage_selectable, {engage + selectable
                                    for engage in engage_set
                                    for selectable in selectable_set}),
    (TargetKind.field, field_set),
    (TargetKind.field_selectable, {field + selectable
                                   for field in field_set
                                   for selectable in selectable_set}),
]
kansuuji_table = str.maketrans('〇一二三四五六七八九零壱弐参', '01234567890123', '体')


class Target:
    def __init__(
        self,
        target_kind: TargetKind,
        target_num: int = None,
    ) -> None:
        self._kind = target_kind
        if self._kind is TargetKind.multiple:
            assert target_num is not None and target_num >= 2
            self._num = target_num

    def __str__(self):
        if self._kind is TargetKind.myself:
            return '自身'
        elif self._kind is TargetKind.single:
            return '単体'
        elif self._kind is TargetKind.force_single:
            return '単体※'
        elif self._kind is TargetKind.multiple:
            return f'{self._num}体'
        elif self._kind is TargetKind.engage:
            return '範囲'
        elif self._kind is TargetKind.engage_selectable:
            return '範囲（選択）'
        elif self._kind is TargetKind.field:
            return '場面'
        else:
            assert self._kind is TargetKind.field_selectable
            return '場面（選択）'

    @staticmethod
    def from_text(text: str) -> Target:
        kind = normalize_and_check(text, unify_target_table)
        if kind is not None:
            return Target(kind)
        assert len(text) > 0
        text = text.translate(kansuuji_table)
        try:
            num = int(text)
        except ValueError:
            num = None
        if num:
            return Target(TargetKind.multiple, num)
        return Target(TargetKind.myself)
