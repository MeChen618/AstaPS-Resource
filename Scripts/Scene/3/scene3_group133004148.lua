-- Compatibility scene adapter for Amber 42702, not a recovered native 7.1 group.
-- Route, 3-unit coin triggers, batch order and 60-second limit: animepython
-- aebc1c39019698224c4d18c01e88f60c95da3a19 SQ427.lua / Q427ClientConfig.lua / Q427FlyCoins*.lua.
local GROUP = 133004148
local QUEST = 42702
local REGION_BASE = 148200
local LOCAL_ID = 148
local TOTAL = 12
local batch_starts = {1, 4, 7, 10}
local batch_ends = {3, 6, 9, 12}
monsters = {

}
npcs = {

}
gadgets = {
    { config_id = 148001, gadget_id = 70690001, pos = { x = 2343.912000, y = 261.035000, z = -707.330000 }, rot = { x = -10.365774, y = -134.477037, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148002, gadget_id = 70690001, pos = { x = 2341.000667, y = 261.781333, z = -710.188667 }, rot = { x = -10.365774, y = -134.477037, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148003, gadget_id = 70690001, pos = { x = 2338.089333, y = 262.527667, z = -713.047333 }, rot = { x = -10.365774, y = -134.477037, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148011, gadget_id = 70710005, pos = { x = 2324.086000, y = 249.990000, z = -725.193000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148012, gadget_id = 70710005, pos = { x = 2324.721000, y = 249.990000, z = -766.071000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148013, gadget_id = 70710005, pos = { x = 2305.214000, y = 247.500000, z = -754.774000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148014, gadget_id = 70710005, pos = { x = 2334.201000, y = 249.795000, z = -741.707000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148101, gadget_id = 70300064, pos = { x = 2324.496000, y = 273.073000, z = -736.836000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148102, gadget_id = 70300064, pos = { x = 2326.110000, y = 272.709000, z = -737.245000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148103, gadget_id = 70300064, pos = { x = 2326.689000, y = 271.877000, z = -736.407000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148104, gadget_id = 70300064, pos = { x = 2328.939000, y = 275.053000, z = -743.668000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148105, gadget_id = 70300064, pos = { x = 2326.621000, y = 273.867000, z = -747.599000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148106, gadget_id = 70300064, pos = { x = 2329.212000, y = 270.484000, z = -752.717000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148107, gadget_id = 70300064, pos = { x = 2326.868000, y = 269.095000, z = -758.397000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148108, gadget_id = 70300064, pos = { x = 2328.966000, y = 269.487000, z = -756.797000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148109, gadget_id = 70300064, pos = { x = 2326.249000, y = 267.634000, z = -761.303000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148110, gadget_id = 70300064, pos = { x = 2315.738000, y = 273.940000, z = -762.206000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148111, gadget_id = 70300064, pos = { x = 2312.834000, y = 272.054000, z = -762.722000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148112, gadget_id = 70300064, pos = { x = 2311.524000, y = 271.473000, z = -760.136000 }, rot = { x = 0.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148021, gadget_id = 70690001, pos = { x = 2293.863000, y = 269.684000, z = -754.825000 }, rot = { x = -2.064034, y = -100.154340, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148022, gadget_id = 70690001, pos = { x = 2288.182000, y = 269.892000, z = -755.842500 }, rot = { x = -2.064034, y = -100.154340, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148023, gadget_id = 70690001, pos = { x = 2282.501000, y = 270.100000, z = -756.860000 }, rot = { x = -2.064034, y = -100.154340, z = 0.000000 }, level = 1, area_id = 1 },
    { config_id = 148024, gadget_id = 70690001, pos = { x = 2276.820000, y = 270.308000, z = -757.877500 }, rot = { x = -2.064034, y = -100.154340, z = 0.000000 }, level = 1, area_id = 1 },
}
regions = {
    { config_id = 148200, shape = RegionShape.SPHERE, radius = 12, pos = { x = 2349.575000, y = 260.030000, z = -700.192000 } },
    { config_id = 148201, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2324.496000, y = 273.073000, z = -736.836000 } },
    { config_id = 148202, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2326.110000, y = 272.709000, z = -737.245000 } },
    { config_id = 148203, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2326.689000, y = 271.877000, z = -736.407000 } },
    { config_id = 148204, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2328.939000, y = 275.053000, z = -743.668000 } },
    { config_id = 148205, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2326.621000, y = 273.867000, z = -747.599000 } },
    { config_id = 148206, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2329.212000, y = 270.484000, z = -752.717000 } },
    { config_id = 148207, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2326.868000, y = 269.095000, z = -758.397000 } },
    { config_id = 148208, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2328.966000, y = 269.487000, z = -756.797000 } },
    { config_id = 148209, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2326.249000, y = 267.634000, z = -761.303000 } },
    { config_id = 148210, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2315.738000, y = 273.940000, z = -762.206000 } },
    { config_id = 148211, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2312.834000, y = 272.054000, z = -762.722000 } },
    { config_id = 148212, shape = RegionShape.SPHERE, radius = 3, pos = { x = 2311.524000, y = 271.473000, z = -760.136000 } },
}
triggers = {
    { config_id = 148300, name = "ENTER_REGION_148200", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_start", action = "start_exam", trigger_count = 0 },
    { config_id = 148301, name = "CHALLENGE_SUCCESS_148301", event = EventType.EVENT_CHALLENGE_SUCCESS, source = "148", condition = "is_exam_active", action = "exam_success", trigger_count = 0 },
    { config_id = 148302, name = "CHALLENGE_FAIL_148302", event = EventType.EVENT_CHALLENGE_FAIL, source = "148", condition = "is_exam_active", action = "exam_failure", trigger_count = 0 },
    { config_id = 148311, name = "ENTER_REGION_148201", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "148", trigger_count = 0 },
    { config_id = 148312, name = "ENTER_REGION_148202", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "148", trigger_count = 0 },
    { config_id = 148313, name = "ENTER_REGION_148203", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "148", trigger_count = 0 },
    { config_id = 148314, name = "ENTER_REGION_148204", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "148", trigger_count = 0 },
    { config_id = 148315, name = "ENTER_REGION_148205", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "148", trigger_count = 0 },
    { config_id = 148316, name = "ENTER_REGION_148206", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "148", trigger_count = 0 },
    { config_id = 148317, name = "ENTER_REGION_148207", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "148", trigger_count = 0 },
    { config_id = 148318, name = "ENTER_REGION_148208", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "148", trigger_count = 0 },
    { config_id = 148319, name = "ENTER_REGION_148209", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "148", trigger_count = 0 },
    { config_id = 148320, name = "ENTER_REGION_148210", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "148", trigger_count = 0 },
    { config_id = 148321, name = "ENTER_REGION_148211", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "148", trigger_count = 0 },
    { config_id = 148322, name = "ENTER_REGION_148212", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_collect_coin", action = "collect_coin", tag = "148", trigger_count = 0 },
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
}
init_config = { suite = 1, end_suite = 0, rand_suite = false }
suites = {
    { monsters = {}, gadgets = {}, regions = {148200}, triggers = {"ENTER_REGION_148200", "CHALLENGE_SUCCESS_148301", "CHALLENGE_FAIL_148302"}, rand_weight = 100 },
    { monsters = {}, gadgets = {148001, 148002, 148003, 148011, 148012, 148013, 148014}, regions = {}, triggers = {}, rand_weight = 100 },
    { monsters = {}, gadgets = {148101}, regions = {148201}, triggers = {"ENTER_REGION_148201"}, rand_weight = 100 },
    { monsters = {}, gadgets = {148102}, regions = {148202}, triggers = {"ENTER_REGION_148202"}, rand_weight = 100 },
    { monsters = {}, gadgets = {148103}, regions = {148203}, triggers = {"ENTER_REGION_148203"}, rand_weight = 100 },
    { monsters = {}, gadgets = {148104}, regions = {148204}, triggers = {"ENTER_REGION_148204"}, rand_weight = 100 },
    { monsters = {}, gadgets = {148105}, regions = {148205}, triggers = {"ENTER_REGION_148205"}, rand_weight = 100 },
    { monsters = {}, gadgets = {148106}, regions = {148206}, triggers = {"ENTER_REGION_148206"}, rand_weight = 100 },
    { monsters = {}, gadgets = {148107}, regions = {148207}, triggers = {"ENTER_REGION_148207"}, rand_weight = 100 },
    { monsters = {}, gadgets = {148108}, regions = {148208}, triggers = {"ENTER_REGION_148208"}, rand_weight = 100 },
    { monsters = {}, gadgets = {148109}, regions = {148209}, triggers = {"ENTER_REGION_148209"}, rand_weight = 100 },
    { monsters = {}, gadgets = {148110}, regions = {148210}, triggers = {"ENTER_REGION_148210"}, rand_weight = 100 },
    { monsters = {}, gadgets = {148111}, regions = {148211}, triggers = {"ENTER_REGION_148211"}, rand_weight = 100 },
    { monsters = {}, gadgets = {148112}, regions = {148212}, triggers = {"ENTER_REGION_148212"}, rand_weight = 100 },
    { monsters = {}, gadgets = {148011, 148012, 148013, 148014, 148021, 148022, 148023, 148024}, regions = {}, triggers = {}, rand_weight = 100 },
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
    for suite = 2, 14 do ScriptLib.RemoveExtraGroupSuite(context, GROUP, suite) end
    ScriptLib.AddExtraGroupSuite(context, GROUP, 15)
    ScriptLib.SetGroupVariableValue(context, "transition", 1)
    return ScriptLib.AddQuestProgress(context, "11330041481")
end

function exam_failure(context, evt)
    ScriptLib.SetGroupVariableValue(context, "started", 0)
    return ScriptLib.AddQuestProgress(context, "11330041482")
end
