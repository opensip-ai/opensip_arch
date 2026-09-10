"""p05 - Does the new check actually FAIL when the enforcement is absent?

The honest way to answer this is not a hand-written neutralisation stub (the author's own stub is
retained in the subject as an explicitly failed attempt). It is to run the IDENTICAL experiment
against the real prior source image - frozen v9's identity-model.py - and show the same inputs
that v10 refuses were admitted by v9.

Both models are loaded from the reviewer's own copies of the two frozen subjects, with their
sha256 recorded, so this is a source-image comparison, not a synthetic mutation.

Also re-runs the exact assertion of the authored check that v9 named but did not test.
"""
import sys
sys.path.insert(0, '/tmp/opensip-design-corrections/post-reset-review.v10/probes')
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import harness

V9 = Path('/tmp/opensip-design-corrections/candidate-subject.v9/docs/coop/design-corrections/foundation')
WORK = Path('/tmp/opensip-design-corrections/post-reset-review.v10/work/v9copy')


def load_v9():
    """Load the frozen v9 foundation from a disposable copy (never the frozen tree)."""
    import shutil
    if WORK.exists():
        shutil.rmtree(WORK)
    shutil.copytree(V9, WORK)
    for n in ('identity-model.py', 'canonical.py', 'relation-payload-schemas.v2.json',
              'identity-schemas.v2.json'):
        a = hashlib.sha256((WORK / n).read_bytes()).hexdigest()
        b = hashlib.sha256((V9 / n).read_bytes()).hexdigest()
        assert a == b, ('v9 copy drift', n)
    spec = importlib.util.spec_from_file_location('rev10_v9_model', WORK / 'identity-model.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod._sha256 = hashlib.sha256((WORK / 'identity-model.py').read_bytes()).hexdigest()
    return mod


m10 = harness.load_model()
m9 = load_v9()

out = {'v10ModelSha256': m10._sha256, 'v9ModelSha256': m9._sha256,
       'v9RelationDocSha256': hashlib.sha256((V9 / 'relation-payload-schemas.v2.json').read_bytes()).hexdigest(),
       'v10RelationDocSha256': hashlib.sha256(
           (harness.SUBJ_FOUND / 'relation-payload-schemas.v2.json').read_bytes()).hexdigest()}
out['relationDocumentIdenticalAcrossV9V10'] = (
    out['v9RelationDocSha256'] == out['v10RelationDocSha256'])

FORMS = ('DigestHex', 'Sha256Text', 'CanonicalPath')
RELS = list(m10.RELATION_DOCUMENT['x-opensip-relation-registry']['relations'].keys())


def selector_of(doc, name):
    row = doc['x-opensip-relation-registry']['relations'][name]
    return doc['$defs'][row['selector'].split('/')[-1]]


def attempt(model, name, doc):
    try:
        model.relation_annotation_closure(name, doc)
        return 'ADMIT'
    except Exception as exc:
        return 'REFUSE:' + str(exc).split(':')[0]


# ------------------------------------------- identical 39 injections against BOTH source images
rows = []
for rel in RELS:
    for form in FORMS:
        base9 = copy.deepcopy(m9.RELATION_DOCUMENT)
        base10 = copy.deepcopy(m10.RELATION_DOCUMENT)
        for doc in (base9, base10):
            selector_of(doc, rel)['properties']['reviewerInjected'] = {'$ref': '#/$defs/' + form}
        rows.append({'relation': rel, 'form': form,
                     'v9': attempt(m9, rel, base9), 'v10': attempt(m10, rel, base10)})
out['injections'] = rows
out['injectionCount'] = len(rows)
out['v9AdmittedAll'] = all(r['v9'] == 'ADMIT' for r in rows)
out['v10RefusedAll'] = all(r['v10'].startswith('REFUSE') for r in rows)
out['v10CauseSet'] = sorted({r['v10'] for r in rows})
out['v9CauseSet'] = sorted({r['v9'] for r in rows})

# ------------------------------------ shipped document is a positive control on BOTH source images
out['shipped_v9'] = {r: attempt(m9, r, copy.deepcopy(m9.RELATION_DOCUMENT)) for r in RELS}
out['shipped_v10'] = {r: attempt(m10, r, copy.deepcopy(m10.RELATION_DOCUMENT)) for r in RELS}
out['shippedAdmitsOnBoth'] = (all(v == 'ADMIT' for v in out['shipped_v9'].values())
                              and all(v == 'ADMIT' for v in out['shipped_v10'].values()))

# ---------------- the authored check's OWN assertion, which v9 named but did not actually test
# check-identity.py: relation_annotation_closure returns non-None for each relation AND the
# join-bearing relation set equals {file, package, vcs-change, clones}.
def authored_assertion(model, doc):
    try:
        closures = {r: model.relation_annotation_closure(r, doc) for r in RELS}
    except Exception as exc:
        return {'assertionEvaluates': False, 'raised': str(exc)[:120]}
    joined = {r for r, row in closures.items() if row and row.get('snapshotJoins')}
    return {'assertionEvaluates': all(v is not None for v in closures.values()),
            'joinBearingSet': sorted(joined),
            'joinBearingSetAsExpected': joined == {'file', 'package', 'vcs-change', 'clones'}}


tainted9 = copy.deepcopy(m9.RELATION_DOCUMENT)
selector_of(tainted9, 'file')['properties']['strayPath'] = {'$ref': '#/$defs/CanonicalPath'}
tainted10 = copy.deepcopy(m10.RELATION_DOCUMENT)
selector_of(tainted10, 'file')['properties']['strayPath'] = {'$ref': '#/$defs/CanonicalPath'}

out['authoredAssertion_v9_withUnannotatedCanonicalPath'] = authored_assertion(m9, tainted9)
out['authoredAssertion_v10_withUnannotatedCanonicalPath'] = authored_assertion(m10, tainted10)

out['ASSESSMENT'] = {
    'sameRelationDocumentBothSides': out['relationDocumentIdenticalAcrossV9V10'],
    'injectionCount': out['injectionCount'],
    'v9_admitted_all_39': out['v9AdmittedAll'],
    'v10_refused_all_39': out['v10RefusedAll'],
    'v10_causes': out['v10CauseSet'],
    'shippedDocumentAdmitsOnBothImages': out['shippedAdmitsOnBoth'],
    'authoredCheckAssertion_v9_stillTrueOnTaintedDoc':
        out['authoredAssertion_v9_withUnannotatedCanonicalPath'].get('assertionEvaluates'),
    'authoredCheckAssertion_v10_nowRefusesTaintedDoc':
        out['authoredAssertion_v10_withUnannotatedCanonicalPath'].get('assertionEvaluates') is False,
    'interpretation': ('the delta, not a stub, supplies the discriminating evidence: identical '
                       'inputs and identical relation document, opposite outcomes across the two '
                       'real source images'),
}

harness.emit(out, '/tmp/opensip-design-corrections/post-reset-review.v10/work/p05.json')
print(json.dumps(out['ASSESSMENT'], indent=2))
