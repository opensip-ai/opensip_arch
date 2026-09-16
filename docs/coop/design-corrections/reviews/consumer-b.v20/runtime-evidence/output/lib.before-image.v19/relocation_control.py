"""Relocation / location-independence controls.

v16: "Runtime location itself must not become evidence of a semantic change: semantic
fixture metadata must be chosen explicitly, and relocation with the same declared inputs
should reproduce selected graph identities. Distinguish whole transport-file equality from
selected retained graph equality."

Three distinct measurements, reported separately:

  A. LOCATION-FREE RETAINED GRAPH -- no retained blob byte and no object-table value of any
     exported Run contains any runtime-location string (this session root, the two prior
     session roots, the output dir, or the interpreter prefix).
  B. RELOCATION REPRODUCES SELECTED GRAPH IDENTITIES -- the same builder, run twice with a
     DIFFERENT output directory and the same declared kit, yields byte-identical selected
     graph identities and a byte-identical retained-graph digest.
  C. TRANSPORT-FILE EQUALITY IS NOT GRAPH EQUALITY -- the transport envelope carries
     location-bearing and run-order-bearing metadata (artefact paths, admission logs,
     closure reports), so whole-file equality is a STRICTLY STRONGER and different claim
     from selected retained graph equality. Both are measured; only (B) is required.
"""
import hashlib
import importlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_fixture as FX
import opensip_closure as CL

V16 = '/tmp/opensip-design-corrections/consumer-b.v19'
OUT = V16 + '/output'

FORBIDDEN = [
    V16,
    '/tmp/opensip-design-corrections/consumer-b' + '.v15',
    '/tmp/opensip-design-corrections/consumer-b' + '.v14',
    'consumer-b.v19', 'consumer-b' + '.v15', 'consumer-b' + '.v14',
    '/tmp/opensip-architecture-review-env',
    OUT,
]

RUNS = [('run_syntax_code_full', 'syntax-code'), ('run_ts_full', 'typescript'),
        ('run_rust_full', 'rust'), ('run_rust_partial', 'rust-partial'),
        ('run_syntax_data', 'syntax-data')]


def graph_digest(store, claim):
    """The SELECTED RETAINED GRAPH digest: the claimed Run identity plus the object table and
    every retained blob, in canonical order. Deliberately excludes the transport envelope."""
    h = hashlib.sha256()
    h.update(K.C({'claim': claim}))
    for tid in sorted(store.objects):
        h.update(tid.encode())
        h.update(K.C(store.objects[tid]))
    for d in sorted(store.blobs):
        h.update(d.encode())
        h.update(store.blobs[d])
    return h.hexdigest()


def build(mod_name):
    mod = importlib.import_module(mod_name)
    if hasattr(mod, 'graph'):
        return mod.graph()
    base = importlib.import_module(mod.BASE) if hasattr(mod, 'BASE') else mod
    return mod.complete(base.build())


def main():
    res = {'standing': __doc__, 'forbiddenLocationStrings': FORBIDDEN, 'runs': []}
    bad_any = []
    for mod_name, label in RUNS:
        g = build(mod_name)
        st, out = g['st'], g['out']
        claim = {'runId': out['runId'], 'sealId': out['sealId'],
                 'evidenceId': out['evidenceId'], 'proofId': out['proofId'],
                 'planId': g['plan_id'], 'snapshotId': g['snapshot_id'],
                 'verdict': out['proof']['verdict']}
        # ---- A
        leaks = FX.assert_location_free(st.blobs, st.objects, FORBIDDEN)
        # ---- B: rebuild with a different output directory, same declared kit
        alt = OUT + '/relocated'
        os.makedirs(alt, exist_ok=True)
        saved = {}
        for m in (mod_name, getattr(importlib.import_module(mod_name), 'BASE', None)):
            if not m:
                continue
            mm = importlib.import_module(m)
            if hasattr(mm, 'OUT'):
                saved[m] = mm.OUT
                mm.OUT = alt
        g2 = build(mod_name)
        for m, v in saved.items():
            importlib.import_module(m).OUT = v
        st2, out2 = g2['st'], g2['out']
        claim2 = {'runId': out2['runId'], 'sealId': out2['sealId'],
                  'evidenceId': out2['evidenceId'], 'proofId': out2['proofId'],
                  'planId': g2['plan_id'], 'snapshotId': g2['snapshot_id'],
                  'verdict': out2['proof']['verdict']}
        gd1, gd2 = graph_digest(st, claim), graph_digest(st2, claim2)
        # ---- C: transport-file equality, measured separately
        tp = OUT + '/runs/%s.store.json' % label
        transport_sha = (hashlib.sha256(open(tp, 'rb').read()).hexdigest()
                         if os.path.exists(tp) else None)
        transport_doc = json.load(open(tp)) if os.path.exists(tp) else {}
        envelope_keys = sorted(k for k in transport_doc
                              if k not in ('objectTable', 'blobs', 'labels'))
        row = {
            'run': label,
            'A_locationFreeRetainedGraph': {
                'leaks': leaks, 'pass': not leaks,
                'blobsScanned': len(st.blobs), 'objectsScanned': len(st.objects)},
            'B_relocationReproducesSelectedGraphIdentities': {
                'firstOutputDir': OUT, 'secondOutputDir': alt,
                'claimFirst': claim, 'claimSecond': claim2,
                'claimedIdentitiesEqual': claim == claim2,
                'selectedRetainedGraphDigestFirst': gd1,
                'selectedRetainedGraphDigestSecond': gd2,
                'selectedRetainedGraphDigestEqual': gd1 == gd2,
                'objectTableKeysEqual': sorted(st.objects) == sorted(st2.objects),
                'blobKeysEqual': sorted(st.blobs) == sorted(st2.blobs),
                'pass': claim == claim2 and gd1 == gd2},
            'C_transportFileEqualityIsADifferentClaim': {
                'transportFileSha256': transport_sha,
                'transportEnvelopeKeysOutsideTheGraph': envelope_keys,
                'why': ('The transport envelope carries artefact paths, the per-record '
                        'schema-admission log and the closure report. Those are runtime '
                        'observations ABOUT the graph, not members of it, so whole-file '
                        'equality is a strictly stronger and different claim. Only the '
                        'selected retained graph digest in (B) is required to be stable '
                        'under relocation.'),
                'declaredExtraBlobsAreExportedButAreNotEvaluatorInputs': (
                    'Every raw blob and frame this exporter declares is exported, including '
                    'retained output frames and evaluation-subject frames that no annotated '
                    '64-hex field names. The closure report lists them under '
                    'UNREFERENCED_CAS_BLOBS_ARE_NOT_EVALUATION_INPUTS: exported for '
                    'independent inspection, never admitted as evaluator inputs.')},
        }
        if leaks or not row['B_relocationReproducesSelectedGraphIdentities']['pass']:
            bad_any.append(label)
        res['runs'].append(row)
        print('%-14s A-locationFree=%-5s B-relocationStable=%-5s graphDigest=%s'
              % (label, row['A_locationFreeRetainedGraph']['pass'],
                 row['B_relocationReproducesSelectedGraphIdentities']['pass'], gd1[:16]))
        if leaks:
            for x in leaks[:4]:
                print('     LEAK', x)
    with open(OUT + '/vectors/relocation-and-transport-equality.json', 'w') as f:
        json.dump(res, f, indent=1)
    print()
    print('runs failing a location/relocation control:', bad_any)
    sys.exit(1 if bad_any else 0)


main()
