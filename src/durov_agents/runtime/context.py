"""Shared company context. Every specialist sees the same pack.

Source of truth is the knowledge base. CRM / МойСклад are a live refresh:
read, date-stamp, do not override a later `kind: fact` in the vault.
"""

from __future__ import annotations

from durov_agents.ids import AgentId
from durov_agents.passport import get_passport
from durov_agents.runtime.types import ContextHit, SharedContext

POLICY = {
    "discount_autonomy_pct": "5",
    "final_price": "human_approval",
    "competitor_intel": "open_sources_only",
    "crm_role": "primary_collection_then_vault",
    "source_of_truth": "vault_backups",
}

# Public-safe fixtures. Real vault / CRM adapters replace this in production
# without changing the SharedContext shape.
_FIXTURES: tuple[ContextHit, ...] = (
    ContextHit(
        source="vault",
        title="Конституция — Human Approval",
        excerpt=(
            "Окончательная цена, скидка сверх лимита, юробязательства, кадры, "
            "банк и обещания от имени владельца — только человек."
        ),
        kind="fact",
        path="00_Agent/Constitution.md",
    ),
    ContextHit(
        source="vault",
        title="Матрица полномочий",
        excerpt="Скидка автономно до 5%. Срок производства — только по утверждённому сроку.",
        kind="fact",
        path="00_Agent/Operating_Principles.md",
    ),
    ContextHit(
        source="vault",
        title="Конкурентная разведка",
        excerpt=(
            "Нельзя использовать ворованную, слитую или инсайдерскую информацию "
            "конкурентов. Допустимы открытые прайсы, сайт, реклама, отзывы."
        ),
        kind="fact",
        path="00_Agent/Legal_Risk_Filter.md",
    ),
    ContextHit(
        source="vault",
        title="Продукт",
        excerpt=(
            "Durov.House — модульные и каркасные дома заводской сборки, "
            "Воронеж / Новая Усмань. Продаём предсказуемость, не квадратные метры."
        ),
        kind="fact",
        path="00_Agent/Constitution.md",
    ),
    ContextHit(
        source="crm",
        title="Воронка (срез-заглушка)",
        excerpt="Живые сделки читаются из amoCRM и переносятся в 03_Clients. CRM не сильнее fact в базе.",
        kind="record",
        path="amocrm",
    ),
    ContextHit(
        source="warehouse",
        title="Склад (срез-заглушка)",
        excerpt="Остатки и техкарты — МойСклад / Soborbum warehouse. После проверки факт уходит в базу.",
        kind="record",
        path="moysklad",
    ),
)


class ContextStore:
    def __init__(self, hits: list[ContextHit] | None = None) -> None:
        self.hits = list(hits) if hits is not None else list(_FIXTURES)

    def gather(self, text: str, agents: list[AgentId]) -> SharedContext:
        allowed_paths: set[str] = {"00_Agent", "02_Business/00_Decision_Log"}
        for agent_id in agents:
            allowed_paths.update(get_passport(agent_id).vault_paths)

        selected: list[ContextHit] = []
        for hit in self.hits:
            if hit.source in {"crm", "warehouse"}:
                selected.append(hit)
                continue
            if hit.path and any(hit.path.startswith(prefix) for prefix in allowed_paths):
                selected.append(hit)
                continue
            if any(token in (hit.title + hit.excerpt).lower() for token in _tokens(text)):
                selected.append(hit)

        # Dedup while keeping order.
        seen: set[tuple[str, str]] = set()
        unique: list[ContextHit] = []
        for hit in selected:
            key = (hit.source, hit.title)
            if key not in seen:
                seen.add(key)
                unique.append(hit)
        return SharedContext(hits=unique, policy=dict(POLICY))


def _tokens(text: str) -> list[str]:
    return [part for part in text.lower().replace(",", " ").split() if len(part) > 3]


DEFAULT_STORE = ContextStore()
