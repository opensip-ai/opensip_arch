import json, hashlib
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/'
C = '/tmp/opensip-design-corrections/candidate-subject.v45/'
R = '/Users/sb/code/opensip-ai/opensip_arch/'
app = json.load(open(S + 'files/docs/coop/design-corrections/application.v1.json'))
rep = app['acceptedDesignReproduction']
orig_p = R + rep['originalExecutedCommandRecord']['path']
ob = open(orig_p, 'rb').read()
print('original record sha ok', hashlib.sha256(ob).hexdigest() == rep['originalExecutedCommandRecord']['sha256'])
orig = json.loads(ob)
print('original keys', list(orig.keys()))
oc = {c['name']: c for c in orig['commands']}
print('original command names', list(oc))
cm = json.load(open(R + 'docs/coop/design-corrections/reviews/candidate-subject.v45.json'))
snap = {e['path']: e['sha256'] for e in cm['files']}
for c in rep['commands']:
    o = oc.get(c['name'])
    print('==', c['name'], 'source in snapshot sha ok', snap.get(c['source']) == c['sourceSha256'], 'orig sourceSha', o and o.get('sourceSha256') == c['sourceSha256'])
    if o:
        ocmd = o.get('command') or o.get('argv')
        print('   original argv', ocmd)
        # normalized: absolute source -> relative; outputs -> recorded
        abs_src = [a for a in ocmd if a.endswith(c['source'])]
        print('   original source abs forms', abs_src, 'endswith relative', bool(abs_src))
        for b in c['outputBindings']:
            i = ocmd.index(b['flag']) if b['flag'] in ocmd else None
            print('   binding', b['flag'], 'recorded==original', i is not None and ocmd[i + 1] == b['recordedOutput'], 'reproduction relative', not b['reproductionOutput'].startswith('/'))
        flags = [a for a in ocmd if a.startswith('--')]
        print('   original flags', flags, 'reproduction flags', [a for a in c['argv'] if a.startswith('--')])
        # all non-output args equal after normalization
        norm_o = [c['source'] if a.endswith(c['source']) else a for a in ocmd]
        norm_r = list(c['argv'])
        for b in c['outputBindings']:
            norm_o = [b['reproductionOutput'] if a == b['recordedOutput'] else a for a in norm_o]
        print('   normalized original == reproduction argv', norm_o == norm_r)
ic = json.load(open(R + app['referenceEvidenceSummary']['identityCountMeasurement']['path']))
print('identity counts sha ok', hashlib.sha256(open(R + app['referenceEvidenceSummary']['identityCountMeasurement']['path'], 'rb').read()).hexdigest() == app['referenceEvidenceSummary']['identityCountMeasurement']['sha256'])
print(json.dumps(ic, indent=1)[:3000])
vs = json.load(open(C + 'docs/coop/design-corrections/validation-summary.v1.json'))
print('accepted frozen summary', json.dumps(vs)[:2500])
cr = json.load(open(S + 'support/root-application45-reproduction-correction.v1/corrected-reproduction.json'))
print('corrected-reproduction equals application block', cr == rep or cr.get('commands') == rep['commands'])
