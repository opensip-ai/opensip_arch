import json, pathlib, collections

R = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/coop/design-corrections')

# ---------------------------------------------------------------- workflow-cases.v1.json
P = R / 'workflows/workflow-cases.v1.json'
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
rs = d['repairScenario']
cases = rs['cases']
ids = [c['id'] for c in cases]
assert 'preview-evidence-requirement-resolution-incomplete-not-applicable' not in ids

# The retained POSITIVE stays exactly as it is: satisfied, no deficiency, admitted.
assert rs['evidenceRequirements'] == [{'relation': 'imports', 'minResolution': 'resolved-target',
                                       'completeness': 'complete', 'satisfied': True}]

def req(**kw):
    r = collections.OrderedDict([('relation', 'references'),
                                 ('minResolution', 'resolved-binding'),
                                 ('completeness', 'complete'),
                                 ('satisfied', False)])
    r.update(kw)
    return r

new = [
    collections.OrderedDict([
        ('id', 'preview-evidence-requirement-resolution-incomplete-not-applicable'),
        ('evidenceRequirements', [req(deficiency='resolution-incomplete')]),
        ('expect', collections.OrderedDict([
            ('applicable', False),
            ('unmet', 'REPAIR.EVIDENCE_RUN_UNAVAILABLE'),
            ('unmetRemedyContains', 'resolution-incomplete'),
        ])),
        ('note', 'CB6-MUST-1 admitted FAILING requirement. resolution-incomplete is the section 4.6 '
                 'step 6 outcome for a universal negative under unresolvedEdgePolicy=forbid over an '
                 'affected target - the outcome a destructive unused-code repair turns on - and it '
                 'has NO D9Deficiency member, so under the former D9 typing this exact record was '
                 'unrepresentable. The plan is not applicable and the exact cause reaches the unmet '
                 'precondition instead of being collapsed to verdict-indeterminate or dropped.'),
    ]),
    collections.OrderedDict([
        ('id', 'preview-evidence-requirement-external-consumers-unknown-not-applicable'),
        ('evidenceRequirements', [req(deficiency='external-consumers-unknown')]),
        ('expect', collections.OrderedDict([
            ('applicable', False),
            ('unmet', 'REPAIR.EVIDENCE_RUN_UNAVAILABLE'),
            ('unmetRemedyContains', 'external-consumers-unknown'),
        ])),
        ('note', 'The second of the four previously unrepresentable outcomes, kept DISTINCT from the '
                 'first: both were verdict-indeterminate under the D9 typing, and they are different '
                 'remedies (resolve the edges vs declare the external consumers).'),
    ]),
    collections.OrderedDict([
        ('id', 'preview-evidence-requirement-satisfied-carrying-a-deficiency-refused'),
        ('evidenceRequirements', [req(satisfied=True, deficiency='resolution-incomplete')]),
        ('expect', collections.OrderedDict([('refusal', None)])),
        ('expectRemedyContains', 'native.sufficiency-outcome-on-satisfied-requirement'),
        ('note', 'sufficiency_v2 returns disclosures, never a deficiency, when it is satisfied; a '
                 'record claiming both contradicts its own producer and refuses before any '
                 'descriptor exists.'),
    ]),
    collections.OrderedDict([
        ('id', 'preview-evidence-requirement-unsatisfied-without-a-cause-refused'),
        ('evidenceRequirements', [req()]),
        ('expect', collections.OrderedDict([('refusal', None)])),
        ('expectRemedyContains', 'native.sufficiency-outcome-missing'),
        ('note', 'The third formerly conforming reading - omit the optional field - is now refused: '
                 'an unsatisfied requirement that names no cause drops the only disclosure of why '
                 'the repair is inapplicable.'),
    ]),
    collections.OrderedDict([
        ('id', 'preview-evidence-requirement-d9-spelling-refused'),
        ('evidenceRequirements', [req(deficiency='verdict-indeterminate')]),
        ('expect', collections.OrderedDict([('refusal', None)])),
        ('expectRemedyContains', 'native.sufficiency-outcome-not-a-native-outcome'),
        ('note', 'verdict-indeterminate is a D9Deficiency member and not a native per-requirement '
                 'outcome. The former D9 typing admitted it here as the lossy D9-mapped value for '
                 'all four successor causes; it is now refused at the boundary as well as by the '
                 'schema.'),
    ]),
]
cases.extend(new)
P.write_text(json.dumps(d, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
print('cases now', len(cases))
