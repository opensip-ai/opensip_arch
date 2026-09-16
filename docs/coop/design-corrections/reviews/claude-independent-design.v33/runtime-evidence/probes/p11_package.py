"""P11 — package status. The root-owned update is PENDING, so the package review is INCOMPLETE.
I ASSESS the preserved package9 failure receipts; I do not rerun the known-stale package9, and I do
not infer any acceptance for package10."""
import hashlib, json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v33'
OUT = os.path.join(BASE, 'receipts')
UPD = os.path.join(BASE, 'author-package-update.json')
VER = '/tmp/opensip-design-corrections/author-package-final33-verification.v1'
P10 = '/tmp/opensip-design-corrections/claude-author-package-successor.v10'
R = {}

b = open(UPD, 'rb').read()
R['updateFileSha256'] = hashlib.sha256(b).hexdigest()
R['updateFile'] = json.loads(b)
R['packageReviewStatus'] = 'INCOMPLETE — root input still PENDING, no package10 manifest named'
print('author-package-update.json (exact version consumed):')
print('   sha256:', R['updateFileSha256'])
print('   status:', R['updateFile']['status'])
print('   names a package10 manifest:', 'artifactManifestSha256' in R['updateFile']
      or 'packageManifestSha256' in R['updateFile'])
R['namesAPackageManifest'] = ('artifactManifestSha256' in R['updateFile']
                              or 'packageManifestSha256' in R['updateFile'])
R['rootVerificationNamed'] = 'verification' in json.dumps(R['updateFile']).lower()

# preserved package9 failure receipts — ASSESSED, not rerun
rows = []
for n in sorted(os.listdir(VER)):
    p = os.path.join(VER, n)
    if os.path.isfile(p) and n.endswith(('.json', '.txt')):
        rows.append({'file': n, 'bytes': os.path.getsize(p),
                     'sha256': hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]})
R['preservedReceipts'] = rows
print('\npreserved package9 verification receipts (%d):' % len(rows))
for x in rows:
    print('   %-40s %8d %s' % (x['file'], x['bytes'], x['sha256']))
R['verificationJsonEmitted'] = os.path.isfile(os.path.join(VER, 'verification.json'))
print('final verification.json emitted:', R['verificationJsonEmitted'])

for grp in ('checkpoint3', 'binding-controls', 'normalized-examples6',
            'rust-selection-examples1', 'semantic-controls1'):
    f = os.path.join(VER, grp, 'report.json')
    if not os.path.isfile(f):
        continue
    d = json.load(open(f))
    ch = d.get('checks', [])
    out = [{'name': c.get('name'), 'ownerAdmission': c.get('ownerAdmission'),
            'semanticAdmission': c.get('semanticAdmission'), 'reason': str(c.get('reason'))[:60]}
           for c in ch]
    R['group_' + grp] = {'passed': d.get('passed'), 'checks': out}
    print('\n%s: passed=%s' % (grp, d.get('passed')))
    for c in out:
        print('   %-30s owner=%-7s semantic=%-7s %s' % (str(c['name'])[:30], c['ownerAdmission'],
                                                        c['semanticAdmission'], c['reason'][:46]))

R['assessmentOfPackage9'] = (
    'Assessed from the preserved receipts, not rerun. The failure is real and is recorded honestly: '
    'package9 was rebound from package8 rather than constructed on source33, and under actual current '
    'verification the TS checkpoint and two positive binding examples structurally admit but then '
    'REFUSE EVALUATOR_COMPLETE_PROOF_REPLAY, while the expected invalid-program-entry first refusal '
    'still holds and the normalized/rust/semantic groups pass. Query assessment then failed and no '
    'final verification.json was emitted. A historical source30 construction does not become a new '
    'execution by rebinding, so this is the correct outcome for a rebound package under changed law, '
    'not a source defect.')
R['package10Standing'] = (
    'A claude-author-package-successor.v10 directory exists in this environment, but the root-owned '
    'author-package-update.json is still PENDING and names no package10 manifest and no root '
    'verification. I therefore do NOT verify or accept package10, and the author package review is '
    'recorded INCOMPLETE. I infer no ACCEPT for it, and I did not remint anything.')
print('\n' + R['assessmentOfPackage9'])
print('\n' + R['package10Standing'])
json.dump(R, open(os.path.join(OUT, 'p11-package.json'), 'w'), indent=1, default=str)
print('\nwrote p11-package.json')
