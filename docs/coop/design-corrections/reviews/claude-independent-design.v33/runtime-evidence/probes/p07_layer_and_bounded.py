"""P07 — layer3 vs layer4 difference, plus the two bounded root scopes I must assess independently:
the candidate-envelope schema-only control, and full-Run reachability of the optional candidate carrier."""
import hashlib, json, os, subprocess, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
A = os.path.join(SRC, 'docs/v2/architecture')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v33/receipts'
R = {}

l3 = json.load(open(os.path.join(A, 'implementation-normative-inputs.v3.json')))
l4 = json.load(open(os.path.join(A, 'implementation-normative-inputs.v4.json')))
p3 = {f['path']: f['sha256'] for f in l3['files']}
p4 = {f['path']: f['sha256'] for f in l4['files']}
R['layer3Pins'], R['layer4Pins'] = len(p3), len(p4)
R['addedToLayer4'] = sorted(set(p4) - set(p3))
R['removedFromLayer4'] = sorted(set(p3) - set(p4))
R['repinnedInLayer4'] = sorted(p for p in set(p3) & set(p4) if p3[p] != p4[p])
print('layer3 pins=%d layer4 pins=%d' % (len(p3), len(p4)))
print('added   :', R['addedToLayer4'])
print('removed :', R['removedFromLayer4'])
print('repinned:', R['repinnedInLayer4'])

# ---- bounded scope 1: candidate-envelope schema-only control ----
CEC = '/tmp/opensip-design-corrections/root-candidate-envelope-schema-control.v1'
if os.path.isdir(CEC):
    names = sorted(os.listdir(CEC))
    R['envelopeControlFiles'] = names
    print('\n=== root-candidate-envelope-schema-control.v1 ===')
    for n in names:
        p = os.path.join(CEC, n)
        if os.path.isfile(p):
            print('   %-46s %d' % (n, os.path.getsize(p)))
    for n in names:
        if n.endswith('.json') and os.path.isfile(os.path.join(CEC, n)):
            try:
                d = json.load(open(os.path.join(CEC, n)))
            except Exception:
                continue
            R['envelopeControl_' + n] = d
            print('   --- %s ---' % n)
            print('   ', json.dumps(d)[:700])

# independently re-run the corrected schema-only control on frozen33
SCH = os.path.join(SRC, 'docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json')
sch = json.load(open(SCH))
R['schemaSha256'] = hashlib.sha256(open(SCH, 'rb').read()).hexdigest()
import importlib.util
spec = importlib.util.spec_from_file_location(
    'canon33', os.path.join(SRC, 'docs/coop/design-corrections/foundation/canonical.py'))
C = importlib.util.module_from_spec(spec)
sys.modules['canon33'] = C
spec.loader.exec_module(C)
defs = sch.get('$defs', {})
cand = [k for k in defs if 'andidate' in k and 'nvelope' in k] or [k for k in defs if 'andidate' in k]
R['candidateDefs'] = cand
print('\ncandidate-ish $defs in the execution-inputs schema:', cand)


def try_validate(name, inst):
    v = {'$defs': defs, '$ref': '#/$defs/' + name}
    try:
        C.validate(v, inst)
        return 'ADMIT', ''
    except Exception as ex:
        return 'REFUSE', str(ex).splitlines()[0][:140]


# the exact unavailable/null envelope, with the CORRECT exec-plan2 prefix vs the author's invalid execution2
for name in cand[:3]:
    for label, pid in (('exec-plan2 (corrected prefix)', 'exec-plan2:' + 'a' * 64),
                       ('execution2 (author q2 invalid prefix)', 'execution2:' + 'a' * 64)):
        inst = {'schemaVersion': 1, 'planId': pid, 'state': 'unavailable',
                'universe': None, 'deficiency': 'provider-unavailable', 'nativeCause': None}
        verdict, why = try_validate(name, inst)
        R.setdefault('envelopeProbe', []).append({'def': name, 'label': label,
                                                  'verdict': verdict, 'reason': why})
        print('   %-24s %-38s -> %-7s %s' % (name[:24], label, verdict, why[:90]))

# ---- bounded scope 2: full-Run reachability of the optional candidate carrier ----
OCC = '/tmp/opensip-design-corrections/root-optional-candidate-carrier-assessment.v1'
if os.path.isdir(OCC):
    names = sorted(os.listdir(OCC))
    R['optionalCandidateFiles'] = names
    print('\n=== root-optional-candidate-carrier-assessment.v1 ===')
    for n in names:
        p = os.path.join(OCC, n)
        print('   %-46s %s' % (n, os.path.getsize(p) if os.path.isfile(p) else '<dir>'))
json.dump(R, open(os.path.join(OUT, 'p07-layer-bounded.json'), 'w'), indent=1, default=str)
print('\nwrote p07-layer-bounded.json')
