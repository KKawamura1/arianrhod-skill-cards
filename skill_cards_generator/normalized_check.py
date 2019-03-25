from typing import List, Tuple, Set, TypeVar, Optional
import mojimoji


T = TypeVar('T')


def normalize_and_check(target: str, table: List[Tuple[T, Set[str]]]) -> Optional[T]:
    for key, candidates in table:
        for candidate in candidates:
            if (mojimoji.zen_to_han(target).lower()
                    == mojimoji.zen_to_han(candidate).lower()):
                return key
    return None
