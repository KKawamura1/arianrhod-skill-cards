from __future__ import annotations

from typing import Sequence, Tuple, Optional
import re
import mojimoji
from .normalized_check import normalize_and_compare


ruby_regex = re.compile(r'(^|[\|｜])(?P<ruby_base>[^\|｜]+)(?P<ruby_top>《[^》]+》|\([^\)]+\)|（[^）]+）)')

class RubyString:
    def __init__(self, strings_with_rubys: Sequence[Tuple[str, Optional[str]]]) -> None:
        self._strings_with_rubys = strings_with_rubys

    def as_html(self) -> str:
        result = ''
        for string, ruby in self._strings_with_rubys:
            if ruby is None:
                result += string
            else:
                result += (
                    f'<ruby>'
                    f'{string}'
                    f'<rp>（</rp>'
                    f'<rt>{ruby}</rt>'
                    f'<rp>）</rp>'
                    f'</ruby>'
                )
        return result

    def __str__(self) -> str:
        result = ''
        for string, ruby in self._strings_with_rubys:
            if ruby is None:
                result += string
            else:
                result += f'{string}（{ruby}）'
        return result

    def get_base(self) -> str:
        return ''.join([base for base, ruby in self._strings_with_rubys])

    @staticmethod
    def from_text(text: str) -> RubyString:
        result = []
        last_pos = 0
        for match in ruby_regex.finditer(text):
            result.append((text[last_pos:match.start()], None))
            ruby_tuple = (match.group('ruby_base'), match.group('ruby_top')[1:-1])
            result.append(ruby_tuple)
            last_pos = match.end()
        result.append((text[last_pos:], None))
        return RubyString(result)
