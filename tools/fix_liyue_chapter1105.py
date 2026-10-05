#!/usr/bin/env python3
from __future__ import annotations

import fix_liyue_chapter1103  # noqa: F401 - extends the shared manifest on import
import fix_liyue_prerequisites as base
from fix_quest_prerequisites import Repair, one

QUEST_GLOBAL_VAR_EQUAL = "QUEST_COND_QUEST_GLOBAL_VAR_EQUAL"


def quest_global_var_equal(var_id: int, value: int) -> tuple[dict, ...]:
    return (
        {
            "type": QUEST_GLOBAL_VAR_EQUAL,
            "param": [var_id, value, 0, 0, 0],
            "param_str": "",
        },
    )


# Chapter 1105 / MQ18000 prerequisite repairs.
#
# Evidence:
# - GCResource 3.7 and 4.0 BinOutput/Quest/18000.json are byte-identical.
# - Both historical references contain the same 29 subquests and prerequisite graph.
# - Current 7.1 BinOutput retains the same 29 subquests but has lost acceptCond for all 29.
# - Current flattened QuestExcel keeps 23 historical edges by coincidence and corrupts exactly six:
#   1800001, 1800008, 1800013, 1800014, 1800015 and 1800029.
CHAPTER_1105_REPAIRS = (
    Repair("18000.json", 18000, 1800001, -1, quest_global_var_equal(10006, 1), (one(0),)),
    Repair("18000.json", 18000, 1800002, -1, one(1800001), ()),
    Repair("18000.json", 18000, 1800003, -1, one(1800002), ()),
    Repair("18000.json", 18000, 1800004, -1, one(1800003), ()),
    Repair("18000.json", 18000, 1800005, -1, one(1800004), ()),
    Repair("18000.json", 18000, 1800006, -1, one(1800005), ()),
    Repair("18000.json", 18000, 1800007, -1, one(1800006), ()),
    Repair("18000.json", 18000, 1800008, -1, one(1800007), (one(0),)),
    Repair("18000.json", 18000, 1800009, -1, one(1800008), ()),
    Repair("18000.json", 18000, 1800010, -1, one(1800009), ()),
    Repair("18000.json", 18000, 1800011, -1, one(1800021), ()),
    Repair("18000.json", 18000, 1800012, -1, one(1800028), ()),
    Repair("18000.json", 18000, 1800013, -1, one(1800028), (one(1800012),)),
    Repair("18000.json", 18000, 1800014, -1, one(1800028), (one(1800013),)),
    Repair("18000.json", 18000, 1800015, -1, one(1800028), (one(1800014),)),
    Repair("18000.json", 18000, 1800016, -1, one(1800015), ()),
    Repair("18000.json", 18000, 1800017, -1, one(1800016), ()),
    Repair("18000.json", 18000, 1800018, -1, one(1800010), ()),
    Repair("18000.json", 18000, 1800019, -1, one(1800017), ()),
    Repair("18000.json", 18000, 1800020, -1, one(1800026), ()),
    Repair("18000.json", 18000, 1800021, -1, one(1800018), ()),
    Repair("18000.json", 18000, 1800022, -1, one(1800019), ()),
    Repair("18000.json", 18000, 1800023, -1, one(1800022), ()),
    Repair("18000.json", 18000, 1800024, -1, one(1800023), ()),
    Repair("18000.json", 18000, 1800025, -1, one(1800024), ()),
    Repair("18000.json", 18000, 1800026, -1, one(1800025), ()),
    Repair("18000.json", 18000, 1800027, -1, one(1800020), ()),
    Repair("18000.json", 18000, 1800028, -1, one(1800011), ()),
    Repair("18000.json", 18000, 1800029, -1, one(99902), (one(1800027),)),
)

base.REPAIRS += CHAPTER_1105_REPAIRS


if __name__ == "__main__":
    raise SystemExit(base.main())
