"""Checkpoint and requirement-status bookkeeping (own process record; never an oracle)."""
import json
import os

OUT = '/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v2/output/'
REQ = '/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v2/requirements.json'
CONSUMER = 'consumer-b.v24'


def requirements():
    return json.load(open(REQ))


def all_ids():
    r = requirements()
    kinds = {x['id']: x for x in r['standing'] + r['requirements']}
    phases = {i: p['n'] for p in r['phases'] for i in p['ids']}
    return kinds, phases, r


def load_status():
    p = OUT + 'requirement-status.json'
    if os.path.exists(p):
        return json.load(open(p))
    kinds, phases, r = all_ids()
    rows = []
    for x in r['standing'] + r['requirements']:
        rows.append({"id": x['id'], "phase": phases[x['id']], "kind": x['kind'],
                     "acceptBlocking": x['acceptBlocking'], "status": "unexecuted", "artifact": None,
                     "firstRefusal": None, "notes": ""})
    for x in r['futureQualification']:
        rows.append({"id": x['id'], "phase": None, "kind": x['kind'], "acceptBlocking": False,
                     "status": "futureQualification", "artifact": None, "firstRefusal": None,
                     "notes": "Not demanded; not claimed as proof."})
    return {"consumerId": CONSUMER, "rows": rows}


def set_status(status, rid, state, artifact=None, first_refusal=None, notes=None):
    for row in status['rows']:
        if row['id'] == rid:
            row['status'] = state
            if artifact is not None:
                row['artifact'] = artifact
            if first_refusal is not None:
                row['firstRefusal'] = first_refusal
            if notes is not None:
                row['notes'] = notes
            return
    raise KeyError(rid)


def save_status(status):
    with open(OUT + 'requirement-status.json', 'w') as fh:
        json.dump(status, fh, indent=1, sort_keys=False)


def write_checkpoint(phase, status, artifacts, helper_corrections, notes):
    kinds, phases, r = all_ids()
    required = sorted([i for i, p in phases.items() if p <= phase])
    prior = set()
    for n in range(phase):
        p = OUT + f'checkpoints/phase-{n}.json'
        if os.path.exists(p):
            prior |= set(json.load(open(p))['requirementIdsRequired'])
    required = sorted(set(required) | prior)
    st = {row['id']: row['status'] for row in status['rows']}
    cp = {"phase": phase, "consumerId": CONSUMER,
          "requirementIdsRequired": required,
          "requirementIdsExecuted": [i for i in required if st.get(i) == 'executed'],
          "requirementIdsUnexecuted": [i for i in required if st.get(i) == 'unexecuted'],
          "requirementIdsFailed": [i for i in required if st.get(i) == 'failed'],
          "artifacts": artifacts, "helperCorrections": helper_corrections, "notes": notes}
    os.makedirs(OUT + 'checkpoints', exist_ok=True)
    with open(OUT + f'checkpoints/phase-{phase}.json', 'w') as fh:
        json.dump(cp, fh, indent=1)
    return cp


def dump(rel, obj):
    p = OUT + rel
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w') as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=False)
    return p
