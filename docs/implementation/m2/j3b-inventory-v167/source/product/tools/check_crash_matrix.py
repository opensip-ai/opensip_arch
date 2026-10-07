"""Check an X9 crash-matrix run set, and scan a release binary for barrier strings.

Law X9 r1 item 7 (and item 2, guard 4). Read-only developer check, standard
library only, under the pinned Python. It reads the scope registry from
crates/platform/src/crash_barrier.rs. It runs nothing and writes nothing.

`check` (law X9 r10, unit X9-6) is the M2 exit gate. It takes both targets'
reviewed required-runs files, storage's and host's, each with its own pair of
lead run sets (`--target <name> <required> <run set> <repeat>`, once for
`storage` and once for `host`). It refuses unless all of these hold for both
lead repetitions:
- every (case, variant) of each target's reviewed required-runs.v1.json has
  exactly one run in that target's set, listed by matrix.json with its bytes
  and sha256, and no extra run exists (r15: a row's `unit` member is
  admitted);
- both required-runs files carry the same clockEpoch (r10);
- every run record and matrix.json is canonical JSON (sorted keys, compact,
  exact integers, no floats or duplicate keys) of the opensip.x9.*.v1 shape;
- every verdict is PASS, and the labels, units, script and expected values
  equal the required row (expected values are never read back from a run);
- product.commit is the reviewed commit, the worktree was clean, the profile
  is dev with exactly the crash-matrix feature, and the host record carries
  the synthetic fixture and BASELINE-ATTESTED standing;
- a process-death run is exactly a run whose script kills, verified by a
  child that ended by signal 9 with lastHeld at the killed point;
- each target's census names only registered scopes with the right
  durability, and its matrix.json kill set equals the one derived from it
  (each durability point at #1, and a repeated one also at (n + 1) // 2 and
  n);
- (r10) the union census of the two targets (by point name, each at its
  largest occurrence count, its durability equal in both) derives the union
  kill set, and every point of it is killed by a process-death run of either
  target, in each repetition;
- the release absence passed (no OPENSIP_X9_ or registered scope string in
  the release binary, and the feature's release build was refused);
- the limits are exactly L1..L11 (law X9 r8), each with a reason and an owner;
- the two repetitions agree run by run on normalizedSha256 (the trust
  store's trustState included) and on every child's trace digest, and on
  the census;
- (law X9 r2 item 3) every run is labelled scripted-clock and records the
  run set's clock (the required runs' clockEpoch, script x9-ordinal-3600),
  and its children's ordinals increase in spawn order;
- (law X9 r12 and r13, item 11's timing guard) a run whose script arms
  x4.observer.tick records timingGuard {monotonicMs, limitMs: 5000} within
  its limit, and no other run records one. It is not compared between
  repetitions.

`check-unit` (law X9 r4 item 7) is the per-unit check of X9-2 to X9-5 before
X9-6: the unit's subset of the reviewed required runs (the rows whose case is
in the unit's list in item 12; r15: a row with a `unit` member is in that
unit's subset only), on two lead run sets. `check` admits the member and
still requires one run for every row. It applies `check`'s
per-run check and repetition agreement with two differences: product.commit
(of each run and of matrix.json) is the stated base commit and worktreeClean
may be false, because a unit is reviewed uncommitted; and full kill-set
coverage is not required, only that every killed point is in the kill set the
census derives. The unit's review subject manifest binds the reviewed bytes.
It is not a matrix pass: X9-6's `check` is unchanged.

The `check` function with one run-set pair is the single-target form the
regression controls exercise; only `check` over both targets reports
`matrixPass: true`.

`coverage` runs nothing and reads no run set. Given each target's census
(census.json, or a matrix.json carrying one) and its reviewed required runs,
it derives the union kill set and reports every kill-set point that no
required row's script kills, and every killed point outside it. It passes
only when nothing is uncovered. It is a transcription aid for X9-6's census
step, not a matrix pass.

`release-absence` reports which of OPENSIP_X9_ and the registered scope names
occur in a binary; it passes only when none does.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

MAX_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32
MIN_INTEGER = -(1 << 63)
MAX_INTEGER = (1 << 64) - 1
REGISTRY_SOURCE = 'crates/platform/src/crash_barrier.rs'
PRIMITIVE_STEPS = ('create', 'write', 'file-barrier', 'rename', 'link', 'directory-barrier', 'reopen-confirm', 'lock', 'unlock')
LABELS = ('process-death', 'injected', 'mutation', 'synthetic', 'scripted-clock')
CLOCK_SCRIPT = 'x9-ordinal-3600'
LIMITS = tuple(f'L{n}' for n in range(1, 12))
TIMING_GUARD_LIMIT_MS = 5000
# Law X9 r10: the two matrix targets, each with its own required-runs file.
TARGETS = ('host', 'storage')
# Law X9 r7 item 12: each unit's cases (a case named by several units is
# checked by each of them; X9 r4 review).
UNIT_CASES = {
    'X9-2': ('F00', 'F02', 'F03', 'F04', 'F05', 'F07', 'F08', 'F09', 'F10', 'F20', 'F21', 'F22', 'F31', 'F46'),
    'X9-3': ('F11', 'F12', 'F13', 'F14', 'F15', 'F23', 'F24', 'F25', 'F27', 'F28', 'F29', 'F33', 'F36', 'F42', 'F43',
             'F44', 'F45', 'F49', 'F52', 'F53'),
    'X9-4': ('F06', 'F18', 'F19', 'F26', 'F30', 'F34', 'F38', 'F39', 'F40', 'F41'),
    'X9-5': ('F01', 'F12', 'F16', 'F17', 'F32', 'F39', 'F40', 'F53'),
}
# Law X9 r16: a row's `unit` may also name X9-6, whose rows are in no unit's
# check-unit subset and are required by `check`. X9 r17 frame rule 3 and
# LD-RC-3: X3c-3's RC rows carry "X3c-3", read as "X9-6" is.
UNIT_VALUES = (*UNIT_CASES, 'X9-6', 'X3c-3', 'J3b', 'J3d')
HEX64 = re.compile(r'[0-9a-f]{64}')
HEX40 = re.compile(r'[0-9a-f]{40}')
SEGMENT = re.compile(r'[a-z0-9_-]+')


class MatrixError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise MatrixError(message)


def registry(repository: Path):
    """The registered scopes and their access, from the Rust registry block."""
    text = (repository / REGISTRY_SOURCE).read_text()
    begin, end = '// BEGIN X9 SCOPE REGISTRY', '// END X9 SCOPE REGISTRY'
    require(text.count(begin) == 1 and text.count(end) == 1, 'scope registry block not found')
    block = text[text.index(begin) + len(begin):text.index(end)]
    scopes = {}
    for line in block.splitlines():
        line = line.strip()
        match = re.fullmatch(r'\("([a-z0-9._-]+)", Access::(Durable|ReadOnly)\),', line)
        if match:
            require(match[1] not in scopes, 'duplicate registered scope')
            scopes[match[1]] = match[2] == 'Durable'
        else:
            require(line in ('', 'pub const SCOPES: &[(&str, Access)] = &[', '];'), 'unexpected registry line: ' + line)
    require(bool(scopes), 'empty scope registry')
    return scopes


def registered_prefix(path, scopes):
    found = None
    parts = path.split('.')
    for n in range(1, len(parts) + 1):
        candidate = '.'.join(parts[:n])
        if candidate in scopes:
            found = candidate
    return found


def segments_valid(path):
    return bool(path) and all(SEGMENT.fullmatch(segment) for segment in path.split('.'))


def point_valid(name, scopes):
    """The barrier module's grammar: a registered scope, further segments,
    and for a primitive point one /<step>.<before|after>."""
    path, _, primitive = name.partition('/')
    if not segments_valid(path):
        return False
    scope = registered_prefix(path, scopes)
    if scope is None:
        return False
    if '/' in name:
        step, _, phase = primitive.rpartition('.')
        return step in PRIMITIVE_STEPS and phase in ('before', 'after')
    return len(scope) < len(path)


def is_durability(name, scopes):
    return '/' in name or scopes[registered_prefix(name, scopes)]


def kill_set(points):
    out = []
    for point in points:
        if point['durability']:
            n = point['occurrences']
            for k in sorted({1, (n + 1) // 2, n}):
                out.append(f"{point['name']}#{k}")
    return out


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def _refuse_constant(text):
    raise MatrixError('non-finite number ' + text)


def _refuse_float(text):
    raise MatrixError('float ' + text)


def _pairs(pairs):
    keys = [key for key, _ in pairs]
    require(len(keys) == len(set(keys)), 'duplicate key')
    return dict(pairs)


def _profile(value, depth=0):
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return
    if isinstance(value, int):
        require(MIN_INTEGER <= value <= MAX_INTEGER, 'integer out of range')
        return
    require(depth < MAX_DEPTH, 'container depth over 32')
    children = value.values() if isinstance(value, dict) else value
    for child in children:
        _profile(child, depth + 1)


def load(path: Path):
    """A canonical JSON file: the bytes must equal their own encoding."""
    raw = path.read_bytes()
    require(len(raw) <= MAX_BYTES, 'record over 4 MiB: ' + str(path))
    try:
        value = json.loads(raw.decode('utf-8'), object_pairs_hook=_pairs, parse_float=_refuse_float, parse_constant=_refuse_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MatrixError(f'invalid JSON {path}: {exc}') from exc
    _profile(value)
    require(canonical(value) == raw, 'noncanonical JSON: ' + str(path))
    return value


def pin(path: Path, relative):
    raw = path.read_bytes()
    return {'path': relative, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def keys(value, required, optional=(), what='record'):
    require(isinstance(value, dict), what + ' must be an object')
    require(set(required) <= set(value) <= set(required) | set(optional), what + ' keys differ: ' + ', '.join(sorted(set(value) ^ set(required))))


def strings(value, what):
    require(isinstance(value, list) and all(isinstance(x, str) and x for x in value), what + ' must be a list of strings')


def digest(value, what):
    keys(value, ('records', 'sha256'), what=what)
    require(type(value['records']) is int and value['records'] >= 0 and HEX64.fullmatch(value['sha256'] or ''), 'invalid ' + what)


def check_required(document):
    keys(document, ('schema', 'clockEpoch', 'runs'), what='required runs')
    require(document['schema'] == 'opensip.x9.required-runs.v1', 'unknown required-runs schema')
    require(type(document['clockEpoch']) is int and document['clockEpoch'] >= 0, 'invalid clockEpoch')
    rows = {}
    for row in document['runs']:
        # Law X9 r15: an optional `unit` names the X9 unit a law moved the
        # row to, whatever its case (F14's moved kill row, X9-4); r16 adds
        # X9-6 (the 50 coverage rows).
        keys(row, ('case', 'variant', 'units', 'labels', 'script', 'expected'), ('unit',), what='required run')
        require('unit' not in row or row['unit'] in UNIT_VALUES, 'invalid required unit')
        identity = (row['case'], row['variant'])
        require(identity not in rows, 'duplicate required run')
        require(re.fullmatch(r'F[0-5][0-9]', row['case']) and re.fullmatch(r'[a-z0-9][a-z0-9-]*', row['variant']), 'invalid required case or variant')
        strings(row['labels'], 'required labels')
        require(len(set(row['labels'])) == len(row['labels']) and set(row['labels']) <= set(LABELS) and {'synthetic', 'scripted-clock'} <= set(row['labels']),
                'invalid required labels')
        strings(row['units'], 'required units')
        require(isinstance(row['script'], list), 'required script must be a list')
        rows[identity] = row
    require(bool(rows), 'no required runs')
    return rows, document['clockEpoch']


def in_unit(identity, row, unit):
    """Law X9 r4 item 7 with r15: a row with a `unit` member is in that
    unit's subset only (r16: an X9-6 row is in no unit's subset); any other
    row is in each unit whose case list names its case."""
    if 'unit' in row:
        return row['unit'] == unit
    return identity[0] in UNIT_CASES[unit]


def kills(run):
    return [step['await'] for step in run['script'] if isinstance(step, dict) and step.get('then') == 'kill']


def check_run(run, row, commit, epoch, unit=False):
    keys(run, ('schema', 'case', 'variant', 'units', 'labels', 'product', 'host', 'clock', 'script', 'children', 'postState', 'ladder', 'expected', 'verdict'),
         ('ladderEnd', 'notApplicable', 'timingGuard'), 'run')
    name = f"{run['case']}-{run['variant']}"
    require(run['schema'] == 'opensip.x9.run.v1', name + ': unknown run schema')
    require(run['verdict'] == 'PASS', name + ': verdict ' + str(run['verdict']))
    require(run['labels'] == row['labels'], name + ': labels differ from the required row')
    for field in ('units', 'script', 'expected'):
        require(run[field] == row[field], f'{name}: {field} differs from the required row')
    product = run['product']
    keys(product, ('commit', 'worktreeClean', 'toolchain', 'profile', 'features'), what='product')
    require(product['commit'] == commit, name + ': product.commit is not the reviewed commit')
    require(product['worktreeClean'] is True or (unit and product['worktreeClean'] is False), name + ': dirty worktree')
    require(product['profile'] == 'dev' and product['features'] == ['crash-matrix'], name + ': profile or features')
    require(isinstance(product['toolchain'], str) and product['toolchain'], name + ': toolchain')
    host = run['host']
    keys(host, ('os', 'arch', 'filesystem', 'profileStanding', 'fixture'), what='host')
    require(host['profileStanding'] == 'BASELINE-ATTESTED' and host['fixture'] == 'synthetic-signed-v2', name + ': fixture labels')
    require(run['clock'] == {'epoch': epoch, 'script': CLOCK_SCRIPT}, name + ': clock is not the run set\'s script')
    require(isinstance(run['children'], list) and run['children'], name + ': no children')
    ordinals = [child.get('ordinal') if isinstance(child, dict) else None for child in run['children']]
    require(all(type(k) is int and k >= 0 for k in ordinals) and ordinals == sorted(set(ordinals)), name + ': child ordinals do not follow spawn order')
    for child in run['children']:
        keys(child, ('role', 'ordinal', 'exit', 'lastHeld', 'trace', 'outcome'), what='child')
        require(isinstance(child['role'], str) and child['role'], name + ': child role')
        exit_ = child['exit']
        require(isinstance(exit_, dict) and len(exit_) == 1 and next(iter(exit_)) in ('signal', 'code') and type(next(iter(exit_.values()))) is int, name + ': child exit')
        require(child['lastHeld'] is None or isinstance(child['lastHeld'], str), name + ': lastHeld')
        digest(child['trace'], name + ' child trace')
    arms_tick = any('x4.observer.tick' in step.get('arm', '') for step in run['script'] if isinstance(step, dict) and isinstance(step.get('arm', ''), str))
    if arms_tick:
        guard = run.get('timingGuard')
        keys(guard, ('monotonicMs', 'limitMs'), what='timingGuard')
        require(guard['limitMs'] == TIMING_GUARD_LIMIT_MS and type(guard['monotonicMs']) is int
                and 0 <= guard['monotonicMs'] <= guard['limitMs'], name + ': timing guard over its limit')
    else:
        require('timingGuard' not in run, name + ': a timing guard on a run that arms no observer tick')
    killed = kills(run)
    require(bool(killed) == ('process-death' in run['labels']), name + ': process-death label and kill script disagree')
    for point in killed:
        require(any(c['exit'] == {'signal': 9} and c['lastHeld'] == point for c in run['children']), name + ': kill at ' + point + ' not verified by signal 9 and lastHeld')
    post = run['postState']
    keys(post, ('raw', 'logical', 'normalizedSha256'), what='postState')
    require(isinstance(post['raw'], list) and HEX64.fullmatch(post['normalizedSha256'] or ''), name + ': postState')
    for entry in post['raw']:
        keys(entry, ('path', 'bytes', 'sha256'), what='raw entry')
    require(isinstance(run['ladder'], list), name + ': ladder')
    return killed


def check_set(directory: Path, rows, commit, scopes, epoch, unit=False, deferred=False):
    """One run set. `unit`: check-unit's set (base commit, no coverage, killed
    points inside the kill set). `deferred`: one target of the two-target
    gate, whose coverage is checked over the union census (law X9 r10)."""
    matrix = load(directory / 'matrix.json')
    keys(matrix, ('schema', 'product', 'runs', 'census', 'killSet', 'releaseAbsence', 'limits'), what='matrix')
    require(matrix['schema'] == 'opensip.x9.matrix.v1', 'unknown matrix schema')
    keys(matrix['product'], ('commit', 'worktreeClean'), what='matrix product')
    if unit:
        require(matrix['product']['commit'] == commit and matrix['product']['worktreeClean'] in (True, False), 'matrix product is not the base commit')
    else:
        require(matrix['product'] == {'commit': commit, 'worktreeClean': True}, 'matrix product is not the reviewed clean commit')
    require(HEX40.fullmatch(commit), 'reviewed commit must be 40 hex')
    listed = {}
    for entry in matrix['runs']:
        keys(entry, ('path', 'bytes', 'sha256'), what='matrix run')
        require(entry['path'] not in listed, 'duplicate matrix run')
        listed[entry['path']] = entry
    present = {'runs/' + p.name for p in (directory / 'runs').iterdir()}
    require(present == set(listed), 'run files differ from matrix.json')
    runs, killed = {}, set()
    for path, entry in sorted(listed.items()):
        require(pin(directory / path, path) == entry, 'run bytes differ from matrix.json: ' + path)
        run = load(directory / path)
        identity = (run.get('case'), run.get('variant'))
        require(path == f'runs/{identity[0]}-{identity[1]}.json', 'run file name differs from its case and variant: ' + path)
        require(identity in rows, 'extra run ' + path)
        require(identity not in runs, 'duplicate run ' + path)
        killed.update(check_run(run, rows[identity], commit, epoch, unit))
        runs[identity] = run
    missing = sorted(set(rows) - set(runs))
    require(not missing, 'missing runs: ' + ', '.join(f'{c}-{v}' for c, v in missing))
    census = matrix['census']
    keys(census, ('points', 'trace'), what='census')
    digest(census['trace'], 'census trace')
    names = []
    for point in census['points']:
        keys(point, ('name', 'occurrences', 'durability'), what='census point')
        require(isinstance(point['name'], str) and point_valid(point['name'], scopes), 'census point outside the registry: ' + str(point['name']))
        require(type(point['occurrences']) is int and point['occurrences'] >= 1, 'census occurrences')
        require(point['durability'] is is_durability(point['name'], scopes), 'census durability differs: ' + point['name'])
        names.append(point['name'])
    require(names == sorted(set(names)), 'census points must be sorted and unique')
    require(matrix['killSet'] == kill_set(census['points']), 'kill set differs from the census')
    if unit:
        outside = sorted(p for p in killed if p not in matrix['killSet'])
        require(not outside, 'killed points outside the kill set: ' + ', '.join(outside))
    elif not deferred:
        uncovered = [p for p in matrix['killSet'] if p not in killed]
        require(not uncovered, 'kill-set points without a process-death run: ' + ', '.join(uncovered))
    absence = matrix['releaseAbsence']
    keys(absence, ('binary', 'profile', 'features', 'strings', 'found', 'featureBuildRefused', 'passed'), what='release absence')
    keys(absence['binary'], ('path', 'bytes', 'sha256'), what='release binary')
    wanted = {'OPENSIP_X9_', *scopes}
    require(absence['profile'] == 'release' and absence['features'] == [] and set(absence['strings']) >= wanted
            and absence['found'] == [] and absence['featureBuildRefused'] is True and absence['passed'] is True, 'release absence did not pass')
    ids = []
    for limit in matrix['limits']:
        keys(limit, ('id', 'reason', 'owner'), what='limit')
        require(isinstance(limit['reason'], str) and limit['reason'] and isinstance(limit['owner'], str) and limit['owner'], 'limit without a reason or owner')
        ids.append(limit['id'])
    require(tuple(ids) == LIMITS, 'limits must be exactly L1..L11 in order')
    return matrix, runs, killed


def check(repository: Path, run_set: Path, repeat: Path, required: Path, commit: str, unit=None):
    scopes = registry(repository)
    rows, epoch = check_required(load(required))
    if unit is not None:
        require(unit in UNIT_CASES, 'unknown unit ' + str(unit))
        rows = {identity: row for identity, row in rows.items() if in_unit(identity, row, unit)}
        require(bool(rows), 'no required runs for ' + unit)
    first, first_runs, _ = check_set(run_set, rows, commit, scopes, epoch, unit is not None)
    second, second_runs, _ = check_set(repeat, rows, commit, scopes, epoch, unit is not None)
    agree(first, first_runs, second, second_runs, rows)
    result = {'passed': True, 'commit': commit, 'runs': len(rows), 'killSet': len(first['killSet']), 'censusPoints': len(first['census']['points']),
              'limits': list(LIMITS), 'repetitionsAgree': True, 'productQualification': False}
    if unit is not None:
        killed = sorted({point for run in first_runs.values() for point in kills(run)})
        result.update({'unit': unit, 'matrixPass': False, 'killedPoints': len(killed),
                       'normalizedSha256': {'-'.join(i): first_runs[i]['postState']['normalizedSha256'] for i in sorted(rows)}})
    return result


def agree(first, first_runs, second, second_runs, rows, what=''):
    """Item 7: the two lead repetitions agree on the census and, run by run,
    on normalizedSha256 (trustState included) and every child's trace
    digest. The timing guard is not compared."""
    require(first['census'] == second['census'], what + 'repetitions disagree on the census')
    for identity in sorted(rows):
        a, b = first_runs[identity], second_runs[identity]
        label = what + '-'.join(identity)
        require(a['postState']['normalizedSha256'] == b['postState']['normalizedSha256'], label + ': repetitions disagree on normalizedSha256')
        require([c['trace'] for c in a['children']] == [c['trace'] for c in b['children']], label + ': repetitions disagree on a trace digest')


def union_points(censuses, scopes):
    """Law X9 r10 (r11): the union of the targets' censuses by point name,
    each point at its largest occurrence count. A point's durability is the
    registry's, so it must be equal in every census that names it."""
    union = {}
    for census in censuses:
        keys(census, ('points', 'trace'), what='census')
        for point in census['points']:
            keys(point, ('name', 'occurrences', 'durability'), what='census point')
            name = point['name']
            require(isinstance(name, str) and point_valid(name, scopes), 'census point outside the registry: ' + str(name))
            require(type(point['occurrences']) is int and point['occurrences'] >= 1, 'census occurrences')
            require(point['durability'] is is_durability(name, scopes), 'census durability differs: ' + name)
            if name in union:
                union[name]['occurrences'] = max(union[name]['occurrences'], point['occurrences'])
            else:
                union[name] = dict(point)
    return [union[name] for name in sorted(union)]


