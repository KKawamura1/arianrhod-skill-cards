from typing import List, Tuple, Set, TypeVar, Optional
import mojimoji


T = TypeVar('T')


def normalize_and_compare(source: str, target: str) -> bool:
    return (mojimoji.zen_to_han(source).lower()
            == mojimoji.zen_to_han(target).lower())


def normalize_and_check(
    target: str,
    table: List[Tuple[T, Set[str]]]
) -> Optional[T]:
    for key, candidates in table:
        for candidate in candidates:
            if normalize_and_compare(target, candidate):
                return key
    return None
