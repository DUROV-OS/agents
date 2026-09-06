from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from durov_agents.ids import RU_LABELS
from durov_agents.labeling.schema import LabelRecord
from durov_agents.labeling.validate import LabelError, validate_record
from durov_agents.passport import load_roster
from durov_agents.runtime.coordinator import run_task


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="durov-agents")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("roster", help="Показать восемь паспортов MVP")

    run_p = sub.add_parser("run", help="Прогнать запрос через координатора")
    run_p.add_argument("text")
    run_p.add_argument("--json", action="store_true")

    lab = sub.add_parser("label", help="Разметка")
    lab_sub = lab.add_subparsers(dest="label_cmd", required=True)
    val = lab_sub.add_parser("validate", help="Проверить JSONL разметки")
    val.add_argument("path")
    lab_sub.add_parser("plan", help="Кто и что размечает")

    args = parser.parse_args(argv)
    if args.cmd == "roster":
        return _roster()
    if args.cmd == "run":
        return _run(args.text, as_json=args.json)
    if args.cmd == "label" and args.label_cmd == "validate":
        return _validate(args.path)
    if args.cmd == "label" and args.label_cmd == "plan":
        return _plan()
    return 1


def _roster() -> int:
    for passport in load_roster().values():
        print(f"{passport.id}: {passport.title_ru}")
        print(f"  зона: {passport.owns[0]}")
        print(f"  не зона: {passport.does_not_own[0]}")
        print(f"  вопрос дня: {passport.daily_question}")
        print()
    return 0


def _run(text: str, *, as_json: bool) -> int:
    result = run_task(text)
    if as_json:
        print(result.model_dump_json(indent=2, ensure_ascii=False))
        return 0
    print(result.reply)
    print()
    print(f"released={result.released} legal={result.legal.verdict} trace={result.trace_id}")
    print("маршрут:", ", ".join(RU_LABELS[a] for a in result.route.specialists))
    return 0


def _validate(path: str) -> int:
    raw = Path(path).read_text(encoding="utf-8").splitlines()
    errors = 0
    for index, line in enumerate(raw, start=1):
        if not line.strip():
            continue
        record = LabelRecord.model_validate_json(line)
        try:
            validate_record(record)
        except LabelError as exc:
            print(f"{path}:{index}: {exc}", file=sys.stderr)
            errors += 1
    if errors:
        return 1
    print(f"ok: {path}")
    return 0


def _plan() -> int:
    from durov_agents.labeling.process import FIELDS, PEOPLE

    for field in FIELDS:
        print(f"{field.field}")
        print(f"  primary: {field.primary} — {PEOPLE[field.primary]}")
        print(f"  confirm: {field.confirmer}")
        if field.forbidden:
            print(f"  нельзя: {', '.join(r.value for r in field.forbidden)}")
        print(f"  SLA: {field.sla_business_days} раб. дня")
        print(f"  приёмка: {field.acceptance}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