def check_targets(repository: Path, targets, commit: str):
    """Law X9 r10 item 7: the two-target gate. `targets` is a list of
    (name, required, run set, repeat). Each target's rows are checked in its
    own sets exactly as `check` checks one; the coverage is the union
    census's kill set against the process-death runs of every target, in
    each repetition."""
    scopes = registry(repository)
    names = [t[0] for t in targets]
    require(bool(targets) and len(set(names)) == len(names), 'targets must be named once each')
    require(HEX40.fullmatch(commit), 'reviewed commit must be 40 hex')
    epochs, firsts, seconds, report = set(), [], [], {}
    killed = ([], [])
    total = 0
    for name, required, run_set, repeat in targets:
        rows, epoch = check_required(load(required))
        epochs.add(epoch)
        what = name + ': '
        try:
            first, first_runs, first_killed = check_set(run_set, rows, commit, scopes, epoch, deferred=True)
            second, second_runs, second_killed = check_set(repeat, rows, commit, scopes, epoch, deferred=True)
            agree(first, first_runs, second, second_runs, rows)
        except MatrixError as exc:
            raise MatrixError(what + str(exc)) from exc
        firsts.append(first['census'])
        seconds.append(second['census'])
        killed[0].extend(first_killed)
        killed[1].extend(second_killed)
        total += len(rows)
        report[name] = {'runs': len(rows), 'censusPoints': len(first['census']['points']), 'killSet': len(first['killSet']),
                        'killedPoints': len(set(first_killed)), 'censusTrace': first['census']['trace'],
                        'normalizedSha256': {'-'.join(i): first_runs[i]['postState']['normalizedSha256'] for i in sorted(rows)}}
    require(len(epochs) == 1, 'the required-runs files differ on clockEpoch')
    union = union_points(firsts, scopes)
    require(union == union_points(seconds, scopes), 'repetitions disagree on the union census')
    union_kill = kill_set(union)
    for n, points in enumerate(killed, 1):
        uncovered = [p for p in union_kill if p not in set(points)]
        require(not uncovered, f'repetition {n}: union kill-set points without a process-death run: ' + ', '.join(uncovered))
    every = set(killed[0])
    return {'passed': True, 'commit': commit, 'targets': report, 'runs': total, 'unionCensusPoints': len(union),
            'killSet': len(union_kill), 'killedPoints': len(every),
            'killedOutsideKillSet': sorted(every - set(union_kill)), 'limits': list(LIMITS), 'repetitionsAgree': True,
            'matrixPass': sorted(names) == sorted(TARGETS), 'productQualification': False}


