from __future__ import annotations

import enum
import mojimoji
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
    [JudgeKind.auto_success, ('自', '成', '自動', '成功', '自動成功')],
    [JudgeKind.hit, ('命', '命中', 'hit', 'ht')],
    [JudgeKind.spell, ('魔', '魔術', 'spell', 'spl', 'sp',
                       'magic', 'mag', 'mg')],
    [JudgeKind.song, ('呪', '歌', '呪歌', 'song', 'sg')],
    [JudgeKind.alchemy, ('錬', '錬金', '錬金術', 'alchemy',
                         'alc', 'ac', 'acm')],
]


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

    def __str__(self):
        if self._judge_kind is JudgeKind.nothing:
            return 'ー'
        elif self._judge_kind is JudgeKind.auto_success:
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
            return str(self._ability)
        else:
            assert self._judge_kind is JudgeKind.string
            return self._string

    @staticmethod
    def from_text(text: str) -> Judge:
        original = text
        if len(text) >= 2 and text[-2:] == '判定':
            text = text[:-2]
        for kind, candidates in unify_judge_table:
            for candidate in candidates:
                if (mojimoji.zen_to_han(text).lower()
                        == mojimoji.zen_to_han(candidate).lower()):
                    return Judge(kind)
        ability = Ability.from_text(text)
        if ability is not None:
            return Judge(JudgeKind.ability, ability)
        return Judge(JudgeKind.string, original)
