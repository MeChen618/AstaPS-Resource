#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Iterable


DEFAULT_QUEST_EXCEL = Path("ExcelBinOutput/QuestExcelConfigData.json")
DEFAULT_CHAPTER_EXCEL = Path("ExcelBinOutput/ChapterExcelConfigData.json")

STATE_EQUAL = "QUEST_COND_STATE_EQUAL"
STATE_NOT_EQUAL = "QUEST_COND_STATE_NOT_EQUAL"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def meaningful_conditions(value) -> list[dict]:
    if not isinstance(value, list):
        return []
    return [entry for entry in value if isinstance(entry, dict) and entry.get("type")]


def normalize_condition(entry: dict) -> dict:
    params = entry.get("param", [])
    if not isinstance(params, list):
        params = []
    if entry.get("type") in (STATE_EQUAL, STATE_NOT_EQUAL) and len(params) >= 2:
        params = params[:2]
    return {
        "type": entry.get("type"),
        "param": params,
        "param_str": entry.get("param_str", entry.get("paramStr", "")) or "",
    }


def normalize_accept(value) -> list[dict]:
    return [normalize_condition(entry) for entry in meaningful_conditions(value)]


def normalize_comb(row: dict) -> str:
    value = row.get("acceptCondComb")
    return value if value not in (None, "", "LOGIC_NONE") else "LOGIC_AND"


def iter_subquests(document) -> Iterable[dict]:
    if isinstance(document, dict):
        subquests = document.get("subQuests")
        if isinstance(subquests, list):
            yield from (row for row in subquests if isinstance(row, dict))
        return
    if isinstance(document, list):
        yield from (row for row in document if isinstance(row, dict))


def chapter_begin_ids(path: Path) -> set[int]:
    if not path.is_file():
        return set()
    root = load_json(path)
    if not isinstance(root, list):
        raise ValueError(f"{path} must contain a top-level JSON array")
    return {
        int(row.get("beginQuestId"))
        for row in root
        if isinstance(row, dict)
        and isinstance(row.get("beginQuestId"), int)
        and row.get("beginQuestId") > 0
    }


def reference_file(root: Path, json_file: str, main_id: int) -> Path | None:
    candidates = []
    if json_file:
        candidates.append(root / Path(json_file).name)
    if main_id:
        candidates.append(root / f"{main_id}.json")
    for path in candidates:
        if path.is_file():
            return path
    return None


def load_reference_row(
    root: Path, json_file: str, main_id: int, sub_id: int
) -> tuple[dict | None, str | None]:
    path = reference_file(root, json_file, main_id)
    if path is None:
        return None, None
    try:
        document = load_json(path)
    except (OSError, json.JSONDecodeError):
        return None, str(path)
    for row in iter_subquests(document):
        if int(row.get("subId") or 0) == sub_id:
            return row, str(path)
    return None, str(path)


def load_reference_main(root: Path, main_id: int) -> tuple[list[dict], str | None]:
    path = reference_file(root, "", main_id)
    if path is None:
        return [], None
    try:
        document = load_json(path)
    except (OSError, json.JSONDecodeError):
        return [], str(path)
    return list(iter_subquests(document)), str(path)


def is_zero_finished(conditions: list[dict]) -> bool:
    if len(conditions) != 1:
        return False
    cond = conditions[0]
    return cond.get("type") == STATE_EQUAL and cond.get("param") == [0, 3]


def classify(
    current: list[dict], current_comb: str, reference: list[dict], reference_comb: str
) -> str:
    if current == reference and current_comb == reference_comb:
        return "match"
    if is_zero_finished(current) and reference:
        return "zeroed-predecessor"
    if not current and reference:
        return "missing-accept"
    if len(current) < len(reference):
        return "conditions-lost"
    if len(current) > len(reference):
        return "conditions-added"
    if current_comb != reference_comb:
        return "combiner-drift"
    if len(current) == 1 and len(reference) == 1:
        cur = current[0]
        ref = reference[0]
        if cur.get("type") == ref.get("type") == STATE_EQUAL:
            cp = cur.get("param", [])
            rp = ref.get("param", [])
            if len(cp) >= 2 and len(rp) >= 2 and cp[1] == rp[1] and cp[0] != rp[0]:
                return "predecessor-drift"
    return "condition-drift"


