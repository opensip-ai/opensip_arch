#!/usr/bin/env python3
"""Execute design fixtures, never a product adapter or qualification harness.

Run from any directory: python3 docs/coop/completion/check_qualification_design.py
Only writes qualification-design-report.v1.json. Inputs and expected outcomes are
separate checked-in files; hostile bytes were authored before this checker.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import io
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import tempfile
import tarfile
import unicodedata

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PLATFORMS = {'macOS-arm64', 'macOS-x86_64', 'Linux-x86_64', 'Linux-arm64'}
SURFACES = dict(zip(['CORE', 'PROTOCOL', 'SEMANTIC', 'LOCK', 'OFFLINE', 'BUNDLE'], [f'SL-{i}' for i in range(1, 7)]))
RESULTS = []


def sha(b):
    return hashlib.sha256(b).hexdigest()


def canon(x):
    # Fixture custody encoding only; does not mint the production metadata profile.
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()


def check(name, observed, expected):
    RESULTS.append({'id': name, 'pass': observed == expected, 'expected': expected, 'observed': observed})


def load(name):
    d = json.loads((HERE / name).read_text())
    for pin in d['sourcePins']:
        check('pin/' + pin['path'], sha((ROOT / pin['path']).read_bytes()), pin['sha256'])
    return d


def capacity(tree):
    for e in tree:
        if len(e['path'].encode()) > 100:
            return 'PATH-EXCEEDS-USTAR-NAME'
        if len(e.get('target', '').encode()) > 100:
            return 'LINKTARGET-EXCEEDS-USTAR-LINKNAME'
        if e['mode'] < 0 or e['mode'] > 2097151:
            return 'MODE-EXCEEDS-USTAR-FIELD'
        if e.get('length', 0) < 0 or e.get('length', 0) > 8589934591:
            return 'SIZE-EXCEEDS-USTAR-FIELD'
    return 'ACCEPT'


def octal(field, width):
    if len(field) != width or not re.fullmatch(b'[0-7]{' + str(width - 1).encode() + b'}\x00', field):
        raise ValueError('noncanonical octal')
    return int(field[:-1], 8)


def string_field(field):
    parts = field.split(b'\0', 1)
    if len(parts) == 2 and parts[1] != bytes(len(parts[1])):
        raise ValueError('embedded data after NUL')
    return parts[0].decode('utf-8', 'strict')


def admit_archive(data, tree):
    """Independent field-by-field decoder, not comparison with our encoder."""
    try:
        offset = 0
        for e in sorted(tree, key=lambda e: e['path']):
            h = data[offset:offset + 512]
            if len(h) != 512 or h == bytes(512):
                raise ValueError('missing member')
            if string_field(h[:100]) != e['path']:
                raise ValueError('path')
            if octal(h[100:108], 8) != e['mode']:
                raise ValueError('mode')
            for a, b in [(108, 116), (116, 124), (329, 337), (337, 345)]:
                if octal(h[a:b], 8) != 0:
                    raise ValueError('nonzero identity field')
            if octal(h[136:148], 12) != 0:
                raise ValueError('mtime')
            size = octal(h[124:136], 12)
            if size != (e['length'] if e['type'] == 'file' else 0):
                raise ValueError('size')
            if not re.fullmatch(b'[0-7]{6}\x00 ', h[148:156]):
                raise ValueError('checksum encoding')
            if int(h[148:154], 8) != sum(h[:148] + b' ' * 8 + h[156:]):
                raise ValueError('checksum')
            if h[156:157] != {'file': b'0', 'dir': b'5', 'symlink': b'2'}[e['type']]:
                raise ValueError('type')
            if string_field(h[157:257]) != e.get('target', ''):
                raise ValueError('target')
            if h[257:265] != b'ustar\x0000':
                raise ValueError('magic/version')
            if h[265:329] != bytes(64) or h[345:] != bytes(167):
                raise ValueError('noncanonical reserved fields')
            offset += 512
            body = data[offset:offset + size]
            if e['type'] == 'file' and (len(body) != size or sha(body) != e['sha256'] or body != bytes.fromhex(e['bodyHex'])):
                raise ValueError('body')
            pad = (-size) % 512
            if data[offset + size:offset + size + pad] != bytes(pad):
                raise ValueError('body padding')
            offset += size + pad
        if data[offset:] != bytes(1024):
            raise ValueError('extra/missing member, trailer or EOF')
        return 'ACCEPT'
    except (ValueError, KeyError, UnicodeError):
        return 'REFUSE'


def library_cross_decode(data, tree):
    """Second implementation (stdlib tarfile) verifies fixed-vector semantics."""
    observed = []
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:') as tf:
        for member in tf.getmembers():
            kind = 'file' if member.isfile() else 'dir' if member.isdir() else 'symlink' if member.issym() else 'other'
            observed.append({'path': member.name, 'type': kind, 'mode': member.mode,
                             'bodyHex': tf.extractfile(member).read().hex() if member.isfile() else '',
                             'target': member.linkname})
    expected = [{'path': e['path'], 'type': e['type'], 'mode': e['mode'], 'bodyHex': e.get('bodyHex', ''), 'target': e.get('target', '')}
                for e in sorted(tree, key=lambda e: e['path'])]
    return observed == expected


def library_encode_fixed_vector(tree):
    """A second design encoder uses stdlib ustar header construction.

    tarfile's defaults permit encodings forbidden by profile.1; fix the two
    documented differences (directory slash and device numeric zeros), then
    recompute checksum. This is not a production Rust adapter execution.
    """
    out = bytearray()
    for e in sorted(tree, key=lambda e: e['path']):
        info = tarfile.TarInfo(e['path'])
        info.mode = e['mode']
        info.type = {'file': tarfile.REGTYPE, 'dir': tarfile.DIRTYPE, 'symlink': tarfile.SYMTYPE}[e['type']]
        info.size = e.get('length', 0)
        info.linkname = e.get('target', '')
        h = bytearray(info.tobuf(format=tarfile.USTAR_FORMAT, encoding='utf-8', errors='strict'))
        h[:100] = e['path'].encode().ljust(100, b'\0')
        h[329:345] = b'0000000\0' * 2
        h[148:156] = b' ' * 8
        h[148:156] = (f'{sum(h):06o}\0 ').encode()
        out.extend(h)
        body = bytes.fromhex(e.get('bodyHex', ''))
        out.extend(body)
        out.extend(bytes((-len(body)) % 512))
    out.extend(bytes(1024))
    return bytes(out)


def path_diagnostics(case):
    diagnostics = set()
    paths = case['paths']
    normalized = []
    folded = []
    for p in paths:
        if not p or p.startswith('/') or '\\' in p or '\0' in p or re.match(r'^[A-Za-z]:', p) or any(s in ('', '.', '..') for s in p.split('/')):
            diagnostics.add('syntax')
        n = unicodedata.normalize('NFC', p)
        if n != p:
            diagnostics.add('non-NFC')
        normalized.append(n)
        folded.append(n.casefold())
    if len(set(paths)) != len(paths):
        diagnostics.add('byte-duplicate')
    if len(set(normalized)) != len(normalized):
        diagnostics.add('normalization-duplicate')
    if len(set(folded)) != len(folded):
        diagnostics.add('casefold-duplicate')
    if case['entrypoint'] not in paths:
        diagnostics.add('entrypoint-absent')
    if 'symlink' in case:
        s = case['symlink']
        depth = len(s['path'].split('/')) - 1
        for part in s['target'].split('/'):
            depth += -1 if part == '..' else 0 if part == '.' else 1
            if depth < 0:
                diagnostics.add('symlink-escape')
    return sorted(diagnostics)


def symlink_boundary(case):
    parts = case['entry'].split('/')[:-1]
    within = True
    for part in case['target'].split('/'):
        if part == '..':
            if not parts:
                within = False
                break
            parts.pop()
        elif part not in ('', '.'):
            parts.append(part)
    declared = within and '/'.join(parts) in case['declaredPaths']
    grammar = not any(part in ('', '.', '..') for part in case['target'].split('/'))
    return {'withinRoot': within, 'targetDeclared': declared,
            'inheritedV11Admission': 'ACCEPT' if within and declared and grammar else 'RJ-3'}


def at_result(kind, x):
    if kind == 'assembly':
        return 'RJ-5' if x['networkAttempts'] else 'ACCEPT' if set(x['present']) == {'manifest', 'tree', 'archive', 'archiveDigest', 'declarations'} else 'REFUSE'
    if kind == 'ambient':
        return 'RJ-5' if x['implicitDownloads'] else 'ACCEPT' if x['declaredInputsComplete'] and not any(x[k] for k in ['ambientPath', 'ambientRuntime', 'projectPackages']) else 'REFUSE'
    if kind == 'health-record':
        h = x.get('health', {})
        valid = bool(x.get('roleSubprotocol')) and bool(x.get('subprotocolVersion'))
        if h.get('standing') in ['executed-pass', 'executed-fail']:
            valid = valid and isinstance(h.get('path'), str) and bool(re.fullmatch(r'[0-9a-f]{64}', h.get('sha256', '')))
        elif h.get('standing') in ['not-applicable', 'blocked-on-ride']:
            valid = valid and h.get('ride') == 'AT-4/ID-DEP-P4'
        else:
            valid = False
        return 'ACCEPT' if valid else 'REFUSE'
    if kind == 'trusted-install':
        return 'ACCEPT' if all(x[k] for k in ['signatureValid', 'currentTrustPermits', 'completeClosure']) and x['networkAttempts'] == 0 else 'REFUSE'
    if kind == 'negotiation':
        return 'ACCEPT' if x['pinnedRole'] == x['offeredRole'] and x['pinnedVersion'] == x['confirmedVersion'] and not x['dataBeforeSelectAck'] else 'REFUSE'
    if kind == 'rollback':
        return 'ACCEPT' if x['oldDigest'] == x['oldPostDigest'] and x['targetVerified'] and x['currentTrustPermits'] and x['trustEpochAfter'] >= x['trustEpochBefore'] and not x['updateDataPresent'] else 'REFUSE'
    if kind == 'gate-result':
        return 'ACCEPT' if all(x['results'].get(k, {}).get('standing') == 'pass' and x['results'][k].get('custodyVerified') and re.fullmatch('[0-9a-f]{64}', x['results'][k].get('sha256', '')) for k in x['applicable']) else 'REFUSE'
    raise ValueError('unimplemented AT class ' + kind)


def select_ci(r):
    components = set(r['previousComponents']) | set(r['currentComponents'])
    all_lanes = components | set(SURFACES.values())
    refusal = not r['complete'] or r.get('missingDeclaration') or r['predicate'] != 2 or not r['dependencyCustodyValid']
    refusal = refusal or set(r['consumers']) != set(SURFACES) or set(r['dependencies']) != components
    for c in components:
        ps = r['platforms'].get(c, [])
        roles = r['roles'].get(c, [])
        refusal = refusal or not ps or not set(ps) <= PLATFORMS or not roles or not set(roles) <= {'TypeScript', 'ROLELESS-NA'}
        refusal = refusal or ('ROLELESS-NA' in roles and roles != ['ROLELESS-NA'])
        refusal = refusal or not set(r['dependencies'].get(c, [])) <= components
    for consumers in r['consumers'].values():
        refusal = refusal or not set(consumers) <= components
    changed = set(r['changed'])
    if r['recordChanged']:
        changed |= set(r['previousOwners']) | set(r['currentOwners'])
    # The committed unit inventory is independent of the owner map; a missing
    # untouched unit cannot silently erase its owner requirement.
    for units, owners in [(r['previousUnits'], r['previousOwners']), (r['currentUnits'], r['currentOwners'])]:
        refusal = refusal or set(units) != set(owners) or any(not owners.get(u) for u in units)
    selected, conflict = set(), False
    for unit in changed:
        owners = r['currentOwners'].get(unit, r['previousOwners'].get(unit, []))
        refusal = refusal or not owners or not set(owners) <= components | set(SURFACES)
        conflict = conflict or len(owners) > 1
        for owner in owners:
            selected.add(SURFACES.get(owner, owner))
    if refusal:
        return {'selected': [], 'ambiguity': 'refuse-only'}
    if conflict:
        return {'selected': sorted(all_lanes), 'ambiguity': 'conflict-universe'}
    while True:
        before = selected.copy()
        for c, dependencies in r['dependencies'].items():
            if selected.intersection(dependencies):
                selected.add(c)
        for surface, consumers in r['consumers'].items():
            if SURFACES[surface] in selected:
                selected.update(consumers)
        if len(selected & components) >= 2:
            selected.update(['SL-2', 'SL-3', 'SL-4'])
        if selected == before:
            return {'selected': sorted(selected), 'ambiguity': 'none'}


def lane_evidence_ok(record, decision, envelope, fdb_digest):
    """Check joins and standing after the separate trust verifier's observation.

    SignatureVerified is an observation input, not fabricated cryptographic proof.
    Future G16 must supply real detached signatures from the security profile.
    """
    universe = set(record['previousComponents']) | set(record['currentComponents']) | set(SURFACES.values())
    inputs = {'ownership': sha(canon(record)), 'dependencies': sha(canon(record['dependencies'])),
              'changeSet': sha(canon(record['changed'])), 'fixtureDomainBasis': fdb_digest}
    if envelope.get('inputsDigest') != sha(canon(inputs)):
        return False
    if envelope.get('selectorDecisionDigest') != sha(canon({'decision': decision, 'inputs': inputs})):
        return False
    if set(envelope.get('lanes', {})) != universe:
        return False
    for lane, result in envelope['lanes'].items():
        if lane in decision['selected']:
            if result.get('selectorDecisionDigest') != envelope['selectorDecisionDigest']:
                return False
            if result.get('standing') == 'blocked-on-ride' and lane in ['SL-5', 'SL-6']:
                continue
            if result.get('standing') != 'pass' or result.get('signatureVerified') is not True:
                return False
        elif result.get('standing') != 'skipped-proof' or result.get('rule') != 'no-fixedpoint-selection':
            return False
    aggregate = envelope.get('aggregate')
    if aggregate and (aggregate.get('selectorDecisionDigest') != envelope['selectorDecisionDigest'] or aggregate.get('route') == 'bundle-only'):
        return False
    return True


def evidence(record, decision, fdb_digest):
    inputs = {'ownership': sha(canon(record)), 'dependencies': sha(canon(record['dependencies'])),
              'changeSet': sha(canon(record['changed'])), 'fixtureDomainBasis': fdb_digest}
    d = sha(canon({'decision': decision, 'inputs': inputs}))
    universe = set(record['previousComponents']) | set(record['currentComponents']) | set(SURFACES.values())
    return {'inputsDigest': sha(canon(inputs)), 'selectorDecisionDigest': d,
            'lanes': {l: ({'standing': 'pass', 'signatureVerified': True, 'selectorDecisionDigest': d}
                          if l in decision['selected'] else {'standing': 'skipped-proof', 'rule': 'no-fixedpoint-selection'}) for l in universe},
            'aggregate': {'selectorDecisionDigest': d, 'route': 'individual-signed-release'}}


def recover(events):
    # Volatile selection writes are discarded until the SQLite commit record is durable.
    persistent = {'selection': 'g-old', 'operationSelection': 'g-old', 'trustEpoch': 8}
    prepared, ready, committed = False, False, False
    for event in events:
        if event == 'record-PREPARING':
            prepared = True
        if event == 'record-READY':
            ready = True
        if event == 'commit-selection-WAL':
            if not ready:
                raise ValueError('commit without complete READY closure')
            committed = True
    if committed:
        persistent['selection'] = 'g-new'
    persistent['newTreeMayBeCollected'] = not prepared  # prepared/READY transitions remain GC roots until explicit abort cleanup
    persistent['quarantineRequired'] = prepared and not ready
    return persistent


def lifecycle_property(x):
    k = x['case']
    if k == 'cas':
        return 'ACCEPT' if x['actualOld'] == x['expectedOld'] else 'REFUSE'
    if k == 'gc':
        return 'KEEP' if x['roots'] else 'DELETE'
    if k == 'reap':
        return 'KEEP' if x['osLeaseHeld'] else 'REAP'
    if k == 'rollback':
        return 'ACCEPT' if x['targetVerified'] and x['permittedNow'] and x['trustAfter'] >= x['trustBefore'] else 'REFUSE'
    if k == 'recovery':
        return 'REFUSE' if not x['databaseReadable'] else 'QUARANTINE' if not x['treeVerified'] or not x['currentTrust'] else 'ACCEPT'
    if k == 'staging':
        return 'ACCEPT' if x['sameFilesystem'] else 'REFUSE'
    if k == 'migration':
        return 'ACCEPT' if not x['noReturn'] and x['observedState'] == ('new' if x['phase'] == 'commit' else x['oldState']) else 'REFUSE'
    raise ValueError(k)


def sqlite_process_death_checks():
    """Actual local SQLite rollback-on-process-exit evidence, not power-loss proof."""
    with tempfile.TemporaryDirectory(prefix='opensip-design-sqlite-') as td:
        db = Path(td) / 'lifecycle.sqlite'
        con = sqlite3.connect(db)
        con.executescript("""
          PRAGMA journal_mode=WAL;
          PRAGMA synchronous=FULL;
          CREATE TABLE selection(project TEXT PRIMARY KEY, generation TEXT NOT NULL);
          CREATE TABLE operation(id TEXT PRIMARY KEY, generation TEXT NOT NULL);
          CREATE TABLE transition(id TEXT PRIMARY KEY, phase TEXT NOT NULL);
          INSERT INTO selection VALUES ('A','g-old'), ('B','g-other');
          INSERT INTO operation VALUES ('already-running','g-old');
          INSERT INTO transition VALUES ('tx','READY');
        """)
        con.commit()
        con.close()
        child = """
