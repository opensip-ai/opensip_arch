#!/usr/bin/env python3
"""Probe 12 (independent): every {path, sha256} cross-reference inside the v16
governance records must resolve to the exact frozen bytes.

A record that cites a digest which does not match the artifact it names is a
custody defect regardless of what the prose says, so this is checked rather
than assumed.
"""
import hashlib, json, os, re, sys

SUBJ = '/tmp/opensip-design-corrections/candidate-subject.v16'
OUT = '/tmp/opensip-design-corrections/post-reset-review.v16'

def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

RECORDS = [
    'docs/coop/design-corrections/post-reset-dispositions.v16.proposed.json',
    'docs/coop/design-corrections/historical-preservation-report.v16.json',
    'docs/coop/design-corrections/reviews/codex-post-reset.v1/successor-source-assessment.v16.json',
    'docs/coop/design-corrections/reviews/codex-post-reset.v1/blind-assessment.v5.json',
    'docs/coop/design-corrections/reviews/codex-post-reset.v1/advisory-application-account.v16.proposed.json',
    'docs/coop/design-corrections/reviews/codex-post-reset.v1/source-integration.v16.json',
    'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-source-account.v16.json',
    'docs/coop/design-corrections/reviews/codex-post-reset.v1/identity-check-counts.v16.json',
    'docs/coop/design-corrections/reviews/codex-post-reset.v1/coauthor-assessment-bv5-v1.json',
    'docs/coop/design-corrections/reviews/bv5-corrections-author.v2/handoff.json',
    'docs/coop/design-corrections/reviews/bv5-corrections-author.v2/custody.json',
    'docs/coop/design-corrections/reviews/bv5-corrections-author.v1/handoff.json',
    'docs/coop/design-corrections/reviews/bv5-corrections-author.v1/custody.json',
    'docs/coop/design-corrections/reviews/consumer-b.v5/custody.json',
    'docs/coop/design-corrections/reviews/post-reset-review.v15/custody.json',
    'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v16/reference-checks.json',
    'docs/coop/design-corrections/correction-crosswalk.proposed.json',
    'docs/coop/design-corrections/validation-summary.v1.json',
    'docs/coop/design-corrections/reviews/codex-post-reset.v1/crosswalk-update-v16.json',
    'docs/coop/design-corrections/reviews/bv5-corrections-author.v2/source-copy-accounts.json',
    'docs/coop/design-corrections/reviews/bv5-corrections-author.v1/source-copy-accounts.json',
    'docs/coop/design-corrections/reviews/post-reset-review.v15/source-copy-accounts.json',
    'docs/coop/design-corrections/reviews/codex-post-reset.v1/bv5-final-root-probes.v16/execution.json',
]

HEX = re.compile(r'^[0-9a-f]{64}$')

def candidates(path, record=None):
    """Resolve a cited path against the plausible roots the records use.

    custody.json files list their members RELATIVE TO THEIR OWN DIRECTORY, which my
    first attempt did not try (failed-attempt-07): 369 references were reported
    unresolved purely because of that.
    """
    p = path.lstrip('./')
    if record:
        yield os.path.join(SUBJ, os.path.dirname(record), p)
    yield os.path.join(SUBJ, p)
    yield os.path.join(SUBJ, 'docs/coop/design-corrections', p)
    yield os.path.join(SUBJ, 'docs/coop/design-corrections/reviews', p)
    yield os.path.join(SUBJ, 'docs/coop/design-corrections/reviews/codex-post-reset.v1', p)
    yield os.path.join(SUBJ, 'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v16', p)

rows = []
def scan(doc, record, ptr=''):
    if isinstance(doc, dict):
        pathv = next((doc[k] for k in ('path', 'file', 'source', 'sourcePath', 'sourceReport')
                      if isinstance(doc.get(k), str)), None)
        shav = next((doc[k] for k in ('sha256', 'sourceSha256', 'sourceReportSha256', 'digest')
                     if isinstance(doc.get(k), str) and HEX.match(doc[k])), None)
        if pathv and shav:
            resolved, got = None, None
            for c in candidates(pathv, record):
                if os.path.isfile(c):
                    resolved, got = c, sha256(c); break
            rows.append({'record': record, 'pointer': ptr, 'citedPath': pathv,
                         'citedSha256': shav, 'resolvedTo': resolved,
                         'observedSha256': got, 'resolves': resolved is not None,
                         'matches': got == shav})
        for k, v in doc.items():
            scan(v, record, ptr + '/' + k)
    elif isinstance(doc, list):
        for i, v in enumerate(doc):
            scan(v, record, ptr + f'[{i}]')

present, missing_records = [], []
for r in RECORDS:
    full = os.path.join(SUBJ, r)
    if not os.path.isfile(full):
        missing_records.append(r); continue
    present.append({'record': r, 'sha256': sha256(full)})
    scan(json.load(open(full)), r)

unresolved = [x for x in rows if not x['resolves']]
mismatched = [x for x in rows if x['resolves'] and not x['matches']]

res = {
    'probe': 'probe-12-record-cross-references',
    'recordsScanned': present,
    'recordsMissing': missing_records,
    'crossReferencesFound': len(rows),
    'crossReferencesResolvedAndMatching': sum(1 for x in rows if x['matches']),
    'unresolvedCount': len(unresolved),
    'unresolved': unresolved,
    'mismatchedCount': len(mismatched),
    'mismatched': mismatched,
    'allResolvedReferencesMatch': not mismatched,
    'rows': rows,
    'notProductQualification': True,
}
with open(os.path.join(OUT, 'probe-12-record-cross-references.result.json'), 'w') as f:
    json.dump(res, f, indent=2, sort_keys=True)
print(json.dumps({k: v for k, v in res.items() if k not in ('rows', 'unresolved', 'mismatched')},
                 indent=2, sort_keys=True))
print('\nMISMATCHED:')
for x in mismatched:
    print(' ', x['record'], x['pointer'], x['citedPath'], x['citedSha256'], '!=', x['observedSha256'])
print('\nUNRESOLVED (first 25):')
for x in unresolved[:25]:
    print(' ', x['record'], x['pointer'], x['citedPath'])
