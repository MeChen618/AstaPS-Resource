#!/usr/bin/env python3
"""Source-reviewed compatibility in the 7.1 Mondstadt Acts I-III.
BinOutput beginExec is historical compatibility data, NOT native 7.1 full Quest.
Excel populated lists remain authoritative; shadowing repairs must fail CI.
"""
import json
from pathlib import Path

EXPECTED = json.loads(r'''{"307":{"30710":{"finishCondComb":"LOGIC_OR"}},"308":{"30810":{"finishCondComb":"LOGIC_OR"},"30814":{"finishCondComb":"LOGIC_OR"}},"309":{"30901":{"finishCondComb":"LOGIC_AND"},"30904":{"beginExec":[{"type":"QUEST_EXEC_ADD_QUEST_PROGRESS","param":["359011","1"]}]}},"372":{"37203":{"gainItems":[{"itemId":100164,"count":1}]}},"373":{"37303":{"beginExec":[{"type":"QUEST_EXEC_REFRESH_GROUP_SUITE","param":["3","133001305,2"]}]}},"376":{"37602":{"failCondComb":"LOGIC_OR"}},"382":{"38201":{"finishCondComb":"LOGIC_OR"},"38202":{"beginExec":[{"type":"QUEST_EXEC_REFRESH_GROUP_SUITE","param":["3","133001249,2"]}]}},"383":{"38303":{"gainItems":[{"itemId":100163,"count":1}]}},"384":{"38406":{"gainItems":[{"itemId":100165,"count":1}]}},"388":{"38802":{"failCondComb":"LOGIC_OR"}},"389":{"38905":{"beginExec":[{"type":"QUEST_EXEC_NOTIFY_GROUP_LUA","param":["3","133007227"]}]}},"390":{"39003":{"beginExec":[{"type":"QUEST_EXEC_NOTIFY_GROUP_LUA","param":["3","133007227"]}]}},"394":{"39401":{"beginExec":[{"type":"QUEST_EXEC_UNLOCK_POINT","param":["3","38"]}]},"39404":{"failCondComb":"LOGIC_OR"}},"396":{"39604":{"beginExec":[{"type":"QUEST_EXEC_REFRESH_GROUP_SUITE","param":["3","133001910,2"]}]}},"397":{"39703":{"beginExec":[{"type":"QUEST_EXEC_REFRESH_GROUP_SUITE","param":["3","133002233,2"]}],"failCondComb":"LOGIC_OR"}},"398":{"39801":{"beginExec":[{"type":"QUEST_EXEC_REFRESH_GROUP_SUITE","param":["3","133003910,2"]}]},"39807":{"finishCondComb":"LOGIC_OR"},"39808":{"beginExec":[{"type":"QUEST_EXEC_REFRESH_GROUP_SUITE","param":["3","133004917,1"]}]},"39812":{"beginExec":[{"type":"QUEST_EXEC_NOTIFY_GROUP_LUA","param":["3","133003910"]}]}},"20101":{"2010101":{"beginExec":[{"type":"QUEST_EXEC_DEL_PACK_ITEM","param":["100175","1"]},{"type":"QUEST_EXEC_REFRESH_GROUP_SUITE","param":["3","133002334,2"]}]},"2010102":{"beginExec":[{"type":"QUEST_EXEC_GRANT_TRIAL_AVATAR","param":["11"]}]},"2010145":{"gainItems":[{"itemId":100175,"count":1}]},"2010146":{"gainItems":[{"itemId":100175,"count":1}]},"2010147":{"gainItems":[{"itemId":100175,"count":1}]},"2010148":{"gainItems":[{"itemId":100175,"count":1}]},"2010149":{"gainItems":[{"itemId":100175,"count":1}]},"2010150":{"gainItems":[{"itemId":100175,"count":1}]},"2010151":{"gainItems":[{"itemId":100175,"count":1}]}}}''')

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def verify():
    flattened = {str(r.get("subId")):r for r in read("ExcelBinOutput/QuestExcelConfigData.json")
                 if isinstance(r, dict)}
    n = 0
    conflicts = []
    for main, tasks in EXPECTED.items():
        subs = {str(r["subId"]):r for r in read(f"BinOutput/Quest/{main}.json")["subQuests"]}
        for sub, fields in tasks.items():
            assert sub in subs and sub in flattened, f"Missing {sub} in quest / Excel"
            for key, value in fields.items():
                actual = subs[sub].get(key)
                assert actual == value, f"{sub}.{key}: expected {value}, got {actual}"
                excel = flattened[sub].get(key)
                if key in ("beginExec","finishExec","failExec","gainItems"):
                    # Match QuestData.effectiveExecList: type-less materialized
                    # entries are placeholders, not executable overrides.
                    # param_str is metadata and is irrelevant to action identity.
                    usable = ([
                        x for x in (excel or [])
                        if isinstance(x, dict) and x.get("type")]
                        if key != "gainItems" else [
                        x for x in (excel or [])
                        if isinstance(x, dict) and x.get("itemId", 0) > 0
                        and x.get("count", 0) > 0])
                    if usable:
                        def matches(want, candidate):
                            keys = ("itemId", "count") if key == "gainItems" else ("type", "param")
                            return all(want.get(k) == candidate.get(k) for k in keys)
                        if not all(any(matches(i, j) for j in usable) for i in value):
                            conflicts.append((sub, key, "BinOutput", value, "QuestExcel", usable))
                elif excel and excel != "LOGIC_NONE":
                    if excel != value:
                        conflicts.append((sub, key, "BinOutput", value, "QuestExcel", excel))
                n += 1
    dungeon = {r["subId"]:r for r in read("BinOutput/Quest/309.json")["subQuests"]}[30901]
    assert [c["param"][0] for c in dungeon["finishCond"]] == [1001,1,1003]
    assert dungeon["finishCondComb"] == "LOGIC_AND"

    # 38402 has no fail condition in exact 7.1 or flattened QuestExcel. A failExec on this row is
    # unreachable in AstaPS and must not be reintroduced as compatibility data.
    q38402 = {r["subId"]:r for r in read("BinOutput/Quest/384.json")["subQuests"]}[38402]
    x38402 = flattened["38402"]
    assert not q38402.get("failExec"), "38402 must not carry a dead failExec"
    assert not x38402.get("failCond"), "38402 flattened QuestExcel unexpectedly gained failCond"
    assert not x38402.get("failExec"), "38402 flattened QuestExcel unexpectedly gained failExec"
    if conflicts:
        for conflict in conflicts:
            print("CONFLICT", repr(conflict))
        raise AssertionError(f"{len(conflicts)} QuestExcel precedence conflict(s)")
    print(f"PASS: {len(EXPECTED)} main quests, {n} reviewed compatibility fields, no Excel masks")

if __name__ == "__main__":
    verify()
