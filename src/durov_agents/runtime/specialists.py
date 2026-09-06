"""Specialist replies without an LLM: cite shared context and stay in zone.

This is the MVP contract, not a chat persona. A model call may later fill
the stance text; it may not invent citations that are not in SharedContext.
"""

from durov_agents.ids import AgentId, RU_LABELS
from durov_agents.passport import get_passport
from durov_agents.runtime.legal_gate import lawyer_reply
from durov_agents.runtime.types import ActionClass, LegalDecision, Opinion, SharedContext


def speak(agent_id: AgentId, text: str, context: SharedContext, legal: LegalDecision) -> Opinion:
    if agent_id == AgentId.LAWYER:
        return Opinion(
            agent=agent_id,
            stance=lawyer_reply(legal),
            action_class=ActionClass.ESCALATE if legal.blocked else ActionClass.READ,
            citations=["legal_gate", *list(context.policy.keys())[:2]],
            escalate=legal.blocked,
        )

    passport = get_passport(agent_id)
    relevant = [hit for hit in context.hits if _useful(agent_id, hit.source, hit.path)]
    citations = [hit.title for hit in relevant[:3]]
    if not citations:
        citations = ["общий контекст компании не дал профильного факта"]

    stance = (
        f"{RU_LABELS[agent_id].capitalize()} ({passport.purpose.split('.')[0]}). "
        f"По запросу «{_clip(text)}» опираюсь на: {'; '.join(citations)}. "
        f"Не моё: {passport.does_not_own[0]}."
    )
    return Opinion(
        agent=agent_id,
        stance=stance,
        action_class=ActionClass.DRAFT,
        citations=citations,
        escalate=False,
    )


def _useful(agent_id: AgentId, source: str, path: str | None) -> bool:
    if source == "crm" and agent_id in {AgentId.SALES, AgentId.MARKETER, AgentId.FINANCE}:
        return True
    if source == "warehouse" and agent_id in {AgentId.WAREHOUSE, AgentId.PRODUCTION, AgentId.FINANCE}:
        return True
    if not path:
        return False
    return any(path.startswith(prefix) for prefix in get_passport(agent_id).vault_paths)


def _clip(text: str, limit: int = 120) -> str:
    compact = " ".join(text.split())
    return compact if len(compact) <= limit else compact[: limit - 1] + "…"
