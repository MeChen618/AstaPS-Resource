#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_QUEST_EXCEL = Path("ExcelBinOutput/QuestExcelConfigData.json")
DEFAULT_CHAPTER_EXCEL = Path("ExcelBinOutput/ChapterExcelConfigData.json")
DEFAULT_BIN_ROOT = Path("BinOutput/Quest")
STATE_EQUAL = "QUEST_COND_STATE_EQUAL"
FINISHED = 3


@dataclass(frozen=True)
class Candidate:
    json_file: str
    main_id: int
    sub_id: int
    order: int
    show_type: str
    desc_hash: int
    is_chapter_begin: bool
    accept_index: int


@dataclass(frozen=True)
class ReferenceMatch:
    predecessor: int
    state: int
    source: str


@dataclass(frozen=True)
class SourceProbe:
    found: bool
    meaningful_count: int
    source: str | None


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def meaningful_conditions(value) -> list[dict]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict) and item.get("type")]


def is_zero_finished(cond: dict) -> bool:
    if cond.get("type") != STATE_EQUAL:
        return False
    params = cond.get("param")
    return isinstance(params, list) and len(params) >= 2 and params[0] == 0 and params[1] == FINISHED


def chapter_begin_ids(chapter_path: Path) -> set[int]:
    if not chapter_path.is_file():
        return set()
    root = load_json(chapter_path)
    if not isinstance(root, list):
        raise ValueError(f"{chapter_path} must contain a top-level JSON array")
    out: set[int] = set()
    for row in root:
        if not isinstance(row, dict):
            continue
        quest_id = row.get("beginQuestId")
        if isinstance(quest_id, int) and quest_id > 0:
            out.add(quest_id)
    return out


def collect_candidates(quest_path: Path, chapter_begins: set[int]) -> tuple[list[Candidate], list[dict]]:
    root = load_json(quest_path)
    if not isinstance(root, list):
        raise ValueError(f"{quest_path} must contain a top-level JSON array")

    candidates: list[Candidate] = []
    for row in root:
        if not isinstance(row, dict):
            continue
        conditions = meaningful_conditions(row.get("acceptCond"))
        for index, cond in enumerate(conditions):
            if not is_zero_finished(cond):
                continue
            candidates.append(
                Candidate(
                    json_file=str(row.get("json_file") or ""),
                    main_id=int(row.get("mainId") or 0),
                    sub_id=int(row.get("subId") or 0),
                    order=int(row.get("order") or 0),
                    show_type=str(row.get("showType") or ""),
                    desc_hash=int(row.get("descTextMapHash") or 0),
                    is_chapter_begin=int(row.get("subId") or 0) in chapter_begins,
                    accept_index=index,
                )
            )
    return candidates, root


def quest_file_for(root: Path, json_file: str, main_id: int) -> Path | None:
    candidates: list[Path] = []
    if json_file:
        candidates.append(root / Path(json_file).name)
    if main_id:
        candidates.append(root / f"{main_id}.json")
    for path in candidates:
        if path.is_file():
            return path
    return None


def iter_subquests(document) -> Iterable[dict]:
    if isinstance(document, dict):
        subquests = document.get("subQuests")
        if isinstance(subquests, list):
            for row in subquests:
                if isinstance(row, dict):
                    yield row
        return
    if isinstance(document, list):
        for row in document:
            if isinstance(row, dict):
                yield row


def find_source_probe(root: Path | None, candidate: Candidate) -> SourceProbe:
    if root is None:
        return SourceProbe(False, 0, None)
    path = quest_file_for(root, candidate.json_file, candidate.main_id)
    if path is None:
        return SourceProbe(False, 0, None)
    try:
        document = load_json(path)
    except (OSError, json.JSONDecodeError):
        return SourceProbe(False, 0, str(path))
    for row in iter_subquests(document):
        if int(row.get("subId") or 0) == candidate.sub_id:
            return SourceProbe(True, len(meaningful_conditions(row.get("acceptCond"))), str(path))
    return SourceProbe(False, 0, str(path))


def find_reference_match(root: Path | None, candidate: Candidate) -> ReferenceMatch | None:
    if root is None:
        return None
    path = quest_file_for(root, candidate.json_file, candidate.main_id)
    if path is None:
        return None

    try:
        document = load_json(path)
    except (OSError, json.JSONDecodeError):
        return None

    for row in iter_subquests(document):
        if int(row.get("subId") or 0) != candidate.sub_id:
            continue
        conditions = meaningful_conditions(row.get("acceptCond"))
        matches: list[tuple[int, int]] = []
        for cond in conditions:
            if cond.get("type") != STATE_EQUAL:
                continue
            params = cond.get("param")
            if not isinstance(params, list) or len(params) < 2:
                continue
            predecessor = params[0]
            state = params[1]
            if isinstance(predecessor, int) and isinstance(state, int):
                matches.append((predecessor, state))
        if len(matches) != 1:
            return None
        predecessor, state = matches[0]
        if predecessor <= 0:
            return None
        return ReferenceMatch(predecessor=predecessor, state=state, source=str(path))
    return None


