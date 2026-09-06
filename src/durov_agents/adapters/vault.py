"""Knowledge base adapter.

Production: VAULT_ROOT = checkout of DUROV-OS/vault_backups
or VAULT_MCP_URL = vault-server-MCP (read_index, search_notes, read_note).

Claude Team already uses the same vault via CLAUDE.md. This adapter is the
programmatic twin so all eight agents see one source of truth.
"""

from pathlib import Path

from durov_agents.runtime.types import ContextHit


class LocalVaultAdapter:
    name = "vault"

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def search(self, query: str, limit: int = 8) -> list[ContextHit]:
        if not self.root.exists():
            return []
        hits: list[ContextHit] = []
        needle = query.lower()
        for path in self.root.rglob("*.md"):
            if any(part.startswith(".") or part == "_trash" for part in path.parts):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if needle not in text.lower():
                continue
            rel = path.relative_to(self.root).as_posix()
            hits.append(
                ContextHit(
                    source="vault",
                    title=path.stem,
                    excerpt=text.strip().splitlines()[0][:240] if text.strip() else "",
                    kind="record",
                    path=rel,
                )
            )
            if len(hits) >= limit:
                break
        return hits
