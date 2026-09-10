"""Scratch: measure the observed refusals for the CB-GAP-1/2 near-neighbour vectors."""
import hashlib
import importlib.util
import json
from pathlib import Path

B = Path('/tmp/opensip-design-corrections/v20-coauthor.v1/work/docs/coop/design-corrections')


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


M = load('m', B / 'foundation/identity-model.py')
W = load('w', B / 'workflows/workflows_model.v1.py')
N = load('n', B / 'native/native_evidence_model.v2.py')
C = M.C

POLICY = (B / 'workflows/schemas/policy-document.schema.json').read_bytes()
IMPORTCTX = (B / 'foundation/import-source-context.schema.json').read_bytes()
PD = hashlib.sha256(POLICY).hexdigest()
ID = hashlib.sha256(IMPORTCTX).hexdigest()
A = {'schemaFamily': 'opensip.product.scope', 'schemaMajor': 1, 'include': ['src/**'], 'exclude': []}
Bd = {'schemaFamily': 'opensip.product.scope', 'schemaMajor': 1, 'include': ['src/**'],
      'exclude': ['src/generated/**']}


def dg(v):
    return hashlib.sha256(C.canonical(v)).hexdigest()


def t(label, fn):
    try:
        print('%-46s ADMIT %s' % (label, str(fn())[:80]))
    except BaseException as e:                                          # noqa: BLE001
        print('%-46s REFUSE %s: %s' % (label, type(e).__name__, str(e)[:130]))


rows_two = [{'schemaDigest': PD, 'payloadDigest': dg(A)}, {'schemaDigest': PD, 'payloadDigest': dg(Bd)}]
rows_dup = [{'schemaDigest': PD, 'payloadDigest': dg(A)}, {'schemaDigest': PD, 'payloadDigest': dg(A)}]
rows_mixed = [{'schemaDigest': PD, 'payloadDigest': dg(A)}, {'schemaDigest': ID, 'payloadDigest': dg(A)}]
rows_import_two = [{'schemaDigest': ID, 'payloadDigest': dg(A)}, {'schemaDigest': ID, 'payloadDigest': dg(Bd)}]

t('helper two distinct scope rows', lambda: M.admit_parameter_selection(rows_two))
t('helper exact duplicate rows', lambda: M.admit_parameter_selection(rows_dup))
t('helper one of each row (legal)', lambda: M.admit_parameter_selection(rows_mixed))
t('helper two import-context rows', lambda: M.admit_parameter_selection(rows_import_two))
t('helper zero rows', lambda: M.admit_parameter_selection([]))
t('helper unregistered document row',
  lambda: M.admit_parameter_selection([{'schemaDigest': 'a' * 64, 'payloadDigest': 'b' * 64},
                                       {'schemaDigest': 'a' * 64, 'payloadDigest': 'c' * 64}]))


def spec(rows, caps=None):
    return {'schemaVersion': 2, 'policyPackIds': [],
            'requestedCapabilities': caps if caps is not None else [],
            'parameters': sorted(rows, key=C.canonical)}


t('native admit two distinct scope rows', lambda: N.admit_analysis_spec(spec(rows_two)) and 'ok')
t('native admit exact duplicate rows', lambda: N.admit_analysis_spec(spec(rows_dup)) and 'ok')
t('native admit one of each', lambda: N.admit_analysis_spec(spec(rows_mixed)) and 'ok')
t('native admit zero', lambda: N.admit_analysis_spec(spec([])) and 'ok')

t('verify binding two rows, doc A supplied', lambda: W.verify_scope_parameter_binding(spec(rows_two), A))
t('verify binding one row, doc A supplied',
  lambda: W.verify_scope_parameter_binding(spec([rows_two[0]]), A))
t('verify binding one row, doc B supplied',
  lambda: W.verify_scope_parameter_binding(spec([rows_two[0]]), Bd))
t('verify binding zero rows', lambda: W.verify_scope_parameter_binding(spec([]), A))

# ---- CB-GAP-2
DUP = [{'capabilityId': 'inventory', 'languageMode': 'ts-tsconfig', 'workspaceRoot': '.', 'required': False},
       {'capabilityId': 'inventory', 'languageMode': 'ts-tsconfig', 'workspaceRoot': '.', 'required': True}]
OKROOT = [DUP[0], dict(DUP[1], workspaceRoot='pkg/a')]
OKMODE = [DUP[0], dict(DUP[1], languageMode='ts-jsconfig')]
EXACT = [DUP[0], dict(DUP[0])]
UNREG = [dict(DUP[0], capabilityId='made-up'), DUP[1]]
t('caps duplicate tuple', lambda: N.admit_requested_capabilities(DUP) and 'ok')
t('caps different root', lambda: N.admit_requested_capabilities(OKROOT) and 'ok')
t('caps different mode', lambda: N.admit_requested_capabilities(OKMODE) and 'ok')
t('caps exact duplicate via helper', lambda: N.admit_requested_capabilities(EXACT) and 'ok')
t('caps unregistered + duplicate', lambda: N.admit_requested_capabilities(UNREG) and 'ok')
t('spec duplicate tuple', lambda: N.admit_analysis_spec(spec([], sorted(DUP, key=C.canonical))) and 'ok')
t('spec exact duplicate', lambda: N.admit_analysis_spec(spec([], EXACT)) and 'ok')
t('route lookup', lambda: N.public_termination_for(
    'native.requested-capability-duplicate-ownership-tuple:inventory:ts-tsconfig:.', 'external-configuration'))
t('route lookup host', lambda: N.public_termination_for(
    'native.requested-capability-duplicate-ownership-tuple:inventory:ts-tsconfig:.',
    'host-generated-internal-layer'))
t('route lookup no origin', lambda: N.public_termination_for(
    'native.requested-capability-duplicate-ownership-tuple:inventory:ts-tsconfig:.'))
t('envelope errors', lambda: N.failure_envelope_errors(
    'native.requested-capability-duplicate-ownership-tuple:inventory:ts-tsconfig:.', 'externally-supplied-spec'))
