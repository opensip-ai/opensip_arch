"""Bounded independent probe of the v20 final ROOT DELTA (4 changed files).

Scope, stated exactly: this does NOT re-run the six suites. It execs the final
check-identity.py once (three of the five delta changes live in it) inside a PRIVATE
COPY of the final work tree, then interrogates the resulting namespace for:
  P2 selected-scope positive helper truth + detail-projection lossiness
  P3 coverageView schemaDigest arithmetic vs registered_schema_documents()
  P4 non-vacuity (mutation) of the new fragment membership guard
  P5 reachable refusals on the default capability-selection path
Nothing under v20-final-source.v1 is written or imported from.
"""
import json, sys, hashlib
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path('/private/tmp/opensip-design-corrections/v20-final-delta-peer.v1/work/finaltree')
DC = ROOT / 'docs/coop/design-corrections'
CHECK = DC / 'foundation/check-identity.py'

FINAL_SCHEMA_SHA = 'f20b8353a7be50d7a0c24f413df74e35d23a4e9fc2a4ecc661235655c43c51be'
STALE_SCHEMA_SHA = 'b1fff36d7c09afaecdf2e043ddcb8c88791b13a7bbb58822651e2654f34dc5c8'

out = {}

# ---------------------------------------------------------------- P1: exec the suite once
ns = {'__file__': str(CHECK), '__name__': '__probe__'}
sys.argv = ['check-identity.py']
try:
    exec(compile(CHECK.read_text(), str(CHECK), 'exec'), ns)
    exit_code = 0
except SystemExit as e:
    exit_code = e.code
out['P1_suite'] = {'sysexit': exit_code,
                   'passed': ns['report']['passed'], 'failed': ns['report']['failed'],
                   'failing_ids': [x['id'] for x in ns['results'] if not x['passed']]}

W, M, NF = ns['W'], ns['M'], ns['NATIVE_FIXTURES']

# --------------------------------------- P2: is the strengthened positive true, and true WHY?
raised = None
try:
    art = ns['_adopt']([ns['_SCOPE_ROW_A']], ns['SCOPE_DOCUMENT'])
    returned = type(art).__name__
except BaseException as e:                      # noqa: BLE001 - probe wants everything
    raised, returned = f'{type(e).__name__}:{e}', None
out['P2_positive'] = {
    'raised_anything': raised,
    'returned_type': returned,
    'helper_result_is_None': ns['_adopt_scope_detail']([ns['_SCOPE_ROW_A']], ns['SCOPE_DOCUMENT']) is None,
}

# The lossiness of projecting a Refusal to `.detail`: adopt_baseline itself owns a detail-less
# Refusal (workflows_model.v1.py:744). Reach it with the SAME caller, duplicate entries only.
dup = [{'fingerprint': 'fp1'}, {'fingerprint': 'fp1'}]
try:
    W.adopt_baseline(ns['_ADOPT_RUN'], 'plan2:x', 'proj', {'schemaVersion': 1, 'rules': []},
                     ns['SCOPE_DOCUMENT'], {'schemaVersion': 1, 'waivers': []}, [], dup, [], [], {},
                     '0.0.0', analysis_spec=ns['_spec']([ns['_SCOPE_ROW_A']]))
    out['P2_lossy'] = {'refused': False}
except W.Refusal as exc:
    out['P2_lossy'] = {'refused': True, 'error_code': exc.error_code, 'detail': exc.detail,
                       'detail_is_None': exc.detail is None,
                       'would_satisfy_new_predicate': exc.detail is None}

# ------------------------------------------------- P3: coverageView digest arithmetic
regs = M.registered_schema_documents()
declared = NF['coverageView']['schemaDigests']
on_disk = hashlib.sha256((DC / 'native/native-evidence.schemas.v2.json').read_bytes()).hexdigest()
out['P3_arithmetic'] = {
    'declared_schemaDigests': declared,
    'final_schema_file_sha256': on_disk,
    'declared_equals_final_bytes': declared == [on_disk] == [FINAL_SCHEMA_SHA],
    'final_in_registered_documents': FINAL_SCHEMA_SHA in regs,
    'stale_b1fff_in_registered_documents': STALE_SCHEMA_SHA in regs,
    'registered_document_count': len(regs),
}

# ------------------------------- P4: non-vacuity of the new membership guard (in-memory mutation)
def guard(digests):
    return bool(digests) and set(digests) <= M.registered_schema_documents()

out['P4_mutation'] = {
    'as_shipped_passes': guard(declared),
    'stale_digest_fails': not guard([STALE_SCHEMA_SHA]),
    'empty_fails': not guard([]),
    'unregistered_junk_fails': not guard(['0' * 64]),
    'mixed_valid_plus_junk_fails': not guard(declared + ['0' * 64]),
}

# ------------------- P5: which refusals can the DEFAULT capability-selection path actually reach?
N = ns['N']
import inspect, ast
src = inspect.getsource(N.default_capability_selection)
tree = ast.parse(src.lstrip() if src.startswith(' ') else src)
raises = []
for node in ast.walk(tree):
    if isinstance(node, ast.Raise) and node.exc is not None:
        raises.append(ast.dump(node.exc, annotate_fields=False)[:120])
out['P5_default_path'] = {
    'direct_raise_sites_in_default_capability_selection': len(raises),
    'raise_exprs': raises,
    'calls_admit_analysis_spec': 'admit_analysis_spec' in src,
}

print(json.dumps(out, indent=2, default=str))
