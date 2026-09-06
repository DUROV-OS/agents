"""Shared company context. Every specialist sees the same pack.

Source of truth is the knowledge base checkout (VAULT_ROOT).
CRM / МойСклад are a live refresh later: read, date-stamp, do not override
a later `kind: fact` in the vault.
"""

from __future__ import annotations

from durov_agents.adapters.vault import LocalVaultAdapter, vault_root_from_env
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

# Used only when VAULT_ROOT is unset (public CI, offline). Not a fake company.
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
)


class ContextStore:
    def __init__(
        self,
        hits: list[ContextHit] | None = None,
        vault: LocalVaultAdapter | None = None,
    ) -> None:
        self.hits = list(hits) if hits is not None else None
        self.vault = vault

    def gather(self, text: str, agents: list[AgentId]) -> SharedContext:
        if self.hits is not None:
            selected = list(self.hits)
        elif self.vault is not None:
            prefixes = _prefixes(agents)
            selected = self.vault.gather(text, prefixes)
        else:
            selected = list(_FIXTURES)

        selected.extend(_pending_connectors(agents))
        return SharedContext(hits=_dedup(selected), policy=dict(POLICY))


def _prefixes(agents: list[AgentId]) -> list[str]:
    prefixes = {"02_Business/00_Decision_Log"}
    for agent_id in agents:
        prefixes.update(get_passport(agent_id).vault_paths)
    return sorted(prefixes)


def _pending_connectors(agents: list[AgentId]) -> list[ContextHit]:
    hits: list[ContextHit] = []
    if any(agent_id in {AgentId.SALES, AgentId.MARKETER, AgentId.FINANCE} for agent_id in agents):
        hits.append(
            ContextHit(
                source="crm",
                title="amoCRM",
                excerpt="Коннектор ещё не вшит в gather(). Живые сделки появятся после чтения MCP; истина — 03_Clients.",
                kind="record",
                path="amocrm",
            )
        )
    if any(agent_id in {AgentId.WAREHOUSE, AgentId.PRODUCTION, AgentId.FINANCE} for agent_id in agents):
        hits.append(
            ContextHit(
                source="warehouse",
                title="МойСклад",
                excerpt="Коннектор ещё не вшит в gather(). Остатки читаются после проверки; факт уходит в базу.",
                kind="record",
                path="moysklad",
            )
        )
    return hits


def _dedup(hits: list[ContextHit]) -> list[ContextHit]:
    seen: set[tuple[str, str]] = set()
    unique: list[ContextHit] = []
    for hit in hits:
        key = (hit.source, hit.path or hit.title)
        if key in seen:
            continue
        seen.add(key)
        unique.append(hit)
    return unique


def default_store() -> ContextStore:
    root = vault_root_from_env()
    if root is not None:
        return ContextStore(vault=LocalVaultAdapter(root))
    return ContextStore()


DEFAULT_STORE = default_store()
