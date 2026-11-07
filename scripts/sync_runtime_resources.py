"""Incrementally sync six runtime resource groups from a local snapshot."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import subprocess


BIN_ROOTS = (
    'BinOutput/Avatar/', 'BinOutput/Ability/', 'BinOutput/AbilityGroup/',
    'BinOutput/AbilityPath/', 'BinOutput/Talent/', 'BinOutput/Monster/',
    'BinOutput/MonsterPreview/', 'BinOutput/Scene/Point/',
    'BinOutput/Scene/WorldArea/', 'BinOutput/Scene/SceneNpcBorn/',
)
DEPENDENCIES = {
    'ProudSkillExcelConfigData.json', 'EquipAffixExcelConfigData.json',
    'MaterialExcelConfigData.json', 'RewardExcelConfigData.json',
    'SceneExcelConfigData.json', 'SceneTagConfigData.json',
    'MapAreaConfigData.json', 'MapLayerExcelConfigData.json',
    'MapLayerGroupExcelConfigData.json', 'MapLayerFloorExcelConfigData.json',
    'WorldAreaConfigData.json', 'WorldAreaLevelupConfigData.json',
}
IDENTITIES = {
    'AvatarCostumeExcelConfigData.json': ('skinId',),
    'AvatarPromoteExcelConfigData.json': ('avatarPromoteId', 'promoteLevel'),
    'AvatarRecommendDataExcelConfigData.json': ('avatarId',),
    'AvatarTalentExcelConfigData.json': ('talentId',),
    'AvatarTraceEffectExcelConfigData.json': ('itemId',),
    'EquipAffixExcelConfigData.json': ('affixId',),
    'FetterCharacterCardExcelConfigData.json': ('avatarId', 'fetterLevel'),
    'FetterInfoExcelConfigData.json': ('fetterId',),
    'FetterStoryExcelConfigData.json': ('fetterId',),
    'FettersExcelConfigData.json': ('fetterId',),
    'MonsterSpecialNameExcelConfigData.json': ('specialNameID',),
    'MonsterTitleExcelConfigData.json': ('titleID',),
    'ProudSkillExcelConfigData.json': ('proudSkillId',),
    'RewardExcelConfigData.json': ('rewardId',),
    'WeaponCodexExcelConfigData.json': ('Id',),
    'WeaponPromoteExcelConfigData.json': ('weaponPromoteId', 'promoteLevel'),
    'WorldAreaConfigData.json': ('ID',),
}
MANIFEST = 'docs/runtime-7.2-manifest.json'


class GitSnapshot:
    def __init__(self, root, ref):
        self.root = str(root)
        self.commit = self.git('rev-parse', ref).decode().strip()
        self.files = {}
        for entry in self.git('ls-tree', '-r', '-z', self.commit).split(b'\0'):
            if not entry:
                continue
            meta, path = entry.split(b'\t', 1)
            mode, kind, sha = meta.decode().split()
            if kind == 'blob':
                self.files[path.decode()] = (mode, sha)
        self.batch = subprocess.Popen(['git', '-C', self.root, 'cat-file', '--batch'],
                                      stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def git(self, *args):
        return subprocess.check_output(['git', '-C', self.root, *args])

    def read(self, path):
        sha = self.files[path][1]
        self.batch.stdin.write((sha + '\n').encode())
        self.batch.stdin.flush()
        header = self.batch.stdout.readline().decode().strip().split()
        assert len(header) == 3 and header[:2] == [sha, 'blob'], (path, header)
        data = self.batch.stdout.read(int(header[2]))
        assert self.batch.stdout.read(1) == b'\n'
        return data

    def close(self):
        self.batch.stdin.close()
        assert self.batch.wait() == 0


def selected(path):
    return (path.startswith(BIN_ROOTS)
            or path == 'BinOutput/Common/ConfigGlobalCombat.json'
            or (path.startswith('ExcelBinOutput/') and (
                Path(path).name.startswith(('Avatar', 'Weapon', 'Monster', 'Fetter'))
                or Path(path).name in DEPENDENCIES)))


def load(data):
    return json.loads(data)


def dump(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()


def identity(filename, rows):
    columns = IDENTITIES.get(filename)
    if columns is None:
        candidates = [key for key in ('id', 'ID', 'Id') if any(key in r for r in rows)]
        assert len(candidates) == 1, (filename, candidates)
        columns = (candidates[0],)
    for row in rows:
        assert isinstance(row, dict)
        assert all(isinstance(row.get(key, 0), int) and not isinstance(row.get(key, 0), bool)
                   for key in columns), (filename, row)
    return columns


def keyed(rows, columns):
    result = {}
    for row in rows:
        key = tuple(row.get(col, 0) for col in columns)
        assert key not in result, ('Duplicate resource identity', columns, key)
        result[key] = row
    return result


def merge_excel(path, old, source):
    assert isinstance(old, list) and isinstance(source, list)
    columns = identity(Path(path).name, old + source)
    previous, incoming = keyed(old, columns), keyed(source, columns)
    added = [row for key, row in incoming.items() if key not in previous]
    changed = [list(key) for key in previous.keys() & incoming.keys()
               if previous[key] != incoming[key]]
    return old + added, dict(identity=list(columns), rows_added=len(added),
                             added_ids=[list(tuple(row.get(c, 0) for c in columns)) for row in added],
                             differing_existing_ids_preserved=changed)


def merge_points(old, source):
    previous, incoming = old.get('points', {}), source.get('points', {})
    assert isinstance(previous, dict) and isinstance(incoming, dict)
    added = {key: value for key, value in incoming.items() if key not in previous}
    result = {**old, 'points': {**previous, **added}} if added else old
    return result, dict(points_added=len(added), point_ids=list(added),
                        point_types=dict(Counter(p.get('$type', '') for p in added.values())))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--source-ref', default='HEAD')
    parser.add_argument('--target', type=Path, default=Path(__file__).resolve().parents[1])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    target = args.target.resolve()
    source = GitSnapshot(args.source, args.source_ref)
    baseline = GitSnapshot(target, 'HEAD')
    manifest_path = target / MANIFEST
    gitdir = Path(baseline.git('rev-parse', '--absolute-git-dir').decode().strip())
    local_state_path = gitdir / 'runtime-resource-sync-local.json'
    prior = load(manifest_path.read_bytes()) if manifest_path.is_file() else {}
    paths = sorted(p for p in source.files if selected(p))
    changes, retained = [], []

    def current(path):
        local = target / path
        if local.is_file():
            return local.read_bytes()
        if path in baseline.files:
            return baseline.read(path)
        return None

    def stage(path, data, detail, old):
        if old == data:
            return
        before = load(old) if old is not None else None
        after = load(data)
        if before == after:
            return
        record = dict(path=path, added_file=old is None,
                      baseline_git_blob=baseline.files.get(path, (None, None))[1],
                      result_sha256=hashlib.sha256(data).hexdigest(), **detail)
        changes.append(record)
        if args.apply:
            output = target / path
            output.parent.mkdir(parents=True, exist_ok=True)
            temporary = output.with_name(output.name + '.sync-tmp')
            temporary.write_bytes(data)
            temporary.replace(output)

    for path in paths:
        previous = current(path)
        if path in baseline.files and source.files[path] == baseline.files[path]:
            # 共同文件已经一致，保留本地可能存在的修正。
            continue
        raw = source.read(path)
        incoming = load(raw)
        if previous is not None and load(previous) == incoming:
            continue
        if previous is None:
            stage(path, raw, dict(copied_verbatim=True), previous)
        elif path.startswith('ExcelBinOutput/'):
            merged, detail = merge_excel(path, load(previous), incoming)
            if detail['differing_existing_ids_preserved']:
                retained.append(dict(path=path, ids=detail['differing_existing_ids_preserved']))
            stage(path, raw if merged == incoming else dump(merged), detail, previous)
        elif path.startswith('BinOutput/Scene/Point/'):
            merged, detail = merge_points(load(previous), incoming)
            stage(path, raw if merged == incoming else dump(merged), detail, previous)
        elif load(previous) != incoming:
            # 现有能力、天赋等定义可能含手工修正，不做整文件替换。
            retained.append(dict(path=path, reason='Existing non-Excel definition preserved'))

    # AstaPS 按 monsterId 找模型；由已有的 monsterName 和真实文件名补索引。
    monster_file = 'ExcelBinOutput/MonsterExcelConfigData.json'
    monsters = load(current(monster_file))
    if not args.apply:
        incoming = load(source.read(monster_file))
        monsters = merge_excel(monster_file, monsters, incoming)[0]
    configs = defaultdict(list)
    for path in source.files.keys() | baseline.files.keys():
        if path.startswith('BinOutput/Monster/') and path.endswith('.json'):
            stem = Path(path).stem
            match = re.search(r'_(\d+)$', stem)
            if match:
                configs[int(match.group(1))].append(stem)
    configs = {key: sorted(set(value)) for key, value in configs.items()}
    mapping_file = 'Server/MonsterMapping.json'
    previous = current(mapping_file)
    mapping = load(previous)
    old_map = {row['monsterId']: row for row in mapping}
    assert len(old_map) == len(mapping)
    extra = []
    for row in monsters:
        ident = row['id']
        if ident in old_map:
            continue
        expected = row['monsterName'] + '_' + str(ident)
        if configs.get(ident) == [expected]:
            extra.append(dict(monsterId=ident, monsterJson=expected))
    stage(mapping_file, dump(mapping + extra),
          dict(rows_added=len(extra), identity=['monsterId'],
               added_ids=[[row['monsterId']] for row in extra],
               derived_from='MonsterExcel monsterName + id, joined to a unique existing config file'), previous)

    # 只补这些资源实际引用的 Gadget，避免顺带导入无关活动整表。
    reference_changes = {r['path']: r for r in prior.get('changes', [])}
    reference_changes.update({r['path']: r for r in changes})
    gadget_refs = defaultdict(set)
    point_dungeons, point_daily_dungeons = set(), set()

    def collect_gadgets(node, path):
        if isinstance(node, dict):
            for key, value in node.items():
                if key.lower() == 'gadgetid' and isinstance(value, int) and value > 0:
                    gadget_refs[value].add(path)
                collect_gadgets(value, path)
        elif isinstance(node, list):
            for value in node:
                collect_gadgets(value, path)

    for path, record in reference_changes.items():
        if path.startswith(('BinOutput/Ability/', 'BinOutput/Avatar/', 'BinOutput/Monster/',
                            'BinOutput/Scene/Point/')):
            data = load(current(path) or source.read(path))
            if record.get('point_ids'):
                data = [data['points'][key] for key in record['point_ids']]
            elif path.startswith('BinOutput/Scene/Point/'):
                data = list(data.get('points', {}).values())
            if path.startswith('BinOutput/Scene/Point/'):
                for point in data:
                    point_dungeons.update(v for v in point.get('dungeonIds', point.get('JHHFPGJNMIN', [])) if v)
                    point_daily_dungeons.update(v for v in point.get('dungeonRandomList', point.get('GLEKJMEEOMH', [])) if v)
            collect_gadgets(data, path)
        elif path in ('ExcelBinOutput/MonsterExcelConfigData.json', 'ExcelBinOutput/WeaponExcelConfigData.json'):
            ids = {key[0] for key in record['added_ids']}
            data = load(current(path))
            for row in data:
                if row['id'] in ids:
                    collect_gadgets(row, path)
                    for ident in row.get('equips', []):
                        if ident > 0:
                            gadget_refs[ident].add(path)
    gadget_file = 'ExcelBinOutput/GadgetExcelConfigData.json'
    previous = current(gadget_file)
    gadgets = load(previous)
    known_gadgets = keyed(gadgets, ('id',))
    incoming_gadgets = keyed(load(source.read(gadget_file)), ('id',))
    needed = sorted(ident for ident in gadget_refs if (ident,) not in known_gadgets)
    imported = [incoming_gadgets[ident,] for ident in needed if (ident,) in incoming_gadgets]
    unresolved_gadgets = [dict(id=ident, references=sorted(gadget_refs[ident]))
                          for ident in gadget_refs if (ident,) not in known_gadgets and (ident,) not in incoming_gadgets]
    stage(gadget_file, dump(gadgets + imported),
          dict(identity=['id'], rows_added=len(imported), added_ids=[[r['id']] for r in imported],
               dependency_only=True), previous)

    unresolved_dungeons = []
    for path, ids in [('ExcelBinOutput/DungeonExcelConfigData.json', point_dungeons),
                      ('ExcelBinOutput/DailyDungeonConfigData.json', point_daily_dungeons)]:
        previous = current(path)
        old = load(previous)
        have = keyed(old, ('id',))
        incoming = keyed(load(source.read(path)), ('id',))
        missing = sorted(ident for ident in ids if (ident,) not in have)
        added = [incoming[ident,] for ident in missing if (ident,) in incoming]
        unresolved_dungeons.extend(dict(file=path, id=ident) for ident in missing if (ident,) not in incoming)
        stage(path, dump(old + added), dict(identity=['id'], rows_added=len(added),
              added_ids=[[r['id']] for r in added], dependency_only=True), previous)

    pending_changes = list(changes)
    if args.apply and prior.get('target_base_commit') == baseline.commit:
        combined = {r['path']: r for r in prior.get('changes', [])}
        combined.update({r['path']: r for r in changes})
        changes = sorted(combined.values(), key=lambda r: r['path'])
        for record in changes:
            path = record['path']
            record['result_sha256'] = hashlib.sha256(current(path)).hexdigest()
            if path.startswith('ExcelBinOutput/') and path in baseline.files:
                old, now = load(baseline.read(path)), load(current(path))
                columns = identity(Path(path).name, old + now)
                before, after = keyed(old, columns), keyed(now, columns)
                record['identity'] = list(columns)
                record['added_ids'] = [list(key) for key in after if key not in before]
                record['rows_added'] = len(record['added_ids'])

    totals = Counter()
    for row in changes:
        totals['files_added' if row['added_file'] else 'files_updated'] += 1
        if row['path'].startswith('ExcelBinOutput/'):
            if row['added_file']:
                totals['excel_tables_added'] += 1
                totals['excel_rows_in_added_tables'] += len(load(source.read(row['path'])))
            else:
                totals['excel_tables_extended'] += 1
                totals['excel_rows_added_to_existing_tables'] += row['rows_added']
        totals['points_added_to_existing_files'] += row.get('points_added', 0)
    report = dict(resource_version='7.2', target_repository='MeChen618/AstaPS-Resource',
                  target_base_commit=baseline.commit, policy='Add records by explicit IDs, preserve existing records and definitions',
                  totals=dict(totals), changes=changes, retained_differences=retained,
                  unresolved_fields_preserved=True,
                  pending_gadget_references=unresolved_gadgets,
                  pending_dungeon_references=unresolved_dungeons,
                  existing_quests_lua_drops_unchanged=True)
    source.close()
    baseline.close()
    if args.apply and changes:
        manifest = target / MANIFEST
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_bytes(dump(report))
        local_state_path.write_bytes(dump(dict(source_commit=source.commit, source_ref=args.source_ref)))
    if args.check:
        assert not pending_changes, 'Sync would still change resources: ' + str([r['path'] for r in pending_changes])
    print(json.dumps(dict(totals=report['totals'], retained_differences=len(retained),
                          idempotent=not changes), ensure_ascii=False))


if __name__ == '__main__':
    main()
