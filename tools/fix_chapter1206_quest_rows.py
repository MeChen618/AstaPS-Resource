#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import os
from collections import defaultdict
from pathlib import Path

import fix_liyue_chapter1205  # noqa: F401 - keeps the cumulative prerequisite chain loaded
import fix_liyue_prerequisites as liyue
from fix_quest_prerequisites import Repair, normalize_accept, normalized_variant, state_equal

DEFAULT_SOURCE_ROOT = Path("BinOutput/Quest")
DEFAULT_EXCEL_PATH = Path("ExcelBinOutput/QuestExcelConfigData.json")

QUEST_GLOBAL_VAR_EQUAL = "QUEST_COND_QUEST_GLOBAL_VAR_EQUAL"
QUEST_VAR_EQUAL = "QUEST_COND_QUEST_VAR_EQUAL"


def condition(kind: str, *params: int) -> dict:
    return {"type": kind, "param": list(params), "param_str": ""}


def one_state(sub_id: int, state: int = 3) -> tuple[dict, ...]:
    return (state_equal(sub_id, state),)


# Chapter 1206 prerequisite + missing flattened-row restoration.
# Evidence:
# - GCResource 3.7 and 4.0 are byte-identical for MQ8004..8007.
# - Current 7.1 BinOutput contains the same 53 subquest identities, but every
#   meaningful acceptCond is absent.
# - Current QuestExcel contains zero rows for these 53 subquests.
#
# As with Chapter 1104, full flattened rows are materialized from CURRENT 7.1
# BinOutput. Only prerequisite semantics come from the historical two-version
# consensus, so current descriptions/finish conditions/exec data remain current.
CHAPTER_1206_REPAIRS = (
    # MQ8004
    Repair(
        "8004.json",
        8004,
        800401,
        -1,
        (condition(QUEST_GLOBAL_VAR_EQUAL, 10014, 1, 0, 0, 0),),
        (),
    ),
    Repair("8004.json", 8004, 800402, -1, one_state(800401), ()),
    Repair("8004.json", 8004, 800403, -1, one_state(800407), ()),
    Repair("8004.json", 8004, 800404, -1, one_state(800405), ()),
    Repair("8004.json", 8004, 800405, -1, one_state(800403, 4), ()),
    Repair("8004.json", 8004, 800406, -1, one_state(800407), ()),
    Repair("8004.json", 8004, 800407, -1, one_state(800402), ()),

    # MQ8005
    Repair(
        "8005.json",
        8005,
        800501,
        -1,
        (state_equal(800404), state_equal(800403)),
        (),
        expected_comb="LOGIC_OR",
    ),
    Repair("8005.json", 8005, 800502, -1, one_state(800501), ()),
    Repair("8005.json", 8005, 800503, -1, one_state(800502), ()),
    Repair("8005.json", 8005, 800504, -1, one_state(800503), ()),
    Repair("8005.json", 8005, 800505, -1, one_state(800504), ()),
    Repair("8005.json", 8005, 800506, -1, one_state(800505), ()),
    Repair("8005.json", 8005, 800508, -1, one_state(800506), ()),
    Repair("8005.json", 8005, 800509, -1, one_state(800508), ()),
    Repair("8005.json", 8005, 800510, -1, one_state(800509), ()),
    Repair("8005.json", 8005, 800511, -1, one_state(800510), ()),
    Repair("8005.json", 8005, 800512, -1, one_state(800511), ()),
    Repair("8005.json", 8005, 800513, -1, one_state(800512), ()),
    Repair("8005.json", 8005, 800514, -1, one_state(800513), ()),
    Repair("8005.json", 8005, 800515, -1, one_state(800514), ()),
    Repair("8005.json", 8005, 800516, -1, one_state(800510), ()),
    Repair("8005.json", 8005, 800517, -1, one_state(800510), ()),
    Repair("8005.json", 8005, 800518, -1, one_state(800516), ()),
    Repair("8005.json", 8005, 800519, -1, one_state(800510), ()),
    Repair("8005.json", 8005, 800520, -1, one_state(800503), ()),

    # MQ8006
    Repair(
        "8006.json",
        8006,
        800601,
        -1,
        (state_equal(800515), state_equal(800518)),
        (),
        expected_comb="LOGIC_OR",
    ),
    Repair("8006.json", 8006, 800602, -1, one_state(800601), ()),
    Repair("8006.json", 8006, 800603, -1, one_state(800602), ()),
    Repair("8006.json", 8006, 800604, -1, one_state(800603), ()),
    Repair(
        "8006.json",
        8006,
        800605,
        -1,
        (state_equal(800604), state_equal(800612)),
        (),
        expected_comb="LOGIC_OR",
    ),
    Repair("8006.json", 8006, 800606, -1, one_state(800605), ()),
    Repair("8006.json", 8006, 800607, -1, one_state(800606), ()),
    Repair("8006.json", 8006, 800608, -1, one_state(800607), ()),
    Repair(
        "8006.json",
        8006,
        800609,
        -1,
        (state_equal(800604), state_equal(800612)),
        (),
        expected_comb="LOGIC_OR",
    ),
    Repair(
        "8006.json",
        8006,
        800610,
        -1,
        (state_equal(800604), state_equal(800612)),
        (),
        expected_comb="LOGIC_OR",
    ),
    Repair(
        "8006.json",
        8006,
        800611,
        -1,
        (state_equal(800604), state_equal(800612)),
        (),
        expected_comb="LOGIC_OR",
    ),
    Repair("8006.json", 8006, 800612, -1, one_state(800601), ()),
    Repair(
        "8006.json",
        8006,
        800613,
        -1,
        (state_equal(800604), state_equal(800612)),
        (),
        expected_comb="LOGIC_OR",
    ),
    Repair("8006.json", 8006, 800614, -1, one_state(800605), ()),

    # MQ8007
    Repair("8007.json", 8007, 800701, -1, one_state(800608), ()),
    Repair("8007.json", 8007, 800702, -1, one_state(800711), ()),
    Repair("8007.json", 8007, 800703, -1, one_state(800702), ()),
    Repair("8007.json", 8007, 800704, -1, one_state(800703), ()),
    Repair("8007.json", 8007, 800705, -1, one_state(800703), ()),
    Repair("8007.json", 8007, 800706, -1, one_state(800703), ()),
    Repair("8007.json", 8007, 800707, -1, one_state(800703), ()),
    Repair("8007.json", 8007, 800708, -1, one_state(800703), ()),
    Repair("8007.json", 8007, 800709, -1, one_state(800712), ()),
    Repair("8007.json", 8007, 800710, -1, one_state(800709), ()),
    Repair("8007.json", 8007, 800711, -1, one_state(800701), ()),
    Repair("8007.json", 8007, 800712, -1, one_state(800708), ()),
    Repair(
        "8007.json",
        8007,
        800713,
        -1,
        (condition(QUEST_VAR_EQUAL, 4, 1, 0, 0, 0),),
        (),
    ),
)

