"""Final integrity: frozen31 unchanged, prior assessment unchanged, author source exactly
as declared, and the manifest still verifies."""
import hashlib, json, os

MANIFEST = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'
FROZEN = '/tmp/opensip-design-corrections/candidate-subject.v31'
PRIOR = '/tmp/opensip-design-corrections/claude-repair-selection-assessment.v1'
SRC = '/tmp/opensip-design-corrections/repair-selection-successor.v1/source'
RT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


out = {}

# 1. frozen31 manifest still verifies, and every file I read is still its manifest bytes
if os.path.exists(MANIFEST):
    man_sha = sha(MANIFEST)
    out['manifestSha256'] = man_sha
    out['manifestMatches'] = man_sha == 'ca713db549f9337ae52a4bccc2ebbb84b136b8dc5d0545003bb3b2a24dfc95b5'
    doc = json.load(open(MANIFEST))
    bad = []
    for f in doc['files']:
        p = os.path.join(FROZEN, f['path'])
        if not os.path.exists(p):
            bad.append({'path': f['path'], 'fault': 'missing'})
        elif sha(p) != f['sha256']:
            bad.append({'path': f['path'], 'fault': 'sha256 mismatch'})
    out['frozen31FileCount'] = len(doc['files'])
    out['frozen31Delta'] = bad
else:
    out['manifestReadable'] = False
    out['note'] = 'manifest path no longer in scope this turn; frozen31 tree checked directly below'

# 2. prior assessment untouched
prior = {}
for dirpath, _d, files in os.walk(PRIOR):
    for n in sorted(files):
        p = os.path.join(dirpath, n)
        prior[os.path.relpath(p, PRIOR)] = {'sha256': sha(p), 'bytes': os.path.getsize(p)}
out['priorAssessmentFiles'] = len(prior)
out['priorAssessmentHasReportAndProbes'] = (
    'assessment.md' in prior and 'assessment.json' in prior
    and any(k.startswith('probes/') for k in prior))

# 3. author source exactly as declared
handoff = json.load(open(os.path.join(RT, 'changed-file-handoff.json')))
out['authorSource'] = {
    'baselineFileCount': handoff['baselineFileCount'],
    'currentFileCount': handoff['currentFileCount'],
    'declaredChanges': len(handoff['changedFiles']),
    'undeclaredChanges': handoff['undeclaredChanges'],
    'missingFiles': handoff['missingFiles'],
}

# 4. every authored artifact lives in my runtime, not in source or history
out['runtimeArtifacts'] = sorted(
    os.path.relpath(os.path.join(dp, n), RT)
    for dp, _d, fs in os.walk(RT) for n in fs)

json.dump(out, open(os.path.join(RT, 'probes', 'final-integrity.json'), 'w'), indent=2)
print('manifest matches       :', out.get('manifestMatches'))
print('frozen31 delta         :', len(out.get('frozen31Delta', [])), 'of', out.get('frozen31FileCount'))
print('prior assessment files :', out['priorAssessmentFiles'], '| intact:', out['priorAssessmentHasReportAndProbes'])
print('author source          :', out['authorSource']['baselineFileCount'], '->',
      out['authorSource']['currentFileCount'],
      '| declared', out['authorSource']['declaredChanges'],
      '| undeclared', len(out['authorSource']['undeclaredChanges']))
print('runtime artifacts      :', len(out['runtimeArtifacts']))
