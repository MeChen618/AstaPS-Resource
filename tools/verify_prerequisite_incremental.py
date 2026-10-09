#!/usr/bin/env python3
"""Reject new prerequisite defects without hiding the upstream baseline debt.

The cumulative prerequisite manifest covers Liyue and Inazuma as well as the
Prologue. Upstream main already has 277 pending flattened repairs. Requiring
zero pending rows would make an unrelated Mondstadt PR fail before its own
checks run. We instead require all existing pending rows to remain identical
(or become fully repaired) and reject any newly pending or mutated row.

The GitHub workflow checks out two commits, making HEAD^ the first parent of
the PR test merge commit (upstream target), or the previous push commit.
"""
from __future__ import annotations

import json
import subprocess
import sys

# Register the complete cumulative manifest, including Chapter 1207.
import fix_chapter1207_prerequisites as entry  # noqa: F401
import fix_liyue_prerequisites as base
from fix_quest_prerequisites import normalize_accept, patch_object

EXCEL_PATH = "ExcelBinOutput/QuestExcelConfigData.json"
EXPECTED_ROWS = 678


def pending_rows(text: str) -> dict[int, str]:
    rows = json.loads(text)
    if not isinstance(rows, list):
        raise ValueError("QuestExcelConfigData must be a JSON array")

    repairs = {repair.sub_id: repair for repair in base.REPAIRS}
    if len(repairs) != EXPECTED_ROWS:
        raise ValueError("Cumulative prerequisite manifest contains duplicate rows")
    found: set[int] = set()
    pending: dict[int, str] = {}

    for row in rows:
        if not isinstance(row, dict):
            continue
        sub_id = int(row.get("subId") or 0)
        repair = repairs.get(sub_id)
        if repair is None:
            continue
        if row.get("json_file") != repair.json_file or int(row.get("mainId") or 0) != repair.main_id:
            continue
        if sub_id in found:
            raise ValueError(f"Duplicate prerequisite row {sub_id}")
        found.add(sub_id)

        # Reuse the exact production repair predicate. Unexpected meaningful
        # conditions are always a failure, even when they also existed in base.
        _, status, _ = patch_object(json.dumps(row, ensure_ascii=False), repair)
        if status == "changed":
            pending[sub_id] = json.dumps(
                {
                    "acceptCond": normalize_accept(row.get("acceptCond")),
                    "acceptCondComb": row.get("acceptCondComb"),
                },
                ensure_ascii=False,
                sort_keys=True,
            )

    missing = set(repairs) - found
    if missing:
        raise ValueError(f"Missing cumulative prerequisite rows: {sorted(missing)}")
    return pending


def regression_errors(before: dict[int, str], after: dict[int, str]) -> list[str]:
    errors = []
    for sub_id in sorted(after):
        if sub_id not in before:
            errors.append(f"{sub_id}: newly pending prerequisite repair")
        elif after[sub_id] != before[sub_id]:
            errors.append(f"{sub_id}: existing pending prerequisite was modified without being repaired")
    return errors


def main() -> int:
    ids = [repair.sub_id for repair in base.REPAIRS]
    if len(ids) != EXPECTED_ROWS or len(ids) != len(set(ids)):
        raise ValueError(f"Expected {EXPECTED_ROWS} unique cumulative prerequisite repairs")

    # Explicit first-parent ref: HEAD^ on GitHub's PR merge commit is the
    # upstream base, not the contributing fork's previous commit.
    previous = subprocess.run(
        ["git", "show", f"HEAD^:{EXCEL_PATH}"],
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8")
    with open(EXCEL_PATH, encoding="utf-8") as stream:
        current = stream.read()

    before = pending_rows(previous)
    after = pending_rows(current)
    errors = regression_errors(before, after)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"Found {len(errors)} introduced prerequisite defects.", file=sys.stderr)
        return 1

    repaired = len(set(before) - set(after))
    print(f"Cumulative prerequisite audit: {EXPECTED_ROWS} manifest rows checked.")
    print(f"Existing upstream flattened prerequisite debt: {len(before)} rows.")
    print(f"Still pending: {len(after)}; repaired by this commit: {repaired}; introduced: 0.")
    if after:
        print("NOTICE: Existing upstream debt is not silently counted as repaired.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
