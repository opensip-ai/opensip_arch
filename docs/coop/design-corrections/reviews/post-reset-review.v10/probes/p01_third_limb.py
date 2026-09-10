"""p01 - Does the THIRD limb (unannotated governed field) actually refuse now?

v9-S1 was: relation_annotation_closure iterated only fields that already carry x-opensip-digest,
so an unannotated DigestHex/Sha256Text/CanonicalPath was invisible; the v9 reviewer injected 39
such fields (13 relations x 3 forms) and every one ADMITTED.

This probe re-runs that exact experiment against the v10 reference, in all supported governed
forms, plus:
  - the unmodified document as a positive control (must ADMIT for all 13),
  - REMOVAL of each existing shipped annotation (must REFUSE, and specifically as unannotated),
  - a lawful annotated+joined injection (must ADMIT) so the refusals are not just "any new field
    refuses",
  - the inline-pattern form and the alias-$ref form, not only the direct $ref form.
"""
import sys
sys.path.insert(0, '/tmp/opensip-design-corrections/post-reset-review.v10/probes')
import copy
import harness

m = harness.load_model()
BASE = harness.base_document(m)
RELS = list(BASE['x-opensip-relation-registry']['relations'].keys())
FORMS = ('DigestHex', 'Sha256Text', 'CanonicalPath')

out = {'modelSha256': m._sha256, 'relations': RELS, 'forms': list(FORMS)}


def selector_of(doc, name):
    row = doc['x-opensip-relation-registry']['relations'][name]
    return doc['$defs'][row['selector'].split('/')[-1]]


# ---------------------------------------------------------------- positive control: shipped doc
out['control_shipped'] = {r: harness.try_closure(m, r, harness.base_document(m)) for r in RELS}
out['control_shipped_all_admit'] = all(v[0] == 'ADMIT' for v in out['control_shipped'].values())

cov = m.relation_digest_annotation_coverage(BASE)
out['shipped_coverage'] = {'total': cov['total'], 'annotated': cov['annotated'],
                           'unannotated': cov['unannotated']}

# ---------------------------------------------- 1. direct $ref injection, 13 relations x 3 forms
direct = {}
for rel in RELS:
    for form in FORMS:
        doc = harness.base_document(m)
        selector_of(doc, rel)['properties']['reviewerInjected'] = {'$ref': '#/$defs/' + form}
        direct[rel + '/' + form] = harness.try_closure(m, rel, doc)
out['inject_direct_ref'] = direct
out['inject_direct_ref_count'] = len(direct)
out['inject_direct_ref_all_refuse'] = all(v[0] == 'REFUSE' for v in direct.values())
out['inject_direct_ref_all_unannotated_cause'] = all(
    v[0] == 'REFUSE' and 'RELATION_DIGEST_UNANNOTATED' in v[1] for v in direct.values())

# ------------------------------------------------------ 2. inline pattern injection (no $ref)
inline = {}
for rel in RELS:
    for form in FORMS:
        doc = harness.base_document(m)
        pattern = doc['$defs'][form].get('pattern')
        selector_of(doc, rel)['properties']['reviewerInlined'] = {
            'type': 'string', 'pattern': pattern}
        inline[rel + '/' + form] = harness.try_closure(m, rel, doc)
out['inject_inline_pattern'] = inline
out['inject_inline_pattern_all_unannotated_cause'] = all(
    v[0] == 'REFUSE' and 'RELATION_DIGEST_UNANNOTATED' in v[1] for v in inline.values())

# ------------------------------------------- 3. transitive alias $ref injection (alias -> form)
alias = {}
for rel in RELS:
    for form in FORMS:
        doc = harness.base_document(m)
        doc['$defs']['ReviewerAlias'] = {'$ref': '#/$defs/' + form}
        selector_of(doc, rel)['properties']['reviewerAliased'] = {'$ref': '#/$defs/ReviewerAlias'}
        alias[rel + '/' + form] = harness.try_closure(m, rel, doc)
out['inject_alias_ref'] = alias
out['inject_alias_ref_all_unannotated_cause'] = all(
    v[0] == 'REFUSE' and 'RELATION_DIGEST_UNANNOTATED' in v[1] for v in alias.values())