REPAIR_BY_SUB_ID = {repair.sub_id: repair for repair in CHAPTER_1206_REPAIRS}
EXPECTED_SUB_IDS = set(REPAIR_BY_SUB_ID)
EXPECTED_MAIN_IDS = {8004, 8005, 8006, 8007}

REQUIRED_LIST_FIELDS = (
    "acceptCond",
    "finishCond",
    "failCond",
    "beginExec",
    "finishExec",
    "failExec",
)


def load_sources(root: Path) -> dict[int, tuple[Path, dict, dict]]:
    rows: dict[int, tuple[Path, dict, dict]] = {}
    expected_by_main: dict[int, set[int]] = defaultdict(set)
    for repair in CHAPTER_1206_REPAIRS:
        expected_by_main[repair.main_id].add(repair.sub_id)

    for main_id in sorted(EXPECTED_MAIN_IDS):
        path = root / f"{main_id}.json"
        if not path.is_file():
            raise SystemExit(f"Expected source quest file not found: {path}")
        document = json.loads(path.read_text(encoding="utf-8"))
        subquests = document.get("subQuests") if isinstance(document, dict) else None
        if not isinstance(subquests, list):
            raise SystemExit(f"{path} has no subQuests list")

        actual_ids = {
            int(row.get("subId") or 0)
            for row in subquests
            if isinstance(row, dict) and int(row.get("subId") or 0) > 0
        }
        expected_ids = expected_by_main[main_id]
        if actual_ids != expected_ids:
            raise SystemExit(
                f"Chapter 1206 source membership drift in {path}: "
                f"current-only={sorted(actual_ids - expected_ids)}, "
                f"expected-only={sorted(expected_ids - actual_ids)}"
            )

        for row in subquests:
            if not isinstance(row, dict):
                continue
            sub_id = int(row.get("subId") or 0)
            if sub_id not in expected_ids:
                continue
            if sub_id in rows:
                raise SystemExit(f"Quest {sub_id} appears more than once in source files")
            rows[sub_id] = (path, document, row)

    missing = sorted(EXPECTED_SUB_IDS - set(rows))
    if missing:
        raise SystemExit(f"Chapter 1206 source quests missing: {missing}")
    return rows


