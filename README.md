# Durov Agents

Публичный репозиторий ML-контура Durov.House: **восемь агентов MVP**, общий контекст компании, юрист как фильтр, процесс разметки с фамилиями и SLA.

Список ролей зафиксирован: координатор, продажник, маркетолог, производственник, кладовщик, финансист, юрист, инженер.

## Что здесь есть уже сейчас

- Паспорт каждой роли: зона, запреты, источники, KPI — `src/durov_agents/specs/`
- Координатор: legal scan → маршрут → общий контекст → специалисты → выпуск или стоп
- Юридический фильтр, который **блокирует** ворованные данные конкурентов до любого черновика
- Контракт разметки: кто ставит gold, кто не имеет права, сколько примеров нужно, прежде чем говорить «агент обучен»
- CLI и тесты без API-ключа

Это не замена [soborum-backend](https://github.com/DUROV-OS/soborum-backend) (Марина, склад, клиенты) и не совет директоров. Это слой операционной команды.

## Быстрый старт

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
durov-agents roster
durov-agents run "Можно ли использовать ворованную базу клиентов конкурента в рекламе?"
durov-agents label plan
durov-agents label validate data/labeling/gold/seed.jsonl
```

Без `ANTHROPIC_API_KEY` специалисты отвечают по паспорту и цитатам контекста. Этого достаточно, чтобы проверить маршрут и фильтр.

## Документы

- [Восемь агентов](docs/AGENTS.md)
- [Общий контекст](docs/SHARED_CONTEXT.md)
- [Юрист-фильтр](docs/LEGAL_GATE.md)
- [Разметка](docs/LABELING.md)
- [Claude-организация](docs/CLAUDE_ORG.md)

База знаний (private): [vault_backups](https://github.com/DUROV-OS/vault_backups). Те же правила для Claude Team лежат там в `00_Agent/`.

## Связанные репозитории

| Репозиторий | Роль |
|---|---|
| [soborum-backend](https://github.com/DUROV-OS/soborum-backend) | рабочая система и Марина |
| [soborum-frontend](https://github.com/DUROV-OS/soborum-frontend) | интерфейс |
| [vault_backups](https://github.com/DUROV-OS/vault_backups) | источник истины |
| [vault-server-MCP](https://github.com/DUROV-OS/vault-server-MCP) | коннектор базы в Claude |
| [amocrm-MCP](https://github.com/DUROV-OS/amocrm-MCP) | CRM |
| [moysklad-MCP](https://github.com/DUROV-OS/moysklad-MCP) | склад |
| [mail-MCP](https://github.com/DUROV-OS/mail-MCP) | почта |
