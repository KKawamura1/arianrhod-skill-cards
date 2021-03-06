from __future__ import annotations

import enum
import mojimoji
import re
from typing import Tuple, Optional
from .ability import Ability


class JudgeKind(enum.Enum):
    nothing = enum.auto()
    auto_success = enum.auto()
    hit = enum.auto()
    spell = enum.auto()
    song = enum.auto()
    alchemy = enum.auto()
    ability = enum.auto()
    string = enum.auto()


unify_judge_table = [
    [JudgeKind.nothing, ('-', '')],
    [JudgeKind.auto_success, ('自', '成', '自動', '成功',
                              '自動成功', 'success', 'suc', 'sc', 's')],
    [JudgeKind.hit, ('命', '命中', 'hit', 'ht', 'h')],
    [JudgeKind.spell, ('魔', '魔術', 'spell', 'spl', 'sp',
                       'magic', 'mag', 'mg', 'm')],
    [JudgeKind.song, ('呪', '歌', '呪歌', 'song', 'sg')],
    [JudgeKind.alchemy, ('錬', '錬金', '錬金術', 'alchemy',
                         'alc', 'ac', 'acm', 'a')],
]
judge_border_regex = re.compile(
    r'(.+?)[\s(（\[]?(難)?(難易度)?([0-9０１２３４５６７８９]+)[)）\]\s]?')


class Judge:
    def __init__(
        self,
        judge_kind: JudgeKind,
        ability: Ability = None,
        string: str = None
    ) -> None:
        self._judge_kind = judge_kind
        if judge_kind is JudgeKind.ability:
            assert ability is not None
            self._ability = ability
        if judge_kind is JudgeKind.string:
            assert string is not None
            self._string = string

    def to_str(self, is_for_effect: bool):
        if self._judge_kind is JudgeKind.nothing:
            if is_for_effect:
                return '判定'
            return 'ー'
        elif self._judge_kind is JudgeKind.auto_success:
            if is_for_effect:
                return '判定'
            return '自動成功'
        elif self._judge_kind is JudgeKind.hit:
            return '命中判定'
        elif self._judge_kind is JudgeKind.spell:
            return '魔術判定'
        elif self._judge_kind is JudgeKind.song:
            return '呪歌判定'
        elif self._judge_kind is JudgeKind.alchemy:
            return '錬金術判定'
        elif self._judge_kind is JudgeKind.ability:
            if is_for_effect:
                return f'【{str(self._ability)}】判定'
            return str(self._ability)
        else:
            assert self._judge_kind is JudgeKind.string
            return self._string

    def __str__(self):
        return self.to_str(False)

    @staticmethod
    def from_text(text: str) -> Tuple[Judge, Optional[int]]:
        original = text
        match = judge_border_regex.fullmatch(text)
        difficulty = None
        if match is not None:
            text = match.group(1)
            difficulty = int(match.group(4))
        if len(text) >= 2 and text[-2:] == '判定':
            text = text[:-2]
        for kind, candidates in unify_judge_table:
            for candidate in candidates:
                if (mojimoji.zen_to_han(text).lower()
                        == mojimoji.zen_to_han(candidate).lower()):
                    return Judge(kind), difficulty
        ability = Ability.from_text(text)
        if ability is not None:
            return Judge(JudgeKind.ability, ability), difficulty
        return Judge(JudgeKind.string, string=original), None
