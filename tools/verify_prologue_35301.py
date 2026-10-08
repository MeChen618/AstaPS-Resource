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

    excel_path = Path("ExcelBinOutput/QuestExcelConfigData.json")
    if excel_path.is_file():
        excel = json.loads(excel_path.read_text(encoding="utf-8"))
        matches = [r for r in excel if r.get("subId") == 35301]
        assert len(matches) == 1, f"QuestExcel 35301 count: {len(matches)}"
        assert_no_trial(matches[0], "QuestExcelConfigData.json#35301")

    print("PASS: 35301 no early Amber, 35302 slime suite, 35401 after forest")


if __name__ == "__main__":
    main()
