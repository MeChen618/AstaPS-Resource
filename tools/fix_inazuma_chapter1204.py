#!/usr/bin/env python3
from __future__ import annotations

import fix_inazuma_chapter1203  # noqa: F401 - extends the shared manifest on import
import fix_liyue_prerequisites as base
from fix_quest_prerequisites import Repair, one

QUEST_GLOBAL_VAR_EQUAL = "QUEST_COND_QUEST_GLOBAL_VAR_EQUAL"


def global_var_equal(var_id: int, value: int) -> tuple[dict, ...]:
    return ({"type": QUEST_GLOBAL_VAR_EQUAL, "param": [var_id, value, 0, 0, 0], "param_str": ""},)


# Inazuma Chapter 1204 prerequisite repairs.
# Evidence: GCResource 3.7 + 4.0 byte-identical for MQ2010, 2014-2021;
# current 7.1 BinOutput lost acceptCond on all 83 rows; flattened QuestExcel damages exactly 23.
CHAPTER_1204_REPAIRS = (
    # MQ2010
    Repair("2010.json", 2010, 201001, -1, global_var_equal(10012, 1), (one(0),)),
    Repair("2010.json", 2010, 201002, -1, one(201001), ()),
    Repair("2010.json", 2010, 201003, -1, one(201002), ()),
    Repair("2010.json", 2010, 201004, -1, one(201003), ()),
    Repair("2010.json", 2010, 201005, -1, one(201004), ()),
    Repair("2010.json", 2010, 201006, -1, one(201005), ()),
    Repair("2010.json", 2010, 201007, -1, one(201013), (one(201017),)),
    Repair("2010.json", 2010, 201008, -1, one(201016), (one(201018),)),
    Repair("2010.json", 2010, 201009, -1, one(201011), ()),
    Repair("2010.json", 2010, 201010, -1, one(201014), ()),
    Repair("2010.json", 2010, 201011, -1, one(201015), ()),
    Repair("2010.json", 2010, 201012, -1, one(201006), ()),
    Repair("2010.json", 2010, 201013, -1, one(201012), ()),
    Repair("2010.json", 2010, 201014, -1, one(201007), ()),
    Repair("2010.json", 2010, 201015, -1, one(201008), ()),
    Repair("2010.json", 2010, 201016, -1, one(201010), ()),
    Repair("2010.json", 2010, 201017, -1, one(201006), (one(201013),)),
    Repair("2010.json", 2010, 201018, -1, one(201010), (one(201016),)),

    # MQ2014
    Repair("2014.json", 2014, 201401, -1, one(201009), (one(0),)),
    Repair("2014.json", 2014, 201402, -1, one(99902), (one(201401),)),
    Repair("2014.json", 2014, 201403, -1, one(201401), (one(201402),)),
    Repair("2014.json", 2014, 201404, -1, one(201403), ()),
    Repair("2014.json", 2014, 201405, -1, one(201404), ()),
    Repair("2014.json", 2014, 201406, -1, one(201405), ()),
    Repair("2014.json", 2014, 201407, -1, one(201406), ()),
    Repair("2014.json", 2014, 201408, -1, one(201407), ()),

    # MQ2015
    Repair("2015.json", 2015, 201501, -1, one(201408), (one(0),)),
    Repair("2015.json", 2015, 201502, -1, one(201501), ()),
    Repair("2015.json", 2015, 201503, -1, one(201502), ()),
    Repair("2015.json", 2015, 201504, -1, one(201503), ()),
    Repair("2015.json", 2015, 201505, -1, one(201504), ()),

    # MQ2016
    Repair("2016.json", 2016, 201601, -1, one(201505), (one(0),)),
    Repair("2016.json", 2016, 201602, -1, one(201608), ()),
    Repair("2016.json", 2016, 201603, -1, one(201607), ()),
    Repair("2016.json", 2016, 201604, -1, one(201603), ()),
    Repair("2016.json", 2016, 201605, -1, one(201604), ()),
    Repair("2016.json", 2016, 201606, -1, one(201601), ()),
    Repair("2016.json", 2016, 201607, -1, one(201602), ()),
    Repair("2016.json", 2016, 201608, -1, one(201606), ()),
    Repair("2016.json", 2016, 201609, -1, one(201605), ()),

    # MQ2017
    Repair("2017.json", 2017, 201701, -1, one(201609), (one(0),)),
    Repair("2017.json", 2017, 201702, -1, one(201701), ()),
    Repair("2017.json", 2017, 201703, -1, one(201702), (one(201712),)),
    Repair("2017.json", 2017, 201704, -1, one(201703), ()),
    Repair("2017.json", 2017, 201705, -1, one(201710), ()),
    Repair("2017.json", 2017, 201706, -1, one(201705), ()),
    Repair("2017.json", 2017, 201707, -1, one(201706), ()),
    Repair("2017.json", 2017, 201708, -1, one(201707), ()),
    Repair("2017.json", 2017, 201709, -1, one(201715), (one(201713),)),
    Repair("2017.json", 2017, 201710, -1, one(201704), ()),
    Repair("2017.json", 2017, 201711, -1, one(201714), ()),
    Repair("2017.json", 2017, 201712, -1, one(201701), (one(201702),)),
    Repair("2017.json", 2017, 201713, -1, one(201711, state=4), (one(201715),)),
    Repair("2017.json", 2017, 201714, -1, one(201708), (one(201716),)),
    Repair("2017.json", 2017, 201715, -1, one(201711), ()),
    Repair("2017.json", 2017, 201716, -1, one(201708), ()),

    # MQ2018
    Repair("2018.json", 2018, 201801, -1, one(99902), (one(0),)),
    Repair("2018.json", 2018, 201802, -1, one(201709), (one(201801),)),
    Repair("2018.json", 2018, 201803, -1, one(201802), ()),
    Repair("2018.json", 2018, 201804, -1, one(201807), ()),
    Repair("2018.json", 2018, 201805, -1, one(201803), ()),
    Repair("2018.json", 2018, 201806, -1, one(201805), ()),
    Repair("2018.json", 2018, 201807, -1, one(201806), ()),

    # MQ2019
    Repair("2019.json", 2019, 201901, -1, one(201905), ()),
    Repair("2019.json", 2019, 201902, -1, one(201901), ()),
    Repair("2019.json", 2019, 201903, -1, one(201902), ()),
    Repair("2019.json", 2019, 201904, -1, one(201903), ()),
    Repair("2019.json", 2019, 201905, -1, one(201804), (one(0),)),

    # MQ2020
    Repair("2020.json", 2020, 202001, -1, one(201904), (one(0),)),
    Repair("2020.json", 2020, 202002, -1, one(202009), ()),
    Repair("2020.json", 2020, 202003, -1, one(202013), ()),
    Repair("2020.json", 2020, 202004, -1, one(202003), ()),
    Repair("2020.json", 2020, 202005, -1, one(202011), ()),
    Repair("2020.json", 2020, 202006, -1, one(202005), ()),
    Repair("2020.json", 2020, 202007, -1, one(201904), (one(202001),)),
    Repair("2020.json", 2020, 202008, -1, one(202007), ()),
    Repair("2020.json", 2020, 202009, -1, one(202008), ()),
    Repair("2020.json", 2020, 202010, -1, one(202004), ()),
    Repair("2020.json", 2020, 202011, -1, one(202010), ()),
    Repair("2020.json", 2020, 202012, -1, one(202006), ()),
    Repair("2020.json", 2020, 202013, -1, one(202002), ()),

    # MQ2021
    Repair("2021.json", 2021, 202101, -1, one(99902), (one(0),)),
    Repair("2021.json", 2021, 202102, -1, one(202012), (one(202101),)),
)

base.REPAIRS += CHAPTER_1204_REPAIRS


if __name__ == "__main__":
    raise SystemExit(base.main())