def census_of(path: Path):
    """A census as census.json carries it, or as matrix.json does."""
    value = load(path)
    return value['census'] if isinstance(value, dict) and 'census' in value else value


def coverage(repository: Path, targets):
    """Before any run: the union kill set of the targets' censuses against
    the kill scripts of their reviewed required runs. `targets` is a list of
    (name, census file, required). Runs nothing."""
    scopes = registry(repository)
    union = union_points([census_of(census) for _, census, _ in targets], scopes)
    union_kill = kill_set(union)
    killed = {}
    for name, _, required in targets:
        rows, _ = check_required(load(required))
        for identity, row in sorted(rows.items()):
            for point in kills(row):
                killed.setdefault(point, []).append(f'{name}:{identity[0]}-{identity[1]}')
    uncovered = [p for p in union_kill if p not in killed]
    return {'passed': not uncovered, 'unionCensusPoints': len(union), 'killSet': len(union_kill),
            'killedPoints': len(killed), 'uncovered': uncovered,
            'killedOutsideKillSet': sorted(p for p in killed if p not in set(union_kill)), 'matrixPass': False}


def release_absence(repository: Path, binary: Path):
    scopes = registry(repository)
    data = binary.read_bytes()
    wanted = ['OPENSIP_X9_', *sorted(scopes)]
    found = [s for s in wanted if s.encode() in data]
    return {'passed': not found, 'binary': {'path': str(binary), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()},
            'strings': wanted, 'found': found}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)
    run = commands.add_parser('check', help="the M2 exit gate: both targets' lead run sets against their reviewed required runs (X9 r10)")
    run.add_argument('--repository', required=True, type=Path)
    run.add_argument('--target', required=True, action='append', nargs=4, metavar=('NAME', 'REQUIRED', 'RUN_SET', 'REPEAT'),
                     help='once for storage and once for host')
    run.add_argument('--commit', required=True)
    per_unit = commands.add_parser('check-unit', help="check one unit's subset of the required runs (X9 r4 item 7)")
    per_unit.add_argument('--repository', required=True, type=Path)
    per_unit.add_argument('--unit', required=True, choices=sorted(UNIT_CASES))
    per_unit.add_argument('--run-set', required=True, type=Path)
    per_unit.add_argument('--repeat', required=True, type=Path)
    per_unit.add_argument('--required', required=True, type=Path)
    per_unit.add_argument('--commit', required=True, help='the base commit the unit was built on')
    census = commands.add_parser('coverage', help="the union kill set against the required runs' kills, before any run")
    census.add_argument('--repository', required=True, type=Path)
    census.add_argument('--target', required=True, action='append', nargs=3, metavar=('NAME', 'CENSUS', 'REQUIRED'))
    scan = commands.add_parser('release-absence', help='scan a release binary for barrier strings')
    scan.add_argument('--repository', required=True, type=Path)
    scan.add_argument('--binary', required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'check':
            names = sorted(t[0] for t in args.target)
            if names != sorted(TARGETS):
                raise MatrixError('check takes exactly the targets ' + ' and '.join(TARGETS) + ', once each')
            targets = [(name, Path(required), Path(run_set), Path(repeat)) for name, required, run_set, repeat in args.target]
            result = check_targets(args.repository, targets, args.commit)
        elif args.command == 'coverage':
            result = coverage(args.repository, [(name, Path(c), Path(r)) for name, c, r in args.target])
        elif args.command == 'check-unit':
            result = check(args.repository, args.run_set, args.repeat, args.required, args.commit, args.unit)
        else:
            result = release_absence(args.repository, args.binary)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        parser.exit(1, 'crash matrix check refused: ' + str(exc) + '\n')
    print(json.dumps(result, sort_keys=True))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
