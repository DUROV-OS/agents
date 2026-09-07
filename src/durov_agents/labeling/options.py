"""Fixed multiple-choice options for a labeling questionnaire row."""

from __future__ import annotations

from durov_agents.ids import MVP_AGENT_IDS, RU_LABELS
from durov_agents.runtime.types import ActionClass, LegalCategory, LegalVerdict

VERDICT_RU: dict[LegalVerdict, str] = {
    LegalVerdict.ALLOW: "можно",
    LegalVerdict.ALLOW_WITH_CONDITIONS: "можно с оговоркой",
    LegalVerdict.ESCALATE_HUMAN: "к человеку",
    LegalVerdict.BLOCK: "блок",
}

CATEGORY_RU: dict[LegalCategory, str] = {
    LegalCategory.NONE: "нет риска",
    LegalCategory.COMPETITOR_INTEL_ILLEGAL: "конкурентная разведка (ворованное)",
    LegalCategory.PRICING_AUTHORITY: "цена/скидка вне полномочий",
    LegalCategory.CONTRACT: "договор",
    LegalCategory.OWNER_PROMISE: "обещание от имени владельца",
    LegalCategory.SAFETY_CODE: "безопасность/нормы (СП/ГОСТ)",
    LegalCategory.PERSONAL_DATA: "персональные данные",
    LegalCategory.LABOR: "трудовое право",
    LegalCategory.INTELLECTUAL_PROPERTY: "интеллектуальная собственность",
}

ACTION_RU: dict[ActionClass, str] = {
    ActionClass.READ: "прочитать / ответить",
    ActionClass.DRAFT: "черновик",
    ActionClass.ACT: "действие в системе",
    ActionClass.ESCALATE: "эскалация",
}


def choice(id_: str, label: str) -> dict[str, str]:
    return {"id": id_, "label": label}


def labeling_options() -> dict[str, list[dict[str, str]]]:
    """Same checkbox set as the paper questionnaire — for every JSONL row."""
    verdict_order = (
        LegalVerdict.ALLOW,
        LegalVerdict.ALLOW_WITH_CONDITIONS,
        LegalVerdict.ESCALATE_HUMAN,
        LegalVerdict.BLOCK,
    )
    category_order = (
        LegalCategory.NONE,
        LegalCategory.COMPETITOR_INTEL_ILLEGAL,
        LegalCategory.PRICING_AUTHORITY,
        LegalCategory.CONTRACT,
        LegalCategory.OWNER_PROMISE,
        LegalCategory.SAFETY_CODE,
        LegalCategory.PERSONAL_DATA,
        LegalCategory.LABOR,
        LegalCategory.INTELLECTUAL_PROPERTY,
    )
    action_order = (
        ActionClass.READ,
        ActionClass.DRAFT,
        ActionClass.ACT,
        ActionClass.ESCALATE,
    )
    return {
        "agents": [choice(a.value, RU_LABELS[a]) for a in MVP_AGENT_IDS],
        "legal_verdict": [choice(v.value, VERDICT_RU[v]) for v in verdict_order],
        "legal_category": [choice(c.value, CATEGORY_RU[c]) for c in category_order],
        "action": [choice(a.value, ACTION_RU[a]) for a in action_order],
    }


def blank_answer() -> dict:
    """Slots the annotator fills; empty until someone marks the row."""
    return {
        "agents": [],
        "legal_verdict": None,
        "legal_category": None,
        "action": None,
        "comment": "",
    }
