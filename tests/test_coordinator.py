from durov_agents.ids import AgentId
from durov_agents.runtime.coordinator import run_task
from durov_agents.runtime.types import LegalVerdict


def test_block_is_not_released_and_skips_commercial_work():
    result = run_task("Используем ворованную информацию конкурентов для оффера")
    assert result.released is False
    assert result.legal.verdict == LegalVerdict.BLOCK
    assert result.opinions
    assert result.opinions[0].agent == AgentId.LAWYER
    assert all(o.agent == AgentId.LAWYER for o in result.opinions)


def test_shared_context_is_always_attached():
    result = run_task("Какой следующий шаг по зависшей сделке в воронке?")
    assert result.context.hits
    assert result.context.policy["discount_autonomy_pct"] == "5"
    assert result.context.policy["competitor_intel"] == "open_sources_only"
    assert AgentId.SALES in result.route.specialists


def test_production_and_warehouse_route_together():
    result = run_task("Цех не успевает модуль, каких материалов не хватает на складе?")
    assert AgentId.PRODUCTION in result.route.specialists
    assert AgentId.WAREHOUSE in result.route.specialists
    assert result.released is True


def test_empty_rejected():
    try:
        run_task("   ")
    except ValueError:
        return
    raise AssertionError("empty task must fail")
