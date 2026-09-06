# Claude-организация и GitHub

Отдельного GitHub-органа «Claude» у DUROV-OS нет. Связка такая:

| Где | Что это |
|---|---|
| Claude Team / организация в claude.ai | Люди компании и проекты. Системный промпт — `CLAUDE.md` в [vault_backups](https://github.com/DUROV-OS/vault_backups). |
| Custom connectors в Claude | [vault-server-MCP](https://github.com/DUROV-OS/vault-server-MCP), [amocrm-MCP](https://github.com/DUROV-OS/amocrm-MCP), [moysklad-MCP](https://github.com/DUROV-OS/moysklad-MCP), [mail-MCP](https://github.com/DUROV-OS/mail-MCP) |
| Soborbum backend | Марина (`app/ai`) и совет директоров (`app/board`) ходят в ту же базу через MCP |
| Этот репозиторий | Восемь операционных агентов, фильтр юриста, разметка |

Как жить в Claude Team, не плодя восемь несвязных чатов:

1. Один проект «Durov-OS» с `CLAUDE.md` + папкой `00_Agent/` — это координатор и конституция.
2. Восемь паспортов из `src/durov_agents/specs/` кладутся в базу (`Agent_Roster_MVP`). Claude их читает как правила, не как «новую личность на каждый запрос».
3. Юридический фильтр дублируется в базе (`Legal_Risk_Filter`) — чтобы даже чат в Claude, минуя этот рантайм, знал про ворованные данные конкурентов.
4. Обучение и gold живут здесь, не в истории чатов Claude.

Писать восемь отдельных Claude Projects на старте не нужно: разъедется контекст. Сначала этот рантайм и одна конституция.
