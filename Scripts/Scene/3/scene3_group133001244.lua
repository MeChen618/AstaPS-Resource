-- Compatibility scene adapter for Amber 48002, not a recovered native 7.1 group.
-- Route, six 5-unit markers and 60-second exam: animepython aebc1c39019698224c4d18c01e88f60c95da3a19,
-- LQ480.lua / Q480ClientConfig.lua / Q480Marks.lua; positions remain the current scene3 dummy points.
local GROUP = 133001244
monsters = {}
npcs = {}
gadgets = {
    { config_id = 244001, gadget_id = 70690001, pos = { x = 1739.451000, y = 259.639000, z = -1302.307000 }, rot = { x = 17.350851, y = 62.794586, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244002, gadget_id = 70690001, pos = { x = 1745.563250, y = 257.491750, z = -1299.165000 }, rot = { x = 17.350851, y = 62.794586, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244003, gadget_id = 70690001, pos = { x = 1751.675500, y = 255.344500, z = -1296.023000 }, rot = { x = 17.350851, y = 62.794586, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244004, gadget_id = 70690001, pos = { x = 1757.787750, y = 253.197250, z = -1292.881000 }, rot = { x = 17.350851, y = 62.794586, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244005, gadget_id = 70690001, pos = { x = 1833.653000, y = 248.737000, z = -1268.836000 }, rot = { x = -7.526332, y = 90.000000, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244006, gadget_id = 70690001, pos = { x = 1839.294333, y = 249.482333, z = -1268.836000 }, rot = { x = -7.526332, y = 90.000000, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244007, gadget_id = 70690001, pos = { x = 1844.935667, y = 250.227667, z = -1268.836000 }, rot = { x = -7.526332, y = 90.000000, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244008, gadget_id = 70690001, pos = { x = 1887.778000, y = 253.980000, z = -1285.707000 }, rot = { x = 22.602992, y = 164.297464, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244009, gadget_id = 70690001, pos = { x = 1889.485333, y = 251.353667, z = -1291.780000 }, rot = { x = 22.602992, y = 164.297464, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244010, gadget_id = 70690001, pos = { x = 1891.192667, y = 248.727333, z = -1297.853000 }, rot = { x = 22.602992, y = 164.297464, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244011, gadget_id = 70690001, pos = { x = 1896.949000, y = 244.608000, z = -1319.179000 }, rot = { x = 20.187333, y = -164.966240, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244012, gadget_id = 70690001, pos = { x = 1895.206000, y = 242.137333, z = -1325.668667 }, rot = { x = 20.187333, y = -164.966240, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244013, gadget_id = 70690001, pos = { x = 1893.463000, y = 239.666667, z = -1332.158333 }, rot = { x = 20.187333, y = -164.966240, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244014, gadget_id = 70690001, pos = { x = 1885.137000, y = 233.502000, z = -1358.114000 }, rot = { x = 21.831708, y = 139.244996, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244015, gadget_id = 70690001, pos = { x = 1891.383667, y = 229.668667, z = -1365.362333 }, rot = { x = 21.831708, y = 139.244996, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244016, gadget_id = 70690001, pos = { x = 1897.630333, y = 225.835333, z = -1372.610667 }, rot = { x = 21.831708, y = 139.244996, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244017, gadget_id = 70690001, pos = { x = 1903.877000, y = 222.002000, z = -1379.859000 }, rot = { x = 11.778511, y = 170.223948, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244018, gadget_id = 70690001, pos = { x = 1906.166000, y = 219.191000, z = -1393.144000 }, rot = { x = 11.778511, y = 170.223948, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244019, gadget_id = 70690001, pos = { x = 1908.455000, y = 216.380000, z = -1406.429000 }, rot = { x = 12.986423, y = -120.577732, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244020, gadget_id = 70690001, pos = { x = 1903.721333, y = 215.112000, z = -1409.226000 }, rot = { x = 12.986423, y = -120.577732, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244021, gadget_id = 70690001, pos = { x = 1898.987667, y = 213.844000, z = -1412.023000 }, rot = { x = 12.986423, y = -120.577732, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244022, gadget_id = 70690001, pos = { x = 1874.000000, y = 207.000000, z = -1429.000000 }, rot = { x = 90.000000, y = 0.000000, z = 0.000000 }, level = 1, area_id = 3 },
    { config_id = 244023, gadget_id = 70710005, pos = { x = 1799.439000, y = 232.470000, z = -1275.774000 }, rot = { x = 0, y = 0, z = 0 }, level = 1, area_id = 3 },
    { config_id = 244024, gadget_id = 70710005, pos = { x = 1883.170000, y = 233.100000, z = -1274.900000 }, rot = { x = 0, y = 0, z = 0 }, level = 1, area_id = 3 },
    { config_id = 244025, gadget_id = 70710005, pos = { x = 1864.070000, y = 242.700000, z = -1268.390000 }, rot = { x = 0, y = 0, z = 0 }, level = 1, area_id = 3 },
    { config_id = 244101, gadget_id = 70300064, pos = { x = 1768.211000, y = 250.280000, z = -1288.532000 }, rot = { x = 0, y = 0, z = 0 }, level = 1, area_id = 3 },
    { config_id = 244102, gadget_id = 70300064, pos = { x = 1855.753000, y = 251.453000, z = -1268.800000 }, rot = { x = 0, y = 0, z = 0 }, level = 1, area_id = 3 },
    { config_id = 244103, gadget_id = 70300064, pos = { x = 1887.800000, y = 253.739000, z = -1283.603000 }, rot = { x = 0, y = 0, z = 0 }, level = 1, area_id = 3 },
    { config_id = 244104, gadget_id = 70300064, pos = { x = 1897.410000, y = 244.600000, z = -1317.396000 }, rot = { x = 0, y = 0, z = 0 }, level = 1, area_id = 3 },
    { config_id = 244105, gadget_id = 70300064, pos = { x = 1903.900000, y = 222.000000, z = -1379.900000 }, rot = { x = 0, y = 0, z = 0 }, level = 1, area_id = 3 },
    { config_id = 244106, gadget_id = 70300064, pos = { x = 1894.300000, y = 212.600000, z = -1414.800000 }, rot = { x = 0, y = 0, z = 0 }, level = 1, area_id = 3 },
}
regions = {
    { config_id = 244200, shape = RegionShape.SPHERE, radius = 12, pos = { x = 1723.400000, y = 263.249000, z = -1310.966000 } },
    { config_id = 244201, shape = RegionShape.SPHERE, radius = 5, pos = { x = 1768.211000, y = 250.280000, z = -1288.532000 } },
    { config_id = 244202, shape = RegionShape.SPHERE, radius = 5, pos = { x = 1855.753000, y = 251.453000, z = -1268.800000 } },
    { config_id = 244203, shape = RegionShape.SPHERE, radius = 5, pos = { x = 1887.800000, y = 253.739000, z = -1283.603000 } },
    { config_id = 244204, shape = RegionShape.SPHERE, radius = 5, pos = { x = 1897.410000, y = 244.600000, z = -1317.396000 } },
    { config_id = 244205, shape = RegionShape.SPHERE, radius = 5, pos = { x = 1903.900000, y = 222.000000, z = -1379.900000 } },
    { config_id = 244206, shape = RegionShape.SPHERE, radius = 5, pos = { x = 1894.300000, y = 212.600000, z = -1414.800000 } },
}
triggers = {
    { config_id = 244300, name = "ENTER_REGION_244200", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_start", action = "start_exam", trigger_count = 0 },
    { config_id = 244301, name = "CHALLENGE_SUCCESS_244301", event = EventType.EVENT_CHALLENGE_SUCCESS, source = "244", condition = "is_exam_active", action = "exam_success", trigger_count = 0 },
    { config_id = 244302, name = "CHALLENGE_FAIL_244302", event = EventType.EVENT_CHALLENGE_FAIL, source = "244", condition = "is_exam_active", action = "exam_failure", trigger_count = 0 },
    { config_id = 244311, name = "ENTER_REGION_244201", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_pass_marker", action = "pass_marker", tag = "244", trigger_count = 0 },
    { config_id = 244312, name = "ENTER_REGION_244202", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_pass_marker", action = "pass_marker", tag = "244", trigger_count = 0 },
    { config_id = 244313, name = "ENTER_REGION_244203", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_pass_marker", action = "pass_marker", tag = "244", trigger_count = 0 },
    { config_id = 244314, name = "ENTER_REGION_244204", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_pass_marker", action = "pass_marker", tag = "244", trigger_count = 0 },
    { config_id = 244315, name = "ENTER_REGION_244205", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_pass_marker", action = "pass_marker", tag = "244", trigger_count = 0 },
    { config_id = 244316, name = "ENTER_REGION_244206", event = EventType.EVENT_ENTER_REGION, source = "", condition = "can_pass_marker", action = "pass_marker", tag = "244", trigger_count = 0 },
}
variables = {
    { config_id = 1, name = "started", value = 0, no_refresh = false },
    { config_id = 2, name = "step", value = 0, no_refresh = false },
}
init_config = { suite = 1, end_suite = 0, rand_suite = false }
suites = {
    { monsters = {}, gadgets = {}, regions = {244200}, triggers = {"ENTER_REGION_244200", "CHALLENGE_SUCCESS_244301", "CHALLENGE_FAIL_244302"}, rand_weight = 100 },
    { monsters = {}, gadgets = {244001, 244002, 244003, 244004, 244005, 244006, 244007, 244008, 244009, 244010, 244011, 244012, 244013, 244014, 244015, 244016, 244017, 244018, 244019, 244020, 244021, 244022, 244023, 244024, 244025}, regions = {244201, 244202, 244203, 244204, 244205, 244206}, triggers = {"ENTER_REGION_244201", "ENTER_REGION_244202", "ENTER_REGION_244203", "ENTER_REGION_244204", "ENTER_REGION_244205", "ENTER_REGION_244206"}, rand_weight = 100 },
    { monsters = {}, gadgets = {244101}, regions = {}, triggers = {}, rand_weight = 100 },
    { monsters = {}, gadgets = {244102}, regions = {}, triggers = {}, rand_weight = 100 },
    { monsters = {}, gadgets = {244103}, regions = {}, triggers = {}, rand_weight = 100 },
    { monsters = {}, gadgets = {244104}, regions = {}, triggers = {}, rand_weight = 100 },
    { monsters = {}, gadgets = {244105}, regions = {}, triggers = {}, rand_weight = 100 },
    { monsters = {}, gadgets = {244106}, regions = {}, triggers = {}, rand_weight = 100 },
}

function is_exam_active(context, evt)
    return ScriptLib.GetQuestState(context, 0, 48002) == 2
        and ScriptLib.GetGroupVariableValue(context, "started") == 1
end

function can_start(context, evt)
    return evt.param1 == 244200 and ScriptLib.GetQuestState(context, 0, 48002) == 2
        and ScriptLib.GetGroupVariableValue(context, "started") == 0
        and ScriptLib.GetRegionEntityCount(context, { region_eid = evt.source_eid, entity_type = EntityType.AVATAR }) > 0
end

function start_exam(context, evt)
    -- Do not consume the start trigger if an unrelated world challenge owns the HUD.
    if ScriptLib.ActiveChallenge(context, 244, 295, 60, GROUP, 244, 6) ~= 0 then return 0 end
    ScriptLib.SetGroupVariableValue(context, "started", 1)
    ScriptLib.SetGroupVariableValue(context, "step", 0)
    ScriptLib.AddExtraGroupSuite(context, GROUP, 2)
    ScriptLib.AddExtraGroupSuite(context, GROUP, 3)
    return 0
end

function can_pass_marker(context, evt)
    return is_exam_active(context, evt)
        and evt.param1 == 244201 + ScriptLib.GetGroupVariableValue(context, "step")
        and ScriptLib.GetRegionEntityCount(context, { region_eid = evt.source_eid, entity_type = EntityType.AVATAR }) > 0
end

function pass_marker(context, evt)
    local step = evt.param1 - 244200
    ScriptLib.SetGroupVariableValue(context, "step", step)
    ScriptLib.RemoveExtraGroupSuite(context, GROUP, step + 2)
    if step < 6 then ScriptLib.AddExtraGroupSuite(context, GROUP, step + 3) end
    return 0
end

function exam_success(context, evt)
    ScriptLib.SetGroupVariableValue(context, "started", 0)
    return ScriptLib.AddQuestProgress(context, "11330012441")
end

function exam_failure(context, evt)
    ScriptLib.SetGroupVariableValue(context, "started", 0)
    return ScriptLib.AddQuestProgress(context, "11330012442")
end
