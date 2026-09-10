"""Independent controls for CX-V19-REPAIR-PROJECTION-MAPPING, CX-V19-WORKFLOW-SUBJECT-PROJECTION,
the withdrawn CB7-SHOULD-1 premise, and the corrected 'generic exception' wording.
Disposable copy only."""
import importlib.util, json, sys
from pathlib import Path

ROOT = Path('/tmp/opensip-design-corrections/post-reset-review.v19/copies/repro-v19')
DC = ROOT / 'docs/coop/design-corrections'
BEFORE = DC / 'reviews/codex-post-reset.v1/source-before-v19/docs/coop/design-corrections'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

W = load('wfm', DC / 'workflows/workflows_model.v1.py')
N = load('nem', DC / 'native/native_evidence_model.v2.py')

R = []
def ck(cid, desc, got, want):
    R.append({'id': cid, 'desc': desc, 'pass': got == want, 'observed': got, 'expected': want})

src_now = (DC / 'workflows/workflows_model.v1.py').read_text()
src_was = (BEFORE / 'workflows/workflows_model.v1.py').read_text()

# --- E1 the repair projection code is UNCHANGED by v19 ---------------------
def region(text, start, end):
    return text[text.index(start):text.index(end)]
seg_now = region(src_now, "    unmet = []", "    desc = {'schemaFamily': 'opensip.product.repair-plan'")
seg_was = region(src_was, "    unmet = []", "    desc = {'schemaFamily': 'opensip.product.repair-plan'")
ck('E1:unchanged', 'the repair preview emission body is byte-identical to pre-v19',
   seg_now == seg_was, True)
ck('E1:diff-is-subject-only', 'the ONLY v19 change to the workflow model is the subject copy',
   [l for l in src_now.splitlines() if l not in src_was.splitlines()],
   ["            # Preserve an explicitly supplied subject, including an empty string, which the",
    "            # published BoundedText schema admits. Native scope refusals carry field:count>limit.",
    "            # This projects trusted observations; schema validation still owns malformed values.",
    "            if 'subject' in obs:",
    "                t['domainDetail']['subject'] = obs['subject']"])

# --- E2 per-requirement emission is MANDATORY, and the code is EXISTING ----
ck('E2:mandatory', 'an unsatisfied requirement emits unconditionally (no flag, no option)',
   "if not req['satisfied']:\n            unmet.append({'code': 'REPAIR.EVIDENCE_RUN_UNAVAILABLE'," in seg_now, True)
ck('E2:two-routes', 'exactly two routes reach the ONE code inside preview',
   seg_now.count("'code': 'REPAIR.EVIDENCE_RUN_UNAVAILABLE'"), 2)
ck('E2:no-new-codes', 'no per-deficiency detail code is minted (code set unchanged vs pre-v19)',
   sorted({l.split("'code': '")[1].split("'")[0] for l in seg_now.splitlines() if "'code': '" in l}),
   sorted({l.split("'code': '")[1].split("'")[0] for l in seg_was.splitlines() if "'code': '" in l}))
# The two remedies differ, and only the per-requirement one carries cause fields.
retention = [l for l in seg_now.splitlines() if 'restore or regenerate the Run evidence' in l]
perreq = [l for l in seg_now.splitlines() if 'evidence requirement unsatisfied' in l]
ck('E2:retention-remedy-has-no-cause-fields',
   'the RETENTION remedy names Run-level restoration and no per-requirement cause',
   [len(retention) == 1,
    all(tok not in retention[0] for tok in ("req['relation']", "req['minResolution']", 'plane', 'deficiency'))],
   [True, True])
ck('E2:perreq-remedy-carries-cause-fields',
   'the PER-REQUIREMENT remedy names relation, minResolution, plane and deficiency',
   [len(perreq) == 1] + [tok in ' '.join(perreq + seg_now.splitlines()[
       seg_now.splitlines().index(perreq[0]):seg_now.splitlines().index(perreq[0]) + 3])
       for tok in ("req['relation']", "req['minResolution']", 'plane', 'deficiency')],
   [True, True, True, True, True])

# --- E3 the withdrawn CB7-SHOULD-1 premise: cause is NOT the code ----------
ck('E3:cause-carrier-is-separate',
   'deficiency is admitted separately from the detail code (cause != code)',
   "plane, deficiency = admit_evidence_requirement(req)" in seg_now, True)
# No deficiency value from the native sufficiency vocabulary is ever used as a detail CODE.
DEFICIENCIES = set(N.SCHEMAS['$defs']['CoverageDeficiencyV1']['enum']) if 'CoverageDeficiencyV1' in N.SCHEMAS['$defs'] else set(N.RUNG_CAUSE.values())
CODES_IN_SEG = {l.split(chr(39)+'code'+chr(39)+': '+chr(39))[1].split(chr(39))[0]
                for l in seg_now.splitlines() if chr(39)+'code'+chr(39)+': '+chr(39) in l}
ck('E3:deficiency-never-a-code',
   'no native deficiency value is minted as a public detail code',
   sorted(CODES_IN_SEG & DEFICIENCIES), [])
