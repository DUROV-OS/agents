"""Who labels what. This is the plan, not a slogan.

ML engineer owns schema, tooling, IAA, gold-set hygiene.
Domain people own the meaning of the label.
Legal gold is never a one-person ML decision.
"""

from dataclasses import dataclass

from durov_agents.ids import AgentId
from durov_agents.labeling.schema import AnnotatorRole


@dataclass(frozen=True)
class FieldOwner:
    field: str
    primary: AnnotatorRole
    confirmer: AnnotatorRole
    forbidden: tuple[AnnotatorRole, ...]
    sla_business_days: int
    acceptance: str


FIELDS: tuple[FieldOwner, ...] = (
    FieldOwner(
        field="gold_agents",
        primary=AnnotatorRole.ML_ENGINEER,
        confirmer=AnnotatorRole.OWNER,
        forbidden=(),
        sla_business_days=2,
        acceptance="Совпадение с паспортом зоны. κ ≥ 0.70 на пересечении двух разметчиков.",
    ),
    FieldOwner(
        field="gold_legal_verdict / gold_legal_category",
        primary=AnnotatorRole.DOMAIN_LEGAL,
        confirmer=AnnotatorRole.OWNER,
        forbidden=(AnnotatorRole.ML_ENGINEER, AnnotatorRole.DOMAIN_SALES, AnnotatorRole.DOMAIN_MARKETING),
        sla_business_days=5,
        acceptance="30 gold-примеров юриста до любого утверждения «модель умеет право».",
    ),
    FieldOwner(
        field="gold_action",
        primary=AnnotatorRole.ML_ENGINEER,
        confirmer=AnnotatorRole.OWNER,
        forbidden=(),
        sla_business_days=2,
        acceptance="act только если матрица полномочий это разрешает; иначе escalate.",
    ),
    FieldOwner(
        field="quality / grounding",
        primary=AnnotatorRole.ML_ENGINEER,
        confirmer=AnnotatorRole.OWNER,
        forbidden=(),
        sla_business_days=2,
        acceptance="hallucinated = цитата, которой нет во входе и в SharedContext.",
    ),
)

DOMAIN_OWNER: dict[AgentId, AnnotatorRole] = {
    AgentId.COORDINATOR: AnnotatorRole.OWNER,
    AgentId.SALES: AnnotatorRole.DOMAIN_SALES,
    AgentId.MARKETER: AnnotatorRole.DOMAIN_MARKETING,
    AgentId.PRODUCTION: AnnotatorRole.DOMAIN_PRODUCTION,
    AgentId.WAREHOUSE: AnnotatorRole.DOMAIN_WAREHOUSE,
    AgentId.FINANCE: AnnotatorRole.DOMAIN_FINANCE,
    AgentId.LAWYER: AnnotatorRole.DOMAIN_LEGAL,
    AgentId.ENGINEER: AnnotatorRole.DOMAIN_ENGINEER,
}

# Concrete people for MVP. Title, not a wish list.
PEOPLE = {
    AnnotatorRole.ML_ENGINEER: "Leo Vesin — схема, CLI, IAA, prelabel, не legal gold",
    AnnotatorRole.OWNER: "Игорь Дуров — спор маршрута, изменение паспорта, legal fallback",
    AnnotatorRole.DOMAIN_LEGAL: "практикующий юрист компании; до найма — владелец, не ML-инженер",
    AnnotatorRole.DOMAIN_SALES: "продажник / владелец на продах",
    AnnotatorRole.DOMAIN_MARKETING: "маркетолог / владелец на контенте",
    AnnotatorRole.DOMAIN_PRODUCTION: "начальник производства",
    AnnotatorRole.DOMAIN_WAREHOUSE: "кладовщик / снабжение",
    AnnotatorRole.DOMAIN_FINANCE: "финансист / владелец на экономике",
    AnnotatorRole.DOMAIN_ENGINEER: "проектировщик / инженер",
}

WEEKLY_RITUAL = {
    "when": "пятница, 30 минут",
    "who": "ML-инженер + один доменный разметчик по кругу",
    "does": (
        "разбирает 10 расхождений недели, правит гайдлайн одной фразой, "
        "не размножает исключения"
    ),
}

ACCEPTANCE_BEFORE_TRAINING_CLAIM = {
    "gold_per_agent": 50,
    "legal_gold": 30,
    "iaa_kappa": 0.70,
    "double_label_share": 0.20,
    "blocked_examples_required": True,
}

LABELING_PROCESS = {
    "fields": FIELDS,
    "domain_owner": DOMAIN_OWNER,
    "people": PEOPLE,
    "weekly": WEEKLY_RITUAL,
    "acceptance": ACCEPTANCE_BEFORE_TRAINING_CLAIM,
}


def legal_gold_forbidden_for(role: AnnotatorRole) -> bool:
    legal_field = next(f for f in FIELDS if f.field.startswith("gold_legal"))
    return role in legal_field.forbidden
