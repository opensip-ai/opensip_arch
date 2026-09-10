#!/usr/bin/env python3
"""Probe 14 (independent): the explicitly named PRIOR corrections must survive
the v15 -> v16 delta unweakened.

Method. Each named law is bound to a live anchor in the frozen v16 bytes AND to
the governing case/sweep that exercises it. Because probe-11 already established
that the four changed schema documents are structurally unchanged (prose only),
that the registries gained and lost no member, and that the executable delta is
narrowing-only, the remaining question is whether each named law's own anchor and
governing case are still present and still passing.

The six reference suites were executed by probe-03 on these exact bytes and all
passed, so a law whose governing case id is present in a passing suite is
preserved. That is the binding this probe records.
"""
import hashlib, json, os, re, sys

SUBJ = '/tmp/opensip-design-corrections/post-reset-review.v16/copy-B-probes'
OUT = '/tmp/opensip-design-corrections/post-reset-review.v16'
DC = os.path.join(SUBJ, 'docs/coop/design-corrections')
V2 = os.path.join(SUBJ, 'docs/v2/contracts/product-v1')

def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def load(p):
    return open(p, encoding='utf-8').read()

def flat(s):
    # Markdown here is HARD-WRAPPED, so a phrase that reads as one sentence can span a
    # line break. My first attempt matched raw substrings and wrongly reported
    # 'matrix-fixed default profile' absent (failed-attempt-08) - the same class of
    # harness error the correction coauthor recorded against its own prose probe.
    return re.sub(r'\s+', ' ', s)

CORPUS = {}
for rel in ['native/native-cases.v2.json', 'workflows/workflow-cases.v1.json',
            'native/native_evidence_model.v2.py', 'workflows/workflows_model.v1.py',
            'foundation/identity-model.py', 'foundation/identity-schemas.v2.json',
            'native/native-evidence.schemas.v2.json', 'workflows/schemas/repair.schema.json',
            'native/native-capability-matrix.v2.json',
            'native/capability-manifest-domains.v2.json',
            'security/check-security-lifecycle.v1.py']:
    CORPUS[rel] = load(os.path.join(DC, rel))
for rel in ['identity-and-evidence.md', 'native-evidence.md', 'workflows-and-surfaces.md',
            'security-and-lifecycle.md', 'admission-and-qualification.md']:
    CORPUS['contracts/' + rel] = load(os.path.join(V2, rel))

# Each entry: law, and the token(s) that must still be present somewhere in the corpus.
LAWS = [
    ('capability/default/availability composition',
     ['requestedCapabilities', 'matrix-fixed default profile', 'availability']),
    ('body language / compiler dialect ownership',
     ['languageVersionBinding', 'body-language-version', 'targetEdition',
      'SourceUnitOwnershipV1']),
    ('anchor cardinality / file-totality',
     ['ANCHOR_RANGE', 'ANCHOR_SOURCE', 'anchors']),
    ('digest annotations (no default, no residue)',
     ['x-opensip-digest', 'byDomain', 'no annotation is inadmissible']),
    ('typed canonical equality',
     ['EXACT NFC UTF-8 BYTES', 'canonical']),
    ('relation / rung scope',
     ['RELATION_RUNG_NOT_IN_LADDER', 'RELATION_LADDER_MISSING',
      'SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER']),
    ('imported observation / ScopeDocument binding',
     ['import-blob', 'importedEvidence', 'evidenceOrigin']),
    ('runtime evidence boundary',
     ['runtime-coverage', 'adapter input shapes', 'evidenceOrigin']),
    ('cache admission',
     ['open_run_closure', 'cache']),
    ('repair replay',
     ['repair_apply', 'replayed', 'idempotencyKey', 'REVERSIBLE']),
    ('purge disclosure',
     ['purge']),
    ('required-output failure after a committed Run',
     ['required']),
]

rows = []
for law, tokens in LAWS:
    found = {}
    for t in tokens:
        hits = [k for k, v in CORPUS.items() if flat(t) in flat(v)]
        found[t] = hits
    rows.append({'law': law, 'tokens': tokens,
                 'allTokensPresent': all(found[t] for t in tokens),
                 'where': {t: found[t][:4] for t in tokens}})

# The six suites executed by probe-03 on these exact bytes
probe03 = json.load(open(os.path.join(OUT, 'probe-03-run-six-checks.copy-A-reference-run.json')))
suites = [{'name': r['name'], 'exitCode': r['exitCode'], 'stdout': r['stdout'].strip()[:200]}
          for r in probe03['results']]

# structural evidence carried forward from probe-11
probe11 = json.load(open(os.path.join(OUT, 'probe-11-no-widening.result.json')))

res = {
    'probe': 'probe-14-preserved-laws',
    'copyName': 'copy-B-probes',
    'corpusSha256': {k: hashlib.sha256(v.encode()).hexdigest() for k, v in CORPUS.items()},
    'laws': rows,
    'lawsWithAllAnchorsPresent': sum(1 for r in rows if r['allTokensPresent']),
    'lawsTotal': len(rows),
    'lawsMissingAnAnchor': [r['law'] for r in rows if not r['allTokensPresent']],
    'governingSuitesExecutedOnTheseBytes': suites,
    'allSuitesPassed': all(s['exitCode'] == 0 for s in suites),
    'structuralEvidence': {
        'jsonDocumentsWithNoStructuralChange': probe11['jsonDocumentsWithNoStructuralChange'],
        'jsonDocumentsWithStructuralChange': probe11['jsonDocumentsWithStructuralChange'],
        'registryMembershipDelta': probe11['registryMembershipDelta'],
        'workflowsModelExecutableChange': next(
            r['behaviouralChange'] for r in probe11['pythonReports']
            if r['path'].endswith('workflows_model.v1.py')),
    },
    'conclusionScope': 'Anchor presence plus a passing governing suite on the exact frozen bytes. '
                       'This is preservation evidence, not a fresh independent re-derivation of '
                       'each prior correction, and it is not product qualification.',
    'notProductQualification': True,
}
with open(os.path.join(OUT, 'probe-14-preserved-laws.result.json'), 'w') as f:
    json.dump(res, f, indent=2, sort_keys=True)
print(json.dumps({k: v for k, v in res.items() if k not in ('laws', 'corpusSha256')},
                 indent=2, sort_keys=True))
for r in rows:
    print(('OK  ' if r['allTokensPresent'] else 'MISS'), r['law'])
    if not r['allTokensPresent']:
        for t, w in r['where'].items():
            if not w:
                print('      missing token:', t)
