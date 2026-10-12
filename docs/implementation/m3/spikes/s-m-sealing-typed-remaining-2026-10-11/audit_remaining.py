from pathlib import Path
import json, hashlib, statistics, struct, sys, ast, tarfile
# Read-only audit of the remaining Rust/TS development read-set typed sealing set. Follows the closed audit's identity,
# shape and statistical checks, but RECORDS each snapshot2 bound (PROPOSAL-r5 SM-5 / MC item 5) instead of asserting it,
# and reports a refused child from its retained evidence. Raw children are read from raw/<id>.tar.xz when present
# (staged form) or from the loose files (as produced). Writes checks.json beside itself, or prints with --stdout.
B = Path(__file__).resolve().parent; P = Path('/Users/sb/code/opensip-ai/opensip'); sys.path.insert(0, str(P / 'tools/contracts/python-packages'))
from jsonschema import Draft202012Validator
j = json.loads((B / 'results.json').read_text()); template = json.loads((B / 'control-template.json').read_text())
fixture_path = P / 'crates/host/tests/fixtures/replay-fixtures.json'; raw = fixture_path.read_bytes(); assert hashlib.sha256(raw).hexdigest() == '4004eb2a751eb5d55a0dd8170d1ff81545282ca27a863215763e8b7c4393d163'; fixture = json.loads(raw)
schema = json.loads((P / 'schemas/sources/identity-v3.schema.json').read_text())
assert schema['$defs']['snapshot']['properties']['sourceInventory'] == {'$ref': '#/$defs/source-inventory'} and schema['$defs']['source-inventory']['maxItems'] == 100000
def C(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def identity(kind, v): r = C(v); return ('snapshot2:' if kind == 'snapshot' else 'plan2:') + hashlib.sha256(b'opensip.product.v1\0' + kind.encode() + b'\0' + struct.pack('>Q', len(r)) + r).hexdigest()
def children(wid):
    packed = B / 'raw' / (wid + '.tar.xz')
    if packed.exists():
        with tarfile.open(packed, mode='r:xz') as t: return {m.name: t.extractfile(m).read() for m in t.getmembers()}
    return {p.name: p.read_bytes() for p in B.glob(wid + '-*.std*') if p.name[len(wid) + 1:].split('.')[0].isdigit()}
controls = []
for kind in ['snapshot', 'plan']:
    matches = [v for v in fixture['objectPool'].values() if v['domain'] == kind and v['descriptor'] == template[kind]]; assert len(matches) == 1
    assert identity(kind, template[kind]) == matches[0]['id']; Draft202012Validator(dict(schema, **{'$ref': '#/$defs/' + kind})).validate(template[kind])
    controls.append(dict(domain=kind, id=matches[0]['id'], publicFixturePreimageAndIdentityMatched=True))
assert len(j['workloads']) == 21 and j['observedParentNiceness'] == 10 and j['snapshotPlanIdentitiesAdmitted'] is False
rows = []; observed = 0
def bounds(inv, snapshot): return dict(rows100000=len(inv) <= 100000, descriptor4MiB=len(C(snapshot)) <= 4 * 1024 * 1024, total8GiB=sum(r['bytes'] for r in inv) <= 8 * 1024 ** 3)
for w in j['workloads']:
    assert w['heldOut'] is False; files = children(w['id']); shape = None; observations = []
    for n, r in enumerate(w['runs']):
        out = json.loads(files[f'{w["id"]}-{n}.stdout']); elapsed = out.pop('elapsedNanos'); shape = out if shape is None else shape
        assert out == shape and elapsed == r['elapsedNanos'] and files[f'{w["id"]}-{n}.stderr'] == b''
        assert r['ordinal'] == n and r['warmup'] == (n < 3) and r['observedChildNiceness'] == 10 and r['exitCode'] == 0 and r['rssUnit'] == 'bytes' and r['rssNative'] == r['rssBytes'] and 0 <= r['rssBytes'] < 2 ** 64
        observed += 1
        if n >= 3: observations.append(elapsed)
    if w['failure'] is None:
        assert len(w['runs']) == 10 and statistics.median(observations) == w['medianNanos'] and max(observations) == w['maxNanos']
        inv = shape['regularRows']; assert shape['registeredSnapshotPlanShapesPassed'] is True
        assert inv == sorted(inv, key=lambda r: r['path'].encode()) and len({r['path'] for r in inv}) == len(inv) and shape['rows'] == len(inv) == w['rows'] and shape['bytes'] == sum(r['bytes'] for r in inv) == w['bytes']
        snapshot = dict(template['snapshot'], sourceInventory=inv); plan = dict(template['plan'], snapshotId=identity('snapshot', snapshot))
        assert identity('snapshot', snapshot) == shape['snapshotEquivalentDigest'] and identity('plan', plan) == shape['planEquivalentDigest']
        assert len(C(snapshot)) == shape['snapshotEquivalentDescriptorBytes'] == w['snapshotEquivalentDescriptorBytes'] and len(C(plan)) == shape['planEquivalentDescriptorBytes'] and len(C(inv)) == shape['inventoryCanonicalBytes']
        for kind, v in [('snapshot', snapshot), ('plan', plan)]: Draft202012Validator(dict(schema, **{'$ref': '#/$defs/' + kind})).validate(v)
        b = bounds(inv, snapshot); assert b == dict(rows100000=w['withinSnapshot2Rows'], descriptor4MiB=w['withinSnapshot2Descriptor'], total8GiB=w['withinSnapshot2TotalBytes'])
        rows.append(dict(id=w['id'], outcome='SEALED-EQUIVALENT', regularRows=len(inv), bytes=shape['bytes'], nonregularExcluded=len(shape['nonregularExcluded']), snapshotDescriptorBytes=len(C(snapshot)), planDescriptorBytes=len(C(plan)),
                         snapshotEquivalentDigest=shape['snapshotEquivalentDigest'], medianNanos=w['medianNanos'], maxNanos=w['maxNanos'], measuredPeakRssBytes=max(r['rssBytes'] for r in w['runs'][3:]), bounds=b, registeredShapeAccepted=True, overlayConfigurationNotCaptured=w['overlayConfigurationNotCaptured']))
    else:
        # The refused child's retained stderr carries the probe's exact sorted inventory as the ValidationError instance.
        f = w['failure']; assert len(w['runs']) == f['ordinal'] == 0 and f['exitCode'] == 1
        err = files[f'{w["id"]}-0.stderr']; assert hashlib.sha256(err).hexdigest() == f['stderr']['sha256'] and len(err) == f['stderr']['bytes'] and files[f'{w["id"]}-0.stdout'] == b''
        text = err.decode(); head = 'jsonschema.exceptions.ValidationError: '; start = text.index(head) + len(head); end = text.index(' is too long\n', start)
        inv = ast.literal_eval(text[start:end]); assert "Failed validating 'maxItems' in schema['properties']['sourceInventory']" in text
        assert all(set(r) == {'path', 'sha256', 'bytes'} for r in inv) and inv == sorted(inv, key=lambda r: r['path'].encode()) and len({r['path'] for r in inv}) == len(inv)
        snapshot = dict(template['snapshot'], sourceInventory=inv)
        errors = list(Draft202012Validator(dict(schema, **{'$ref': '#/$defs/snapshot'})).iter_errors(snapshot)); assert [(e.validator, list(e.absolute_path)) for e in errors] == [('maxItems', ['sourceInventory'])]
        b = bounds(inv, snapshot); assert b['rows100000'] is False
        rows.append(dict(id=w['id'], outcome='REFUSED-BY-REGISTERED-SNAPSHOT-SHAPE', refusal='snapshot sourceInventory maxItems 100000', regularRows=len(inv), bytes=sum(r['bytes'] for r in inv), snapshotDescriptorBytes=len(C(snapshot)),
                         inventoryDerivedFromRetainedRefusalEvidence=True, timingAvailable=False, refusedChildren=1, bounds=b, registeredShapeAccepted=False, overlayConfigurationNotCaptured=w['overlayConfigurationNotCaptured']))
outside = sorted(r['id'] for r in rows if not all(r['bounds'].values()))
result = dict(standing='UNREVIEWED READONLY TYPED SEALING STATISTICAL/IDENTITY/REGISTERED SHAPE AUDIT; BOUNDS RECORDED NOT ASSERTED', publicControlIdentityMatches=controls,
              fixturePin=dict(path=str(fixture_path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()), workloads=rows, successfulChildren=observed, refusedChildren=sum(r.get('refusedChildren', 0) for r in rows),
              allObservedChildPriorities10=True, workloadsWithinAllSnapshot2Bounds=len(rows) - len(outside), workloadsOutsideSnapshot2Bounds=outside,
              rowBoundMisses=sorted(r['id'] for r in rows if not r['bounds']['rows100000']), descriptorBoundMisses=sorted(r['id'] for r in rows if not r['bounds']['descriptor4MiB']), totalBytesBoundMisses=sorted(r['id'] for r in rows if not r['bounds']['total8GiB']),
              snapshot2BoundMissIsMCSuccessorQuestion=True, SM5FigureComplete=False, SM5PlaceholderFilled=False, SMComplete=False, LG1Met=False, snapshotPlanIdentitiesAdmitted=False, dependencySourceSetsIncluded=False, effectiveL=False, productQualification=False)
text = json.dumps(result, indent=2) + '\n'
if sys.argv[1:] == ['--stdout']: sys.stdout.write(text)
else: (B / 'checks.json').write_text(text); print(json.dumps({k: v for k, v in result.items() if k != 'workloads'}, indent=2))
