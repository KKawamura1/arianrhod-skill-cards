import re
from typing import Optional, List
from sys import stdin
import mojimoji
from .skill import Skill
from .skill_range import SkillRange
from .judge import Judge
from .html_generator import generate_html


skill_regex = re.compile(
    r'^《([^》/]+)》\s*([^\s/]+)\s*/\s*([^\s/]*)\s*/\s*([^\s/]*)\s*/\s*([^\s/]*)\s*/\s*([^\s/]*)\s*/\s*([^\s/]*)\s*/\s*([^\s/]*)\s*/\s*([^\s]*)\s*$', re.MULTILINE)
skill_area_begin_regex = re.compile(r'^■スキル■\s*$', re.MULTILINE)
skill_area_end_regex = re.compile(r'^■コネクション■\s*$', re.MULTILINE)

replace_text_slash = '___SLASH___'

keyword_unify_table = {
    'セットアッププロセス': ('セットアップ', 'setup', 'sup', 'set'),
    'イニシアチブプロセス': ('イニシアチブ', 'init', 'ini', 'in'),
    'ムーブアクション': ('ムーブ', 'move', 'mov', 'mv'),
    'マイナーアクション': ('マイナー', 'minor', 'mnr', 'mn'),
    'メジャーアクション': ('メジャー', 'major', 'maj', 'mjr', 'mj'),
    'クリンナッププロセス': ('クリンナップ', 'クリナップ', 'クリナッププロセス', 'clean', 'cup', 'c', 'clean up', 'cleanup'),
    'ダメージロールの直前': ('ダメージロール直前', 'DR直前', 'bdr', 'bfdr'),
    'ダメージロールの直後': ('ダメージロール直後', 'DR直後', 'adr', 'afdr'),
    '判定の直前': ('判定直前', 'bfjg', 'bjd', 'br'),
    '判定の直後': ('判定直後', 'afjg', 'ajd', 'ar'),
    'パッシブ': ('パッシヴ', 'pv', 'passive', 'pass', 'pas'),
    '戦闘前': {'bco', 'bfbtl'},
    'シーン': {'sn', 'scene', 'scn'},
    'アイテム': {'itm', 'item'},
    'シナリオ': {'シナ', 'sr', 'scenario'},
    'メインプロセス': {'mp', 'mainprocess', 'main process'},
}


def unify_keyword(word: str) -> str:
    for target, candidates in keyword_unify_table.items():
        for candidate in candidates:
            if (mojimoji.zen_to_han(word).lower()
                    == mojimoji.zen_to_han(candidate).lower()):
                return target
    return word


def unify_timing(timing: str) -> str:
    return unify_keyword(timing)


def unify_limitation(limitation: str) -> Optional[str]:
    def unify_limitation_with_one_word(word: str) -> str:
        slash_separated = word.split('/')
        if len(slash_separated) == 2:
            return f'{unify_keyword(slash_separated[1])}{slash_separated[0]}回'
        return word

    limitation_str = limitation.replace(replace_text_slash, '/')
    result = []
    for limitation_spaced in limitation_str.split():
        for limitation_sep in limitation_spaced.split(','):
            if len(limitation_sep) == 0:
                continue
            result.append(unify_limitation_with_one_word(limitation_sep))
    if len(result) == 0:
        return None
    return '、'.join(result)


def make_skill_from_text(text: str) -> Optional[Skill]:
    match = skill_regex.fullmatch(text)
    if match is None:
        return None
    name = match.group(1)
    if name in ('スキル名', '一般スキル'):
        return None
    elif name[0] == name[-1] == '■':
        return None
    sl_str = match.group(2)
    try:
        sl = int(sl_str)
    except ValueError:
        sl = 1
    if 7 <= sl <= 9:
        sl -= 5
    timing = unify_timing(match.group(3))
    judge = Judge.from_text(match.group(4))
    target = match.group(5)
    skill_range_str = match.group(6)
    skill_range = SkillRange.from_text(skill_range_str)
    cost_str = match.group(7)
    if len(cost_str) == 0:
        cost = None
    else:
        try:
            cost = int(cost_str)
        except ValueError:
            cost = None
    limitation = match.group(8)
    level_above = None
    if len(limitation) != 0:
        try:
            # If there is only a number in limitation area, we treat it as a sl above limitation
            level_above = int(limitation)
            limitation = ''
        except ValueError:
            pass
    limitation = unify_limitation(limitation)
    effect = match.group(9)
    return Skill(
        name=name,
        level_now=sl,
        timing=timing,
        judge=judge,
        target=target,
        skill_range=skill_range,
        cost=cost,
        usage_limitation=limitation,
        effect=effect,
        level_above=level_above
    )


def make_skills_from_charasheet(sheet: str) -> List[Skill]:
    # If it seems a entire sheet, drop others
    match_begin = skill_area_begin_regex.match(sheet)
    match_end = skill_area_end_regex.match(sheet)
    if match_begin is not None:
        begin = match_begin.end
    else:
        begin = 0
    if match_end is not None:
        end = match_end.start
    else:
        end = len(sheet)
    sheet = sheet[begin:end]

    # Escape slashes like '1/Sn', 'SL/Sr', and so on
    check_set_before = set([str(i) for i in range(20)] + ['sl', 'SL'])
    check_set_after = set(
        ['sn', 'sr', 'Sn', 'Sr', 'SN', 'SR', 'mp', 'MP', 'Mp'])
    for b in check_set_before:
        for a in check_set_after:
            sheet = sheet.replace(f'{b}/{a}', f'{b}{replace_text_slash}{a}')

    # Zenkakify all Kana characters
    sheet = mojimoji.han_to_zen(sheet, digit=False, ascii=False)

    # Check lines
    skills = []
    for line in sheet.split('\n'):
        skill = make_skill_from_text(line)
        if skill is not None:
            skills.append(skill)

    # Repair escaped slash
    for skill in skills:
        if skill.usage_limitation is not None:
            skill.usage_limitation = skill.usage_limitation.replace(
                replace_text_slash, '/')

    # Unify Times symbol
    origin = ['*', '＊']
    target = '×'
    for skill in skills:
        for o in origin:
            skill.effect = skill.effect.replace(o, target)

    # Zenkakify characters in effect area
    for skill in skills:
        skill.effect = mojimoji.han_to_zen(skill.effect, digit=False)

    return skills


def main(is_sleeve_mode: bool) -> None:
    input_text = stdin.read()
    skills = make_skills_from_charasheet(input_text)
    print(generate_html(skills, is_sleeve_mode))
