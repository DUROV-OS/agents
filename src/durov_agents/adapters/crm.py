"""amoCRM adapter.

Live connector: https://github.com/DUROV-OS/amocrm-MCP
Policy: read for freshness, write facts into the vault. CRM is not stronger
than a later `kind: fact` in the knowledge base.
"""

from durov_agents.runtime.types import ContextHit


class FixtureCrmAdapter:
    name = "crm"

    def search(self, query: str, limit: int = 8) -> list[ContextHit]:
        del query, limit
        return [
            ContextHit(
                source="crm",
                title="amoCRM",
                excerpt="Коннектор живой. После выгрузки сделка живёт в 03_Clients.",
                kind="record",
                path="amocrm",
            )
        ]
