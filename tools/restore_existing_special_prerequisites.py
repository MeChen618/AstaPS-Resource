#!/usr/bin/env python3
"""Restore verified Chapter 1104 / 1206 prerequisites on *existing* QuestExcel rows.

This is a strict one-shot 7.1 compatibility patch. It preserves all non-prerequisite
fields and row identity, checks the 3.7/4.0 reference consensus, and refuses
unexpected upstream shapes. It never materializes or deletes a quest record.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import fix_chapter1104_quest_rows as ch1104
import fix_chapter1206_quest_rows as ch1206
from fix_early_quest_fields import iter_top_level_objects
from fix_quest_prerequisites import normalize_accept, render_object

DEFAULT_EXCEL = Path("ExcelBinOutput/QuestExcelConfigData.json")
EXPECTED_COUNT = 33217


def read_excel(path: Path) -> dict[int, dict]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(rows, list) and len(rows) == EXPECTED_COUNT, (path, len(rows))
    index = {int(r["subId"]): r for r in rows}
    assert len(index) == len(rows), f"Duplicate subquest IDs in {path}"
    return index


def read_reference(root: Path, mains: set[int]) -> dict[int, dict]:
    result = {}
    for main in sorted(mains):
        doc = json.loads((root / "BinOutput" / "Quest" / f"{main}.json").read_text(encoding="utf-8"))
        for row in doc["subQuests"]:
            sid = int(row["subId"])
            assert sid not in result, (root, sid)
            result[sid] = row
    return result


def collect_repairs(ref37: Path, ref40: Path) -> dict[int, object]:
    repairs = ch1104.CHAPTER_1104_REPAIRS + ch1206.CHAPTER_1206_REPAIRS
    assert len(repairs) == 95
    by_sub_id = {r.sub_id: r for r in repairs}
    assert len(by_sub_id) == 95
    mains = {r.main_id for r in repairs}
    historical = [read_reference(root, mains) for root in (ref37, ref40)]
    for sub_id, repair in by_sub_id.items():
        expect = normalize_accept(repair.expected_accept)
        for index, reference in enumerate(historical):
            old = reference.get(sub_id)
            assert old is not None, (index, sub_id, "historical row missing")
            assert normalize_accept(old.get("acceptCond")) == expect, (
                index, sub_id, "historical prerequisite disagree", old.get("acceptCond"), expect
            )
            if repair.expected_comb is not None:
                assert old.get("acceptCondComb") == repair.expected_comb, (
                    index, sub_id, "historical combiner disagrees"
                )
    return by_sub_id


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--excel", type=Path, default=DEFAULT_EXCEL)
    parser.add_argument("--baseline", type=Path, required=True,
                        help="Pinned upstream QuestExcel before the cumulative 277-row repair")
    parser.add_argument("--reference-3700", type=Path, required=True)
    parser.add_argument("--reference-4000", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    fixes = collect_repairs(args.reference_3700, args.reference_4000)
    current = read_excel(args.excel)
    baseline = read_excel(args.baseline)
    assert set(current) == set(baseline)
    assert all(current.get(sid) is not None and current[sid] == baseline[sid]
               for sid in fixes), "Special-chapter rows drifted from pinned main; abort"

    original = args.excel.read_text(encoding="utf-8")
    edits = []
    touched = []
    found = set()
    for start, end in iter_top_level_objects(original):
        obj = json.loads(original[start:end])
        sid = int(obj.get("subId", 0))
        repair = fixes.get(sid)
        if repair is None:
            continue
        assert sid not in found, sid
        found.add(sid)
        assert int(obj.get("mainId", 0)) == repair.main_id, sid
        assert obj.get("json_file") == repair.json_file, (sid, obj.get("json_file"))
        assert obj == current[sid], sid

        expected_cond = [dict(x) for x in repair.expected_accept]
        dirty = False
        if normalize_accept(obj.get("acceptCond")) != normalize_accept(expected_cond):
            obj["acceptCond"] = expected_cond
            dirty = True
        if repair.expected_comb is not None and obj.get("acceptCondComb") != repair.expected_comb:
            obj["acceptCondComb"] = repair.expected_comb
            dirty = True
        if dirty:
            edits.append((start, end, render_object(obj)))
            touched.append(sid)
    assert found == set(fixes), ("missing target IDs", sorted(set(fixes) - found))

    print("TARGET_ROWS", len(fixes))
    print("CHANGED_ROWS", len(touched))
    print("CHANGED_SUBQUEST_IDS", sorted(touched))
    if args.check:
        return 1 if touched else 0
    if not touched:
        return 0

    new = original
    for start, end, replacement in reversed(edits):
        new = new[:start] + replacement + new[end:]
    assert new != original
    after = json.loads(new)
    assert isinstance(after, list) and len(after) == EXPECTED_COUNT
    index = {int(row["subId"]): row for row in after}
    assert set(index) == set(current)
    changed = 0
    for sid, before in current.items():
        patch = index[sid]
        if before != patch:
            changed += 1
            assert sid in fixes, sid
            keys = {key for key in (before.keys() | patch.keys())
                    if before.get(key) != patch.get(key)}
            assert keys <= {"acceptCond", "acceptCondComb"}, (sid, keys)
            repair = fixes[sid]
            assert normalize_accept(patch.get("acceptCond")) == normalize_accept(repair.expected_accept)
            if repair.expected_comb is not None:
                assert patch.get("acceptCondComb") == repair.expected_comb
    assert changed == len(touched)
    assert index[35301] == current[35301], "Early Amber quest mutated"
    tmp = args.excel.with_suffix(".json.tmp")
    tmp.write_text(new, encoding="utf-8", newline="")
    os.replace(tmp, args.excel)
    print("PASS patched verified 95-row prerequisite manifest without modifying unrelated fields")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
