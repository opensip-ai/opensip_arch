"""Do the NEW statements in this patch hold of the implemented projection, or are they assertions?

Limits: pure helper calls over synthetic already-admitted inputs. The fingerprints are
SYNTHETICALLY FORMATTED LABELS, not rehashed closure identities, and no import, Run closure or host
behaviour is exercised. Bounds inputs are supplied where an outcome is computed so the satisfied
rows are not matching-only."""
import importlib.util, json, sys, pathlib
W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v4/work')
sp = importlib.util.spec_from_file_location('M', W / 'docs/coop/design-corrections/workflows/workflows_model.v1.py')
M = importlib.util.module_from_spec(sp); sp.loader.exec_module(M)

FP_A = 'finding-key2:' + 'a' * 64      # synthetic label, NOT a rehashed identity
FP_B = 'finding-key2:' + 'b' * 64
def desc(path, qname, language='typescript', kind='function', disc='d1'):
    return {'schemaVersion': 2, 'ruleStableId': 'r', 'detectorSemanticsMajor': 1,
            'relatedSubjectKeys': [],
            'subjectKey': {'language': language, 'kind': kind, 'logicalPath': path,
                           'qualifiedName': qname, 'discriminator': disc}}
FINDINGS = {FP_A: {'fingerprint': FP_A}, FP_B: {'fingerprint': FP_B}}
RT_BOUNDS = {'observationWindow': {'startUtc': '2026-09-01T00:00:00Z',
                                   'endUtc': '2026-09-02T00:00:00Z'},
             'observedPopulation': 'test-suite'}
rows = []

# CLAIM 1 (new): "neither format distinguishes language, kind or discriminator: distinct findings
# can project to the same observation." Two DIFFERENT fingerprints whose subjectKeys agree on
# path+name but differ on all three other members.
descs = {FP_A: desc('src/a.ts', 'foo'),
         FP_B: desc('src/a.ts', 'foo', language='javascript', kind='method', disc='d2')}
row = [{'path': 'src/a.ts', 'symbol': 'foo', 'observability': 'observed-hit'}]
p = M.project_targets_to_imported_subjects([FP_A, FP_B], 'runtime', FINDINGS, descs, row)
rows.append({'claim': 'distinct findings differing only in language/kind/discriminator project to '
                      'the same observation',
             'holds': p[FP_A]['matched'] and p[FP_B]['matched']
                      and p[FP_A]['answerGranularity'] == p[FP_B]['answerGranularity'] == 'symbol',
             'detail': {k: v['answerGranularity'] for k, v in p.items()}})

# CLAIM 2: one row serving two targets is NOT the ambiguity refusal (ambiguity is many ROWS for one
# TARGET). Confirms the coarsening is disclosed rather than refused, which is what the law says.
rows.append({'claim': 'one row serving two targets is a disclosed coarsening, not the ambiguity '
                      'refusal',
             'holds': len(p) == 2 and all(v['matched'] for v in p.values())})

# CLAIM 3 (retained): ambiguity IS many rows for one target.
try:
    M.project_targets_to_imported_subjects(
        [FP_A], 'runtime', FINDINGS, descs,
        row + [{'path': 'src/a.ts', 'observability': 'observed-hit'}])
    amb = 'ADMIT'
except Exception as e:
    amb = getattr(e, 'remedy', str(e)).split(':')[0]
rows.append({'claim': 'two rows matching one target still refuse',
             'holds': amb == 'native.imported-projection-ambiguous-target', 'detail': amb})

# CLAIM 4 (new prose): granularityWidenedToFile is disclosed "in the projection and successful
# outcome" - so present on a SATISFIED outcome and absent from a FAILING one. Bounds supplied.
pf = M.project_targets_to_imported_subjects([FP_A], 'runtime', FINDINGS, descs,
                                            [{'path': 'src/a.ts', 'observability': 'observed-hit'}])
req = {'relation': 'runtime-observation', 'minResolution': 'observed', 'completeness': 'complete'}
ok = M.imported_requirement_outcome(req, pf, dict(RT_BOUNDS, available=True, consumable=True,
                                                  windowSatisfiesRequirement=True), True)
bad = M.imported_requirement_outcome(req, pf, dict(RT_BOUNDS, available=True, consumable=True,
                                                   windowSatisfiesRequirement=False), True)
rows.append({'claim': 'widening is disclosed on a satisfied outcome and absent from a failing one',
             'holds': pf[FP_A]['granularityWidenedToFile'] is True
                      and any(d['kind'] == 'granularity-widened-to-file' for d in ok['disclosures'])
                      and not any(d['kind'] == 'granularity-widened-to-file' for d in bad['disclosures'])
                      and bad['deficiency'] == 'observation-window-insufficient',
             'detail': {'satisfiedDisclosures': [d['kind'] for d in ok['disclosures']],
                        'failingDeficiency': bad['deficiency']}})

# CLAIM 5: the satisfied outcome still carries the admitted BOUNDS, so a satisfied result is a
# bounded observation and not a matching-only assertion.
rows.append({'claim': 'a satisfied outcome carries its observation window and population',
             'holds': any(d.get('observationWindow') == RT_BOUNDS['observationWindow']
                          and d.get('observedPopulation') == 'test-suite'
                          for d in ok['disclosures']),
             'detail': [d for d in ok['disclosures'] if d['kind'] == 'observation-bounds']})

# CLAIM 6: the structural presence of every lookupMeaning survives the removed prose control.
import json as J
rep = J.loads((W / 'docs/coop/design-corrections/workflows/schemas/repair.schema.json').read_text())
keys = rep['x-opensip-mutation-operation-map']['receiptIdempotencyKeyByStepKind']['recipes']
rows.append({'claim': 'every step kind still publishes a key and a lookup meaning',
             'holds': all(keys[k].get('key') and keys[k].get('lookupMeaning') for k in keys)
                      and set(keys) == {'mutation', 'repair-apply', 'import', 'native-preparation'},
             'detail': sorted(keys)})

print(json.dumps({'standing': __doc__, 'allHold': all(r['holds'] for r in rows), 'claims': rows},
                 indent=1))