def classify(
    candidate: Candidate,
    source_probe: SourceProbe,
    local_match: ReferenceMatch | None,
    historical_match: ReferenceMatch | None,
) -> str:
    # Historical intact data is the strongest evidence that the flattened zero is a conversion loss.
    if historical_match is not None and historical_match.state == FINISHED:
        return "historical-repair"
    # Some source BinOutput files still retain a real predecessor even when the flattened Excel lost it.
    if local_match is not None and local_match.state == FINISHED:
        return "local-binout-repair"
    # Newer 7.x quests often have no source acceptCond at all. Their flattened [0,3] is therefore a
    # root/external-trigger placeholder until another intact source proves a missing predecessor.
    if source_probe.found and source_probe.meaningful_count == 0:
        return "source-root-or-external"
    if candidate.is_chapter_begin:
        return "chapter-begin-unresolved"
    if candidate.order > 1:
        return "internal-order-unresolved"
    return "root-like-unresolved"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit QUEST_COND_STATE_EQUAL [0, FINISHED] prerequisites in the 7.1 quest dump. "
            "The command only reports evidence; it never rewrites resources."
        )
    )
    parser.add_argument("quest_excel", nargs="?", type=Path, default=DEFAULT_QUEST_EXCEL)
    parser.add_argument("--chapter-excel", type=Path, default=DEFAULT_CHAPTER_EXCEL)
    parser.add_argument(
        "--bin-root",
        type=Path,
        default=DEFAULT_BIN_ROOT,
        help="Current BinOutput/Quest directory used for same-repo cross-checks.",
    )
    parser.add_argument(
        "--reference-bin-root",
        type=Path,
        default=None,
        help=(
            "Optional intact historical BinOutput/Quest directory. A candidate is marked "
            "historical-repair only when the same subQuest has exactly one non-zero "
            "QUEST_COND_STATE_EQUAL predecessor there."
        ),
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        type=Path,
        default=None,
        help="Write the complete machine-readable audit report to this path.",
    )
    categories = (
        "historical-repair",
        "local-binout-repair",
        "source-root-or-external",
        "chapter-begin-unresolved",
        "internal-order-unresolved",
        "root-like-unresolved",
    )
    parser.add_argument(
        "--only",
        choices=categories,
        default=None,
        help="Print only one classification while keeping totals over the full scan.",
    )
    args = parser.parse_args()

    chapter_begins = chapter_begin_ids(args.chapter_excel)
    candidates, _ = collect_candidates(args.quest_excel, chapter_begins)

    report: list[dict] = []
    counts: Counter[str] = Counter()
    for candidate in candidates:
        source_probe = find_source_probe(args.bin_root, candidate)
        local_match = find_reference_match(args.bin_root, candidate)
        historical_match = find_reference_match(args.reference_bin_root, candidate)
        kind = classify(candidate, source_probe, local_match, historical_match)
        counts[kind] += 1

        best = historical_match or local_match
        item = {
            "classification": kind,
            "json_file": candidate.json_file,
            "main_id": candidate.main_id,
            "sub_id": candidate.sub_id,
            "order": candidate.order,
            "show_type": candidate.show_type,
            "desc_hash": candidate.desc_hash,
            "chapter_begin": candidate.is_chapter_begin,
            "accept_index": candidate.accept_index,
            "source_row_found": source_probe.found,
            "source_meaningful_accept_count": source_probe.meaningful_count,
            "source_file": source_probe.source,
            "reference_predecessor": best.predecessor if best else None,
            "reference_state": best.state if best else None,
            "reference_source": best.source if best else None,
        }
        report.append(item)

    print(f"Candidates with QUEST_COND_STATE_EQUAL [0,{FINISHED}]: {len(candidates)}")
    for name in categories:
        print(f"  {name}: {counts[name]}")

    printable = report if args.only is None else [row for row in report if row["classification"] == args.only]
    if printable:
        print()
        print("class\tmain\tsub\torder\tchapterBegin\tsourceAcceptCount\tpredecessor\tjson_file\treference")
        for row in printable:
            print(
                "\t".join(
                    [
                        str(row["classification"]),
                        str(row["main_id"]),
                        str(row["sub_id"]),
                        str(row["order"]),
                        "yes" if row["chapter_begin"] else "no",
                        str(row["source_meaningful_accept_count"]),
                        str(row["reference_predecessor"] or ""),
                        str(row["json_file"]),
                        str(row["reference_source"] or ""),
                    ]
                )
            )

    if args.json_output is not None:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(
                {
                    "candidate_count": len(candidates),
                    "counts": dict(counts),
                    "candidates": report,
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
