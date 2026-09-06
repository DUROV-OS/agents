from enum import StrEnum


class AgentId(StrEnum):
    COORDINATOR = "coordinator"
    SALES = "sales"
    MARKETER = "marketer"
    PRODUCTION = "production"
    WAREHOUSE = "warehouse"
    FINANCE = "finance"
    LAWYER = "lawyer"
    ENGINEER = "engineer"


MVP_AGENT_IDS: tuple[AgentId, ...] = tuple(AgentId)

RU_LABELS: dict[AgentId, str] = {
    AgentId.COORDINATOR: "координатор",
    AgentId.SALES: "продажник",
    AgentId.MARKETER: "маркетолог",
    AgentId.PRODUCTION: "производственник",
    AgentId.WAREHOUSE: "кладовщик",
    AgentId.FINANCE: "финансист",
    AgentId.LAWYER: "юрист",
    AgentId.ENGINEER: "инженер",
}
