"""R02 — measure the CURRENT facts needed to write truthful current fields: package10 membership,
the residual assessment binding, and F-10's actual mixed provenance (which groups are newly
constructed on 33 vs exact earlier bytes re-verified)."""
import hashlib, json, os

PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v10'
V33 = '/tmp/opensip-design-corrections/claude-independent-design.v33'
MAN33 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v33.json'
OUT = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1/receipts'
R = {}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


am = json.load(open(os.path.join(PKG, 'artifact-manifest.json')))
rows = am['files'] if isinstance(am, dict) else am
R['package10Members'] = len(rows)
R['package10ManifestSha256'] = sha(os.path.join(PKG, 'artifact-manifest.json'))
print('package10 members:', R['package10Members'])

era = os.path.join(PKG, 'evaluation-residual-author-assessment.json')
if os.path.isfile(era):
    d = json.load(open(era))
    R['residualAssessmentSubjectManifest'] = d.get('subjectManifestSha256')
    R['residualAssessmentBindsFrozen33'] = d.get('subjectManifestSha256') == sha(MAN33)
    R['residualRows'] = len(d.get('items', []))
    verd = {}
    for i in d.get('items', []):
        verd[i.get('authorAssessment')] = verd.get(i.get('authorAssessment'), 0) + 1
    R['residualVerdicts'] = verd
    dep = d.get('sharedReviewDependencies')
    R['tcbDependents'] = dep[0]['dependentResidualIds'] if dep else None
    print('residual assessment binds frozen33 :', R['residualAssessmentBindsFrozen33'])
    print('rows=%d verdicts=%s tcbDependents=%d'
          % (R['residualRows'], json.dumps(verd), len(R['tcbDependents'] or [])))

# F-10 provenance: compare package10 store bytes with the source30-era exports where available
sr = os.path.join(PKG, 'source-rebuild.v1.json')
sb = [f for f in os.listdir(PKG) if f.startswith('source-binding')]
R['packageProvenanceFiles'] = {'source-rebuild.v1.json': os.path.isfile(sr), 'sourceBinding': sb}
if os.path.isfile(sr):
    d = json.load(open(sr))
    R['sourceRebuild'] = {k: (json.dumps(v)[:260] if not isinstance(v, str) else v[:260])
                          for k, v in d.items()}
    print('\nsource-rebuild.v1.json:')
    for k, v in R['sourceRebuild'].items():
        print('   %-32s %s' % (k, str(v)[:200]))
for n in sb:
    d = json.load(open(os.path.join(PKG, n)))
    R['binding_' + n] = {k: (json.dumps(v)[:300] if not isinstance(v, str) else v[:300])
                         for k, v in d.items()}
    print('\n%s:' % n)
    for k, v in R['binding_' + n].items():
        print('   %-34s %s' % (k, str(v)[:210]))

# which group stores changed versus the package9-era bytes? use my own p12 receipt digests
p12 = json.load(open(os.path.join(V33, 'receipts', 'p12-package10.json')))
R['package10ExportDigests'] = {r['name']: r['exportSha256'] for r in p12['rows']}
print('\npackage10 export digests measured in my v33 pass:')
for k, v in R['package10ExportDigests'].items():
    print('   %-30s %s' % (k, v[:20]))
json.dump(R, open(os.path.join(OUT, 'r02-currentfacts.json'), 'w'), indent=1, default=str)
print('\nwrote r02-currentfacts.json')
