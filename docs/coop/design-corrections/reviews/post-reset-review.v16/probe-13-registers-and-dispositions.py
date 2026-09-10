#!/usr/bin/env python3
"""Probe 13 (independent): compute the ACTUAL basis for every AR / FW /
inherited-residual / scoped-owner disposition across the exact v15 -> v16 delta,
plus the evaluation subresiduals, the 32 qualification gates and the carried
advisory account.

Nothing here grades an application outcome. It measures, per row, whether the
row moved and, if so, exactly which fields moved.
"""
import hashlib, json, os, sys

SUBJ = '/tmp/opensip-design-corrections/candidate-subject.v16'
OUT = '/tmp/opensip-design-corrections/post-reset-review.v16'
DC = 'docs/coop/design-corrections'
V15_MANIFEST = ('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/'
                'reviews/candidate-subject.v15.json')

def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

v15 = {r['path']: r['sha256'] for r in json.load(open(V15_MANIFEST))['files']}
v16m = {r['path']: r['sha256'] for r in json.load(open(
    '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
    'candidate-subject.v16.json'))['files']}

def identical(rel):
    return {'path': rel, 'v15Sha256': v15.get(rel), 'v16Sha256': v16m.get(rel),
            'byteIdentical': v15.get(rel) == v16m.get(rel)}

OWNERS = {k: identical(k) for k in [
    f'{DC}/correction-crosswalk.proposed.json',
    f'{DC}/current-source-map.proposed.md',
    f'{DC}/inherited-residuals.proposed.md',
    f'{DC}/inherited-row-sources.proposed.json',
    f'{DC}/evaluation-residual-dispositions.proposed.json',
    f'{DC}/README.md',
    f'{DC}/D-372-corrections.proposed.md',
]}

# --- crosswalk row-by-row delta -------------------------------------------
# v15 bytes come from the retained v15 review evidence if present; otherwise the
# in-subject crosswalk-before-v16.json, whose digest I verify against v15.
BEFORE = os.path.join(SUBJ, DC, 'reviews/codex-post-reset.v1/crosswalk-before-v16.json')
before_sha = sha256(BEFORE)
before_is_v15 = before_sha == v15.get(f'{DC}/correction-crosswalk.proposed.json')
cw_before = json.load(open(BEFORE))
cw_after = json.load(open(os.path.join(SUBJ, DC, 'correction-crosswalk.proposed.json')))

def rows_of(doc):
    for key in ('rows', 'items', 'entries', 'crosswalk'):
        if isinstance(doc.get(key), list):
            return {r.get('id') or r.get('ar') or r.get('key'): r for r in doc[key]}
    # fall back: any list of dicts carrying an AR-* id
    out = {}
    def walk(o):
        if isinstance(o, dict):
            i = o.get('id')
            if isinstance(i, str) and (i.startswith('AR-') or i.startswith('FW-')
                                       or i.startswith('DR-')):
                out[i] = o
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(doc)
    return out

RB, RA = rows_of(cw_before), rows_of(cw_after)
row_delta = {}
for rid in sorted(set(RB) | set(RA)):
    a, b = RB.get(rid), RA.get(rid)
    if a is None:
        row_delta[rid] = {'status': 'ADDED-IN-V16'}
    elif b is None:
        row_delta[rid] = {'status': 'REMOVED-IN-V16'}
    elif a == b:
        row_delta[rid] = {'status': 'BYTE-IDENTICAL', 'changedFields': []}
    else:
        changed = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
        row_delta[rid] = {'status': 'CHANGED', 'changedFields': changed,
                          'before': {k: a.get(k) for k in changed},
                          'after': {k: b.get(k) for k in changed}}

ar_ids = sorted(r for r in row_delta if r.startswith('AR-'))
fw_ids = sorted(r for r in row_delta if r.startswith('FW-'))
dr_ids = sorted(r for r in row_delta if r.startswith('DR-'))

# --- FW rows live in current-source-map.proposed.md ------------------------
import re
fw_src = open(os.path.join(SUBJ, DC, 'current-source-map.proposed.md'), encoding='utf-8').read()
fw_in_map = sorted(set(re.findall(r'\bFW-\d{2}\b', fw_src)))

# --- inherited residuals ---------------------------------------------------
inh_src = open(os.path.join(SUBJ, DC, 'inherited-residuals.proposed.md'), encoding='utf-8').read()
inh_ids = sorted(set(re.findall(r'\bDR-\d{3}\b', inh_src)))
inh_rows = json.load(open(os.path.join(SUBJ, DC, 'inherited-row-sources.proposed.json')))

