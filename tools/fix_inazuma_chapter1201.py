#!/usr/bin/env python3
from __future__ import annotations

import fix_liyue_chapter1105  # noqa: F401 - extends the shared manifest on import
import fix_liyue_prerequisites as base
from fix_quest_prerequisites import Repair, one

QUEST_GLOBAL_VAR_EQUAL = "QUEST_COND_QUEST_GLOBAL_VAR_EQUAL"
ACTIVITY_END = "QUEST_COND_ACTIVITY_END"


def condition(kind: str, params: list[int]) -> dict:
    return {"type": kind, "param": params, "param_str": ""}


def quest_global_var_equal(var_id: int, value: int) -> dict:
    return condition(QUEST_GLOBAL_VAR_EQUAL, [var_id, value, 0, 0, 0])


def activity_end(activity_id: int) -> dict:
    return condition(ACTIVITY_END, [activity_id, 0, 0, 0, 0])


# Inazuma Chapter 1201 prerequisite repairs.
#
# Evidence:
# - GCResource 3.7 and 4.0 are byte-identical for MQ2000, MQ2001 and MQ2002.
# - Current 7.1 BinOutput keeps the same 39 subquests but has lost acceptCond on all 39.
# - Current flattened QuestExcel has all 39 rows; 30 already match the historical graph and
#   exactly nine rows are damaged. Those nine damaged shapes are listed explicitly below.
CHAPTER_1201_REPAIRS = (
    # MQ2000: pre-Inazuma transition and parallel preparation fan-out.
    Repair(
        "2000.json",
        2000,
        200001,
        -1,
        (quest_global_var_equal(10010, 1), activity_end(2005001)),
        (one(200012),),
        expected_comb="LOGIC_AND",
    ),
    Repair("2000.json", 2000, 200002, -1, one(200001), ()),
    Repair("2000.json", 2000, 200003, -1, one(200002), ()),
    Repair("2000.json", 2000, 200004, -1, one(200003), ()),
    Repair("2000.json", 2000, 200005, -1, one(200011), ()),
    Repair("2000.json", 2000, 200006, -1, one(200011), (one(200005),)),
    Repair("2000.json", 2000, 200007, -1, one(200011), (one(200006),)),
    Repair("2000.json", 2000, 200008, -1, one(200011), (one(200007),)),
    Repair("2000.json", 2000, 200009, -1, one(200011), (one(200008),)),
    Repair("2000.json", 2000, 200010, -1, one(200009), ()),
    Repair("2000.json", 2000, 200011, -1, one(200004), ()),
    Repair(
        "2000.json",
        2000,
        200012,
        -1,
        (quest_global_var_equal(10006, 1),),
        (one(0),),
    ),

    # MQ2001: linear continuation with 200114 inserted between 200102 and 200103.
    Repair("2001.json", 2001, 200101, -1, one(200010), (one(0),)),
    Repair("2001.json", 2001, 200102, -1, one(200101), ()),
    Repair("2001.json", 2001, 200103, -1, one(200114), ()),
    Repair("2001.json", 2001, 200104, -1, one(200103), ()),
    Repair("2001.json", 2001, 200105, -1, one(200104), ()),
    Repair("2001.json", 2001, 200106, -1, one(200105), ()),
    Repair("2001.json", 2001, 200107, -1, one(200106), ()),
    Repair("2001.json", 2001, 200108, -1, one(200107), ()),
    Repair("2001.json", 2001, 200109, -1, one(200108), ()),
    Repair("2001.json", 2001, 200110, -1, one(200109), ()),
    Repair("2001.json", 2001, 200111, -1, one(200110), ()),
    Repair("2001.json", 2001, 200112, -1, one(200111), ()),
    Repair("2001.json", 2001, 200113, -1, one(200112), ()),
    Repair("2001.json", 2001, 200114, -1, one(200102), ()),

    # MQ2002: chapter finale. 200203 fans into both 200204 and hidden/progress node 200213;
    # 200201 follows 200204 and the visible chain then continues to endQuestId 200212.
    Repair("2002.json", 2002, 200201, -1, one(200204), ()),
    Repair("2002.json", 2002, 200202, -1, one(200113), (one(0),)),
    Repair("2002.json", 2002, 200203, -1, one(200202), ()),
    Repair("2002.json", 2002, 200204, -1, one(200203), (one(200213),)),
    Repair("2002.json", 2002, 200205, -1, one(200201), ()),
    Repair("2002.json", 2002, 200206, -1, one(200205), ()),
    Repair("2002.json", 2002, 200207, -1, one(200206), ()),
    Repair("2002.json", 2002, 200208, -1, one(200207), ()),
    Repair("2002.json", 2002, 200209, -1, one(200208), ()),
    Repair("2002.json", 2002, 200210, -1, one(200209), ()),
    Repair("2002.json", 2002, 200211, -1, one(200210), ()),
    Repair("2002.json", 2002, 200212, -1, one(200211), ()),
    Repair("2002.json", 2002, 200213, -1, one(200203), ()),
)

base.REPAIRS += CHAPTER_1201_REPAIRS


if __name__ == "__main__":
    raise SystemExit(base.main())
