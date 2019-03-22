from .skill import Skill
from .skill_range import SkillRange, SkillRangeKind
from typing import Sequence
from yattag import Doc, indent


def generate_html(skills: Sequence[Skill]) -> str:
    """Generate html file from given skills."""

    doc, tag, text, line = Doc().ttl()
    stag = doc.stag
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            stag('meta', charset='utf-8')
            line('title', 'Arianrhod Skill Cards')
            stag('meta', name='viewport',
                 content='width=device-width, initial-scale=1')
            stag('link', rel='stylesheet', type='text/css',
                 media='screen', href='main.css')
        with tag('body'):
            with tag('div', klass='cards-container'):
                for skill in skills:
                    with tag('div', klass='card-outline-box'):
                        with tag('div', klass='card-title-box'):
                            if skill.skill_class is not None:
                                line('h3', skill.skill_class,
                                     klass='skill-class')
                            line('h2', skill.name, klass='skill-name')
                        with tag('div', klass='card-main-box'):
                            line('p', skill.timing, klass='timing')
                            with tag('div', klass='inner-horizontal-box'):
                                line('p', skill.judge, klass='judge')
                                line('p', skill.target, klass='target')
                            with tag('div', klass='inner-horizontal-box'):
                                line('p', str(skill.skill_range),
                                     klass='effect-range')
                                if skill.cost is not None:
                                    line('p', skill.cost, klass='skill-cost')
                                else:
                                    line('p', 'ー', klass='skill-cost')
                            line('p', skill.level_above,
                                 klass='skill-level-bound')
                            line('p', skill.usage_limitation,
                                 klass='limitation')
                            line('p', skill.effect, klass='effect')
                            if skill.critical is not None:
                                line('p', skill.critical, klass='critical')
                            if skill.flavor is not None:
                                line('p', skill.flavor, klass='flavor')
    return indent(doc.getvalue())


def main() -> None:
    skills = [
        Skill(
            name='ゲイルスラッシュ',
            timing='メジャーアクション',
            judge='自動成功',
            target='自身',
            skill_range=SkillRange(SkillRangeKind.nothing),
            cost=15,
            level_above=3,
            usage_limitation='シーンＳＬ回',
            effect=('《ワイドアタック》 による白兵攻撃を 2 回行なう。'
                    'この 《ワイドアタック》 はコストを消費しない。'
                    '同じ対象に 2 回攻撃しても、別々の対象を攻撃してもよい。'),
            flavor='疾風のごとき素早さで、複数の対象を連続して攻撃するスキル。'
        ),
        Skill(
            name='コンストレイン',
            timing='メジャーアクション',
            judge='命中判定',
            target='単体',
            skill_range=SkillRange(SkillRangeKind.weapon),
            cost=7,
            level_above=1,
            usage_limitation='ー',
            effect=('武器攻撃を行なう。その攻撃で対象に 1 点でもダメージを与えた場合、'
                    '対象が行なう回避判定にー2Ｄする。'
                    'この効果はラウンド終了まで持続する。'),
            critical='ダイスロール増加',
            flavor=('相手の動きを阻害するように攻撃するスキル。脚を傷つける、'
                    '視界を塞ぐなどにより、攻撃をよけにくいようにするのだ。')
        ),
        Skill(
            name='コキュートス',
            skill_class='魔術〈水〉',
            timing='メジャーアクション',
            judge='魔術判定',
            target='単体',
            skill_range=SkillRange(SkillRangeKind.with_unit, 20),
            cost=12,
            level_above=1,
            usage_limitation='ー',
            effect=('《ウォータースピア》 1 で取得可能。対象に魔法攻撃を行なう。'
                    'その攻撃のダメージは［2Ｄ＋20］（〈水〉属性の魔法ダメージ）となる。'
                    'また、その攻撃で対象に 1 点でもHPダメージを与えた場合、［放心］を与える。'),
            critical='ダイスロール増加',
            flavor='〈水〉の精霊の力により、極低温の冷気で攻撃する魔術である。'
        ),
        Skill(
            name='フロストプリズム',
            skill_class='魔術〈水／光〉',
            timing='メジャーアクション',
            judge='魔術判定',
            target='単体',
            skill_range=SkillRange(SkillRangeKind.with_unit, 30),
            cost=18,
            level_above=5,
            usage_limitation='ー',
            effect=('《マスターマジック》 5 《コキュートス》 1 '
                    '《セレスチャルスター》 1 で取得可能。'
                    '対象に魔法攻撃を行なう。その攻撃のダメージは'
                    '［（ＳＬ＋1）Ｄ＋50］（〈水／光〉属性の魔法ダメージ）となる。'
                    'また、その攻撃で対象に 1 点でもHPダメージを'
                    '与えた場合、［放心］を与える。'),
            critical='ダイスロール増加',
            flavor='結晶化した光が乱舞する魔術。'
        ),

    ]
    print(generate_html(skills))
