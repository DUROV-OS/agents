from typing import Protocol

from durov_agents.runtime.types import ContextHit


class ContextAdapter(Protocol):
    """Read-only slice of a company system. Writes stay in Soborbum / human approval."""

    name: str

    def search(self, query: str, limit: int = 8) -> list[ContextHit]:
        ...
