#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from fix_quest_prerequisites import REPAIRS, STATE_EQUAL


DEFAULT_REPORT = Path("audit-prerequisite-consensus-3700-4000.json")
DEFAULT_MAIN_QUEST_EXCEL = Path("ExcelBinOutput/MainQuestExcelConfigData.json")
PROLOGUE_MAIN_IDS = {
    306,
    307,
    308,
    309,
    311,
    351,
    352,
    353,
    354,
    355,
    356,
    357,
    358,
    359,
    360,
    361,
    362,
    363,
    370,
    371,
    372,
    373,
    374,
    375,
    376,
    377,
    20101,
    379,
    380,
    381,
    382,
    383,
    384,
    397,
    388,
    389,
    390,
    393,
    394,
    398,
    396,
    399,
}

CLASS_PRIORITY = {
    "missing-accept": 80,
    "zeroed-predecessor": 70,
    "conditions-lost": 60,
    "combiner-drift": 50,
    "condition-drift": 40,
    "predecessor-drift": 30,
    "conditions-added": 20,
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def is_simple_state_equal(row: dict) -> bool:
    reference = row.get("reference_accept")
    if not isinstance(reference, list) or len(reference) != 1:
        return False
    cond = reference[0]
    return (
        isinstance(cond, dict)
        and cond.get("type") == STATE_EQUAL
        and isinstance(cond.get("param"), list)
        and len(cond["param"]) >= 2
        and row.get("reference_comb") == "LOGIC_AND"
    )


def infer_main_quest_type(row: dict) -> str:
    explicit = str(row.get("type") or "")
    if explicit:
        return explicit
    lua_path = str(row.get("luaPath") or "")
    leaf = lua_path.rsplit("/", 1)[-1]
    if leaf.startswith("MQ"):
        return "MQ"
    if leaf.startswith("WQ"):
        return "WQ"
    if leaf.startswith("LQ"):
        return "LQ"
    return ""


def load_main_quest_metadata(path: Path) -> dict[int, dict]:
    if not path.is_file():
        return {}
    root = load_json(path)
    if not isinstance(root, list):
        raise SystemExit(f"{path} must contain a top-level JSON array")
    result: dict[int, dict] = {}
    for row in root:
        if not isinstance(row, dict):
            continue
        main_id = int(row.get("id") or 0)
        if main_id <= 0:
            continue
        result[main_id] = {
            "type": infer_main_quest_type(row),
            "chapter_id": int(row.get("chapterId") or 0),
            "series": int(row.get("series") or 0),
            "lua_path": str(row.get("luaPath") or ""),
            "show_type": str(row.get("showType") or ""),
            "title_text_map_hash": int(row.get("titleTextMapHash") or 0),
        }
    return result


def candidate_priority(row: dict, metadata: dict) -> tuple[int, int, int, int]:
    return (
        1 if row.get("chapter_begin") else 0,
        1 if metadata.get("type") == "MQ" else 0,
        CLASS_PRIORITY.get(str(row.get("classification") or ""), 0),
        1 if str(row.get("show_type") or "") != "QUEST_HIDDEN" else 0,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Filter a multi-reference quest prerequisite drift report down to unresolved rows with "
            "complete historical consensus. Defaults to the Mondstadt Prologue for compatibility, "
            "but can triage all old content. This command never edits resources."
        )
    )
    parser.add_argument("report", nargs="?", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--scope",
        choices=("prologue", "all"),
        default="prologue",
        help="Rows to inspect when --main is not supplied (default: prologue).",
    )
    parser.add_argument(
        "--main",
        dest="main_ids",
        type=int,
        action="append",
        default=[],
        help="Limit to one main quest id. Repeat to select multiple main quests.",
    )
    parser.add_argument(
        "--exclude-main",
        dest="exclude_main_ids",
        type=int,
        action="append",
        default=[],
        help="Exclude one main quest id. Repeat as needed.",
    )
    parser.add_argument(
        "--exclude-prologue",
        action="store_true",
        help="Exclude the completed Mondstadt Prologue set; useful with --scope all.",
    )
    parser.add_argument(
        "--consensus-count",
        type=int,
        default=2,
        help="Required number of agreeing historical references (default: 2).",
    )
    parser.add_argument(
        "--main-quest-excel",
        type=Path,
        default=DEFAULT_MAIN_QUEST_EXCEL,
        help="MainQuestExcelConfigData.json used only to rank and label candidate groups.",
    )
    parser.add_argument(
        "--top-main",
        type=int,
        default=0,
        help="Print detailed candidate rows only for the top N main quests (0 = all).",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        type=Path,
        default=None,
        help="Optional path for the filtered machine-readable report.",
    )
    args = parser.parse_args()

    if args.consensus_count <= 0:
        raise SystemExit("--consensus-count must be positive")
    if args.top_main < 0:
        raise SystemExit("--top-main must be >= 0")

    root = load_json(args.report)
    if not isinstance(root, dict) or not isinstance(root.get("rows"), list):
        raise SystemExit(f"{args.report} is not a quest prerequisite drift JSON report")

    metadata_by_main = load_main_quest_metadata(args.main_quest_excel)
    manifest_sub_ids = {repair.sub_id for repair in REPAIRS}

    if args.main_ids:
        included_main_ids: set[int] | None = set(args.main_ids)
        scope_label = "explicit main ids"
    elif args.scope == "prologue":
        included_main_ids = set(PROLOGUE_MAIN_IDS)
        scope_label = "Mondstadt Prologue"
    else:
        included_main_ids = None
        scope_label = "all comparable old content"

    excluded_main_ids = set(args.exclude_main_ids)
    if args.exclude_prologue:
        excluded_main_ids.update(PROLOGUE_MAIN_IDS)

    def in_scope(row: dict) -> bool:
        main_id = int(row.get("main_id") or 0)
        if included_main_ids is not None and main_id not in included_main_ids:
            return False
        return main_id not in excluded_main_ids

    scoped_rows = [
        row for row in root["rows"] if isinstance(row, dict) and in_scope(row)
    ]
    manifest_rows = [
        row for row in scoped_rows if int(row.get("sub_id") or 0) in manifest_sub_ids
    ]
    residual_rows = [
        row
        for row in scoped_rows
        if row.get("classification") != "match"
        and int(row.get("sub_id") or 0) not in manifest_sub_ids
    ]

    disagreements = [
        row for row in residual_rows if row.get("classification") == "reference-disagreement"
    ]
    partial = [
        row
        for row in residual_rows
        if row.get("classification") != "reference-disagreement"
        and (
            int(row.get("reference_consensus_count") or 0) != args.consensus_count
            or bool(row.get("missing_reference_roots"))
        )
    ]
    consensus = [
        row
        for row in residual_rows
        if row.get("classification") != "reference-disagreement"
        and int(row.get("reference_consensus_count") or 0) == args.consensus_count
        and not row.get("missing_reference_roots")
    ]

    simple = [row for row in consensus if is_simple_state_equal(row)]
    manual = [row for row in consensus if not is_simple_state_equal(row)]

    class_counts = Counter(str(row.get("classification") or "") for row in residual_rows)
    consensus_class_counts = Counter(
        str(row.get("classification") or "") for row in consensus
    )

    grouped: dict[int, list[dict]] = defaultdict(list)
    for row in consensus:
        grouped[int(row.get("main_id") or 0)].append(row)

    main_groups: list[dict] = []
    for main_id, rows in grouped.items():
        metadata = metadata_by_main.get(main_id, {})
        classes = Counter(str(row.get("classification") or "") for row in rows)
        manual_count = sum(1 for row in rows if not is_simple_state_equal(row))
        chapter_begin_count = sum(1 for row in rows if row.get("chapter_begin"))
        best_priority = max(
            (candidate_priority(row, metadata) for row in rows),
            default=(0, 0, 0, 0),
        )
        main_groups.append(
            {
                "main_id": main_id,
                "type": metadata.get("type", ""),
                "chapter_id": metadata.get("chapter_id", 0),
                "series": metadata.get("series", 0),
                "lua_path": metadata.get("lua_path", ""),
                "candidate_count": len(rows),
                "manual_count": manual_count,
                "chapter_begin_count": chapter_begin_count,
                "class_counts": dict(classes),
                "_priority": best_priority,
            }
        )

    main_groups.sort(
        key=lambda item: (
            -item["_priority"][0],
            -item["_priority"][1],
            -item["_priority"][2],
            -item["manual_count"],
            -item["candidate_count"],
            item["main_id"],
        )
    )
    for item in main_groups:
        item.pop("_priority", None)

    detailed_main_ids = {item["main_id"] for item in main_groups}
    if args.top_main:
        detailed_main_ids = {
            item["main_id"] for item in main_groups[: args.top_main]
        }

    simple_print = [
        row for row in simple if int(row.get("main_id") or 0) in detailed_main_ids
    ]
    manual_print = [
        row for row in manual if int(row.get("main_id") or 0) in detailed_main_ids
    ]

    print("Quest prerequisite consensus filter")
    print(f"  report: {args.report}")
    print(f"  scope: {scope_label}")
    if args.main_ids:
        print("  included main ids: " + ", ".join(str(v) for v in sorted(set(args.main_ids))))
    if excluded_main_ids:
        print(
            "  excluded main ids: "
            + ", ".join(str(v) for v in sorted(excluded_main_ids))
        )
    print(f"  rows in scope: {len(scoped_rows)}")
    print(f"  manifest rows present/excluded: {len(manifest_rows)}")
    print(f"  residual differences: {len(residual_rows)}")
    print(f"  complete {args.consensus_count}-reference consensus: {len(consensus)}")
    print(f"  reference disagreements: {len(disagreements)}")
    print(f"  partial reference coverage: {len(partial)}")
    print(f"  simple state-equal review candidates: {len(simple)}")
    print(f"  manual/compound review candidates: {len(manual)}")
    print(f"  candidate main quests: {len(main_groups)}")
    if class_counts:
        print(
            "  residual classes: "
            + ", ".join(f"{k}={v}" for k, v in sorted(class_counts.items()))
        )
    if consensus_class_counts:
        print(
            "  consensus classes: "
            + ", ".join(
                f"{k}={v}" for k, v in sorted(consensus_class_counts.items())
            )
        )

    if main_groups:
        print()
        print("Priority main-quest groups")
        print("rank\tmain\ttype\tchapter\tcandidates\tmanual\tchapterBegin\tclasses")
        for index, item in enumerate(main_groups, start=1):
            classes = ",".join(
                f"{name}:{count}"
                for name, count in sorted(item["class_counts"].items())
            )
            print(
                "\t".join(
                    [
                        str(index),
                        str(item["main_id"]),
                        str(item["type"]),
                        str(item["chapter_id"]),
                        str(item["candidate_count"]),
                        str(item["manual_count"]),
                        str(item["chapter_begin_count"]),
                        classes,
                    ]
                )
            )

    group_rank = {
        item["main_id"]: index for index, item in enumerate(main_groups)
    }

    def print_rows(title: str, rows: list[dict]) -> None:
        if not rows:
            return
        print()
        print(title)
        print(
            "class\tmain\tsub\torder\tchapterBegin\tcurrent\treference\tcurrentComb\treferenceComb"
        )
        for row in sorted(
            rows,
            key=lambda item: (
                group_rank.get(int(item.get("main_id") or 0), len(group_rank)),
                int(item.get("order") or 0),
                int(item.get("sub_id") or 0),
            ),
        ):
            print(
                "\t".join(
                    [
                        str(row.get("classification") or ""),
                        str(row.get("main_id") or 0),
                        str(row.get("sub_id") or 0),
                        str(row.get("order") or 0),
                        "yes" if row.get("chapter_begin") else "no",
                        json.dumps(
                            row.get("current_accept"),
                            ensure_ascii=False,
                            separators=(",", ":"),
                        ),
                        json.dumps(
                            row.get("reference_accept"),
                            ensure_ascii=False,
                            separators=(",", ":"),
                        ),
                        str(row.get("current_comb") or ""),
                        str(row.get("reference_comb") or ""),
                    ]
                )
            )

    print_rows("Simple state-equal candidates (still review before repair)", simple_print)
    print_rows("Manual / compound consensus candidates", manual_print)
    if args.scope != "all" or args.main_ids:
        print_rows(
            "Reference disagreements (do not repair from historical consensus)",
            disagreements,
        )
        print_rows(
            "Partial coverage (do not treat as complete historical consensus)",
            partial,
        )
    elif disagreements or partial:
        print()
        print(
            "Blocked-row details suppressed for --scope all; use repeated --main to inspect a focused set."
        )

    if args.json_output is not None:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(
                {
                    "scope": args.scope,
                    "included_main_ids": (
                        sorted(included_main_ids)
                        if included_main_ids is not None
                        else None
                    ),
                    "excluded_main_ids": sorted(excluded_main_ids),
                    "required_consensus_count": args.consensus_count,
                    "manifest_sub_ids": sorted(manifest_sub_ids),
                    "manifest_rows_present": len(manifest_rows),
                    "residual_counts": dict(class_counts),
                    "consensus_counts": dict(consensus_class_counts),
                    "main_quest_groups": main_groups,
                    "simple": simple,
                    "manual": manual,
                    "reference_disagreements": disagreements,
                    "partial_reference_coverage": partial,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print()
        print(f"Wrote filtered JSON report: {args.json_output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
