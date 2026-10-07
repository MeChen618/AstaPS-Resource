#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import os
from collections import defaultdict
from pathlib import Path

import fix_liyue_prerequisites as liyue
from fix_quest_prerequisites import Repair, normalize_accept, normalized_variant, state_equal

DEFAULT_SOURCE_ROOT = Path("BinOutput/Quest")
DEFAULT_EXCEL_PATH = Path("ExcelBinOutput/QuestExcelConfigData.json")

ACTIVITY_END = "QUEST_COND_ACTIVITY_END"
QUEST_GLOBAL_VAR_EQUAL = "QUEST_COND_QUEST_GLOBAL_VAR_EQUAL"


def condition(kind: str, *params: int) -> dict:
    return {"type": kind, "param": list(params), "param_str": ""}


def one_state(sub_id: int) -> tuple[dict, ...]:
    return (state_equal(sub_id),)


# Chapter 1104 ("We Will Meet Again") is absent from the current flattened
# QuestExcel resource even though its 7.1 BinOutput/Quest files are present.
#
# Evidence:
# - GCResource 3.7 and 4.0 are byte-identical for MQ8000, MQ8001, MQ8002 and MQ8003.
# - The historical prerequisite graph therefore has exact two-version consensus.
# - Current 7.1 BinOutput contains all 42 subquests but has lost every meaningful
#   acceptCond in this chapter.
# - Current QuestExcelConfigData contains zero rows for mainId 8000..8003.
#
# We restore only prerequisite semantics from the historical consensus. Full
# flattened rows are materialized from the CURRENT 7.1 BinOutput rows so newer
# descriptions, finish conditions, execution data, guides and other fields stay
# on the current resource version.
CHAPTER_1104_REPAIRS = (
    # MQ8000. 800010 is an independent global-var controller; 800001 is the
    # compound chapter gate and 800002 is ChapterExcel.beginQuestId.
    Repair(
        "8000.json",
        8000,
        800010,
        -1,
        (condition(QUEST_GLOBAL_VAR_EQUAL, 10006, 1, 0, 0, 0),),
        (),
    ),
    Repair(
        "8000.json",
        8000,
        800001,
        -1,
        (
            state_equal(1800027),
            state_equal(45406),
            condition(ACTIVITY_END, 2003001, 0, 0, 0, 0),
        ),
        (),
        expected_comb="LOGIC_AND",
    ),
    Repair("8000.json", 8000, 800002, -1, one_state(800001), ()),
    Repair("8000.json", 8000, 800003, -1, one_state(800002), ()),
    Repair("8000.json", 8000, 800004, -1, one_state(800003), ()),
    Repair("8000.json", 8000, 800005, -1, one_state(800004), ()),
    Repair("8000.json", 8000, 800009, -1, one_state(800005), ()),
    Repair("8000.json", 8000, 800006, -1, one_state(800009), ()),
    Repair("8000.json", 8000, 800008, -1, one_state(800006), ()),
    Repair("8000.json", 8000, 800007, -1, one_state(800008), ()),

    # MQ8001.
    Repair("8001.json", 8001, 800101, -1, one_state(800007), ()),
    Repair("8001.json", 8001, 800102, -1, one_state(800101), ()),
    Repair("8001.json", 8001, 800103, -1, one_state(800102), ()),
    Repair("8001.json", 8001, 800104, -1, one_state(800103), ()),
    Repair("8001.json", 8001, 800105, -1, one_state(800104), ()),
    Repair("8001.json", 8001, 800109, -1, one_state(800105), ()),
    Repair("8001.json", 8001, 800108, -1, one_state(800109), ()),
    Repair("8001.json", 8001, 800106, -1, one_state(800108), ()),
    Repair("8001.json", 8001, 800107, -1, one_state(800106), ()),

    # MQ8002.
    Repair("8002.json", 8002, 800201, -1, one_state(800107), ()),
    Repair("8002.json", 8002, 800209, -1, one_state(800201), ()),
    Repair("8002.json", 8002, 800202, -1, one_state(800209), ()),
    Repair("8002.json", 8002, 800210, -1, one_state(800202), ()),
    Repair("8002.json", 8002, 800203, -1, one_state(800210), ()),
    Repair("8002.json", 8002, 800204, -1, one_state(800203), ()),
    Repair("8002.json", 8002, 800205, -1, one_state(800204), ()),
    Repair("8002.json", 8002, 800206, -1, one_state(800205), ()),
    Repair("8002.json", 8002, 800211, -1, one_state(800206), ()),
    Repair("8002.json", 8002, 800207, -1, one_state(800211), ()),
    Repair("8002.json", 8002, 800212, -1, one_state(800207), ()),
    Repair("8002.json", 8002, 800208, -1, one_state(800207), ()),

    # MQ8003. 800302 and 800308 are independent hidden controllers.
    Repair("8003.json", 8003, 800301, -1, one_state(800208), ()),
    Repair("8003.json", 8003, 800306, -1, one_state(800301), ()),
    Repair("8003.json", 8003, 800307, -1, one_state(800306), ()),
    Repair("8003.json", 8003, 800302, -1, one_state(99902), ()),
    Repair("8003.json", 8003, 800308, -1, one_state(99902), ()),
    Repair("8003.json", 8003, 800309, -1, one_state(800307), ()),
    Repair("8003.json", 8003, 800303, -1, one_state(800309), ()),
    Repair("8003.json", 8003, 800310, -1, one_state(800303), ()),
    Repair("8003.json", 8003, 800304, -1, one_state(800310), ()),
    Repair("8003.json", 8003, 800305, -1, one_state(800304), ()),
    Repair("8003.json", 8003, 800311, -1, one_state(800305), ()),
)

