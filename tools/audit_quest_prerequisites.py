#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_QUEST_EXCEL = Path("ExcelBinOutput/QuestExcelConfigData.json")
DEFAULT_REFERENCE_ROOT = None
STATE_TYPES = {
    "QUEST_COND_STATE_EQUAL",
    "QUEST_COND_STATE_NOT_EQUAL",
}


@dataclass(frozen=True)
class QuestKey:
    json_file: str
    main_id: int
    sub_id: int
    order: int


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def meaningful_conditions(value) -> list[dict]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict) and item.get("type")]


def normalize_condition(cond: dict) -> dict:
    params = cond.get("param")
    if not isinstance(params, list):
        params = []
    # The third integer in early state conditions is an unused fixed-width resource slot in the
    # intact data. Comparing the first two values avoids reporting harmless [x,3] vs [x,3,0].
    if cond.get("type") in STATE_TYPES and len(params) >= 2:
        params = params[:2]
    return {
        "type": cond.get("type"),
        "param": params,
        "param_str": cond.get("param_str", cond.get("paramStr", "")) or "",
    }


def normalize_conditions(value) -> list[dict]:
    return [normalize_condition(cond) for cond in meaningful_conditions(value)]


def iter_subquests(document) -> Iterable[dict]:
    if isinstance(document, dict):
        rows = document.get("subQuests")
        if isinstance(rows, list):
            yield from (row for row in rows if isinstance(row, dict))
    elif isinstance(document, list):
        yield from (row for row in document if isinstance(row, dict))


def reference_file(root: Path, json_file: str, main_id: int) -> Path | None:
    candidates: list[Path] = []
    if json_file:
        candidates.append(root / Path(json_file).name)
    if main_id:
        candidates.append(root / f"{main_id}.json")
    for path in candidates:
        if path.is_file():
            return path
    return None


def load_reference_quest(root: Path, key: QuestKey) -> tuple[dict | None, str | None]:
    path = reference_file(root, key.json_file, key.main_id)
    if path is None:
        return None, None
    try:
        document = load_json(path)
    except (OSError, json.JSONDecodeError):
        return None, str(path)
    for row in iter_subquests(document):
        if int(row.get("subId") or 0) == key.sub_id:
            return row, str(path)
    return None, str(path)


def classify(current: list[dict], expected: list[dict], current_comb: str, expected_comb: str) -> str:
    if current == expected and (not expected_comb or current_comb == expected_comb):
        return "same"
    if not expected:
        return "reference-has-no-accept"
    if not current:
        return "accept-missing"

    current_state = [x for x in current if x["type"] in STATE_TYPES]
    expected_state = [x for x in expected if x["type"] in STATE_TYPES]
    if len(current) == 1 and current_state:
        params = current_state[0]["param"]
        if len(params) >= 2 and params[0] == 0 and params[1] == 3:
            return "zeroed-predecessor"
    if len(current) != len(expected):
        return "condition-count-mismatch"
    if current_state != expected_state:
        return "state-graph-mismatch"
    if current_comb != expected_comb:
        return "logic-mismatch"
    return "condition-mismatch"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compare 7.1 QuestExcel accept conditions with an intact historical BinOutput/Quest "
            "tree. This is an audit only: no files are modified."
        )
    )
    parser.add_argument("quest_excel", nargs="?", type=Path, default=DEFAULT_QUEST_EXCEL)
    parser.add_argument(
        "--reference-bin-root",
        type=Path,
        required=True,
        help="Intact historical BinOutput/Quest directory to compare against.",
    )
    parser.add_argument(
        "--main",
        dest="main_ids",
        type=int,
        action="append",
        default=[],
        help="Limit to one main quest id; repeat for multiple ids.",
    )
    parser.add_argument(
        "--main-min",
        type=int,
        default=None,
        help="Optional inclusive main quest lower bound.",
    )
    parser.add_argument(
        "--main-max",
        type=int,
        default=None,
        help="Optional inclusive main quest upper bound.",
    )
    parser.add_argument(
        "--only-diff",
        action="store_true",
        help="Suppress identical rows.",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        type=Path,
        default=None,
        help="Write the complete machine-readable report to this path.",
    )
    args = parser.parse_args()

    current_root = load_json(args.quest_excel)
    if not isinstance(current_root, list):
        raise SystemExit(f"{args.quest_excel} must contain a top-level JSON array")

    wanted = set(args.main_ids)
    rows: list[dict] = []
    counts: Counter[str] = Counter()
    missing_reference_files: set[str] = set()

    for current_row in current_root:
        if not isinstance(current_row, dict):
            continue
        main_id = int(current_row.get("mainId") or 0)
        if wanted and main_id not in wanted:
            continue
        if args.main_min is not None and main_id < args.main_min:
            continue
        if args.main_max is not None and main_id > args.main_max:
            continue

        key = QuestKey(
            json_file=str(current_row.get("json_file") or ""),
            main_id=main_id,
            sub_id=int(current_row.get("subId") or 0),
            order=int(current_row.get("order") or 0),
        )
        reference_row, reference_source = load_reference_quest(args.reference_bin_root, key)
        if reference_row is None:
            if reference_source is None:
                missing_reference_files.add(key.json_file or f"{main_id}.json")
            continue

        current_accept = normalize_conditions(current_row.get("acceptCond"))
        expected_accept = normalize_conditions(reference_row.get("acceptCond"))
        current_comb = str(current_row.get("acceptCondComb") or "LOGIC_NONE")
        expected_comb = str(reference_row.get("acceptCondComb") or "LOGIC_NONE")
        kind = classify(current_accept, expected_accept, current_comb, expected_comb)
        counts[kind] += 1

        if args.only_diff and kind == "same":
            continue
        rows.append(
            {
                "classification": kind,
                "json_file": key.json_file,
                "main_id": key.main_id,
                "sub_id": key.sub_id,
                "order": key.order,
                "current_accept": current_accept,
                "expected_accept": expected_accept,
                "current_accept_comb": current_comb,
                "expected_accept_comb": expected_comb,
                "reference_source": reference_source,
            }
        )

    print("Prerequisite audit")
    print(f"  compared rows: {sum(counts.values())}")
    for kind in sorted(counts):
        print(f"  {kind}: {counts[kind]}")
    if missing_reference_files:
        print(f"  missing reference files: {len(missing_reference_files)}")

    if rows:
        print()
        print("class\tmain\tsub\torder\tcurrent\texpected\tlogic\tjson_file")
        for row in rows:
            print(
                "\t".join(
                    [
                        row["classification"],
                        str(row["main_id"]),
                        str(row["sub_id"]),
                        str(row["order"]),
                        json.dumps(row["current_accept"], ensure_ascii=False, separators=(",", ":")),
                        json.dumps(row["expected_accept"], ensure_ascii=False, separators=(",", ":")),
                        f'{row["current_accept_comb"]}->{row["expected_accept_comb"]}',
                        row["json_file"],
                    ]
                )
            )

    if args.json_output is not None:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(
                {
                    "counts": dict(counts),
                    "missing_reference_files": sorted(missing_reference_files),
                    "rows": rows,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print()
        print(f"Wrote JSON report: {args.json_output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
