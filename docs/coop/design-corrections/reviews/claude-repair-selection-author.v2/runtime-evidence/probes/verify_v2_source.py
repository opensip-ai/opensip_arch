"""Verify the v2 author source is an exact copy of the completed v1 handoff source."""
import hashlib, json, os

V2 = '/tmp/opensip-design-corrections/repair-selection-successor.v2/source'
V2_CUSTODY = '/tmp/opensip-design-corrections/repair-selection-successor.v2/input-custody.json'
V1 = '/tmp/opensip-design-corrections/repair-selection-successor.v1/source'
V1_HANDOFF = '/tmp/opensip-design-corrections/claude-repair-selection-author.v1/changed-file-handoff.json'
HERE = os.path.dirname(os.path.abspath(__file__))


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


custody = json.load(open(V2_CUSTODY))
declared = {f['path']: f for f in custody['files']}

present = {}
for dp, _d, fs in os.walk(V2):
    for n in fs:
        full = os.path.join(dp, n)
        present[os.path.relpath(full, V2)] = {'sha256': sha(full), 'bytes': os.path.getsize(full)}

mismatch = [p for p, row in declared.items()
            if p not in present or present[p]['sha256'] != row['sha256']]
extra = sorted(set(present) - set(declared))
missing = sorted(set(declared) - set(present))

print('custody declares', len(declared), '| v2 tree has', len(present))
print('custody mismatches', len(mismatch), mismatch[:5])
print('extra', len(extra), extra[:5])
print('missing', len(missing), missing[:5])

# v2 must equal v1 byte for byte
v1_present = {}
if os.path.isdir(V1):
    for dp, _d, fs in os.walk(V1):
        for n in fs:
            full = os.path.join(dp, n)
            v1_present[os.path.relpath(full, V1)] = sha(full)
    differ = sorted(p for p in present if v1_present.get(p) != present[p]['sha256'])
    only_v1 = sorted(set(v1_present) - set(present))
    print('v1 readable:', len(v1_present), 'files | differ from v2:', len(differ), differ[:5],
          '| only in v1:', len(only_v1))
else:
    differ, only_v1, v1_present = None, None, {}
    print('v1 source not in scope this turn; custody comparison stands alone')

# the eight v1-changed files must be present in v2 with their v1 AFTER hashes
handoff_ok = []
if os.path.exists(V1_HANDOFF):
    for row in json.load(open(V1_HANDOFF))['changedFiles']:
        p = row['path']
        handoff_ok.append({'path': p, 'v1After': row['afterSha256'],
                           'v2Now': present.get(p, {}).get('sha256'),
                           'match': present.get(p, {}).get('sha256') == row['afterSha256']})
    print('v1 handoff carried into v2:', all(r['match'] for r in handoff_ok))
    for r in handoff_ok:
        print('  ', 'OK  ' if r['match'] else 'FAIL', r['path'])

json.dump({'v2Root': V2, 'custodyDeclared': len(declared), 'v2FileCount': len(present),
           'custodyMismatches': mismatch, 'extra': extra, 'missing': missing,
           'v1Differ': differ, 'onlyInV1': only_v1,
           'v1HandoffCarried': handoff_ok, 'baseline': present},
          open(os.path.join(HERE, 'v2-source-baseline.json'), 'w'), indent=2)
print('WROTE v2-source-baseline.json')