REPAIR_BY_SUB_ID = {repair.sub_id: repair for repair in CHAPTER_1104_REPAIRS}
EXPECTED_SUB_IDS = set(REPAIR_BY_SUB_ID)
EXPECTED_MAIN_IDS = {8000, 8001, 8002, 8003}

# QuestData.onLoad() streams these arrays without null checks. Missing flattened
# rows are generated from BinOutput, where some empty arrays are omitted, so make
# them explicit before insertion.
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
    for main_id in sorted(EXPECTED_MAIN_IDS):
        path = root / f"{main_id}.json"
        if not path.is_file():
            raise SystemExit(f"Expected source quest file not found: {path}")
        document = json.loads(path.read_text(encoding="utf-8"))
        subquests = document.get("subQuests") if isinstance(document, dict) else None
        if not isinstance(subquests, list):
            raise SystemExit(f"{path} has no subQuests list")
        for row in subquests:
            if not isinstance(row, dict):
                continue
            sub_id = int(row.get("subId") or 0)
            if sub_id not in EXPECTED_SUB_IDS:
                continue
            if sub_id in rows:
                raise SystemExit(f"Quest {sub_id} appears more than once in source files")
            rows[sub_id] = (path, document, row)

    missing = sorted(EXPECTED_SUB_IDS - set(rows))
    if missing:
        raise SystemExit(f"Chapter 1104 source quests missing: {missing}")
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

    if check:
        if changed_by_path:
            print(f"Pending Chapter 1104 BinOutput files: {len(changed_by_path)}")
            return 1, {sub_id: loaded[sub_id][2] for sub_id in loaded}
        print("Chapter 1104 BinOutput prerequisites are already restored.")
        return 0, {sub_id: loaded[sub_id][2] for sub_id in loaded}

    documents_written: set[Path] = set()
    for path, document, _ in loaded.values():
        if path not in changed_by_path or path in documents_written:
            continue
        path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        documents_written.add(path)
        print(f"Updated: {path} ({len(changed_by_path[path])} quest rows)")

    if documents_written:
        print(f"Updated Chapter 1104 BinOutput files: {len(documents_written)}")
    else:
        print("Nothing to do; Chapter 1104 BinOutput prerequisites are already fixed.")

    return 0, {sub_id: loaded[sub_id][2] for sub_id in loaded}


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
        errors.append(f"Unexpected Chapter 1104 flattened subquests: {unexpected}")

    missing = sorted(EXPECTED_SUB_IDS - set(found))
    for sub_id, row in found.items():
        repair = REPAIR_BY_SUB_ID[sub_id]
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

        # These identity/current-version fields come from current 7.1 BinOutput.
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

    # Guard the external prerequisites used by the compound 800001 gate. These
    # should already exist in QuestExcel; restoring 1104 would not help if its
    # prerequisite quests were absent too.
    all_sub_ids = {
        int(row.get("subId") or 0)
        for row in root
        if isinstance(row, dict) and int(row.get("subId") or 0) > 0
    }
    required_external = {1800027, 45406}
    missing_external = sorted(required_external - all_sub_ids)
    if missing_external:
        raise SystemExit(f"Chapter 1104 external prerequisite rows are missing: {missing_external}")

    missing, errors = validate_excel_rows(root, source_rows)
    if errors:
        raise SystemExit("\n".join(errors))

    if check:
        if missing:
            print(f"Pending Chapter 1104 flattened rows: {len(missing)}")
            return 1
        print("Chapter 1104 flattened quest rows are present and valid.")
        return 0

    if not missing:
        print("Nothing to do; Chapter 1104 flattened quest rows are already restored.")
        return 0

    if set(missing) != EXPECTED_SUB_IDS:
        raise SystemExit(
            "Refusing partial Chapter 1104 row insertion; expected either all 42 rows missing or none. "
            f"Missing now: {missing}"
        )

    rows_to_add = [
        materialize_excel_row(source_rows[repair.sub_id], repair)
        for repair in CHAPTER_1104_REPAIRS
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
    print(f"Restored Chapter 1104 flattened quest rows: {len(rows_to_add)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Restore Chapter 1104 prerequisites in BinOutput and materialize its 42 missing "
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

    if len(CHAPTER_1104_REPAIRS) != 42 or len(EXPECTED_SUB_IDS) != 42:
        raise SystemExit("Chapter 1104 manifest must contain exactly 42 unique subquests")

    source_status, source_rows = patch_sources(args.source_root, check=args.check)
    excel_status = patch_excel(args.excel_path, source_rows, check=args.check)
    return 1 if args.check and (source_status or excel_status) else 0


if __name__ == "__main__":
    raise SystemExit(main())
