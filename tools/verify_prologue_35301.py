#!/usr/bin/env python3
"""Protect Genshin 7.1's wind-element tutorial from the spurious 35301 Amber grant.

Sources: original pre-c98b896710 7.1 BinOutput Quest 353, and
TomyJan/GCResource 3700/4000 (identical 35301 finish-exec semantics).
"""
import json
from pathlib import Path


def quest(main_id, sub_id):
    data = json.loads(Path(f"BinOutput/Quest/{main_id}.json").read_text(encoding="utf-8"))
    matches = [r for r in data["subQuests"] if r["subId"] == sub_id]
    assert len(matches) == 1, (main_id, sub_id)
    return matches[0]


def assert_no_trial(row, source):
    for exec_param in row.get("finishExec", []):
        assert exec_param.get("type") != "QUEST_EXEC_GRANT_TRIAL_AVATAR", (
            f"{source} contains premature trial grant: {exec_param}"
        )


def main():
    first = quest(353, 35301)
    assert_no_trial(first, "BinOutput/Quest/353.json#35301")
    assert {"type": "QUEST_EXEC_REFRESH_GROUP_SUITE", "param": ["3", "133003002,1"]} in first.get("beginExec", [])
    skills = quest(353, 35302)
    assert {"type": "QUEST_EXEC_REFRESH_GROUP_SUITE", "param": ["3", "133003002,2"]} in skills.get("beginExec", [])
    amber = quest(354, 35401)
    assert any(c.get("type") == "QUEST_COND_STATE_EQUAL" and c.get("param", [])[:2] == [35505, 3] for c in amber.get("acceptCond", []))
    amber_dialogue = quest(354, 35402)
    assert amber_dialogue.get("gainItems") == [{"itemId": 1021, "count": 1}], (
        "Native 35402 must grant permanent Amber item 1021 after the encounter"
    )

    floating_target = quest(354, 35404)
    assert floating_target.get("beginExec") == [
        {"param": ["3", "133003439"], "type": "QUEST_EXEC_NOTIFY_GROUP_LUA"}
    ], "35404 must notify scene group 133003439 when Amber's bow tutorial starts"

    group_lua = Path("Scripts/Scene/3/scene3_group133003439.lua").read_text(encoding="utf-8")
    assert 'source = "35404"' in group_lua
    assert 'ScriptLib.CreateGroupTimerEvent(context, 133003439, "born", 1)' in group_lua
    assert 'ScriptLib.CreateGadget(context, { config_id = 3834 })' in group_lua
    assert 'ScriptLib.AddQuestProgress(context, "133003079")' in group_lua

    excel_path = Path("ExcelBinOutput/QuestExcelConfigData.json")
    if excel_path.is_file():
        excel = json.loads(excel_path.read_text(encoding="utf-8"))
        matches = [r for r in excel if r.get("subId") == 35301]
        assert len(matches) == 1, f"QuestExcel 35301 count: {len(matches)}"
        assert_no_trial(matches[0], "QuestExcelConfigData.json#35301")

    print("PASS: 35301 no early Amber, 35302 slime suite, 35401 after forest, 35402 Amber reward, 35404 scripted moving target")


if __name__ == "__main__":
    main()
