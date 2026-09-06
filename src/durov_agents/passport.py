from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from durov_agents.ids import MVP_AGENT_IDS, AgentId

SPECS_DIR = Path(__file__).resolve().parent / "specs"


class AgentPassport(BaseModel):
    """Charter passport. An agent does not run without one."""

    id: AgentId
    title_ru: str
    purpose: str
    owns: list[str]
    does_not_own: list[str]
    daily_question: str
    tools: list[str]
    access_level: str
    data_sources: list[str]
    forbidden: list[str]
    escalate_to: list[str]
    kpi: list[str]
    curiosity: str
    backend_domains: list[str] = Field(default_factory=list)
    vault_paths: list[str] = Field(default_factory=list)


@lru_cache
def load_roster() -> dict[AgentId, AgentPassport]:
    roster: dict[AgentId, AgentPassport] = {}
    for path in sorted(SPECS_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        passport = AgentPassport.model_validate(data)
        roster[passport.id] = passport
    missing = [agent_id for agent_id in MVP_AGENT_IDS if agent_id not in roster]
    if missing:
        raise RuntimeError(f"MVP roster incomplete, missing: {missing}")
    return roster


def get_passport(agent_id: AgentId) -> AgentPassport:
    return load_roster()[agent_id]
