from pathlib import Path

from durov_agents.adapters.vault import ALWAYS_PATHS, LocalVaultAdapter
from durov_agents.ids import AgentId
from durov_agents.runtime.context import ContextStore
from durov_agents.runtime.coordinator import run_task

FIXTURE_VAULT = Path(__file__).parent / "fixtures" / "vault"


def test_always_on_notes_are_in_the_pack():
    store = ContextStore(vault=LocalVaultAdapter(FIXTURE_VAULT))
    pack = store.gather("Каких материалов не хватает на складе для модуля?", [AgentId.WAREHOUSE])
    paths = {hit.path for hit in pack.hits if hit.source == "vault"}
    assert "00_Agent/Constitution.md" in paths
    assert "00_Agent/Legal_Risk_Filter.md" in paths
    assert "02_Business/07_Logistics_and_Supply_Chain/Stock.md" in paths


def test_sales_query_does_not_pull_warehouse_stock():
    store = ContextStore(vault=LocalVaultAdapter(FIXTURE_VAULT))
    pack = store.gather("Какой следующий шаг по зависшей сделке в воронке?", [AgentId.SALES])
    paths = {hit.path for hit in pack.hits if hit.source == "vault"}
    assert "02_Business/07_Logistics_and_Supply_Chain/Stock.md" not in paths
    assert any(hit.source == "crm" for hit in pack.hits)


def test_run_cites_vault_note_not_passport_stub(monkeypatch):
    monkeypatch.setenv("VAULT_ROOT", str(FIXTURE_VAULT))
    result = run_task("Цех не успевает модуль, каких материалов не хватает на складе?")
    assert result.released is True
    blob = result.reply + " ".join(hit.title for hit in result.context.hits)
    assert "Остатки материалов" in blob or "Stock.md" in blob
    assert "Живой vault ещё не подключён" not in result.reply


def test_always_paths_exist_in_fixture():
    for rel in ALWAYS_PATHS:
        assert (FIXTURE_VAULT / rel).exists(), rel
