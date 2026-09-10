"""v9 probe 04 - is the residueRule's THIRD limb consumed anywhere?

Declared law (relation-payload-schemas.v2.json #/x-opensip-digest-law/residueRule):
  "An annotated field with no join, a join naming a field the selector does not have, and
   an unannotated digest/path field are each inadmissible."
and #/x-opensip-digest-law/standing:
  "There is no default and no residue: a new such field added without an annotation is
   inadmissible."

Limbs 1 and 2 are consumed by relation_annotation_closure (p03 verified both, with the
correct relation and without ordering interference). This probe asks whether limb 3 is
consumed by ANY shipped checker, and whether the suite check whose NAME asserts it
("every-relation-payload-digest-and-path-field-is-annotated-and-joined") actually tests it.
"""
import json, copy, hashlib, importlib.util, subprocess
from pathlib import Path

SUB = Path('/tmp/opensip-design-corrections/candidate-subject.v9')
FOUND = SUB / 'docs/coop/design-corrections/foundation'
spec = importlib.util.spec_from_file_location('im_p04', FOUND / 'identity-model.py')
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)

rows = []

# --- A. Limb 2 in isolation (ADD a bogus join field, keep real ones joined) so that the
#        residue check cannot fire first. p03's version renamed an existing role and hit
#        limb 1 first: that was a probe ordering artifact, not a product defect.
doc = copy.deepcopy(M.RELATION_DOCUMENT)
doc['x-opensip-relation-registry']['relations']['file']['snapshotJoins'][0]['anchorPathField'] = 'inventedField'
try:
    M.relation_annotation_closure('file', doc); a = None
except Exception as e:
    a = str(e)
rows.append({'case': 'limb2-join-names-absent-field-isolated', 'raised': a,
             'intended': 'RELATION_JOIN_FIELD_UNKNOWN',
             'reachedIntendedCause': bool(a and 'RELATION_JOIN_FIELD_UNKNOWN' in a)})

# --- B. Limb 3: unannotated governed-ref field added to each relation selector.
for rname in sorted(M.RELATIONS):
    doc = copy.deepcopy(M.RELATION_DOCUMENT)
    sel = M.RELATIONS[rname]['selector'].split('/')[-1]
    for refname in ('DigestHex', 'CanonicalPath', 'Sha256Text'):
        if refname not in doc['$defs']:
            continue
        d2 = copy.deepcopy(doc)
        d2['$defs'][sel]['properties']['strayUnannotated'] = {'$ref': '#/$defs/' + refname}
        try:
            M.relation_annotation_closure(rname, d2); r = None
        except Exception as e:
            r = str(e)
        rows.append({'case': f'limb3-unannotated-{refname}-added-to-{rname}', 'raised': r,
                     'intended': 'any refusal', 'reachedIntendedCause': r is not None})

# --- C. Does the suite check that NAMES this property actually detect it?
#        Reproduce the exact assertion from check-identity.py verbatim against a document
#        carrying an unannotated field.
doc = copy.deepcopy(M.RELATION_DOCUMENT)
doc['$defs']['FilePayloadV1']['properties']['strayUnannotated'] = {'$ref': '#/$defs/CanonicalPath'}
def suite_assertion(document):
    # verbatim shape of check-identity.py 'every-relation-payload-digest-and-path-field-is-annotated-and-joined'
    rels = document['x-opensip-relation-registry']['relations']
    return (all(M.relation_annotation_closure(name, document) is not None for name in rels) and
            {name for name, row in rels.items() if row['snapshotJoins'] or 'bodyIdentityJoin' in row}
            == {'file', 'package', 'vcs-change', 'clones'})
try:
    verdict = suite_assertion(doc)
except Exception as e:
    verdict = 'raised:' + str(e)
rows.append({'case': 'suite-check-named-annotated-and-joined-vs-unannotated-field',
             'suiteCheckStillPasses': verdict,
             'note': 'True means the check whose name asserts annotation coverage does not test it'})

# --- D. Any other consumer anywhere in the subject?
hits = subprocess.run(
    ['grep', '-rn', '--include=*.py', '-e', 'x-opensip-digest', str(SUB / 'docs/coop/design-corrections')],
    capture_output=True, text=True).stdout.strip().splitlines()
consumers = [h for h in hits if 'reviews/' not in h]

# --- E. Positive control: real shipped document is coherent for every relation.
real_ok = {}
for rname in sorted(M.RELATIONS):
    try:
        M.relation_annotation_closure(rname); real_ok[rname] = 'PASS'
    except Exception as e:
        real_ok[rname] = 'REFUSED:' + str(e)

out = {'probe': 'p04_third_limb',
       'standing': 'independent reviewer probe; design/reference only',
       'documentSha256': hashlib.sha256((FOUND / 'relation-payload-schemas.v2.json').read_bytes()).hexdigest(),
       'cases': rows,
       'shippedDocumentCoherent': real_ok,
       'annotationConsumersOutsideReviews': consumers}
print(json.dumps(out, indent=1))
