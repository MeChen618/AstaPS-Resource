-- Compatibility scene adapter for Amber 42705, not a recovered native 7.1 group.
-- Route, 3-unit coin triggers, batch order and 60-second limit: animepython
-- aebc1c39019698224c4d18c01e88f60c95da3a19 SQ427.lua / Q427ClientConfig.lua / Q427FlyCoins*.lua.
local GROUP = 133004149
local QUEST = 42705
local REGION_BASE = 149200
local LOCAL_ID = 149
local TOTAL = 21
local batch_starts = {1, 4, 6, 10, 13, 17, 19}
local batch_ends = {3, 5, 9, 12, 16, 18, 21}
monsters = {

}
npcs = {

}
gadgets = {
    { config_id = 149001, gadget_id = 70690001, pos = { x = 2242.820000, y = 260.213000, z = -788.297000 }, rot = { x = 13.392389, y = -161.948222, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149002, gadget_id = 70690001, pos = { x = 2240.231333, y = 258.224000, z = -796.239667 }, rot = { x = 13.392389, y = -161.948222, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149003, gadget_id = 70690001, pos = { x = 2237.642667, y = 256.235000, z = -804.182333 }, rot = { x = 13.392389, y = -161.948222, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149011, gadget_id = 70710005, pos = { x = 2239.206000, y = 221.000000, z = -847.710000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149012, gadget_id = 70710005, pos = { x = 2239.682000, y = 235.000000, z = -826.538000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149013, gadget_id = 70710005, pos = { x = 2195.404000, y = 214.531000, z = -866.669000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149014, gadget_id = 70710005, pos = { x = 2224.858000, y = 221.000000, z = -865.054000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149101, gadget_id = 70300064, pos = { x = 2232.298000, y = 253.315000, z = -820.584000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149102, gadget_id = 70300064, pos = { x = 2229.016000, y = 252.319000, z = -824.422000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149103, gadget_id = 70300064, pos = { x = 2225.276000, y = 251.140000, z = -827.959000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149104, gadget_id = 70300064, pos = { x = 2222.028000, y = 249.179000, z = -833.803000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149105, gadget_id = 70300064, pos = { x = 2223.559000, y = 248.134000, z = -836.678000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149106, gadget_id = 70300064, pos = { x = 2228.854000, y = 244.497000, z = -841.359000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149107, gadget_id = 70300064, pos = { x = 2231.335000, y = 244.027000, z = -841.795000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149108, gadget_id = 70300064, pos = { x = 2235.120000, y = 244.500000, z = -845.000000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149109, gadget_id = 70300064, pos = { x = 2235.000000, y = 242.500000, z = -844.300000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149110, gadget_id = 70300064, pos = { x = 2234.260000, y = 241.427000, z = -862.830000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149111, gadget_id = 70300064, pos = { x = 2230.800000, y = 241.151000, z = -865.563000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149112, gadget_id = 70300064, pos = { x = 2227.303000, y = 241.800000, z = -866.519000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149113, gadget_id = 70300064, pos = { x = 2213.384000, y = 243.260000, z = -867.564000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149114, gadget_id = 70300064, pos = { x = 2207.574000, y = 242.798000, z = -867.082000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149115, gadget_id = 70300064, pos = { x = 2210.120000, y = 243.014000, z = -867.943000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149116, gadget_id = 70300064, pos = { x = 2204.820000, y = 241.341000, z = -866.804000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149117, gadget_id = 70300064, pos = { x = 2192.720000, y = 239.979000, z = -862.390000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149118, gadget_id = 70300064, pos = { x = 2193.000000, y = 240.031000, z = -860.000000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149119, gadget_id = 70300064, pos = { x = 2192.129000, y = 237.901000, z = -851.557000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149120, gadget_id = 70300064, pos = { x = 2191.552000, y = 236.993000, z = -848.833000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 149121, gadget_id = 70300064, pos = { x = 2190.569000, y = 236.074000, z = -846.600000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
}
regions = {
    { config_id = 149200, shape = RegionShape.SPHERE, radius = 12, pos = { x = 2243.797000, y = 258.259000, z = -773.534000 } },
    { config_id = 149201, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2232.298000, y = 253.315000, z = -820.584000 } },
    { config_id = 149202, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2229.016000, y = 252.319000, z = -824.422000 } },
    { config_id = 149203, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2225.276000, y = 251.140000, z = -827.959000 } },
    { config_id = 149204, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2222.028000, y = 249.179000, z = -833.803000 } },
    { config_id = 149205, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2223.559000, y = 248.134000, z = -836.678000 } },
    { config_id = 149206, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2228.854000, y = 244.497000, z = -841.359000 } },
    { config_id = 149207, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2231.335000, y = 244.027000, z = -841.795000 } },
    { config_id = 149208, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2235.120000, y = 244.500000, z = -845.000000 } },
    { config_id = 149209, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2235.000000, y = 242.500000, z = -844.300000 } },
    { config_id = 149210, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2234.260000, y = 241.427000, z = -862.830000 } },
    { config_id = 149211, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2230.800000, y = 241.151000, z = -865.563000 } },
    { config_id = 149212, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2227.303000, y = 241.800000, z = -866.519000 } },
    { config_id = 149213, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2213.384000, y = 243.260000, z = -867.564000 } },
    { config_id = 149214, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2207.574000, y = 242.798000, z = -867.082000 } },
    { config_id = 149215, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2210.120000, y = 243.014000, z = -867.943000 } },
    { config_id = 149216, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2204.820000, y = 241.341000, z = -866.804000 } },
    { config_id = 149217, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2192.720000, y = 239.979000, z = -862.390000 } },
    { config_id = 149218, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2193.000000, y = 240.031000, z = -860.000000 } },
    { config_id = 149219, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2192.129000, y = 237.901000, z = -851.557000 } },
    { config_id = 149220, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2191.552000, y = 236.993000, z = -848.833000 } },
    { config_id = 149221, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2190.569000, y = 236.074000, z = -846.600000 } },
}
triggers = {
    { config_id = 149300, name = "ENTER_REGION_149200", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_start", action = "start_exam", trigger_count = 0 },
    { config_id = 149301, name = "CHALLENGE_SUCCESS_149301", event = EventType.EVENT_CHALLENGE_SUCCESS, source = "149", condition = "is_exam_active", action = "exam_success", trigger_count = 0 },
    { config_id = 149302, name = "CHALLENGE_FAIL_149302", event = EventType.EVENT_CHALLENGE_FAIL, source = "149", condition = "is_exam_active", action = "exam_failure", trigger_count = 0 },
    { config_id = 149311, name = "ENTER_REGION_149201", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149312, name = "ENTER_REGION_149202", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149313, name = "ENTER_REGION_149203", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149314, name = "ENTER_REGION_149204", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149315, name = "ENTER_REGION_149205", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149316, name = "ENTER_REGION_149206", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149317, name = "ENTER_REGION_149207", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149318, name = "ENTER_REGION_149208", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149319, name = "ENTER_REGION_149209", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149320, name = "ENTER_REGION_149210", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149321, name = "ENTER_REGION_149211", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149322, name = "ENTER_REGION_149212", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149323, name = "ENTER_REGION_149213", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149324, name = "ENTER_REGION_149214", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149325, name = "ENTER_REGION_149215", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149326, name = "ENTER_REGION_149216", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149327, name = "ENTER_REGION_149217", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149328, name = "ENTER_REGION_149218", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149329, name = "ENTER_REGION_149219", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149330, name = "ENTER_REGION_149220", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
    { config_id = 149331, name = "ENTER_REGION_149221", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "149", trigger_count = 0 },
}
variables = {
    { config_id = 1, name = "started", value = 0, no_refresh = false },
    { config_id = 2, name = "batch", value = 1, no_refresh = false },
    { config_id = 3, name = "batch_count", value = 0, no_refresh = false },
    { config_id = 4, name = "transition", value = 0, no_refresh = false },
    { config_id = 5, name = "seen_1", value = 0, no_refresh = false },
    { config_id = 6, name = "seen_2", value = 0, no_refresh = false },
    { config_id = 7, name = "seen_3", value = 0, no_refresh = false },
    { config_id = 8, name = "seen_4", value = 0, no_refresh = false },
    { config_id = 9, name = "seen_5", value = 0, no_refresh = false },
    { config_id = 10, name = "seen_6", value = 0, no_refresh = false },
    { config_id = 11, name = "seen_7", value = 0, no_refresh = false },
    { config_id = 12, name = "seen_8", value = 0, no_refresh = false },
    { config_id = 13, name = "seen_9", value = 0, no_refresh = false },
    { config_id = 14, name = "seen_10", value = 0, no_refresh = false },
    { config_id = 15, name = "seen_11", value = 0, no_refresh = false },
    { config_id = 16, name = "seen_12", value = 0, no_refresh = false },
    { config_id = 17, name = "seen_13", value = 0, no_refresh = false },
    { config_id = 18, name = "seen_14", value = 0, no_refresh = false },
    { config_id = 19, name = "seen_15", value = 0, no_refresh = false },
    { config_id = 20, name = "seen_16", value = 0, no_refresh = false },
    { config_id = 21, name = "seen_17", value = 0, no_refresh = false },
    { config_id = 22, name = "seen_18", value = 0, no_refresh = false },
    { config_id = 23, name = "seen_19", value = 0, no_refresh = false },
    { config_id = 24, name = "seen_20", value = 0, no_refresh = false },
    { config_id = 25, name = "seen_21", value = 0, no_refresh = false },
}
init_config = { suite = 1, end_suite = 0, rand_suite = false }
suites = {
    { monsters = {}, gadgets = {}, regions = {149200}, triggers = {"ENTER_REGION_149200", "CHALLENGE_SUCCESS_149301", "CHALLENGE_FAIL_149302"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149001, 149002, 149003, 149011, 149012, 149013, 149014}, regions = {}, triggers = {}, rand_weight = 100 },
    { monsters = {}, gadgets = {149101}, regions = {149201}, triggers = {"ENTER_REGION_149201"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149102}, regions = {149202}, triggers = {"ENTER_REGION_149202"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149103}, regions = {149203}, triggers = {"ENTER_REGION_149203"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149104}, regions = {149204}, triggers = {"ENTER_REGION_149204"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149105}, regions = {149205}, triggers = {"ENTER_REGION_149205"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149106}, regions = {149206}, triggers = {"ENTER_REGION_149206"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149107}, regions = {149207}, triggers = {"ENTER_REGION_149207"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149108}, regions = {149208}, triggers = {"ENTER_REGION_149208"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149109}, regions = {149209}, triggers = {"ENTER_REGION_149209"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149110}, regions = {149210}, triggers = {"ENTER_REGION_149210"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149111}, regions = {149211}, triggers = {"ENTER_REGION_149211"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149112}, regions = {149212}, triggers = {"ENTER_REGION_149212"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149113}, regions = {149213}, triggers = {"ENTER_REGION_149213"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149114}, regions = {149214}, triggers = {"ENTER_REGION_149214"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149115}, regions = {149215}, triggers = {"ENTER_REGION_149215"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149116}, regions = {149216}, triggers = {"ENTER_REGION_149216"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149117}, regions = {149217}, triggers = {"ENTER_REGION_149217"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149118}, regions = {149218}, triggers = {"ENTER_REGION_149218"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149119}, regions = {149219}, triggers = {"ENTER_REGION_149219"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149120}, regions = {149220}, triggers = {"ENTER_REGION_149220"}, rand_weight = 100 },
    { monsters = {}, gadgets = {149121}, regions = {149221}, triggers = {"ENTER_REGION_149221"}, rand_weight = 100 },
}

function is_exam_active(context, evt)
    return ScriptLib.GetQuestState(context, 0, QUEST) == 2
        and ScriptLib.GetGroupVariableValue(context, "started") == 1
end

function show_batch(context, batch)
    if batch_starts[batch] == nil then return end
    for index = batch_starts[batch], batch_ends[batch] do
        ScriptLib.AddExtraGroupSuite(context, GROUP, index + 2)
    end
end

function can_start(context, evt)
    return evt.param1 == REGION_BASE and ScriptLib.GetQuestState(context, 0, QUEST) == 2
        and ScriptLib.GetGroupVariableValue(context, "started") == 0
        and ScriptLib.GetRegionEntityCount(context, { region_eid = evt.source_eid, entity_type = EntityType.AVATAR }) > 0
end

function start_exam(context, evt)
    if ScriptLib.ActiveChallenge(context, LOCAL_ID, 295, 60, GROUP, LOCAL_ID, TOTAL) ~= 0 then return 0 end
    ScriptLib.SetGroupVariableValue(context, "started", 1)
    ScriptLib.SetGroupVariableValue(context, "batch", 1)
    ScriptLib.SetGroupVariableValue(context, "batch_count", 0)
    ScriptLib.SetGroupVariableValue(context, "transition", 0)
    for index = 1, TOTAL do ScriptLib.SetGroupVariableValue(context, "seen_" .. index, 0) end
    ScriptLib.AddExtraGroupSuite(context, GROUP, 2)
    show_batch(context, 1)
    return 0
end

function can_collect_coin(context, evt)
    if not is_exam_active(context, evt) then return false end
    local index = evt.param1 - REGION_BASE
    local batch = ScriptLib.GetGroupVariableValue(context, "batch")
    return batch_starts[batch] ~= nil and index >= batch_starts[batch] and index <= batch_ends[batch]
        and ScriptLib.GetGroupVariableValue(context, "seen_" .. index) == 0
        and ScriptLib.GetRegionEntityCount(context, { region_eid = evt.source_eid, entity_type = EntityType.AVATAR }) > 0
end

function collect_coin(context, evt)
    local index = evt.param1 - REGION_BASE
    local batch = ScriptLib.GetGroupVariableValue(context, "batch")
    local count = ScriptLib.GetGroupVariableValue(context, "batch_count") + 1
    ScriptLib.SetGroupVariableValue(context, "seen_" .. index, 1)
    ScriptLib.RemoveExtraGroupSuite(context, GROUP, index + 2)
    if count == batch_ends[batch] - batch_starts[batch] + 1 then
        ScriptLib.SetGroupVariableValue(context, "batch", batch + 1)
        ScriptLib.SetGroupVariableValue(context, "batch_count", 0)
        show_batch(context, batch + 1)
    else
        ScriptLib.SetGroupVariableValue(context, "batch_count", count)
    end
    return 0
end

function exam_success(context, evt)
    ScriptLib.SetGroupVariableValue(context, "started", 0)
    return ScriptLib.AddQuestProgress(context, "11330041491")
end

function exam_failure(context, evt)
    ScriptLib.SetGroupVariableValue(context, "started", 0)
    return ScriptLib.AddQuestProgress(context, "11330041492")
end
