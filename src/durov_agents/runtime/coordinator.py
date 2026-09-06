from __future__ import annotations

import uuid

from durov_agents.ids import AgentId, RU_LABELS
from durov_agents.runtime.context import DEFAULT_STORE, ContextStore
from durov_agents.runtime.legal_gate import scan
from durov_agents.runtime.router import route
from durov_agents.runtime.specialists import speak
from durov_agents.runtime.types import ActionClass, LegalVerdict, Opinion, RunResult


def run_task(text: str, store: ContextStore | None = None) -> RunResult:
    """Coordinator turn: legal scan → route → shared context → specialists → release check."""
    if not text or not text.strip():
        raise ValueError("Пустой запрос")

    legal = scan(text)
    planned = route(text, legal)
    context = (store or DEFAULT_STORE).gather(text, planned.specialists)

    opinions: list[Opinion] = []
    if legal.verdict == LegalVerdict.BLOCK:
        opinions.append(speak(AgentId.LAWYER, text, context, legal))
        reply = _blocked_reply(opinions[0], legal)
        return RunResult(
            reply=reply,
            route=planned,
            legal=legal,
            opinions=opinions,
            context=context,
            released=False,
            trace_id=_trace_id(),
        )

    for agent_id in planned.specialists:
        if agent_id == AgentId.LAWYER:
            continue
        opinions.append(speak(agent_id, text, context, legal))

    if legal.needs_lawyer or AgentId.LAWYER in planned.specialists:
        opinions.append(speak(AgentId.LAWYER, text, context, legal))

    released = legal.verdict == LegalVerdict.ALLOW
    reply = _synthesize(text, opinions, legal, released)
    return RunResult(
        reply=reply,
        route=planned,
        legal=legal,
        opinions=opinions,
        context=context,
        released=released,
        trace_id=_trace_id(),
    )


def _blocked_reply(lawyer: Opinion, legal) -> str:
    return (
        f"{lawyer.stance}\n\n"
        f"Координатор не передаёт задачу специалистам: legal gate = {legal.verdict}. "
        f"Правила: {', '.join(f.rule_id for f in legal.findings)}."
    )


def _synthesize(text: str, opinions: list[Opinion], legal, released: bool) -> str:
    lines = [
        "Координатор.",
        f"Запрос: {_one_line(text)}",
        f"Legal gate: {legal.verdict}.",
    ]
    if opinions:
        lines.append("Специалисты:")
        for opinion in opinions:
            lines.append(f"- {RU_LABELS[opinion.agent]}: {opinion.stance}")
    if not released:
        lines.append(
            "Ответ не выпущен как действие. Нужен человек."
            if legal.verdict == LegalVerdict.ESCALATE_HUMAN
            else "Ответ не выпущен."
        )
    else:
        lines.append("Выпуск: информационный. Любое изменение данных — подтверждение человека.")
    if any(o.action_class == ActionClass.ESCALATE for o in opinions):
        lines.append("Есть эскалация от специалиста.")
    return "\n".join(lines)


def _one_line(text: str) -> str:
    return " ".join(text.split())


def _trace_id() -> str:
    return uuid.uuid4().hex