def reference_signature(row: dict) -> tuple[str, str]:
    return (
        json.dumps(normalize_accept(row.get("acceptCond")), ensure_ascii=False, sort_keys=True),
        normalize_comb(row),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compare the flattened 7.1 quest prerequisite graph with one or more intact historical "
            "BinOutput/Quest trees. Multiple references must agree before a row is classified as "
            "repairable drift. The command never writes resources."
        )
    )
    parser.add_argument("quest_excel", nargs="?", type=Path, default=DEFAULT_QUEST_EXCEL)
    parser.add_argument(
        "--reference-bin-root",
        type=Path,
        action="append",
        required=True,
        help=(
            "Historical BinOutput/Quest directory. Repeat for multiple versions, e.g. 3700 and 4000. "
            "When multiple references contain the same subquest they must agree exactly on normalized "
            "acceptCond and acceptCondComb; disagreements are reported and never treated as repairs."
        ),
    )
    parser.add_argument("--chapter-excel", type=Path, default=DEFAULT_CHAPTER_EXCEL)
    parser.add_argument(
        "--main",
        dest="main_ids",
        type=int,
        action="append",
        default=[],
        help="Limit output to one main quest id. Repeat to select multiple main quests.",
    )
    parser.add_argument(
        "--include-reference-only",
        action="store_true",
        help=(
            "For explicitly selected --main quests, also report historical consensus subquests that "
            "are completely absent from the flattened QuestExcel resource."
        ),
    )
    parser.add_argument("--only-differences", action="store_true")
    parser.add_argument("--json", dest="json_output", type=Path, default=None)
    args = parser.parse_args()

    root = load_json(args.quest_excel)
    if not isinstance(root, list):
        raise SystemExit(f"{args.quest_excel} must contain a top-level JSON array")

    selected_main_ids = set(args.main_ids)
    if args.include_reference_only and not selected_main_ids:
        raise SystemExit("--include-reference-only requires at least one explicit --main")

    chapter_begins = chapter_begin_ids(args.chapter_excel)
    counts: Counter[str] = Counter()
    report: list[dict] = []
    missing_all_references = 0
    partial_reference_coverage = 0
    reference_disagreements = 0
    current_keys: set[tuple[int, int]] = set()

    for row in root:
        if not isinstance(row, dict):
            continue
        main_id = int(row.get("mainId") or 0)
        sub_id = int(row.get("subId") or 0)
        if selected_main_ids and main_id not in selected_main_ids:
            continue
        current_keys.add((main_id, sub_id))

        json_file = str(row.get("json_file") or "")
        reference_entries: list[tuple[dict, str, str]] = []
        missing_roots: list[str] = []
        for reference_root in args.reference_bin_root:
            reference_row, source = load_reference_row(reference_root, json_file, main_id, sub_id)
            if reference_row is None:
                missing_roots.append(str(reference_root))
                continue
            reference_entries.append((reference_row, source or "", str(reference_root)))

        if not reference_entries:
            missing_all_references += 1
            continue
        if missing_roots:
            partial_reference_coverage += 1

        signatures: dict[tuple[str, str], list[tuple[dict, str, str]]] = {}
        for entry in reference_entries:
            signatures.setdefault(reference_signature(entry[0]), []).append(entry)

        if len(signatures) != 1:
            reference_disagreements += 1
            counts["reference-disagreement"] += 1
            report.append(
                {
                    "classification": "reference-disagreement",
                    "json_file": json_file,
                    "main_id": main_id,
                    "sub_id": sub_id,
                    "order": int(row.get("order") or 0),
                    "show_type": str(row.get("showType") or ""),
                    "chapter_begin": sub_id in chapter_begins,
                    "current_accept": normalize_accept(row.get("acceptCond")),
                    "current_comb": normalize_comb(row),
                    "reference_variants": [
                        {
                            "accept": normalize_accept(ref_row.get("acceptCond")),
                            "comb": normalize_comb(ref_row),
                            "source": source,
                            "root": ref_root,
                        }
                        for ref_row, source, ref_root in reference_entries
                    ],
                    "missing_reference_roots": missing_roots,
                }
            )
            continue

        reference_row = reference_entries[0][0]
        current_accept = normalize_accept(row.get("acceptCond"))
        reference_accept = normalize_accept(reference_row.get("acceptCond"))
        current_comb = normalize_comb(row)
        reference_comb = normalize_comb(reference_row)
        kind = classify(current_accept, current_comb, reference_accept, reference_comb)
        counts[kind] += 1

        if kind == "match" and args.only_differences:
            continue

        report.append(
            {
                "classification": kind,
                "json_file": json_file,
                "main_id": main_id,
                "sub_id": sub_id,
                "order": int(row.get("order") or 0),
                "show_type": str(row.get("showType") or ""),
                "chapter_begin": sub_id in chapter_begins,
                "current_accept": current_accept,
                "reference_accept": reference_accept,
                "current_comb": current_comb,
                "reference_comb": reference_comb,
                "reference_sources": [entry[1] for entry in reference_entries],
                "reference_roots": [entry[2] for entry in reference_entries],
                "missing_reference_roots": missing_roots,
                "reference_consensus_count": len(reference_entries),
            }
        )

    if args.include_reference_only:
        for main_id in sorted(selected_main_ids):
            rows_by_root: list[tuple[dict[int, dict], str, str]] = []
            for reference_root in args.reference_bin_root:
                rows, source = load_reference_main(reference_root, main_id)
                rows_by_root.append(
                    (
                        {int(row.get("subId") or 0): row for row in rows},
                        source or "",
                        str(reference_root),
                    )
                )

            all_sub_ids = sorted({sid for rows, _, _ in rows_by_root for sid in rows if sid > 0})
            for sub_id in all_sub_ids:
                if (main_id, sub_id) in current_keys:
                    continue

                reference_entries: list[tuple[dict, str, str]] = []
                missing_roots: list[str] = []
                for rows, source, root_name in rows_by_root:
                    row = rows.get(sub_id)
                    if row is None:
                        missing_roots.append(root_name)
                    else:
                        reference_entries.append((row, source, root_name))

                if not reference_entries:
                    missing_all_references += 1
                    continue
                if missing_roots:
                    partial_reference_coverage += 1

                signatures: dict[tuple[str, str], list[tuple[dict, str, str]]] = {}
                for entry in reference_entries:
                    signatures.setdefault(reference_signature(entry[0]), []).append(entry)

                reference_row = reference_entries[0][0]
                if len(signatures) != 1:
                    reference_disagreements += 1
                    counts["reference-disagreement"] += 1
                    report.append(
                        {
                            "classification": "reference-disagreement",
                            "json_file": f"{main_id}.json",
                            "main_id": main_id,
                            "sub_id": sub_id,
                            "order": int(reference_row.get("order") or 0),
                            "show_type": str(reference_row.get("showType") or ""),
                            "chapter_begin": sub_id in chapter_begins,
                            "current_accept": [],
                            "current_comb": "LOGIC_AND",
                            "reference_variants": [
                                {
                                    "accept": normalize_accept(ref_row.get("acceptCond")),
                                    "comb": normalize_comb(ref_row),
                                    "source": source,
                                    "root": ref_root,
                                }
                                for ref_row, source, ref_root in reference_entries
                            ],
                            "missing_reference_roots": missing_roots,
                        }
                    )
                    continue

                counts["current-missing-row"] += 1
                report.append(
                    {
                        "classification": "current-missing-row",
                        "json_file": f"{main_id}.json",
                        "main_id": main_id,
                        "sub_id": sub_id,
                        "order": int(reference_row.get("order") or 0),
                        "show_type": str(reference_row.get("showType") or ""),
                        "chapter_begin": sub_id in chapter_begins,
                        "current_accept": [],
                        "reference_accept": normalize_accept(reference_row.get("acceptCond")),
                        "current_comb": "LOGIC_AND",
                        "reference_comb": normalize_comb(reference_row),
                        "reference_sources": [entry[1] for entry in reference_entries],
                        "reference_roots": [entry[2] for entry in reference_entries],
                        "missing_reference_roots": missing_roots,
                        "reference_consensus_count": len(reference_entries),
                    }
                )

    print("Quest prerequisite drift audit")
    print(f"  reference roots: {len(args.reference_bin_root)}")
    if selected_main_ids:
        print(f"  main ids: {','.join(map(str, sorted(selected_main_ids)))}")
    print(f"  compared with consensus: {sum(counts.values()) - counts['reference-disagreement']}")
    print(f"  reference-missing-all: {missing_all_references}")
    print(f"  partial-reference-coverage: {partial_reference_coverage}")
    print(f"  reference-disagreement: {reference_disagreements}")
    for name in (
        "match",
        "current-missing-row",
        "zeroed-predecessor",
        "missing-accept",
        "predecessor-drift",
        "conditions-lost",
        "conditions-added",
        "combiner-drift",
        "condition-drift",
    ):
        print(f"  {name}: {counts[name]}")

    printable = [item for item in report if item["classification"] != "match"]
    if not args.only_differences:
        printable = report

    if printable:
        print()
        print(
            "class\tmain\tsub\torder\tchapterBegin\tconsensusRefs\tcurrent\treference\tcurrentComb\treferenceComb"
        )
        for item in printable:
            if item["classification"] == "reference-disagreement":
                print(
                    "\t".join(
                        [
                            item["classification"],
                            str(item["main_id"]),
                            str(item["sub_id"]),
                            str(item["order"]),
                            "yes" if item["chapter_begin"] else "no",
                            "0",
                            json.dumps(item["current_accept"], ensure_ascii=False, separators=(",", ":")),
                            "<references-disagree>",
                            item["current_comb"],
                            "<references-disagree>",
                        ]
                    )
                )
                continue
            print(
                "\t".join(
                    [
                        item["classification"],
                        str(item["main_id"]),
                        str(item["sub_id"]),
                        str(item["order"]),
                        "yes" if item["chapter_begin"] else "no",
                        str(item["reference_consensus_count"]),
                        json.dumps(item["current_accept"], ensure_ascii=False, separators=(",", ":")),
                        json.dumps(item["reference_accept"], ensure_ascii=False, separators=(",", ":")),
                        item["current_comb"],
                        item["reference_comb"],
                    ]
                )
            )

    if args.json_output is not None:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(
                {
                    "reference_roots": [str(root) for root in args.reference_bin_root],
                    "main_ids": sorted(selected_main_ids),
                    "include_reference_only": args.include_reference_only,
                    "counts": dict(counts),
                    "reference_missing_all": missing_all_references,
                    "partial_reference_coverage": partial_reference_coverage,
                    "reference_disagreements": reference_disagreements,
                    "rows": report,
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
