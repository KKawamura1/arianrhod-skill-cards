from dataclasses import dataclass, field
from typing import Optional
from .skill_range import SkillRange
from .judge import Judge


@dataclass
class Skill:
    """Skill object in Arianrhod."""

    name: str
    timing: str
    judge: Judge
    target: str
    skill_range: SkillRange
    cost: Optional[int]
    usage_limitation: Optional[str]
    effect: str
    skill_class: Optional[str] = field(default=None)
    level_above: Optional[int] = field(default=None)
    level_now: Optional[int] = field(default=None)
    critical: Optional[str] = field(default=None)
    flavor: Optional[str] = field(default=None)
