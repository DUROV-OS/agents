# Разметка: кто и как

Общих слов нет. Если человека нет в таблице — он не размечает это поле.

## Зачем

След `run_task` сам по себе не обучение. Обучение начинается, когда человек ставит gold. До приёмки ниже никто не имеет права сказать «агент обучен».

## Кто

| Роль | Кто сейчас | Делает | Не делает |
|---|---|---|---|
| `ml_engineer` | Leo Vesin | схема JSONL, CLI, prelabel маршрута, quality/grounding, IAA, отбраковка мусора | legal gold, изменение паспорта агента |
| `owner` | Игорь Дуров | спор маршрута, legal fallback до найма юриста, смена паспорта | ежедневная простыня из 200 следов |
| `domain_legal` | практикующий юрист; до найма — владелец | gold по `legal_verdict` и категории | коммерческий маршрут «кто продажник» |
| `domain_sales` … `domain_engineer` | профильный сотрудник | подтверждает, что запрос его зоны | чужие зоны и право |

## Что именно размечается

Одна строка JSONL = один запрос.

```json
{
  "id": "ex-001",
  "text": "Можно ли взять слитую базу конкурента?",
  "options": {
    "agents": [{"id": "coordinator", "label": "координатор"}, {"id": "lawyer", "label": "юрист"}],
    "legal_verdict": [{"id": "allow", "label": "можно"}, {"id": "block", "label": "блок"}],
    "legal_category": [{"id": "none", "label": "нет риска"}, {"id": "competitor_intel_illegal", "label": "конкурентная разведка (ворованное)"}],
    "action": [{"id": "read", "label": "прочитать / ответить"}, {"id": "escalate", "label": "эскалация"}]
  },
  "answer": {
    "agents": [],
    "legal_verdict": null,
    "legal_category": null,
    "action": null,
    "comment": ""
  },
  "gold_agents": ["lawyer"],
  "gold_legal_verdict": "block",
  "gold_legal_category": "competitor_intel_illegal",
  "gold_action": "escalate",
  "annotator_id": "igor.durov",
  "annotator_role": "owner",
  "status": "gold"
}
```

В inbox-партии у каждой строки есть полный набор `options` (как галочки в PDF) и пустой `answer` для ответа разметчика. `gold_*` — черновик ML для сверки после сбора, не подсказка респонденту. Полный список вариантов также в `data/labeling/inbox/*.options.json`.

Поля и хозяева — `src/durov_agents/labeling/process.py`.

- `gold_agents` — кого координатор обязан разбудить. Prelabel ставит ML, подтверждает домен или владелец. SLA 2 рабочих дня.
- `gold_legal_*` — только `domain_legal` или `owner`. ML-инженер не может закрыть gold, если вердикт не `allow`. SLA 5 рабочих дней.
- `gold_action` — `read` / `draft` / `act` / `escalate`. `act` почти не бывает в MVP: запись в систему идёт через Soborbum с подтверждением человека.
- `quality` / `grounding` — ML. `hallucinated` = факт, которого не было во входе и в `SharedContext`.

## Как проходит неделя

1. Рантайм пишет след (после появления продового хука — в `data/traces/`).
2. ML-инженер в понедельник забирает новые следы, ставит prelabel маршрута, отбрасывает дубли.
3. Доменный разметчик в свои 2 дня ставит `domain_done`.
4. Юрист/владелец в 5 дней закрывает legal gold.
5. Пятница, 30 минут: ML + один домен по кругу. Десять расхождений. Одна правка гайдлайна, не десять исключений.
6. Двойная разметка 20% потока для κ.

## Приёмка, без которой нельзя говорить про обучение

- 50 gold на каждого из восьми агентов
- 30 legal gold, среди них обязательны блоки (ворованные данные конкурентов — уже в `data/labeling/gold/seed.jsonl`)
- Cohen's κ ≥ 0.70 на маршруте и на legal verdict
- 20% следов размечены двумя людьми

Пока цифр нет — есть только фильтр и паспорта. Это честнее, чем «датасет в процессе».

## Команда

```bash
durov-agents label plan
durov-agents label validate data/labeling/gold/seed.jsonl
```
