#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict
from pathlib import Path

from fix_quest_prerequisites import (
    Repair,
    iter_top_level_objects,
    normalize_accept,
    normalized_variant,
    one,
    patch_object,
)

DEFAULT_SOURCE_ROOT = Path("BinOutput/Quest")
DEFAULT_EXCEL_PATH = Path("ExcelBinOutput/QuestExcelConfigData.json")

# Early Liyue / post-Prologue prerequisite repairs.
#
# Evidence:
# - GCResource 3.7 and 4.0 agree on the normalized prerequisite graphs below.
# - Current 7.1 BinOutput lost acceptCond for these rows.
# - Current flattened QuestExcelConfigData serializes many missing fan-out edges as
#   order-based chains.
#
# Keep this batch separate from the Prologue manifest until the wider Liyue graph
# audit is complete.
REPAIRS = (
    # Post-Prologue hidden bridge.
    Repair("400.json", 400, 40001, -1, one(39604), (one(0),)),

    # MQ1000: Liyue Act I entry and its fan-out / merge graph.
    Repair("1000.json", 1000, 100099, -1, one(99902), (one(0),)),
    Repair("1000.json", 1000, 100098, -1, one(99902), (one(100099),)),
    Repair("1000.json", 1000, 100000, -1, one(39604), (one(100098),)),
    Repair("1000.json", 1000, 100001, -1, one(100000), (one(100000),)),
    Repair("1000.json", 1000, 100002, -1, one(100001), (one(100001),)),
    Repair("1000.json", 1000, 100003, -1, one(100001), (one(100002),)),
    Repair("1000.json", 1000, 100004, -1, one(100001), (one(100003),)),
    Repair("1000.json", 1000, 100005, -1, one(100001), (one(100004),)),
    Repair("1000.json", 1000, 100006, -1, one(100001), (one(100005),)),
    Repair("1000.json", 1000, 100016, -1, one(100001), (one(100006),)),
    Repair("1000.json", 1000, 100007, -1, one(100006), (one(100016),)),
    Repair("1000.json", 1000, 100021, -1, one(100007), (one(100007),)),
    Repair("1000.json", 1000, 100022, -1, one(100007), (one(100021),)),
    Repair("1000.json", 1000, 100023, -1, one(100007), (one(100022),)),
    Repair("1000.json", 1000, 100024, -1, one(100007), (one(100023),)),
    Repair("1000.json", 1000, 100025, -1, one(100007), (one(100024),)),
    Repair("1000.json", 1000, 100026, -1, one(100024), (one(100025),)),
    Repair("1000.json", 1000, 100008, -1, one(100026), (one(100026),)),
    Repair("1000.json", 1000, 100015, -1, one(100008), (one(100008),)),
    Repair("1000.json", 1000, 100009, -1, one(100015), (one(100015),)),
    Repair("1000.json", 1000, 100027, -1, one(100009), (one(100009),)),
    Repair("1000.json", 1000, 100010, -1, one(100009), (one(100027),)),
    Repair("1000.json", 1000, 100011, -1, one(100010, state=4), (one(100010),)),
    Repair("1000.json", 1000, 100012, -1, one(100010), (one(100011),)),
    Repair("1000.json", 1000, 100013, -1, one(100012), (one(100012),)),
    Repair("1000.json", 1000, 100014, -1, one(100013), (one(100013),)),

    # MQ1002: common entry before the three Act I investigation branches.
    # Historical graph fans both 100202 and 100203 out from 100201; current
    # flattened data incorrectly serializes 100203 -> 100202 -> 100204.
    Repair("1002.json", 1002, 100201, -1, one(100014), (one(0),)),
    Repair("1002.json", 1002, 100202, -1, one(100201), (one(100201),)),
    Repair("1002.json", 1002, 100203, -1, one(100201), (one(100202),)),
    Repair("1002.json", 1002, 100204, -1, one(100202), (one(100203),)),
    Repair("1002.json", 1002, 100205, -1, one(100204), (one(100204),)),

    # MQ1003: one of the three Act I investigation branches.
    # 100320 is an ACTIVE-state gate (state 2), and 100302/100319 form two
    # additional fan-outs from 100301 that the flattened chain loses.
    Repair("1003.json", 1003, 100301, -1, one(100205), (one(0),)),
    Repair("1003.json", 1003, 100320, -1, one(100301, state=2), (one(100301),)),
    Repair("1003.json", 1003, 100302, -1, one(100301), (one(100320),)),
    Repair("1003.json", 1003, 100303, -1, one(100302), (one(100302),)),
    Repair("1003.json", 1003, 100319, -1, one(100301), (one(100303),)),
    Repair("1003.json", 1003, 100304, -1, one(100303), (one(100319),)),
    Repair("1003.json", 1003, 100305, -1, one(100304), (one(100304),)),
    Repair("1003.json", 1003, 100306, -1, one(100305), (one(100305),)),
    Repair("1003.json", 1003, 100307, -1, one(100306), (one(100306),)),
    Repair("1003.json", 1003, 100308, -1, one(100307), (one(100307),)),
    Repair("1003.json", 1003, 100309, -1, one(100308), (one(100308),)),
    Repair("1003.json", 1003, 100310, -1, one(100309), (one(100309),)),
    Repair("1003.json", 1003, 100321, -1, one(100310), (one(100310),)),
    Repair("1003.json", 1003, 100311, -1, one(100321), (one(100321),)),
    Repair("1003.json", 1003, 100312, -1, one(100311), (one(100311),)),
    Repair("1003.json", 1003, 100313, -1, one(100312), (one(100312),)),
    Repair("1003.json", 1003, 100314, -1, one(100313), (one(100313),)),
    Repair("1003.json", 1003, 100315, -1, one(100314), (one(100314),)),
    Repair("1003.json", 1003, 100316, -1, one(100315), (one(100315),)),
    Repair("1003.json", 1003, 100317, -1, one(100316), (one(100316),)),
)


