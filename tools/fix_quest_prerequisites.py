#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_PATH = Path("ExcelBinOutput/QuestExcelConfigData.json")
STATE_EQUAL = "QUEST_COND_STATE_EQUAL"
STATE_NOT_EQUAL = "QUEST_COND_STATE_NOT_EQUAL"
FINISHED = 3


def state_equal(quest_id: int, state: int = FINISHED) -> dict:
    return {"type": STATE_EQUAL, "param": [quest_id, state, 0], "param_str": ""}


def state_not_equal(quest_id: int, state: int = FINISHED) -> dict:
    return {"type": STATE_NOT_EQUAL, "param": [quest_id, state, 0], "param_str": ""}


@dataclass(frozen=True)
class Repair:
    json_file: str
    main_id: int
    sub_id: int
    desc_hash: int
    expected_accept: tuple[dict, ...]
    damaged_accept: tuple[tuple[dict, ...], ...]
    expected_comb: str | None = None
    damaged_comb: tuple[str, ...] = ()


def one(predecessor: int, *, state: int = FINISHED) -> tuple[dict, ...]:
    return (state_equal(predecessor, state),)


# Evidence: intact historical BinOutput for the same Mondstadt quest graph.
# A negative desc_hash means json_file + main_id + sub_id is used as the identity key; this is
# intentional for rows whose text hashes drift slightly between resource revisions. The current
# accept-condition shape is still checked strictly before any rewrite.
REPAIRS = (
    # Fresh-player / Prologue Act I entry.
    Repair("351.json", 351, 35101, 3236261087, one(35100), (one(35107),)),
    Repair("352.json", 352, 35200, 2150333847, one(35102), (one(0),)),

    # Prologue Act I visible chain.
    Repair("354.json", 354, 35401, 2564565335, one(35505), (one(0),)),
    Repair("354.json", 354, 35403, 1527152647, one(35404), (one(35405),)),
    Repair("355.json", 355, 35501, 1480972647, one(35311), (one(0),)),
    Repair(
        "355.json",
        355,
        35502,
        3003852887,
        (state_equal(35501), state_equal(36101), state_equal(36101)),
        ((state_equal(35501),),),
        expected_comb="LOGIC_AND",
    ),
    Repair("356.json", 356, 35601, 1893185559, one(36005), (one(0),)),
    Repair("356.json", 356, 35603, 645974095, one(35601), (one(35602),)),
    Repair("357.json", 357, 35721, 401722439, one(35606), (one(0),)),
    Repair("358.json", 358, 35800, 2056537383, one(35724), (one(0),)),

    # Three temple branches plus the hidden completion controller fan out from 35802.
    Repair("306.json", 306, 30600, 447310999, one(35802), (one(0),)),
    Repair("307.json", 307, 30700, 4264103487, one(35802), (one(0),)),
    Repair("308.json", 308, 30800, 4078363583, one(35802), (one(0),)),
    Repair("309.json", 309, 30901, 2918457247, one(35802), (one(0),)),
    Repair("311.json", 311, 31101, 486980247, one(30904), (one(0),)),

    # Hidden Act-I controllers / non-linear nodes.
    Repair("359.json", 359, 35901, 1736464775, one(35725), (one(0),)),
    Repair("359.json", 359, 35902, 206764287, one(35802), (one(35901),)),
    Repair("359.json", 359, 35903, 4126557215, one(35802), (one(35902),)),
    Repair("359.json", 359, 35904, 969515055, one(35802), (one(35903),)),
    Repair("360.json", 360, 36001, 4087620839, one(35403), (one(0),)),
    Repair("360.json", 360, 36003, 2320130263, one(36001), (one(0),)),
    Repair("361.json", 361, 36100, 0, one(35311), (one(0),)),
    Repair(
        "362.json",
        362,
        36203,
        0,
        (state_equal(99902), state_not_equal(35200), state_not_equal(35200)),
        ((state_equal(0),),),
        expected_comb="LOGIC_AND",
    ),

    # Chapter 1001 controller -> ChapterStateNotify(1001, BEGIN).
    Repair("363.json", 363, 36301, 0, one(35202), (one(0),)),

    # Prologue Act II.
    Repair("370.json", 370, 37001, 984138423, one(31101), (one(0),)),
    Repair("370.json", 370, 37003, 411942639, one(37005, state=2), (one(37005),)),
    Repair("371.json", 371, 37101, 3416483463, one(37005), (one(0),)),
    Repair("372.json", 372, 37201, -1, one(37113), (one(0),)),
    Repair("373.json", 373, 37301, -1, one(37203), (one(0),)),
    Repair("374.json", 374, 37408, -1, one(37304), (one(0),)),
    Repair("375.json", 375, 37501, -1, one(37406), (one(0),)),
    Repair("376.json", 376, 37601, -1, one(37506), (one(0),)),
    Repair("377.json", 377, 37701, -1, one(37608), (one(0),)),
    # Lisa's temple bridge is still in series/chapter 1002.
    Repair("20101.json", 20101, 2010100, -1, one(37706), (one(0),)),
    Repair("379.json", 379, 37901, -1, one(2010151), (one(0),)),
    Repair("380.json", 380, 38001, -1, one(37904), (one(0),)),
    Repair("381.json", 381, 38101, -1, one(37904), (one(0),)),
    Repair("382.json", 382, 38201, -1, one(37904), (one(0),)),
    Repair(
        "383.json",
        383,
        38301,
        -1,
        (state_equal(38004), state_equal(38105), state_equal(38202)),
        (one(0),),
        expected_comb="LOGIC_AND",
    ),
    Repair("384.json", 384, 38401, -1, one(38304), (one(0),)),

    # Prologue Act III.
    Repair("397.json", 397, 39701, 619581215, one(38406), (one(0),)),
    Repair("388.json", 388, 38806, -1, one(39704), (one(0),)),
    Repair("389.json", 389, 38901, -1, one(38804), (one(0),)),
    Repair("390.json", 390, 39003, -1, one(38906), (one(0),)),
    Repair("393.json", 393, 39301, -1, one(39008), (one(0),)),
    Repair("394.json", 394, 39401, -1, one(39303), (one(0),)),
    Repair("398.json", 398, 39810, -1, one(39402), (one(0),)),
    Repair("396.json", 396, 39601, -1, one(39808), (one(0),)),
    Repair("399.json", 399, 39901, -1, one(39812), (one(0),)),
)

