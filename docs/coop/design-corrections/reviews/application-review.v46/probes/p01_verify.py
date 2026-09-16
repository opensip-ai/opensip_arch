import json, hashlib, os, sys
S = '/private/tmp/opensip-design-corrections/application-stage.v46'
R = '/Users/sb/code/opensip-ai/opensip_arch'
MS = 'dab6e00fc3ccf82f015941bc767a10b18be9e6ca5f1c8598fa1fe9a4d05743f7'
raw = open(S + '/application-subject.v46.json', 'rb').read()
out = {'manifestSha256': hashlib.sha256(raw).hexdigest()}
out['manifestMatches'] = out['manifestSha256'] == MS
m = json.loads(raw)
bad = []
def h(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def chk(kind, base, e):
    p = os.path.join(base, e['path'])
    if not os.path.isfile(p):
        bad.append((kind, e['path'], 'missing')); return
    b = open(p, 'rb').read()
    if hashlib.sha256(b).hexdigest() != e['sha256'] or len(b) != e['bytes']:
        bad.append((kind, e['path'], 'mismatch'))
for e in m['files']: chk('files', S + '/files', e)
for e in m['beforeImages']: chk('before', S + '/before', e)
for e in m['support']: chk('support', S, e)
out['mismatches'] = bad
out['counts'] = [len(m['files']), len(m['beforeImages']), len(m['support'])]
listed = set('files/' + e['path'] for e in m['files']) | set('before/' + e['path'] for e in m['beforeImages']) | set(e['path'] for e in m['support']) | {'application-subject.v46.json'}
disk = set()
for r, d, f in os.walk(S):
    for x in f: disk.add(os.path.relpath(os.path.join(r, x), S))
out['unlisted'] = sorted(disk - listed)
out['listedMissing'] = sorted(listed - disk)
out['dups'] = {k: len(m[k]) - len(set(e['path'] for e in m[k])) for k in ['files', 'beforeImages', 'support']}
bi = {e['path']: e['sha256'] for e in m['beforeImages']}
fp = {e['path'] for e in m['files']}
out['filesWithBefore'] = sum(1 for e in m['files'] if 'beforeSha256' in e)
out['beforeShaWrong'] = [e['path'] for e in m['files'] if 'beforeSha256' in e and bi.get(e['path']) != e['beforeSha256']]
out['beforeNotInFiles'] = [p for p in bi if p not in fp]
out['newFiles'] = sum(1 for e in m['files'] if 'beforeSha256' not in e)
out['supportPrefixBad'] = [e['path'] for e in m['support'] if not e['path'].startswith('support/')]
out['unsafe'] = [e['path'] for k in ['files', 'beforeImages', 'support'] for e in m[k] if e['path'].startswith('/') or '..' in e['path'].split('/')]
# live state
live_before = live_after = live_other = 0; other = []; absent_new = 0; present_new = []
for e in m['files']:
    p = os.path.join(R, e['path'])
    if 'beforeSha256' in e:
        if not os.path.isfile(p): other.append((e['path'], 'missing-live')); live_other += 1; continue
        hh = h(p)
        if hh == e['beforeSha256']: live_before += 1
        elif hh == e['sha256']: live_after += 1
        else: live_other += 1; other.append((e['path'], hh))
    else:
        if os.path.exists(p):
            hh = h(p)
            present_new.append((e['path'], hh == e['sha256']))
        else: absent_new += 1
out['live'] = {'before': live_before, 'after': live_after, 'other': other, 'newAbsent': absent_new, 'newPresent': present_new}
out['activationExists'] = os.path.exists(R + '/docs/coop/design-corrections/application-activation.v1.json')
# retained copies
for rp in ['docs/coop/design-corrections/reviews/application-subject.v46.json', 'docs/coop/design-corrections/reviews/application-subject.v45.json', 'docs/coop/design-corrections/reviews/application-review.v45/review.json', 'docs/coop/design-corrections/reviews/application-review.v46/review.json', 'docs/coop/design-corrections/reviews/claude-independent-design.v45/review.json', 'docs/coop/design-corrections/reviews/consumer-b.v24-source45.v1/blind-review.json', 'docs/coop/design-corrections/reviews/candidate-subject.v45.json', 'docs/coop/design-corrections/reviews/root-application46-delta.v1/delta.json']:
    p = os.path.join(R, rp)
    out.setdefault('retained', {})[rp] = h(p) if os.path.isfile(p) else None
print(json.dumps(out, indent=1))