def patch_source_row(row: dict, repair: Repair) -> list[str]:
    if int(row.get("mainId") or 0) != repair.main_id:
        raise ValueError(
            f"Quest {repair.sub_id} has mainId={row.get('mainId')}; expected {repair.main_id}"
        )

    current = normalize_accept(row.get("acceptCond"))
    expected = normalized_variant(repair.expected_accept)
    damaged = [normalized_variant(variant) for variant in repair.damaged_accept]
    changes: list[str] = []

    if current == expected:
        pass
    elif not current or current in damaged:
        row["acceptCond"] = [dict(entry) for entry in repair.expected_accept]
        changes.append(f"acceptCond={expected!r}")
    else:
        raise ValueError(
            f"Quest {repair.sub_id} has unexpected source acceptCond={current!r}; "
            f"expected {expected!r}, missing, or one of {damaged!r}"
        )

    if repair.expected_comb is not None:
        current_comb = row.get("acceptCondComb")
        if current_comb == repair.expected_comb:
            pass
        elif current_comb in (None, "", "LOGIC_NONE") or current_comb in repair.damaged_comb:
            row["acceptCondComb"] = repair.expected_comb
            changes.append(f"acceptCondComb={repair.expected_comb}")
        else:
            raise ValueError(
                f"Quest {repair.sub_id} has unexpected source acceptCondComb={current_comb!r}; "
                f"expected {repair.expected_comb!r}, missing, or one of damaged variants "
                f"{repair.damaged_comb!r}"
            )

    return changes


def patch_sources(root: Path, *, check: bool) -> int:
    grouped: dict[str, list[Repair]] = defaultdict(list)
    for repair in REPAIRS:
        grouped[repair.json_file].append(repair)

    pending: list[tuple[Path, dict, list[str]]] = []
    seen: set[int] = set()

    for json_file, repairs in sorted(grouped.items()):
        path = root / json_file
        if not path.is_file():
            raise SystemExit(f"Expected BinOutput quest file not found: {path}")

        data = json.loads(path.read_text(encoding="utf-8"))
        subquests = data.get("subQuests") if isinstance(data, dict) else None
        if not isinstance(subquests, list):
            raise SystemExit(f"{path} has no subQuests list")

        file_changes: list[str] = []
        for repair in repairs:
            matches = [
                row
                for row in subquests
                if isinstance(row, dict) and int(row.get("subId") or 0) == repair.sub_id
            ]
            if len(matches) != 1:
                raise SystemExit(
                    f"Quest {repair.sub_id} expected exactly once in {path}; found {len(matches)}"
                )
            seen.add(repair.sub_id)
            changes = patch_source_row(matches[0], repair)
            if changes:
                file_changes.append(f"{repair.sub_id}: {', '.join(changes)}")

        if file_changes:
            pending.append((path, data, file_changes))
            for change in file_changes:
                print(f"{path}: pending: {change}")

    missing = sorted({repair.sub_id for repair in REPAIRS} - seen)
    if missing:
        raise SystemExit(f"Repair manifest quests not found in BinOutput: {missing}")

    if check:
        if pending:
            print(f"Pending BinOutput files: {len(pending)}")
            return 1
        print("Liyue BinOutput prerequisites are already restored.")
        return 0

    for path, data, changes in pending:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Updated: {path} ({len(changes)} quest rows)")

    if pending:
        print(f"Updated BinOutput files: {len(pending)}")
    else:
        print("Nothing to do; Liyue BinOutput prerequisites are already fixed.")
    return 0


