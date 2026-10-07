#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from fix_quest_prerequisites import REPAIRS, normalize_accept, normalized_variant

DEFAULT_ROOT = Path("BinOutput/Quest")


def patch_row(row: dict, repair) -> list[str]:
    if int(row.get("mainId") or 0) != repair.main_id:
        raise ValueError(
            f"Quest {repair.sub_id} has mainId={row.get('mainId')}; expected {repair.main_id}"
        )

    current = normalize_accept(row.get("acceptCond"))
    expected = normalized_variant(repair.expected_accept)
    damaged = [normalized_variant(variant) for variant in repair.damaged_accept]
    changes: list[str] = []

    # BinOutput files in the 7.1 dump frequently lost acceptCond entirely. That missing shape is
    # safe to restore only because every row in REPAIRS has an intact historical counterpart.
    if current == expected:
        pass
    elif not current or current in damaged:
        row["acceptCond"] = [dict(entry) for entry in repair.expected_accept]
        changes.append(f"acceptCond={expected!r}")
    else:
        raise ValueError(
            f"Quest {repair.sub_id} has unexpected acceptCond={current!r}; "
            f"expected {expected!r}, missing, or one of {damaged!r}"
        )

    if repair.expected_comb is not None:
        current_comb = row.get("acceptCondComb")
        if current_comb == repair.expected_comb:
            pass
        elif current_comb in (None, "", "LOGIC_NONE"):
            row["acceptCondComb"] = repair.expected_comb
            changes.append(f"acceptCondComb={repair.expected_comb}")
        else:
            raise ValueError(
                f"Quest {repair.sub_id} has unexpected acceptCondComb={current_comb!r}; "
                f"expected missing or {repair.expected_comb}"
            )

    return changes


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Restore evidence-backed quest prerequisites directly in BinOutput/Quest source files. "
            "Uses the same manifest as fix_quest_prerequisites.py."
        )
    )
    parser.add_argument("root", nargs="?", type=Path, default=DEFAULT_ROOT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report pending source repairs without writing files.",
    )
    args = parser.parse_args()

    grouped = defaultdict(list)
    for repair in REPAIRS:
        grouped[repair.json_file].append(repair)

    pending_files: dict[Path, tuple[dict, list[str]]] = {}
    seen: set[int] = set()

    for json_file, repairs in sorted(grouped.items()):
        path = args.root / json_file
        if not path.is_file():
            raise SystemExit(f"Expected BinOutput quest file not found: {path}")

        root = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(root, dict):
            raise SystemExit(f"{path} must contain a JSON object")
        subquests = root.get("subQuests")
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
            changes = patch_row(matches[0], repair)
            if changes:
                file_changes.append(f"{repair.sub_id}: {', '.join(changes)}")

        if file_changes:
            pending_files[path] = (root, file_changes)
            for change in file_changes:
                print(f"{path}: pending: {change}")

    missing = sorted({repair.sub_id for repair in REPAIRS} - seen)
    if missing:
        raise SystemExit(f"Repair manifest quests not found in BinOutput: {missing}")

    if args.check:
        if pending_files:
            print(f"Pending BinOutput files: {len(pending_files)}")
            return 1
        print("All evidence-backed BinOutput quest prerequisites are already restored.")
        return 0

    if not pending_files:
        print("Nothing to do; BinOutput prerequisites are already fixed.")
        return 0

    for path, (root, changes) in pending_files.items():
        path.write_text(json.dumps(root, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Updated: {path} ({len(changes)} quest rows)")

    print(f"Updated BinOutput files: {len(pending_files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
