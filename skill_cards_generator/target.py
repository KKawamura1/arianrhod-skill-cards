from __future__ import annotations

import enum
from typing import List, Tuple, Set
import mojimoji
from .normalized_check import normalize_and_check, normalize_and_compare


class TargetKind(enum.Enum):
    myself = enum.auto()
    single = enum.auto()
    force_single = enum.auto()
    multiple = enum.auto()
    multiple_sl = enum.auto()
    engage = enum.auto()
    engage_selectable = enum.auto()
    field = enum.auto()
    field_selectable = enum.auto()
    line = enum.auto()
    line_selectable = enum.auto()
    cross = enum.auto()
    cross_selectable = enum.auto()
    string = enum.auto()


single_set = {'単', '単体', '1', '一', '1体', '一体', 'one', 'single'}
engage_set = {'範', '範囲', 'eg', 'e', 'engage', 'エンゲージ'}
field_set = {'場', '場面', 'field', 'scene', 's', 'シーン'}
line_set = {'直線', '直'}
cross_set = {'十字', '十'}
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
    (TargetKind.line, line_set),
    (TargetKind.line_selectable, {line + selectable
                                  for line in line_set
                                  for selectable in selectable_set}),
    (TargetKind.cross, cross_set),
    (TargetKind.cross_selectable, {cross + selectable
                                   for cross in cross_set
                                   for selectable in selectable_set}),
]
kansuuji_table = str.maketrans('〇一二三四五六七八九零壱弐参', '01234567890123', '体')


class Target:
    def __init__(
        self,
        target_kind: TargetKind,
        target_num: int = None,
        string: str = None,
    ) -> None:
        self._kind = target_kind
        if self._kind is TargetKind.multiple:
            assert target_num is not None and target_num >= 2
            self._num = target_num
        if self._kind is TargetKind.string:
            assert string is not None
            self._string = string

    def __str__(self):
        if self._kind is TargetKind.myself:
            return '自身'
        elif self._kind is TargetKind.single:
            return '単体'
        elif self._kind is TargetKind.force_single:
            return '単体※'
        elif self._kind is TargetKind.multiple:
            return mojimoji.han_to_zen(f'{self._num}体')
        elif self._kind is TargetKind.multiple_sl:
            return 'ＳＬ体'
        elif self._kind is TargetKind.engage:
            return '範囲'
        elif self._kind is TargetKind.engage_selectable:
            return '範囲（選択）'
        elif self._kind is TargetKind.field:
            return '場面'
        elif self._kind is TargetKind.field_selectable:
            return '場面（選択）'
        elif self._kind is TargetKind.line:
            return '直線'
        elif self._kind is TargetKind.line_selectable:
            return '直線（選択）'
        elif self._kind is TargetKind.cross:
            return '十字'
        elif self._kind is TargetKind.cross_selectable:
            return '十字（選択）'
        else:
            assert self._kind is TargetKind.string
            return mojimoji.han_to_zen(self._string)

    @staticmethod
    def from_text(text: str) -> Target:
        original = text
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
        if normalize_and_compare(text, 'sl'):
            return Target(TargetKind.multiple_sl)
        return Target(TargetKind.string, string=original)