def patch_sources(root: Path, *, check: bool) -> tuple[int, dict[int, dict]]:
    loaded = load_sources(root)
    changed_by_path: dict[Path, list[str]] = defaultdict(list)

    for sub_id in sorted(EXPECTED_SUB_IDS):
        path, _, row = loaded[sub_id]
        changes = liyue.patch_source_row(row, REPAIR_BY_SUB_ID[sub_id])
        if changes:
            changed_by_path[path].append(f"{sub_id}: {', '.join(changes)}")

    for path in sorted(changed_by_path):
        for change in changed_by_path[path]:
            print(f"{path}: pending: {change}")

    source_rows = {sub_id: loaded[sub_id][2] for sub_id in loaded}
    if check:
        if changed_by_path:
            print(f"Pending Chapter 1206 BinOutput files: {len(changed_by_path)}")
            return 1, source_rows
        print("Chapter 1206 BinOutput prerequisites are already restored.")
        return 0, source_rows

    documents_written: set[Path] = set()
    for path, document, _ in loaded.values():
        if path not in changed_by_path or path in documents_written:
            continue
        path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        documents_written.add(path)
        print(f"Updated: {path} ({len(changed_by_path[path])} quest rows)")

    if documents_written:
        print(f"Updated Chapter 1206 BinOutput files: {len(documents_written)}")
    else:
        print("Nothing to do; Chapter 1206 BinOutput prerequisites are already fixed.")
    return 0, source_rows


def materialize_excel_row(source_row: dict, repair: Repair) -> dict:
    row = copy.deepcopy(source_row)
    if int(row.get("mainId") or 0) != repair.main_id or int(row.get("subId") or 0) != repair.sub_id:
        raise ValueError(f"Source identity mismatch while materializing quest {repair.sub_id}")

    row["json_file"] = repair.json_file
    row["acceptCond"] = [dict(entry) for entry in repair.expected_accept]
    if repair.expected_comb is not None:
        row["acceptCondComb"] = repair.expected_comb

    for field in REQUIRED_LIST_FIELDS:
        value = row.get(field)
        if value is None:
            row[field] = []
        elif not isinstance(value, list):
            raise ValueError(f"Quest {repair.sub_id} has non-list {field}: {type(value).__name__}")

    if row.get("guide") is None:
        row["guide"] = {}
    return row


def render_top_level_object(row: dict) -> str:
    raw = json.dumps(row, ensure_ascii=False, indent=2)
    return "\n".join("  " + line for line in raw.splitlines())


