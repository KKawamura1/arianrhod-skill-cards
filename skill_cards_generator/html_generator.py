from .skill import Skill
from .skill_range import SkillRange
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
                                if skill.skill_range is not None:
                                    line('p', skill.skill_range,
                                         klass='effect-range')
                                else:
                                    line('p', 'ー', klass='effect-range')
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
    skill = Skill(
        name='ゲイルスラッシュ',
        timing='メジャーアクション',
        judge='自動成功',
        target='自身',
        skill_range=None,
        cost=15,
        level_above=3,
        usage_limitation='シーンＳＬ回',
        effect=('《ワイドアタック》 による白兵攻撃を 2 回行なう。'
                'この 《ワイドアタック》 はコストを消費しない。'
                '同じ対象に 2 回攻撃しても、別々の対象を攻撃してもよい。'),
        flavor='疾風のごとき素早さで、複数の対象を連続して攻撃するスキル。'
    )
    print(generate_html([skill]))


if __name__ == "__main__":
    main()