# --- evaluation subresiduals ----------------------------------------------
ev = json.load(open(os.path.join(SUBJ, DC, 'evaluation-residual-dispositions.proposed.json')))
def count_sub(o):
    n = 0
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('subresiduals', 'items', 'rows') and isinstance(v, list):
                n += len(v)
            n += count_sub(v)
    elif isinstance(o, list):
        for v in o:
            n += count_sub(v)
    return n
ev_sub = count_sub(ev)

# --- 32 qualification gates ------------------------------------------------
gates = []
def find_gates(o, p=''):
    if isinstance(o, dict):
        if 'demonstrated' in o and 'qualified' in o:
            gates.append({'at': p, 'id': o.get('id') or o.get('gateId'),
                          'demonstrated': o['demonstrated'], 'qualified': o['qualified']})
        for k, v in o.items():
            find_gates(v, p + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            find_gates(v, p + f'[{i}]')
for f in os.listdir(os.path.join(SUBJ, DC)):
    if f.endswith('.json'):
        try:
            find_gates(json.load(open(os.path.join(SUBJ, DC, f))), f)
        except Exception:
            pass

# --- advisory account v15 -> v16 -------------------------------------------
def acct(ver):
    p = os.path.join(SUBJ, DC, f'reviews/codex-post-reset.v1/'
                               f'advisory-application-account.{ver}.proposed.json')
    return json.load(open(p)) if os.path.isfile(p) else None
a15, a16 = acct('v15'), acct('v16')
i15 = {i['id']: i for i in a15['items']} if a15 else {}
i16 = {i['id']: i for i in a16['items']} if a16 else {}
acct_delta = {
    'v15Count': len(i15), 'v16Count': len(i16),
    'added': sorted(set(i16) - set(i15)),
    'removed': sorted(set(i15) - set(i16)),
    'changed': sorted(k for k in set(i15) & set(i16) if i15[k] != i16[k]),
    'severitiesPreserved': all(i15[k].get('originalSeverity') == i16[k].get('originalSeverity')
                               for k in set(i15) & set(i16)),
}

# --- readiness / D-372 -----------------------------------------------------
readme = open(os.path.join(SUBJ, DC, 'README.md'), encoding='utf-8').read()
arch12 = open(os.path.join(SUBJ, 'docs/v2/architecture/12-architecture-completion-goal.md'),
              encoding='utf-8').read()
readiness = {
    'readmeSaysD372NotApplied': 'D-372 has not been applied' in readme,
    'readmeSaysRegisterUnchanged': 'readiness register is unchanged' in readme,
    'arch12Condition5Phrases': [l.strip() for l in arch12.splitlines()
                                if 'Condition 5' in l][:6],
}

res = {
    'probe': 'probe-13-registers-and-dispositions',
    'owningFileIdentity': OWNERS,
    'crosswalkBeforeImage': {'path': BEFORE, 'sha256': before_sha,
                             'isFrozenV15Crosswalk': before_is_v15},
    'crosswalkRowsBefore': len(RB), 'crosswalkRowsAfter': len(RA),
    'arRowIds': ar_ids, 'arRowCount': len(ar_ids),
    'fwRowIdsInCrosswalk': fw_ids,
    'fwRowIdsInSourceMap': fw_in_map, 'fwCount': len(fw_in_map),
    'inheritedResidualIds': inh_ids, 'inheritedResidualCount': len(inh_ids),
    'drRowIdsInCrosswalk': dr_ids,
    'rowDelta': row_delta,
    'rowsChanged': {k: v for k, v in row_delta.items() if v['status'] == 'CHANGED'},
    'rowsAddedOrRemoved': {k: v for k, v in row_delta.items()
                           if v['status'] in ('ADDED-IN-V16', 'REMOVED-IN-V16')},
    'evaluationSubresidualCount': ev_sub,
    'qualificationGates': {'found': len(gates),
                           'demonstratedTrue': sum(1 for g in gates if g['demonstrated']),
                           'qualifiedTrue': sum(1 for g in gates if g['qualified']),
                           'sample': gates[:4]},
    'advisoryAccountDelta': acct_delta,
    'readiness': readiness,
    'notProductQualification': True,
}
with open(os.path.join(OUT, 'probe-13-registers-and-dispositions.result.json'), 'w') as f:
    json.dump(res, f, indent=2, sort_keys=True)
print(json.dumps({k: v for k, v in res.items() if k not in ('rowDelta',)},
                 indent=2, sort_keys=True)[:6000])