def validate_excel_rows(root: list, source_rows: dict[int, dict]) -> tuple[list[int], list[str]]:
    found: dict[int, dict] = {}
    errors: list[str] = []
    for row in root:
        if not isinstance(row, dict):
            continue
        main_id = int(row.get("mainId") or 0)
        if main_id not in EXPECTED_MAIN_IDS:
            continue
        sub_id = int(row.get("subId") or 0)
        if sub_id in found:
            errors.append(f"Quest {sub_id} appears more than once in flattened resource")
            continue
        found[sub_id] = row

    unexpected = sorted(set(found) - EXPECTED_SUB_IDS)
    if unexpected:
        errors.append(f"Unexpected Chapter 1206 flattened subquests: {unexpected}")

    missing = sorted(EXPECTED_SUB_IDS - set(found))
    for sub_id, row in found.items():
        repair = REPAIR_BY_SUB_ID[sub_id]
        if row.get("json_file") != repair.json_file:
            errors.append(
                f"Quest {sub_id} flattened json_file={row.get('json_file')!r}; "
                f"expected {repair.json_file!r}"
            )
        expected = normalized_variant(repair.expected_accept)
        current = normalize_accept(row.get("acceptCond"))
        if current != expected:
            errors.append(f"Quest {sub_id} flattened acceptCond={current!r}; expected {expected!r}")
        if repair.expected_comb is not None:
            current_comb = row.get("acceptCondComb")
            if current_comb != repair.expected_comb:
                errors.append(
                    f"Quest {sub_id} flattened acceptCondComb={current_comb!r}; "
                    f"expected {repair.expected_comb!r}"
                )
        for field in REQUIRED_LIST_FIELDS:
            if not isinstance(row.get(field), list):
                errors.append(f"Quest {sub_id} flattened {field} is not a list")

        source = source_rows[sub_id]
        for field in ("mainId", "subId", "order", "descTextMapHash"):
            if row.get(field) != source.get(field):
                errors.append(
                    f"Quest {sub_id} flattened {field}={row.get(field)!r}; "
                    f"current source has {source.get(field)!r}"
                )

    return missing, errors


def patch_excel(path: Path, source_rows: dict[int, dict], *, check: bool) -> int:
    if not path.is_file():
        raise SystemExit(f"File not found: {path}")

    original = path.read_text(encoding="utf-8")
    root = json.loads(original)
    if not isinstance(root, list):
        raise SystemExit(f"{path} must contain a top-level JSON array")

    missing, errors = validate_excel_rows(root, source_rows)
    if errors:
        raise SystemExit("\n".join(errors))

    if check:
        if missing:
            if set(missing) != EXPECTED_SUB_IDS:
                raise SystemExit(
                    "Refusing partial Chapter 1206 row state; expected either all 53 rows missing "
                    f"or none. Missing now: {missing}"
                )
            print(f"Pending Chapter 1206 flattened rows: {len(missing)}")
            return 1
        print("Chapter 1206 flattened quest rows are present and valid.")
        return 0

    if not missing:
        print("Nothing to do; Chapter 1206 flattened quest rows are already restored.")
        return 0

    if set(missing) != EXPECTED_SUB_IDS:
        raise SystemExit(
            "Refusing partial Chapter 1206 row insertion; expected either all 53 rows missing or none. "
            f"Missing now: {missing}"
        )

    rows_to_add = [
        materialize_excel_row(source_rows[repair.sub_id], repair)
        for repair in CHAPTER_1206_REPAIRS
    ]

    close = original.rfind("]")
    if close < 0 or original[close + 1 :].strip():
        raise SystemExit(f"Could not identify top-level array closing bracket in {path}")
    prefix = original[:close].rstrip()
    if not prefix.endswith("}"):
        raise SystemExit(f"Expected existing non-empty JSON array in {path}")

    addition = ",\n" + ",\n".join(render_top_level_object(row) for row in rows_to_add)
    patched = prefix + addition + "\n]\n"

    parsed = json.loads(patched)
    missing_after, errors_after = validate_excel_rows(parsed, source_rows)
    if missing_after or errors_after:
        raise SystemExit(
            f"Post-write validation failed; missing={missing_after}, errors={errors_after}"
        )

    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(patched, encoding="utf-8", newline="")
    os.replace(tmp, path)
    print(f"Updated: {path}")
    print(f"Restored Chapter 1206 flattened quest rows: {len(rows_to_add)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Restore Chapter 1206 prerequisites in BinOutput and materialize its 53 missing "
            "QuestExcel rows from current 7.1 source data."
        )
    )
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--excel-path", type=Path, default=DEFAULT_EXCEL_PATH)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report pending source/flattened repairs without writing resources.",
    )
    args = parser.parse_args()

    if len(CHAPTER_1206_REPAIRS) != 53 or len(EXPECTED_SUB_IDS) != 53:
        raise SystemExit("Chapter 1206 manifest must contain exactly 53 unique subquests")

    source_status, source_rows = patch_sources(args.source_root, check=args.check)
    excel_status = patch_excel(args.excel_path, source_rows, check=args.check)
    return 1 if args.check and (source_status or excel_status) else 0


if __name__ == "__main__":
    raise SystemExit(main())
