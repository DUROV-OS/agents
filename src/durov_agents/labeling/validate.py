from durov_agents.labeling.process import legal_gold_forbidden_for
from durov_agents.labeling.schema import LabelRecord, LabelStatus


class LabelError(ValueError):
    pass


def validate_record(record: LabelRecord) -> None:
    if not record.text.strip():
        raise LabelError("пустой text")
    if not record.gold_agents:
        raise LabelError("gold_agents пуст")
    if record.status == LabelStatus.GOLD and record.gold_legal_verdict.value != "allow":
        if not record.legal_gold_allowed():
            raise LabelError(
                "legal gold может поставить только domain_legal или owner, "
                f"сейчас {record.annotator_role}"
            )
    if legal_gold_forbidden_for(record.annotator_role) and record.status == LabelStatus.GOLD:
        if record.gold_legal_verdict.value != "allow" or record.gold_legal_category.value != "none":
            raise LabelError("эта роль не имеет права делать legal gold")
