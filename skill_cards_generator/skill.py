from dataclasses import dataclass, field
from typing import Optional
from .skill_range import SkillRange
from .judge import Judge
from .classifier import Classifier
from .target import Target
from .cost import Cost
from .ruby_string import RubyString


@dataclass
class Skill:
    """Skill object in Arianrhod."""

    name: RubyString
    timing: str
    judge: Judge
    target: Target
    skill_range: SkillRange
    cost: Cost
    usage_limitation: Optional[str]
    effect: str
    skill_class: Optional[Classifier] = field(default=None)
    level_above: Optional[int] = field(default=None)
    level_now: Optional[int] = field(default=None)
    critical: Optional[str] = field(default=None)
    flavor: Optional[str] = field(default=None)