import os,sqlite3,sys
c=sqlite3.connect(sys.argv[1]); c.execute('PRAGMA synchronous=FULL')
c.execute('BEGIN IMMEDIATE')
c.execute("UPDATE selection SET generation='g-new' WHERE project='A' AND generation='g-old'")
c.execute("UPDATE transition SET phase='COMMITTED' WHERE id='tx'")
if sys.argv[2]=='after-commit': c.commit()
os._exit(71)
"""
        for phase, generation, txphase in [('before-commit','g-old','READY'), ('after-commit','g-new','COMMITTED')]:
            proc = subprocess.run([sys.executable, '-c', child, str(db), phase], check=False)
            check('lifecycle/sqlite/' + phase + '/process-exit', proc.returncode, 71)
            con = sqlite3.connect(db)
            observed = {'selection': dict(con.execute('SELECT project,generation FROM selection')),
                        'operation': dict(con.execute('SELECT id,generation FROM operation')),
                        'transition': dict(con.execute('SELECT id,phase FROM transition'))}
            check('lifecycle/sqlite/' + phase + '/atomic-recovery', observed,
                  {'selection': {'A':generation,'B':'g-other'}, 'operation': {'already-running':'g-old'}, 'transition': {'tx':txphase}})
            con.close()


def cycles(graph):
    for start in graph:
        seen, todo = set(), [start]
        while todo:
            node = todo.pop()
            for target in graph.get(node, []):
                if target == start:
                    return True
                if target not in seen:
                    seen.add(target)
                    todo.append(target)
    return False


def manifest_predicates(m, index=None):
    """Selected v11 semantic rules. Not a replacement for its complete schema."""
    errors = set()
    if not {'stableId', 'name', 'version', 'commands', 'platforms', 'provenance'} <= set(m):
        return {'MALFORMED-MANIFEST'}
    commands = m['commands']
    roots = [c for c in commands if 'parent' not in c]
    if len(roots) != 1:
        errors.add('RJ-2/MULTIPLE_ROOT_COMMANDS')
    elif roots[0]['name'] != m['name']:
        errors.add('RJ-2/ROOT_COMMAND_NAME_MISMATCH')
    if m['name'] in (m['version'], m['stableId']):
        errors.add('RJ-2/ID_VERSION_INDISTINCT')
    pairs = [(c.get('parent'), c['name']) for c in commands]
    if len(set(pairs)) != len(pairs):
        errors.add('RJ-2/PARENT_LINKAGE_COLLISION')
    names = {c['name'] for c in commands}
    parent = {c['name']: [c['parent']] for c in commands if 'parent' in c}
    if any(c['parent'] not in names for c in commands if 'parent' in c) or cycles(parent):
        errors.add('RJ-2/PARENT_UNKNOWN_OR_CYCLIC')
    aliases = {c['name']: c.get('aliases', []) for c in commands}
    if cycles(aliases):
        errors.add('RJ-2/ALIAS_CYCLE')
    for platform in m['platforms']:
        entries = platform['tree']['entries']
        path_case = {'paths': [e['path'] for e in entries], 'entrypoint': platform['entrypoint']}
        if path_diagnostics(path_case):
            errors.add('RJ-3')
        for e in entries:
            if e['type'] == 'symlink':
                case = dict(path_case, symlink={'path': e['path'], 'target': e['target']})
                # v11 target admission forbids traversal segments too; this does
                # not claim ../outside from bin/ escapes the package root.
                if path_diagnostics(case) or '..' in e['target'].split('/'):
                    errors.add('RJ-3')
    for key in ['stateMigration', 'updateData']:
        if key in m and (m[key].get('reserved') is not True or set(m[key]) != {'reserved', 'ridesOn'}):
            errors.add('RJ-6/RESERVED_FIELD_POPULATED')
    if index:
        for row in index['entries'] + index.get('retiredIds', []):
            if row['stableId'] == m['stableId'] and row['provenance'] != m['provenance']:
                errors.add('RJ-1')
        reserved = set(index['reservedRootCommands'])
        if m['name'] in reserved:
            errors.add('RJ-2/RESERVED_ROOT_COMMAND')
        others = [e for e in index['entries'] if e['stableId'] != m['stableId']]
        live = {e['namesSnapshot']['name'] for e in others} | {e['mountedRootCommand'] for e in others}
        old_aliases = {a for e in others for a in e['namesSnapshot'].get('aliases', [])}
        if m['name'] in live:
            errors.add('RJ-2/LIVE_NAME_COLLISION')
        if set(m.get('aliases', [])) & old_aliases:
            errors.add('RJ-2/ALIAS_COLLISION')
        if set(m.get('aliases', [])) & (live | reserved):
            errors.add('RJ-2/ALIAS_SHADOWS_LIVE_OR_RESERVED')
    return errors


def inherited_predicate(path):
    """Never reads expected fields as an oracle; returns independently observed rules."""
    raw = path.read_bytes()
    duplicates = []
    def pairs(ps):
        out = {}
        for key, value in ps:
            if key in out:
                duplicates.append(key)
            out[key] = value
        return out
    d = json.loads(raw, object_pairs_hook=pairs)
    if duplicates:
        return {'RJ-6/DUPLICATE_JSON_KEY'}, {'duplicatedKeys': duplicates}
    parent = path.parent
    def read(p):
        resolved = next((d[k + 'Resolved'] for k in d if k.endswith('Path') and d[k] == p and k + 'Resolved' in d), None)
        return json.loads((ROOT / resolved if resolved else parent / p).read_text())
    kind = d.get('kind')
    if kind == 'component':
        return manifest_predicates(d) or {'ACCEPT'}, {}
    if 'indexSchemaVersion' in d:
        # Validate only index custody shape. External declarations are dummy
        # placeholders in the old corpus, not actual qualification evidence.
        good = all({'stableId', 'version', 'manifestDigest', 'signatureRef', 'namesSnapshot', 'provenance'} <= set(e) and re.fullmatch('[0-9a-f]{64}', e['manifestDigest']) for e in d['entries'])
        return {'ACCEPT'} if good else {'MALFORMED-INDEX'}, {}
    if kind == 'admission-against-index':
        return manifest_predicates(read(d['manifestPath']), read(d['indexPath'])) or {'ACCEPT'}, {}
    if kind == 'admission-packet':
        if d.get('policyRequiresSignature') and d.get('signatureEnvelope') is None:
            return {'RJ-4/UNSIGNED'}, {}
        actual = sha((parent / d['manifestPath']).read_bytes())
        return {'RJ-4/DIGEST_MISMATCH'} if actual != d['manifestDigest'] else {'ACCEPT'}, {}
    if kind == 'alias-resolve':
        index = read(d['indexPath'])
        for e in index['entries']:
            deprecation = e.get('deprecation', {})
            if deprecation.get('oldName') == d['alias']:
                old_minor = tuple(map(int, deprecation['deprecatedAtRelease'].split('.')[:2]))
                now_minor = tuple(map(int, d['hostCoreVersion'].split('.')[:2]))
                time_expired = d['asOf'] >= deprecation['windowEndsNoEarlierThan']
                minor_elapsed = now_minor > old_minor
                return {'typed non-resolve' if time_expired and minor_elapsed else 'RESOLVE'}, {}
        return {'typed non-resolve'}, {}
    if kind == 'reserved-list-live-grammar-parity':
        a, b = read(d['indexPath']), read(d['liveGrammarPath'])
        return {'ACCEPT iff lists equal'} if sorted(a['reservedRootCommands']) == sorted(b['reservedRootCommands']) else {'REFUSE (lists unequal)'}, {}
    if kind == 'scope-precedence':
        rows = read(d['indexPath'])['entries']
        disclosed = any(e.get('scope') == 'global' and e.get('shadowedBy', {}).get('scope') == 'project' and any(p['scope'] == 'project' and p['stableId'] == e['shadowedBy']['stableId'] for p in rows) for e in rows)
        return {'DISCLOSE'} if disclosed else {'MISSING-DISCLOSURE'}, {}
    if kind == 'resolution-packet':
        if 'discoveredEdge' in d:
            m = read(d['rootManifestPath'])
            missing = d['discoveredEdge']['toStableId'] not in {x['stableId'] for x in m['dependencies']}
        else:
            missing = d['declaredStableId'] not in {e['stableId'] for e in read(d['indexPath'])['entries']}
        return {'RJ-5'} if missing else {'ACCEPT'}, {}
    if kind == 'implicit-download-attempt':
        rejected = d['attempt']['method'] == 'network-fetch'
        remediation = d['typedRemediation']['code'] == 'RJ-5' and bool(d['typedRemediation']['remediation'])
        return {'RJ-5 plus typed remediation'} if rejected and remediation else {'REFUSE-WITHOUT-REMEDIATION'}, {'standing': 'Input/specification checked; no network attempt executed'}
    if kind == 'no-execution-during-admission-probe':
        recorder = d['containsExecutable']
        ok = sha((parent / recorder['path']).read_bytes()) == recorder['sha256'] and sha((parent / recorder['recorderLog']).read_bytes()) == recorder['recorderLogInitialSha256'] and set(d['operations']) == {'admission', 'discovery', 'help', 'completion', 'inventory'}
        return {'PROBE-SPEC-VALID'} if ok else {'PROBE-SPEC-INVALID'}, {'standing': 'NOT-EXECUTED; empty initial recorder is not evidence of product non-execution'}
    if kind == 'digest-recompute':
        ok = all(sha((parent / d[k + 'Path']).read_bytes()) == d[k + 'Digest'] for k in ['manifest', 'index', 'envelope'])
        return {'ACCEPT'} if ok else {'DIGEST-MISMATCH'}, {}
    return {'UNSUPPORTED-FIXTURE-KIND'}, {'kind': kind}


def inherited_schema_checks():
    join = load('qualification-design-schema-join.v1.json')
    check('schema-join/53-keys', len(join['definitions']), 53)
    for item in join['authoredInputs']:
        path = ROOT / item['path']
        check('inherited/' + item['id'] + '/pin', sha(path.read_bytes()), item['sha256'])
        outcomes, details = inherited_predicate(path)
        expected = 'PROBE-SPEC-VALID' if item['id'] == 'TC-METADATA-ONLY.no-execution' else item['expected']
        check('inherited/' + item['id'] + '/predicate', expected in outcomes, True)
        if details:
            RESULTS[-1]['scope'] = details
    for pin in join['supportingPins']:
        check('inherited-support/' + pin['path'], sha((ROOT / pin['path']).read_bytes()), pin['sha256'])
    for key, definition in join['definitions'].items():
        for ref in definition['inputs']:
            p = ROOT / ref['path']
            check('schema-join/' + key + '/input-present', p.is_file(), True)
            if 'sha256' in ref:
                check('schema-join/' + key + '/input-pin', sha(p.read_bytes()), ref['sha256'])
            if 'selector' in ref:
                obj = json.loads(p.read_text())
                try:
                    for bit in ref['selector'].split('/')[1:]:
                        obj = obj[int(bit)] if isinstance(obj, list) else obj[bit]
                    found = True
                except (KeyError, IndexError, ValueError, TypeError):
                    found = False
                check('schema-join/' + key + '/selector-resolves', found, True)
    # A missing manifest/index digest may not hide behind a well-shaped declaration.
    for item in join['authoredInputs']:
        if item['id'].startswith('TC-ACCEPT.') and item['path'].endswith('.manifest.json'):
            data = json.loads((ROOT / item['path']).read_text())
            check('inherited/' + item['id'] + '/declaration-placeholder-honesty',
                  all(v.get('path') == 'dummy.empty' for v in data['declarations'].values() if isinstance(v, dict) and 'path' in v), True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, default=HERE / 'qualification-design-report.v1.json', help='Write replay report here, e.g. /tmp/qualification-replay.json, without changing frozen evidence')
    args = parser.parse_args()
    inherited_schema_checks()
    p = load('qualification-design-packaging.v1.json')
    definitions = set(p['atHalves']) | {a['id'] for a in p['archiveCases'] if a['id'].startswith('AT-')}
    check('packaging/AT-key-count', len(definitions), 27)
    for a in p['archiveCases']:
        cap = capacity(a['tree'])
        result = cap
        if 'archive' in a:
            b = (ROOT / a['archive']['path']).read_bytes()
            check(a['id'] + '/pin', sha(b), a['archive']['sha256'])
            result = admit_archive(b, a['tree']) if cap == 'ACCEPT' else cap
            if a['id'] == 'AT-ARCHIVE-FIXED-VECTOR':
                check(a['id'] + '/golden-digest', sha(b), a['expectedArchiveDigest'])
                check(a['id'] + '/stdlib-decoder', library_cross_decode(b, a['tree']), True)
                check(a['id'] + '/second-design-encoder', sha(library_encode_fixed_vector(a['tree'])), a['expectedArchiveDigest'])
        check(a['id'], result, a['expected'])
    for x in p['pathCases']:
        ds = path_diagnostics(x)
        check(x['id'], 'RJ-3' if ds else 'ACCEPT', x['expected'])
        if x['id'] == 'TC-PATH.11':
            check(x['id'] + '/two-diagnostics', {'non-NFC', 'normalization-duplicate'} <= set(ds), True)
    for x in p['symlinkBoundaryCases']:
        check(x['id'], symlink_boundary(x), x['expected'])
    for key, x in p['atHalves'].items():
        if x['kind'] == 'path-corpus':
            check(key, 'ALL-REFUSE' if all(path_diagnostics(c) for c in p['pathCases']) else 'FAIL', x['expected'])
        else:
            check(key + '/positive', at_result(x['kind'], x['input']), x['expected'])
            check(key + '/negative', at_result(x['kind'], x['negative']), x['negativeExpected'])
    keys = set(json.loads((ROOT / p['sourcePins'][0]['path']).read_text())['conformanceReport']['fixtureMemberMap']['members'])
    cells = set()
    for cell in p['matrix']:
        check(cell['id'] + '/80-keys', set(cell['members']) == keys, True)
        check(cell['id'] + '/27-defined-AT', set(cell['members']) & definitions == definitions, True)
        env = cell['environment']
        check(cell['id'] + '/offline-inputs', env['network'] == 'DENIED' and not env['ambientPath'], True)
        check(cell['id'] + '/prior-preserved', env['expectedPriorAfter'], env['priorTuple']['sha256'] if env['state'] == 'upgrade' else None)
        cells.update((cell['id'], k) for k in definitions)
    check('packaging/324-distinct-AT-cells', len(cells), 324)
    check('packaging/960-distinct-report-slots', sum(len(c['members']) for c in p['matrix']), 960)

    ci = load('qualification-design-ci.v1.json')
    fdb = ci['fixtureDomainBasis']
    check('ci/FDB-digest', sha(canon(fdb)), ci['fixtureDomainBasisSha256'])
    check('ci/FDB-count', len(fdb), 120)
    check('ci/FDB-unique', len({tuple(x[k] for k in ['component', 'role', 'platform', 'changeClass']) for x in fdb}), len(fdb))
    cases = {x['id']: x for x in ci['cases']}
    for x in ci['cases']:
        check('ci/' + x['id'], select_ci(x['input']), x['expected'])
    for cell in fdb:
        x = cases[cell['fixture']]
        # C-A-ONLY and related templates target the cell's component; the twin
        # cell is a real identity permutation, not a relabelled duplicate.
        if cell['component'] == ci['axis']['qualificationOnlyTrustedTwin']:
            encoded = json.dumps(x)
            encoded = encoded.replace(ci['axis']['shippingComponent'], '__SWAP__')
            encoded = encoded.replace(ci['axis']['qualificationOnlyTrustedTwin'], ci['axis']['shippingComponent'])
            x = json.loads(encoded.replace('__SWAP__', ci['axis']['qualificationOnlyTrustedTwin']))
            x['expected']['selected'].sort()
        check('ci/FDB/' + '/'.join(cell[k] for k in ['component', 'role', 'platform', 'changeClass']), select_ci(x['input']), x['expected'])
    # Hostile declarations cannot redefine the pre-mutation domain.
    reduced = fdb[:-1]
    check('ci/FDB-shortfall-rejected', sha(canon(reduced)) != ci['fixtureDomainBasisSha256'], True)
    check('ci/deferred-slot-domain', [x['id'] for x in ci['deferredSlots']], ['DEF-WIN'])
    for x in ci['independentReleases']:
        check('ci/' + x['id'], 'ACCEPT' if x['supported'] and x['route'] not in ['same-version-required', 'bundle-only'] else 'REFUSE', x['expected'])
    base = cases['C-AGGREGATE-RELEASE']
    record, decision = base['input'], base['expected']
    envelope = evidence(record, decision, ci['fixtureDomainBasisSha256'])
    check('ci/G16-evidence-positive', lane_evidence_ok(record, decision, envelope, ci['fixtureDomainBasisSha256']), True)
    attacks = ['omit-lane', 'wrong-lane-decision', 'wrong-inputs', 'bad-signature', 'required-blocked', 'missing-skipped-proof', 'wrong-aggregate-decision', 'bundle-only']
    for attack in attacks:
        e = copy.deepcopy(envelope)
        if attack == 'omit-lane': del e['lanes']['SL-1']
        if attack == 'wrong-lane-decision': e['lanes']['SL-2']['selectorDecisionDigest'] = '0' * 64
        if attack == 'wrong-inputs': e['inputsDigest'] = '0' * 64
        if attack == 'bad-signature': e['lanes']['SL-2']['signatureVerified'] = False
        if attack == 'required-blocked': e['lanes']['SL-2']['standing'] = 'blocked-on-ride'
        if attack == 'missing-skipped-proof': e['lanes']['SL-1'] = {}
        if attack == 'wrong-aggregate-decision': e['aggregate']['selectorDecisionDigest'] = '0' * 64
        if attack == 'bundle-only': e['aggregate']['route'] = 'bundle-only'
        check('ci/G16-evidence/' + attack, lane_evidence_ok(record, decision, e, ci['fixtureDomainBasisSha256']), False)

    life = load('qualification-design-lifecycle.v1.json')
    for x in life['crashCases']:
        check('lifecycle/' + x['id'], recover(x['events']), x['expected'])
    for x in life['propertyCases']:
        check('lifecycle/' + x['id'], lifecycle_property(x), x['expected'])
    initial = life['initial']
    sqlite_process_death_checks()
    check('lifecycle/mixed-closure-rejected', dict(initial['oldClosure'], executable='exe2') in [initial['oldClosure'], initial['newClosure']], False)
    files = sorted(HERE.glob('qualification-design-*.v1.json'))
    files = [f for f in files if f.name not in {'qualification-design-report.v1.json', 'qualification-design-freeze.v1.json'}] + [Path(__file__)]
    report = {'standing': 'DESIGN-CHECKER-RESULT-NOT-PRODUCT-QUALIFICATION', 'passed': sum(x['pass'] for x in RESULTS), 'total': len(RESULTS),
              'sourcePins': [{'path': str(f.relative_to(ROOT)), 'sha256': sha(f.read_bytes())} for f in files],
              'limitations': ['No product adapter, OS process isolation, real power-loss, native platform qualification or release signing was executed.',
                              'Archive identity fixture fixes bytes and validates with independent decoders; two actual adapter runs remain G15 execution.',
                              'AT halves and G16 signatureVerified fields are observation predicates with positive/hostile inputs, not measurements of product behavior.',
                              'G16 shipping axis has one TypeScript component; a qualification-only trusted TypeScript twin exercises dependency and independent-release classes.',
                              'The 120 FDB cells run platform-neutral selector logic; no native platform qualification is implied.',
                              'Lifecycle model uses atomic durable SQLite transaction semantics; actual fault injection must validate those assumptions on each supported filesystem.',
                              'Unicode checks exercise named examples; they do not validate the entire Unicode 15.1 casefold table.'], 'results': RESULTS}
    args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(f"Design checks: {report['passed']}/{report['total']} passed; product qualification NOT CLAIMED")
    for x in RESULTS:
        if not x['pass']: print(json.dumps(x))
    return 0 if report['passed'] == report['total'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
