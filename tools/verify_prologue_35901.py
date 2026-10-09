#!/usr/bin/env python3
"""Verify 7.1 Mondstadt's quest storm and its WeatherExcel gadget identity.

The 35901 begin action is independently reviewed historical compatibility,
not an ordinary 7.1 native full Quest beginExec.
"""
import json
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    quest = next(q for q in load("BinOutput/Quest/359.json")["subQuests"]
                 if q["subId"] == 35901)
    start = {"type": "QUEST_EXEC_SET_WEATHER_GADGET", "param": ["3", "1"]}
    stop3 = {"type": "QUEST_EXEC_SET_WEATHER_GADGET", "param": ["3", "0"]}
    stop1 = {"type": "QUEST_EXEC_SET_WEATHER_GADGET", "param": ["1", "0"]}
    assert quest.get("beginExec") == [start], "35901 storm activation missing"
    assert quest.get("finishExec") == [stop3, stop1], "35901 weather cleanup changed"

    excel = {r.get("subId"): r for r in load("ExcelBinOutput/QuestExcelConfigData.json")
             if isinstance(r, dict)}
    flat_actions = [a for a in excel[35901].get("beginExec", []) if a.get("type")]
    assert not flat_actions or start in flat_actions, (
        "Populated QuestExcel 35901 beginExec would mask the BinOutput storm activation")
    weather = {r["areaID"]: r for r in load("ExcelBinOutput/WeatherExcelConfigData.json")
               if "areaID" in r}
    for area, gadget in ((3, 70020003), (1, 70020001)):
        row = weather[area]
        assert row["sceneID"] == 3 and row["gadgetID"] == gadget, (
            f"Unexpected 7.1 WeatherExcel mapping for area {area}")
    print("PASS 35901 weather activation, cleanup, and client gadget mapping")


if __name__ == "__main__":
    main()
