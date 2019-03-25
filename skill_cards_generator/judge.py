from __future__ import annotations

import enum
from typing import Optional
from .ability import Ability


class JudgeKind(enum.Enum):
    nothing = enum.auto()
    auto_success = enum.auto()
    hit = enum.auto()
    spell = enum.auto()
    song = enum.auto()
    alchemy = enum.auto()
    ability = enum.auto()


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
    ) -> None:
        self._judge_kind = judge_kind
        if judge_kind is JudgeKind.ability:
            assert ability is not None
            self._ability = ability

    @staticmethod
    def from_text(text: str) -> Optional[Judge]:
        if len(text) >= 2 and text[-2:] == '判定':
            text = text[:-2]
        for kind, target_list in unify_judge_table:
            if text in target_list:
                return Judge(kind)
        ability = Ability.from_text(text)
        if ability is not None:
            return Judge(JudgeKind.ability, ability)
        return None
