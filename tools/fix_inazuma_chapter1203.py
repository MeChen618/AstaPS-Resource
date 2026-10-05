#!/usr/bin/env python3
from __future__ import annotations

import fix_inazuma_chapter1202  # noqa: F401 - extends the shared manifest on import
import fix_liyue_prerequisites as base
from fix_quest_prerequisites import Repair, one

ITEM_GIVING_FINISHED = "QUEST_COND_ITEM_GIVING_FINISHED"
QUEST_VAR_EQUAL = "QUEST_COND_QUEST_VAR_EQUAL"


def condition(kind: str, params: list[int]) -> dict:
    return {"type": kind, "param": params, "param_str": ""}


def item_giving_finished(quest_id: int, giving_id: int) -> tuple[dict, ...]:
    return (condition(ITEM_GIVING_FINISHED, [quest_id, giving_id, 0, 0, 0]),)


def quest_var_equal(var_id: int, value: int, quest_id: int) -> tuple[dict, ...]:
    return (condition(QUEST_VAR_EQUAL, [var_id, value, quest_id, 0, 0]),)


# Inazuma Chapter 1203 prerequisite repairs.
#
# Evidence:
# - GCResource 3.7 and 4.0 are byte-identical for MQ2008 and MQ2009.
# - Current 7.1 BinOutput keeps the same 39 subquests but has lost acceptCond on all 39.
# - Current flattened QuestExcel keeps 26 historical prerequisite rows intact and damages exactly 13.
# - 200917 also has an explicit LOGIC_AND -> LOGIC_OR combiner drift; damaged_comb keeps this
#   rewrite strict and scoped to that one known shape.
CHAPTER_1203_REPAIRS = (
    # MQ2008
    Repair("2008.json", 2008, 200801, -1, one(200806), ()),
    Repair("2008.json", 2008, 200802, -1, one(200801), ()),
    Repair("2008.json", 2008, 200803, -1, one(200802), ()),
    Repair("2008.json", 2008, 200804, -1, one(200803), ()),
    Repair(
        "2008.json",
        2008,
        200805,
        -1,
        one(1201309) + one(1200804),
        (one(200807),),
        expected_comb="LOGIC_AND",
    ),
    Repair("2008.json", 2008, 200806, -1, one(200805), ()),
    Repair("2008.json", 2008, 200807, -1, one(200711), (one(0),)),
    Repair("2008.json", 2008, 200808, -1, one(200804), ()),

    # MQ2009
    Repair("2009.json", 2009, 200901, -1, one(200808), (one(0),)),
    Repair("2009.json", 2009, 200902, -1, one(200922), ()),
    Repair("2009.json", 2009, 200903, -1, one(200902), ()),
    Repair("2009.json", 2009, 200904, -1, one(200912), (one(200925),)),
    Repair("2009.json", 2009, 200905, -1, one(200926), ()),
    Repair("2009.json", 2009, 200906, -1, one(200905), ()),
    Repair("2009.json", 2009, 200907, -1, one(200906), ()),
    Repair("2009.json", 2009, 200908, -1, one(200930), (one(200931),)),
    Repair("2009.json", 2009, 200909, -1, one(200910), ()),
    Repair("2009.json", 2009, 200910, -1, one(200901), ()),
    Repair("2009.json", 2009, 200911, -1, one(200919), ()),
    Repair("2009.json", 2009, 200912, -1, one(200913), ()),
    Repair("2009.json", 2009, 200913, -1, one(200911), ()),
    Repair("2009.json", 2009, 200914, -1, one(200903), ()),
    Repair("2009.json", 2009, 200915, -1, one(200914), ()),
    Repair(
        "2009.json",
        2009,
        200916,
        -1,
        one(200914) + item_giving_finished(200915, 20091501),
        (one(200915),),
        expected_comb="LOGIC_AND",
    ),
    Repair(
        "2009.json",
        2009,
        200917,
        -1,
        one(200916) + one(200920),
        (one(200920),),
        expected_comb="LOGIC_OR",
        damaged_comb=("LOGIC_AND",),
    ),
    Repair(
        "2009.json",
        2009,
        200918,
        -1,
        quest_var_equal(1, 1, 200918),
        (one(200924),),
    ),
    Repair("2009.json", 2009, 200919, -1, one(200918), (one(200923),)),
    Repair(
        "2009.json",
        2009,
        200920,
        -1,
        one(200914) + item_giving_finished(200915, 20091502),
        (one(200916),),
        expected_comb="LOGIC_AND",
    ),
    Repair("2009.json", 2009, 200921, -1, one(200909), ()),
    Repair("2009.json", 2009, 200922, -1, one(200921), ()),
    Repair("2009.json", 2009, 200923, -1, one(200918, state=4), (one(200918),)),
    Repair(
        "2009.json",
        2009,
        200924,
        -1,
        quest_var_equal(2, 1, 200924),
        (one(200917),),
    ),
    Repair("2009.json", 2009, 200925, -1, one(99902), (one(200912),)),
    Repair("2009.json", 2009, 200926, -1, one(200904), ()),
    Repair("2009.json", 2009, 200927, -1, one(200907), ()),
    Repair("2009.json", 2009, 200928, -1, one(200927), ()),
    Repair("2009.json", 2009, 200929, -1, one(200928), ()),
    Repair("2009.json", 2009, 200930, -1, one(200929), ()),
    Repair("2009.json", 2009, 200931, -1, one(200930), ()),
)

base.REPAIRS += CHAPTER_1203_REPAIRS


if __name__ == "__main__":
    raise SystemExit(base.main())