# Residual Mondstadt Prologue prerequisite graph repairs.
# Evidence: exact normalized acceptCond + acceptCondComb consensus in GCResource 3.7 and 4.0.
# These are kept separate from the first evidence batch so the consensus provenance stays explicit.
REPAIRS += (
    # 306.json
    Repair("306.json", 306, 30608, -1, one(30602), (one(30607),)),
    Repair("306.json", 306, 30609, -1, one(30602), (one(30608),)),
    Repair("306.json", 306, 30612, -1, one(30602), (one(30609),)),
    Repair("306.json", 306, 30611, -1, one(30602), (one(30612),)),
    Repair("306.json", 306, 30603, -1, one(30602), (one(30611),)),
    Repair("306.json", 306, 30604, -1, one(30603), (one(30610),)),

    # 307.json
    Repair("307.json", 307, 30707, -1, one(30702), (one(30710),)),
    Repair("307.json", 307, 30708, -1, one(30702), (one(30707),)),
    Repair("307.json", 307, 30709, -1, one(30702), (one(30708),)),
    Repair("307.json", 307, 30712, -1, one(30702), (one(30709),)),
    Repair("307.json", 307, 30711, -1, one(30702), (one(30712),)),
    Repair("307.json", 307, 30703, -1, one(30702), (one(30711),)),

    # 308.json
    Repair("308.json", 308, 30807, -1, one(30802), (one(30810),)),
    Repair("308.json", 308, 30808, -1, one(30802), (one(30807),)),
    Repair("308.json", 308, 30809, -1, one(30802), (one(30808),)),
    Repair("308.json", 308, 30812, -1, one(30802), (one(30809),)),
    Repair("308.json", 308, 30811, -1, one(30802), (one(30812),)),
    Repair("308.json", 308, 30803, -1, one(30802), (one(30811),)),
    Repair("308.json", 308, 30804, -1, one(30803), (one(30814),)),

    # 351.json
    Repair("351.json", 351, 35104, -1, (), (one(0),)),
    Repair("351.json", 351, 35103, -1, (state_equal(35106), state_not_equal(35105), state_not_equal(35105)), (one(35105),), expected_comb="LOGIC_AND"),
    Repair("351.json", 351, 35102, -1, (state_equal(35103), state_equal(35105), state_equal(35105)), (one(35103),), expected_comb="LOGIC_OR"),

    # 353.json
    Repair("353.json", 353, 35301, -1, one(35205), (one(0),)),
    Repair("353.json", 353, 35312, -1, one(35205), (one(35301),)),
    Repair("353.json", 353, 35302, -1, one(35301), (one(35312),)),

    # 371.json
    Repair("371.json", 371, 37114, -1, one(37108), (one(37113),)),
    Repair("371.json", 371, 37115, -1, (state_equal(37114), state_not_equal(37109)), (one(37114),), expected_comb="LOGIC_AND"),

    # 374.json
    Repair("374.json", 374, 37407, -1, one(37304), (one(37408),)),

    # 375.json
    Repair("375.json", 375, 37504, -1, one(37503, state=4), (one(37503),)),
    Repair("375.json", 375, 37505, -1, one(37503), (one(37504),)),

    # 376.json
    Repair("376.json", 376, 37603, -1, one(37602, state=4), (one(37602),)),
    Repair("376.json", 376, 37604, -1, one(37602), (one(37603),)),

    # 20101.json
    Repair("20101.json", 20101, 2010101, -1, one(37706), (one(2010100),)),
    Repair("20101.json", 20101, 2010105, -1, one(2010144), (one(2010104),)),
    Repair("20101.json", 20101, 2010106, -1, one(2010144), (one(2010105),)),
    Repair("20101.json", 20101, 2010107, -1, one(2010144), (one(2010106),)),
    Repair("20101.json", 20101, 2010108, -1, one(2010144), (one(2010107),)),
    Repair("20101.json", 20101, 2010109, -1, one(2010144), (one(2010108),)),
    Repair("20101.json", 20101, 2010110, -1, one(2010144), (one(2010109),)),
    Repair("20101.json", 20101, 2010113, -1, (state_equal(2010112), state_equal(2010109)), (one(2010112),), expected_comb="LOGIC_OR"),
    Repair("20101.json", 20101, 2010145, -1, one(2010109), (one(2010113),)),
    Repair("20101.json", 20101, 2010146, -1, one(2010112), (one(2010145),)),
    Repair("20101.json", 20101, 2010153, -1, one(2010144), (one(2010146),)),
    Repair("20101.json", 20101, 2010154, -1, one(2010144), (one(2010153),)),
    Repair("20101.json", 20101, 2010155, -1, one(2010144), (one(2010154),)),
    Repair("20101.json", 20101, 2010156, -1, one(2010144), (one(2010155),)),
    Repair("20101.json", 20101, 2010157, -1, one(2010144), (one(2010156),)),
    Repair("20101.json", 20101, 2010114, -1, one(2010144), (one(2010157),)),
    Repair("20101.json", 20101, 2010115, -1, one(2010144), (one(2010114),)),
    Repair("20101.json", 20101, 2010116, -1, one(2010144), (one(2010115),)),
    Repair("20101.json", 20101, 2010117, -1, one(2010144), (one(2010116),)),
    Repair("20101.json", 20101, 2010118, -1, one(2010144), (one(2010117),)),
    Repair("20101.json", 20101, 2010119, -1, one(2010144), (one(2010118),)),
    Repair("20101.json", 20101, 2010120, -1, one(2010144), (one(2010119),)),
    Repair("20101.json", 20101, 2010123, -1, (state_equal(2010122), state_equal(2010119)), (one(2010122),), expected_comb="LOGIC_OR"),
    Repair("20101.json", 20101, 2010147, -1, one(2010119), (one(2010123),)),
    Repair("20101.json", 20101, 2010148, -1, one(2010122), (one(2010147),)),
    Repair("20101.json", 20101, 2010158, -1, one(2010144), (one(2010148),)),
    Repair("20101.json", 20101, 2010159, -1, one(2010144), (one(2010158),)),
    Repair("20101.json", 20101, 2010160, -1, one(2010144), (one(2010159),)),
    Repair("20101.json", 20101, 2010149, -1, one(2010144), (one(0),)),
    Repair("20101.json", 20101, 2010150, -1, one(2010144), (one(2010149),)),
    Repair("20101.json", 20101, 2010134, -1, one(2010144), (one(2010150),)),
    Repair("20101.json", 20101, 2010135, -1, one(2010144), (one(2010134),)),
    Repair("20101.json", 20101, 2010138, -1, one(2010144), (one(0),)),
    Repair("20101.json", 20101, 2010139, -1, one(2010144), (one(2010138),)),
    Repair("20101.json", 20101, 2010140, -1, one(2010144), (one(2010139),)),
    Repair("20101.json", 20101, 2010141, -1, one(2010144), (one(2010140),)),
    Repair("20101.json", 20101, 2010124, -1, one(99902), (one(0),)),
    Repair("20101.json", 20101, 2010126, -1, one(2010124), (one(2010125),)),
    Repair("20101.json", 20101, 2010127, -1, one(2010124), (one(2010126),)),
    Repair("20101.json", 20101, 2010128, -1, one(2010124), (one(2010127),)),
    Repair("20101.json", 20101, 2010129, -1, one(2010124), (one(2010128),)),
    Repair("20101.json", 20101, 2010130, -1, one(2010124), (one(2010129),)),
    Repair("20101.json", 20101, 2010133, -1, (state_equal(2010132), state_equal(2010129)), (one(2010132),), expected_comb="LOGIC_OR"),
    Repair("20101.json", 20101, 2010136, -1, one(99902), (one(2010133),)),

    # 388.json
    Repair("388.json", 388, 38805, -1, one(38802, state=4), (one(38802),)),
    Repair("388.json", 388, 38803, -1, one(38802), (one(38805),)),

    # 389.json
    Repair("389.json", 389, 38902, -1, one(38804), (one(38901),)),

    # 390.json
    Repair("390.json", 390, 39006, -1, one(39004), (one(39005),)),
    Repair("390.json", 390, 39007, -1, one(39004), (one(39006),)),
    Repair("390.json", 390, 39008, -1, one(39004), (one(39007),)),
    Repair("390.json", 390, 39009, -1, one(39004), (one(39008),)),

    # 394.json
    Repair("394.json", 394, 39405, -1, one(39402), (one(39403),)),

    # 396.json
    Repair("396.json", 396, 39607, -1, one(39605), (one(39604),)),

    # 398.json
    Repair("398.json", 398, 39814, -1, one(39810), (one(39812),)),
    Repair("398.json", 398, 39811, -1, one(39812), (one(39814),)),
    Repair("398.json", 398, 39801, -1, one(39402), (one(39811),)),
    Repair("398.json", 398, 39805, -1, one(99902), (one(39804),)),
    Repair("398.json", 398, 39806, -1, one(99902), (one(39805),)),
    Repair("398.json", 398, 39807, -1, one(39804), (one(39806),)),
    Repair("398.json", 398, 39815, -1, one(99902), (one(39807),)),
    Repair("398.json", 398, 39808, -1, one(39807), (one(39815),)),
    Repair("398.json", 398, 39813, -1, one(39808), (one(39816),)),
    Repair("398.json", 398, 39809, -1, one(39808), (one(39813),)),
)


