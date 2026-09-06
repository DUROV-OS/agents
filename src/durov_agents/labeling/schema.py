from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field

from durov_agents.ids import AgentId
from durov_agents.runtime.types import ActionClass, LegalCategory, LegalVerdict


class AnnotatorRole(StrEnum):
    DOMAIN_SALES = "domain_sales"
    DOMAIN_MARKETING = "domain_marketing"
    DOMAIN_PRODUCTION = "domain_production"
    DOMAIN_WAREHOUSE = "domain_warehouse"
    DOMAIN_FINANCE = "domain_finance"
    DOMAIN_LEGAL = "domain_legal"
    DOMAIN_ENGINEER = "domain_engineer"
    ML_ENGINEER = "ml_engineer"
    OWNER = "owner"


class QualityLabel(StrEnum):
    CORRECT = "correct"
    PARTIAL = "partial"
    HALLUCINATED = "hallucinated"
    OUT_OF_SCOPE = "out_of_scope"


class GroundingLabel(StrEnum):
    CITED = "cited"
    MISSING = "missing"
    CONTRADICTED = "contradicted"


class LabelStatus(StrEnum):
    PRELABEL = "prelabel"
    DOMAIN_DONE = "domain_done"
    GOLD = "gold"
    REJECTED = "rejected"


class LabelRecord(BaseModel):
    """One labeled turn. Gold legal labels cannot be set by the ML engineer alone."""

    id: str
    text: str
    gold_agents: list[AgentId]
    gold_legal_verdict: LegalVerdict
    gold_legal_category: LegalCategory = LegalCategory.NONE
    gold_action: ActionClass
    quality: QualityLabel | None = None
    grounding: GroundingLabel | None = None
    annotator_id: str
    annotator_role: AnnotatorRole
    status: LabelStatus = LabelStatus.PRELABEL
    notes: str = ""
    trace_id: str | None = None
    labeled_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def legal_gold_allowed(self) -> bool:
        return self.annotator_role in {AnnotatorRole.DOMAIN_LEGAL, AnnotatorRole.OWNER}
