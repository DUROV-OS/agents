from pathlib import Path

from durov_agents.ids import AgentId
from durov_agents.labeling.process import legal_gold_forbidden_for
from durov_agents.labeling.schema import AnnotatorRole, LabelRecord, LabelStatus
from durov_agents.labeling.validate import LabelError, validate_record
from durov_agents.runtime.types import ActionClass, LegalCategory, LegalVerdict

GOLD = Path(__file__).resolve().parents[1] / "data" / "labeling" / "gold" / "seed.jsonl"


def test_ml_engineer_cannot_gold_a_legal_block():
    record = LabelRecord(
        id="bad",
        text="слитая база конкурента",
        gold_agents=[AgentId.LAWYER],
        gold_legal_verdict=LegalVerdict.BLOCK,
        gold_legal_category=LegalCategory.COMPETITOR_INTEL_ILLEGAL,
        gold_action=ActionClass.ESCALATE,
        annotator_id="leo.vesin",
        annotator_role=AnnotatorRole.ML_ENGINEER,
        status=LabelStatus.GOLD,
    )
    try:
        validate_record(record)
    except LabelError:
        return
    raise AssertionError("ML engineer must not mint legal gold")


def test_owner_can_gold_legal_block():
    record = LabelRecord(
        id="ok",
        text="слитая база конкурента",
        gold_agents=[AgentId.LAWYER],
        gold_legal_verdict=LegalVerdict.BLOCK,
        gold_legal_category=LegalCategory.COMPETITOR_INTEL_ILLEGAL,
        gold_action=ActionClass.ESCALATE,
        annotator_id="igor.durov",
        annotator_role=AnnotatorRole.OWNER,
        status=LabelStatus.GOLD,
    )
    validate_record(record)


def test_legal_gold_forbidden_roles():
    assert legal_gold_forbidden_for(AnnotatorRole.ML_ENGINEER)
    assert legal_gold_forbidden_for(AnnotatorRole.DOMAIN_SALES)
    assert not legal_gold_forbidden_for(AnnotatorRole.DOMAIN_LEGAL)


def test_seed_gold_file_validates():
    for line in GOLD.read_text(encoding="utf-8").splitlines():
        record = LabelRecord.model_validate_json(line)
        validate_record(record)
    assert "ворован" in GOLD.read_text(encoding="utf-8")