def iter_top_level_objects(text: str):
    depth = 0
    in_string = False
    escaped = False
    start = None
    for i, ch in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth == 0:
                raise ValueError(f"Unexpected closing brace at offset {i}")
            depth -= 1
            if depth == 0 and start is not None:
                yield start, i + 1
                start = None
    if in_string:
        raise ValueError("Unterminated JSON string")
    if depth != 0:
        raise ValueError("Unbalanced JSON object braces")


def meaningful_entries(value) -> list[dict]:
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
    return [normalize_condition(entry) for entry in meaningful_entries(value)]


def normalized_variant(value: tuple[dict, ...]) -> list[dict]:
    return normalize_accept(list(value))


def identify_repair(obj: dict) -> Repair | None:
    for repair in REPAIRS:
        if (
            obj.get("json_file") == repair.json_file
            and obj.get("mainId") == repair.main_id
            and obj.get("subId") == repair.sub_id
            and (repair.desc_hash < 0 or obj.get("descTextMapHash") == repair.desc_hash)
        ):
            return repair
    return None


def render_object(obj: dict) -> str:
    raw = json.dumps(obj, ensure_ascii=False, indent=2)
    lines = raw.splitlines()
    return lines[0] + "\n" + "\n".join("  " + line for line in lines[1:])


