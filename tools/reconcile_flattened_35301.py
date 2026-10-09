#!/usr/bin/env python3
"""One-time 7.1 resource materialization correction, verified against BinOutput/Quest/353.json.

Remove only the erroneous 35301 finishExec GRANT_TRIAL_AVATAR(1) in the
51 MB flattened QuestExcel. Leave every other QuestExcel record unchanged.
Run in the repository root; refuses ambiguous inputs.
"""
import json
import re
from pathlib import Path

path = Path("ExcelBinOutput/QuestExcelConfigData.json")
text = path.read_text(encoding="utf-8")
ids = list(re.finditer(r'"subId"\s*:\s*35301\b', text))
assert len(ids) == 1, f"Expected exactly one 35301 row, found {len(ids)}"
target = ids[0].start()

# The flattened JSON is an array of 2-space-indented quest objects.
starts = list(re.finditer(r"(?m)^  \{", text[:target]))
assert starts, "Cannot locate QuestExcel top-level row"
start = starts[-1].start()
end_match = re.search(r"(?m)^  \}", text[target:])
assert end_match, "Cannot locate QuestExcel row end"
end = target + end_match.end()
row = text[start:end]
parsed = json.loads(row)
assert parsed.get("subId") == 35301, f"Wrong row selected: {parsed.get('subId')}"
expected = [{"param": ["1"], "type": "QUEST_EXEC_GRANT_TRIAL_AVATAR"}]
current = parsed.get("finishExec", [])
if current == []:
    print("ALREADY CORRECT: flattened 35301 contains no trial Amber grant")
else:
    assert current == expected, f"Unreviewed 35301 finishExec: {current!r}"
    field = re.search(r'"finishExec"\s*:\s*\[\s*\{(.*?)\}\s*\]', row, re.S)
    assert field, "Cannot isolate 35301 finishExec array"
    assert json.loads("{" + field.group(1) + "}") == expected[0]
    patched = row[:field.start()] + '"finishExec": []' + row[field.end():]
    assert json.loads(patched)["finishExec"] == [], "Invalid patched row"
    result = text[:start] + patched + text[end:]
    path.write_text(result, encoding="utf-8")
    print("PATCHED: removed sole nonnative 35301 Amber grant from flattened QuestExcel")
