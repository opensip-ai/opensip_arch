"""Checkpoint / requirement-status maintenance for consumer-b.v20.

A later phase may not drop IDs: requirementIdsRequired is the UNION of this phase and
all prior checkpoints, read back off disk.
"""
import json
import os
import sys

ROOT = '/tmp/opensip-design-corrections/consumer-b.v20'
OUT = ROOT + '/output'
CP = OUT + '/checkpoints'
STATUS = OUT + '/requirement-status.json'
CONSUMER = 'consumer-b.v20'

STATUS_ENUM = ('unexecuted', 'executed', 'failed', 'futureQualification')


def load_requirements():
    r = json.load(open(ROOT + '/requirements.json'))
    return r


def all_ids():
    r = load_requirements()
    ids = [q['id'] for q in r['requirements']]
    st = [s['id'] for s in r['standing']]
    fq = [f['id'] for f in r['futureQualification']]
    return ids, st, fq, r


def phase_ids(n):
    _, _, _, r = all_ids()
    for p in r['phases']:
        if p['n'] == n:
            return list(p['ids'])
    return []


def read_prior_union(upto):
    union = set()
    if not os.path.isdir(CP):
        return union
    for fn in sorted(os.listdir(CP)):
        if not fn.startswith('phase-') or not fn.endswith('.json'):
            continue
        j = json.load(open(CP + '/' + fn))
        if j.get('phase') is not None and j['phase'] <= upto:
            union |= set(j.get('requirementIdsRequired', []))
    return union


def read_status():
    if os.path.exists(STATUS):
        return json.load(open(STATUS))
    ids, st, fq, r = all_ids()
    rows = {}
    byid = {q['id']: q for q in r['requirements']}
    byid.update({s['id']: s for s in r['standing']})
    byid.update({f['id']: f for f in r['futureQualification']})
    for i in ids + st:
        q = byid[i]
        rows[i] = {'id': i, 'status': 'unexecuted', 'kind': q.get('kind'),
                   'phase': q.get('phase'), 'acceptBlocking': q.get('acceptBlocking', True),
                   'artifacts': [], 'note': ''}
    for i in fq:
        q = byid[i]
        rows[i] = {'id': i, 'status': 'futureQualification', 'kind': q.get('kind'),
                   'phase': None, 'acceptBlocking': q.get('acceptBlocking', False),
                   'artifacts': [], 'note': 'Must not be demanded as a current blocker.'}
    return rows


def write_status(rows):
    with open(STATUS, 'w') as f:
        json.dump(rows, f, indent=1, sort_keys=True)


def mark(rows, ids, status, artifacts=None, note=''):
    assert status in STATUS_ENUM, status
    for i in ids:
        if i not in rows:
            rows[i] = {'id': i, 'status': 'unexecuted', 'kind': None, 'phase': None,
                       'acceptBlocking': True, 'artifacts': [], 'note': ''}
        rows[i]['status'] = status
        if artifacts:
            rows[i]['artifacts'] = sorted(set(rows[i].get('artifacts', [])) | set(artifacts))
        if note:
            rows[i]['note'] = note
    return rows


def write_checkpoint(phase, executed, failed, artifacts, helper_corrections, notes,
                     extra_required=()):
    """requirementIdsRequired is the UNION of this phase and all prior checkpoints.
    requirementIdsExecuted / Failed are CUMULATIVE: they are read back off the running
    requirement-status.json so a later phase can never drop an earlier ID."""
    os.makedirs(CP, exist_ok=True)
    required = read_prior_union(phase) | set(phase_ids(phase)) | set(extra_required)
    rows = read_status()
    executed = (set(executed) | {i for i, r in rows.items() if r['status'] == 'executed'}) & required
    failed = ((set(failed) | {i for i, r in rows.items() if r['status'] == 'failed'})
              & required) - set(executed)
    unexec = sorted(required - executed - failed)
    doc = {
        'phase': phase,
        'consumerId': CONSUMER,
        'requirementIdsRequired': sorted(required),
        'requirementIdsExecuted': sorted(executed),
        'requirementIdsUnexecuted': unexec,
        'requirementIdsFailed': sorted(failed),
        'artifacts': sorted(artifacts),
        'helperCorrections': helper_corrections,
        'notes': notes,
    }
    with open(CP + '/phase-%d.json' % phase, 'w') as f:
        json.dump(doc, f, indent=1)
    return doc
