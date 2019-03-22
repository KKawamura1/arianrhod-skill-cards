from dataclasses import dataclass, field
from typing import Optional
from .skill_range import SkillRange


@dataclass
class Skill:
    """Skill object in Arianrhod."""

    name: str
    timing: str
    judge: str
    target: str
    skill_range: SkillRange
    cost: Optional[int]
    level_above: int
    usage_limitation: str
    effect: str
    skill_class: Optional[str] = field(default=None)
    critical: Optional[str] = field(default=None)
    flavor: Optional[str] = field(default=None)
