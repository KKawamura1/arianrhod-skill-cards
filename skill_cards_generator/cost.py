from __future__ import annotations

import re
from .normalized_check import normalize_and_compare


fate_regex = re.compile(r'[fフ]a?t?e?ェ?イ?ト?([0-9０１２３４５６７８９]+)点?', re.IGNORECASE)


class Cost:
    def __init__(self, val: int, is_fate: bool = False) -> None:
        self._val = val
        self._is_fate = is_fate

    def __str__(self):
        if self._val == 0 or self._is_fate:
            return 'ー'
        else:
            return str(self._val)

    def as_effect(self) -> str:
        if self._is_fate:
            return f'フェイトを{self._val}点消費。'
        return ''

    @staticmethod
    def from_text(text: str) -> Cost:
        for candidate in ['', '-', '無', 'なし', '無し']:
            if normalize_and_compare(text, candidate):
                return Cost(0)
        match = fate_regex.match(text)
        if match is not None:
            return Cost(int(match.group(1)), True)
        try:
            cost = int(text)
            return Cost(cost)
        except ValueError:
            return Cost(0)