ck('E3:codes-are-repair-namespace',
   'every emitted code stays in the existing REPAIR namespace',
   sorted(c for c in CODES_IN_SEG if not c.startswith('REPAIR.')), [])

# --- E4 subject projection: preserved, additive, schema still owns malformed
base_obs = {'event': 'rejected', 'errorCode': 'REQUEST.UNSATISFIABLE',
            'detail': 'PROJECT.SCOPE_LIMIT', 'remedy': 'narrow the selection explicitly'}
ck('E4:absent-is-additive', 'no subject supplied -> byte-identical to the pre-v19 projection',
   W.terminate(dict(base_obs)),
   {'class': 'request-rejected', 'errorCode': 'REQUEST.UNSATISFIABLE',
    'domainDetail': {'code': 'PROJECT.SCOPE_LIMIT', 'remedy': 'narrow the selection explicitly'}})
ck('E4:present-preserved', 'an explicitly supplied subject is copied exactly',
   W.terminate(dict(base_obs, subject='importIds:257>256'))['domainDetail']['subject'],
   'importIds:257>256')
ck('E4:empty-preserved', 'an explicit EMPTY subject is preserved (presence, not truthiness)',
   W.terminate(dict(base_obs, subject=''))['domainDetail'].get('subject', '<<absent>>'), '')
ck('E4:falsey-preserved', 'other falsey supplied shapes are preserved, not dropped',
   [W.terminate(dict(base_obs, subject=v))['domainDetail'].get('subject', '<<absent>>')
    for v in (False, 0, [], {})], [False, 0, [], {}])
ck('E4:no-detail-no-subject', 'a detail-less observation still carries no domainDetail at all',
   'domainDetail' in W.terminate({'event': 'rejected', 'errorCode': 'REQUEST.UNSATISFIABLE'}), False)

# --- E5 the subject is COPIED, never ADMITTED: schema owns malformed values -
def schema_ok(term):
    try:
        W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/StepTermination', term)
        return True
    except Exception:
        return False
ck('E5:valid-passes', 'a well-formed subject validates', schema_ok(W.terminate(dict(base_obs, subject='importIds:257>256'))), True)
ck('E5:malformed-refused-by-schema', 'malformed supplied subjects are refused by the SCHEMA, not silently repaired',
   [schema_ok(W.terminate(dict(base_obs, subject=v))) for v in ('x' * 2000, False, 0, [], {})],
   [False, False, False, False, False])
ck('E5:empty-admitted', 'the empty string is admitted by BoundedText (so preserving it is lawful)',
   schema_ok(W.terminate(dict(base_obs, subject=''))), True)

# --- E6 end-to-end: the native bounded subject survives the workflow seam ---
try:
    N.admit_plan_selection_cardinality({'importIds': ['import2:%064x' % i for i in range(257)]})
    ck('E6:seam', 'expected refusal', 'none', 'ScopeRefusal')
except N.ScopeRefusal as e:
    t = N.scope_refusal_termination(e)
    obs = {'event': 'rejected', 'errorCode': t['errorCode'], 'detail': t['domainDetail']['code'],
           'subject': t['domainDetail']['subject'], 'remedy': t['domainDetail']['remedy']}
    ck('E6:seam', 'the exact promised count/limit subject survives into the workflow envelope',
       W.terminate(obs)['domainDetail']['subject'], 'importIds:257>256')
    ck('E6:seam-route', 'and the public route is unchanged across the seam',
       [W.terminate(obs)['class'], W.exit_code(W.terminate(obs))], ['request-rejected', 2])

# --- E7 the corrected 'generic exception' wording is factually true --------
import jsonschema
try:
    jsonschema.validate({'a': list(range(5))}, {'type': 'object',
                        'properties': {'a': {'type': 'array', 'maxItems': 3}}})
    ck('E7:structured', 'expected a maxItems error', 'none', 'ValidationError')
except jsonschema.ValidationError as e:
    ck('E7:structured-fields-exist',
       'a maxItems ValidationError DOES carry the failing path and the bound (so the retracted '
       '"names no field/count/limit" wording was rightly corrected)',
       [e.json_path, e.validator, e.validator_value], ['$.a', 'maxItems', 3])
    ck('E7:no-typed-projection',
       'but it carries none of the required typed projection fields',
       [hasattr(e, 'detail'), hasattr(e, 'd9'), hasattr(e, 'subject')], [False, False, False])

fails = [r for r in R if not r['pass']]
Path('/tmp/opensip-design-corrections/post-reset-review.v19/results/ctrl-e.json').write_text(
    json.dumps({'controls': len(R), 'failed': len(fails), 'failures': fails, 'results': R}, indent=1, default=str))
print('CTRL-E controls=%d failed=%d' % (len(R), len(fails)))
for f in fails:
    print('  FAIL', f['id'], f['desc'], '\n   observed=', repr(f['observed'])[:400],
          '\n   expected=', repr(f['expected'])[:400])