# --------------------------------------------------- 4. nested / array / nullable-branch forms
shapes = {}
for form in FORMS:
    variants = {
        'nested_object': {'type': 'object',
                          'properties': {'inner': {'$ref': '#/$defs/' + form}}},
        'array_items': {'type': 'array', 'items': {'$ref': '#/$defs/' + form}},
        'nullable_oneOf': {'oneOf': [{'$ref': '#/$defs/' + form}, {'type': 'null'}]},
        'additionalProperties': {'type': 'object',
                                 'additionalProperties': {'$ref': '#/$defs/' + form}},
        'array_of_object': {'type': 'array', 'items': {
            'type': 'object', 'properties': {'deep': {'$ref': '#/$defs/' + form}}}},
    }
    for vname, schema in variants.items():
        doc = harness.base_document(m)
        selector_of(doc, 'file')['properties']['reviewerShape'] = schema
        shapes[form + '/' + vname] = harness.try_closure(m, 'file', doc)
out['inject_shapes_on_file'] = shapes
out['inject_shapes_all_unannotated_cause'] = all(
    v[0] == 'REFUSE' and 'RELATION_DIGEST_UNANNOTATED' in v[1] for v in shapes.values())

# ------------------------------------------- 5. REMOVE each existing shipped annotation (13 rel)
removed = {}
for rel in RELS:
    sel = selector_of(BASE, rel)
    for field, schema in sel.get('properties', {}).items():
        if isinstance(schema, dict) and 'x-opensip-digest' in schema:
            doc = harness.base_document(m)
            del selector_of(doc, rel)['properties'][field]['x-opensip-digest']
            removed[rel + '.' + field] = harness.try_closure(m, rel, doc)
out['remove_existing_annotation'] = removed
out['remove_existing_annotation_count'] = len(removed)
out['remove_existing_all_refuse'] = all(v[0] == 'REFUSE' for v in removed.values())

# ---------------------------------- 6. NEGATIVE CONTROL: lawful annotated field must still admit
lawful = {}
for rel in RELS:
    for form in FORMS:
        doc = harness.base_document(m)
        selector_of(doc, rel)['properties']['reviewerLawful'] = {
            '$ref': '#/$defs/' + form,
            'x-opensip-digest': {'representation': 'raw-artifact', 'retention': 'not-joined',
                                 'reason': 'reviewer control field, deliberately not joined'}}
        lawful[rel + '/' + form] = harness.try_closure(m, rel, doc)
out['control_lawful_not_joined'] = lawful
out['control_lawful_all_admit'] = all(v[0] == 'ADMIT' for v in lawful.values())

# ------------- 7. NEGATIVE CONTROL: a NON-governed unannotated field must not trip the new limb
nongoverned = {}
for rel in RELS:
    doc = harness.base_document(m)
    selector_of(doc, rel)['properties']['reviewerPlainInt'] = {'type': 'integer'}
    selector_of(doc, rel)['properties']['reviewerPlainStr'] = {'type': 'string'}
    nongoverned[rel] = harness.try_closure(m, rel, doc)
out['control_nongoverned_unannotated'] = nongoverned
out['control_nongoverned_all_admit'] = all(v[0] == 'ADMIT' for v in nongoverned.values())

out['SUMMARY'] = {
    'shippedAdmits': out['control_shipped_all_admit'],
    'directRefRefusals': sum(1 for v in direct.values()
                             if v[0] == 'REFUSE' and 'RELATION_DIGEST_UNANNOTATED' in v[1]),
    'inlineRefusals': sum(1 for v in inline.values()
                          if v[0] == 'REFUSE' and 'RELATION_DIGEST_UNANNOTATED' in v[1]),
    'aliasRefusals': sum(1 for v in alias.values()
                         if v[0] == 'REFUSE' and 'RELATION_DIGEST_UNANNOTATED' in v[1]),
    'shapeRefusals': sum(1 for v in shapes.values()
                         if v[0] == 'REFUSE' and 'RELATION_DIGEST_UNANNOTATED' in v[1]),
    'shapeTotal': len(shapes),
    'removalRefusals': sum(1 for v in removed.values() if v[0] == 'REFUSE'),
    'lawfulAdmits': sum(1 for v in lawful.values() if v[0] == 'ADMIT'),
    'nonGovernedAdmits': sum(1 for v in nongoverned.values() if v[0] == 'ADMIT'),
}

harness.emit(out, '/tmp/opensip-design-corrections/post-reset-review.v10/work/p01.json')
print(harness.json.dumps(out['SUMMARY'], indent=2))