def patch_object(raw: str, repair: Repair) -> tuple[str, str, list[str]]:
    obj = json.loads(raw)
    current = normalize_accept(obj.get("acceptCond"))
    expected = normalized_variant(repair.expected_accept)
    damaged = [normalized_variant(variant) for variant in repair.damaged_accept]
    changes: list[str] = []

    if current == expected:
        pass
    elif current in damaged:
        obj["acceptCond"] = [dict(entry) for entry in repair.expected_accept]
        changes.append(f"acceptCond={expected!r}")
    else:
        raise ValueError(
            f"Quest {repair.sub_id} has unexpected meaningful acceptCond: {current!r}; "
            f"expected {expected!r} or one of damaged variants {damaged!r}"
        )

    if repair.expected_comb is not None:
        current_comb = obj.get("acceptCondComb")
        if current_comb == repair.expected_comb:
            pass
        elif current_comb in (None, "", "LOGIC_NONE") or current_comb in repair.damaged_comb:
            obj["acceptCondComb"] = repair.expected_comb
            changes.append(f"acceptCondComb={repair.expected_comb}")
        else:
            raise ValueError(
                f"Quest {repair.sub_id} has unexpected acceptCondComb={current_comb!r}; "
                f"expected {repair.expected_comb!r}, missing, or one of damaged variants "
                f"{repair.damaged_comb!r}"
            )

    if not changes:
        return raw, "already-correct", []

    patched = render_object(obj)
    parsed = json.loads(patched)
    if normalize_accept(parsed.get("acceptCond")) != expected:
        raise ValueError(f"Quest {repair.sub_id} repair did not survive JSON validation")
    if repair.expected_comb is not None and parsed.get("acceptCondComb") != repair.expected_comb:
        raise ValueError(f"Quest {repair.sub_id} logic repair did not survive JSON validation")
    return patched, "changed", changes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Repair evidence-backed 7.1 quest prerequisite conversion defects."
    )
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_PATH)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate known rows and report pending repairs without writing.",
    )
    args = parser.parse_args()

    path: Path = args.path
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

    found: dict[int, tuple[str, list[str]]] = {}
    replacements: list[tuple[int, int, str]] = []

    for start, end in iter_top_level_objects(text):
        raw = text[start:end]
        obj = json.loads(raw)
        if not isinstance(obj, dict):
            continue
        repair = identify_repair(obj)
        if repair is None:
            continue
        if repair.sub_id in found:
            raise SystemExit(f"Quest {repair.sub_id} appears more than once in {path}")
        patched, status, changes = patch_object(raw, repair)
        found[repair.sub_id] = (status, changes)
        if status == "changed":
            replacements.append((start, end, patched))

    missing = [repair.sub_id for repair in REPAIRS if repair.sub_id not in found]
    if missing:
        raise SystemExit(f"Expected quest rows not found: {missing}")

    for repair in REPAIRS:
        status, changes = found[repair.sub_id]
        detail = ", ".join(changes) if changes else "verified"
        print(f"Quest {repair.sub_id}: {status}: {detail}")

    if args.check:
        if replacements:
            print(f"Pending repaired quest rows: {len(replacements)}")
            return 1
        print("All evidence-backed quest prerequisite repairs are already applied.")
        return 0

    if not replacements:
        print("Nothing to do; the resource is already fixed.")
        return 0

    patched_text = text
    for start, end, patched in reversed(replacements):
        patched_text = patched_text[:start] + patched + patched_text[end:]

    parsed = json.loads(patched_text)
    target_ids = {repair.sub_id for repair in REPAIRS}
    by_sub_id = {
        int(obj.get("subId") or 0): obj
        for obj in parsed
        if isinstance(obj, dict) and int(obj.get("subId") or 0) in target_ids
    }
    for repair in REPAIRS:
        probe = by_sub_id.get(repair.sub_id)
        if probe is None:
            raise SystemExit(f"Quest {repair.sub_id} disappeared after patch")
        if normalize_accept(probe.get("acceptCond")) != normalized_variant(repair.expected_accept):
            raise SystemExit(f"Quest {repair.sub_id} failed post-write acceptCond validation")
        if repair.expected_comb is not None and probe.get("acceptCondComb") != repair.expected_comb:
            raise SystemExit(f"Quest {repair.sub_id} failed post-write logic validation")

    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(patched_text, encoding="utf-8", newline="")
    os.replace(tmp, path)
    print(f"Updated: {path}")
    print(f"Repaired quest rows: {len(replacements)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