def patch_excel(path: Path, *, check: bool) -> int:
    if not path.is_file():
        raise SystemExit(f"File not found: {path}")

    original_bytes = path.read_bytes()
    try:
        text = original_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit(f"{path} is not UTF-8: {exc}") from exc

    root = json.loads(text)
    if not isinstance(root, list):
        raise SystemExit(f"{path} must contain a top-level JSON array")

    wanted = {repair.sub_id: repair for repair in REPAIRS}
    found: dict[int, tuple[str, list[str]]] = {}
    replacements: list[tuple[int, int, str]] = []

    for start, end in iter_top_level_objects(text):
        raw = text[start:end]
        obj = json.loads(raw)
        if not isinstance(obj, dict):
            continue
        sub_id = int(obj.get("subId") or 0)
        repair = wanted.get(sub_id)
        if repair is None:
            continue
        if obj.get("json_file") != repair.json_file or int(obj.get("mainId") or 0) != repair.main_id:
            continue
        if sub_id in found:
            raise SystemExit(f"Quest {sub_id} appears more than once in {path}")

        patched, status, changes = patch_object(raw, repair)
        found[sub_id] = (status, changes)
        if status == "changed":
            replacements.append((start, end, patched))

    missing = [repair.sub_id for repair in REPAIRS if repair.sub_id not in found]
    if missing:
        raise SystemExit(f"Expected quest rows not found in flattened resource: {missing}")

    for repair in REPAIRS:
        status, changes = found[repair.sub_id]
        detail = ", ".join(changes) if changes else "verified"
        print(f"Quest {repair.sub_id}: {status}: {detail}")

    if check:
        if replacements:
            print(f"Pending flattened quest rows: {len(replacements)}")
            return 1
        print("Liyue flattened prerequisites are already restored.")
        return 0

    if not replacements:
        print("Nothing to do; Liyue flattened prerequisites are already fixed.")
        return 0

    patched_text = text
    for start, end, patched in reversed(replacements):
        patched_text = patched_text[:start] + patched + patched_text[end:]

    parsed = json.loads(patched_text)
    by_sub_id = {
        int(obj.get("subId") or 0): obj
        for obj in parsed
        if isinstance(obj, dict) and int(obj.get("subId") or 0) in wanted
    }
    for repair in REPAIRS:
        probe = by_sub_id.get(repair.sub_id)
        if probe is None:
            raise SystemExit(f"Quest {repair.sub_id} disappeared after patch")
        if normalize_accept(probe.get("acceptCond")) != normalized_variant(repair.expected_accept):
            raise SystemExit(f"Quest {repair.sub_id} failed post-write acceptCond validation")

    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(patched_text, encoding="utf-8", newline="")
    os.replace(tmp, path)
    print(f"Updated: {path}")
    print(f"Repaired flattened quest rows: {len(replacements)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Restore evidence-backed early Liyue prerequisites in BinOutput and flattened QuestExcel."
        )
    )
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--excel-path", type=Path, default=DEFAULT_EXCEL_PATH)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report pending repairs without writing either resource layer.",
    )
    args = parser.parse_args()

    source_status = patch_sources(args.source_root, check=args.check)
    excel_status = patch_excel(args.excel_path, check=args.check)
    return 1 if source_status or excel_status else 0


if __name__ == "__main__":
    raise SystemExit(main())
