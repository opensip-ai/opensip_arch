# Control C12 - validate every recovery projection and every post-publication outcome against the
# ACTUAL frozen StepTermination schema, using only existing vocabulary members.
#
# Settles root item 4 (omitted domainDetail) and item 8 (policy-failed / indeterminate survive
# publication) by execution rather than by assertion.
#
# usage: python c12-d9-projection.py <source25Root> <reportPath>
import json
import os
import sys

import jsonschema

SRC, OUT = sys.argv[1], sys.argv[2]
BASE = os.path.join(SRC, 'docs/coop/design-corrections/workflows/schemas')
# The SELECTED successor set is evaluator3/, whose RunId is run3. The sibling
# common.schema.json is the retained predecessor and still carries run2; that split is the same
# retained-selector versus product-successor pattern identity section 2 states for ExecutionId,
# and it is asserted below rather than assumed.
COMMON = os.path.join(BASE, 'evaluator3', 'common.schema.json')
RETAINED = os.path.join(BASE, 'common.schema.json')
doc = json.load(open(COMMON, encoding='utf-8'))
defs = doc['$defs']
retained_defs = json.load(open(RETAINED, encoding='utf-8'))['$defs']

RUN = 'run3:' + '0' * 64
EXEC = 'exec1_' + '1' * 32

# Validate against the real frozen $defs. The document is reused verbatim; only a top-level
# $ref is added so the local JSON pointers resolve inside one self-contained schema.
SCHEMA = dict(doc)
SCHEMA.pop('$ref', None)
SCHEMA['$ref'] = '#/$defs/StepTermination'
jsonschema.Draft202012Validator.check_schema(SCHEMA)
VALIDATOR = jsonschema.Draft202012Validator(SCHEMA)


def errs(inst):
    return [e.message for e in VALIDATOR.iter_errors(inst)]


checks = []


def ck(name, ok, detail=''):
    checks.append({'check': name, 'pass': bool(ok), 'detail': str(detail)[:300]})
    return ok


# ---- 0. the frozen facts the projection table relies on -----------------------
st = defs['StepTermination']
ck('StepTermination requires only class', st['required'] == ['class'], st['required'])
ck('domainDetail is an optional member of StepTermination',
   'domainDetail' in st['properties'] and 'domainDetail' not in st['required'])
ck('DomainDetail itself requires code and remedy when present',
   defs['DomainDetail']['required'] == ['code', 'remedy'])
ck('ledger-corrupt, ledger-busy, host-io and durability-commit are existing faultCause members',
   {'ledger-corrupt', 'ledger-busy', 'host-io', 'durability-commit'}
   <= set(defs['D9FaultCause']['enum']))
ck('LEDGER.CORRUPT, LEDGER.BUSY_TIMEOUT, HOST.IO_FAILURE, DURABILITY.COMMIT_FAILED and '
   'DELIVERY.REQUIRED_FAILED are existing errorCode members',
   {'LEDGER.CORRUPT', 'LEDGER.BUSY_TIMEOUT', 'HOST.IO_FAILURE', 'DURABILITY.COMMIT_FAILED',
    'DELIVERY.REQUIRED_FAILED'} <= set(defs['D9ErrorCode']['enum']))
DETAILS = set(defs['DomainDetailCode']['enum'])
ck('PROJECT.BUSY, RECOVERY.REFUSED and the evidence family are existing DomainDetailCode members',
   {'PROJECT.BUSY', 'RECOVERY.REFUSED', 'evidence.missing', 'evidence.corrupt',
    'evidence.purged', 'evidence.expired'} <= DETAILS)
ck('MIGRATION.CORRUPT exists but is the store-transition detail, not reused here',
   'MIGRATION.CORRUPT' in DETAILS)

# The owner is EXPLICITLY selected by two supplied source25 selectors, not inferred from the
# RunId pattern. Both are asserted verbatim so the choice cannot be mistaken for an inference.
wf = open(os.path.join(SRC, 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'),
          encoding='utf-8').read()
proj = open(os.path.join(SRC, 'docs/coop/design-corrections/workflows/'
                              'workflow-projection-contract.v3.md'), encoding='utf-8').read()
SEL1 = 'Its closed schemas live under `workflows/schemas/evaluator3/`'
SEL2 = 'The current output schemas are under `schemas/evaluator3/`.'
SEL3 = ('Historical output schemas remain retained evidence and are not an alternative\n'
        'parser for this profile.')
ck('workflows-and-surfaces explicitly selects workflows/schemas/evaluator3/',
   SEL1 in wf, SEL1)
ck('the incorporated workflow projection contract explicitly selects schemas/evaluator3/',
   SEL2 in proj, SEL2)
ck('the same paragraph states historical output schemas are NOT an alternative parser',
   SEL3 in wf)
ck('the SELECTED evaluator3 RunId is the current run3 grammar',
   defs['RunId']['pattern'] == '^run3:[0-9a-f]{64}(?![\\s\\S])', defs['RunId'])
ck('the retained sibling carries run2 and is retained evidence, not an unresolved conflict',
   retained_defs['RunId']['pattern'] == '^run2:[0-9a-f]{64}(?![\\s\\S])',
   retained_defs['RunId'])
ck('both documents agree that StepTermination requires only class',
   retained_defs['StepTermination']['required'] == ['class'] == st['required'])
ck('both documents agree domainDetail is optional',
   'domainDetail' not in retained_defs['StepTermination']['required']
   and 'domainDetail' not in st['required'])

# ---- 1. the recovery projections ---------------------------------------------
PROJECTIONS = {
    'committed-historically': {'class': 'success', 'runId': RUN},
    'terminal-not-committed': {'class': 'success', 'executionId': EXEC},
    'unknown-attempt-open': {
        'class': 'operational-failed', 'errorCode': 'LEDGER.BUSY_TIMEOUT',
        'faultCause': 'ledger-busy', 'executionId': EXEC,
        'domainDetail': {'code': 'PROJECT.BUSY', 'remedy': 'retry outside the fence with backoff'}},
    'durability-undetermined caller response (not a custody outcome)': {
        'class': 'operational-failed', 'errorCode': 'DURABILITY.COMMIT_FAILED',
        'faultCause': 'durability-commit', 'executionId': EXEC},
    'unknown-attempt-unobserved': {
        'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE',
        'faultCause': 'host-io', 'executionId': EXEC},
    'unknown-custody': {
        'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE',
        'faultCause': 'host-io', 'executionId': EXEC},
    'unknown-quarantine-condition': {
        'class': 'operational-failed', 'errorCode': 'LEDGER.CORRUPT',
        'faultCause': 'ledger-corrupt', 'executionId': EXEC},
    'unavailable-busy': {
        'class': 'operational-failed', 'errorCode': 'LEDGER.BUSY_TIMEOUT',
        'faultCause': 'ledger-busy', 'executionId': EXEC,
        'domainDetail': {'code': 'PROJECT.BUSY', 'remedy': 'retry outside the fence with backoff'}},
    'binding-unusable': {
        'class': 'request-rejected', 'errorCode': 'EXTENSION.ADMISSION_REJECTED',
        'executionId': EXEC,
        'domainDetail': {'code': 'RECOVERY.REFUSED', 'remedy': 'name the correct store binding',
                         'subject': 'STORE_BINDING_MISMATCH'}},
    'committed-availability-degraded': {
        'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'host-io',
        'runId': RUN,
        'domainDetail': {'code': 'evidence.purged', 'remedy': 'regenerate or restore the evidence',
                         'subject': 'blob:aaaa'}},
}
proj = {}
for name, inst in PROJECTIONS.items():
    e = errs(inst)
    proj[name] = {'instance': inst, 'schemaValid': not e, 'errors': e}
    ck('recovery projection is schema-valid: ' + name, not e, e)
ck('the quarantine projection carries NO domainDetail',
   'domainDetail' not in PROJECTIONS['unknown-quarantine-condition'])
ck('the quarantine projection does not reuse MIGRATION.CORRUPT',
   'MIGRATION.CORRUPT' not in json.dumps(PROJECTIONS))

# ---- 2. negative controls on the projections ---------------------------------
NEG = {
    'operational-failed without errorCode is refused': {
        'class': 'operational-failed', 'faultCause': 'ledger-corrupt'},
    'operational-failed with faultCause none is refused': {
        'class': 'operational-failed', 'errorCode': 'LEDGER.CORRUPT', 'faultCause': 'none'},
    'success carrying an errorCode is refused': {
        'class': 'success', 'errorCode': 'LEDGER.CORRUPT'},
    'an unregistered domainDetail code is refused': {
        'class': 'operational-failed', 'errorCode': 'LEDGER.CORRUPT',
        'faultCause': 'ledger-corrupt',
        'domainDetail': {'code': 'CARRIER.QUARANTINED', 'remedy': 'x'}},
    'an unregistered errorCode is refused': {
        'class': 'operational-failed', 'errorCode': 'RECOVERY.CARRIER_SKEW',
        'faultCause': 'ledger-corrupt'},
    'a domainDetail without remedy is refused': {
        'class': 'operational-failed', 'errorCode': 'LEDGER.BUSY_TIMEOUT',
        'faultCause': 'ledger-busy', 'domainDetail': {'code': 'PROJECT.BUSY'}},
    'indeterminate without reasonCodes is refused': {'class': 'indeterminate'},
    'policy-failed without runId or ephemeral authority is refused': {'class': 'policy-failed'},
}
neg = {}
for name, inst in NEG.items():
    e = errs(inst)
    neg[name] = {'instance': inst, 'refused': bool(e), 'errors': e[:2]}
    ck('negative control: ' + name, bool(e), 'ACCEPTED but should be refused' if not e else '')

# ---- 3. post-publication outcomes survive (root item 8) ----------------------
POST = {
    'policy-failed survives publication carrying the committed runId': {
        'class': 'policy-failed', 'runId': RUN, 'executionId': EXEC},
    'indeterminate survives publication carrying reasonCodes': {
        'class': 'indeterminate', 'runId': RUN, 'executionId': EXEC,
        'reasonCodes': ['VERDICT.INDETERMINATE']},
    'indeterminate survives with a coverage reason code': {
        'class': 'indeterminate', 'runId': RUN,
        'reasonCodes': ['COVERAGE.REQUIRED_RELATION_MISSING']},
    'required delivery failure after commit preserves the runId': {
        'class': 'operational-failed', 'errorCode': 'DELIVERY.REQUIRED_FAILED',
        'faultCause': 'delivery-required', 'runId': RUN, 'executionId': EXEC},
    'ordinary success after publication': {'class': 'success', 'runId': RUN},
    'policy-failed for an explicitly ephemeral analysis with no Run': {
        'class': 'policy-failed', 'authority': 'ephemeral'},
}
post = {}
for name, inst in POST.items():
    e = errs(inst)
    post[name] = {'instance': inst, 'schemaValid': not e, 'errors': e}
    ck('post-publication outcome is schema-valid: ' + name, not e, e)

# an optional surface failure must not be representable as a reset of the class: the same
# policy-failed / indeterminate instances remain valid and unchanged, and success carrying
# reasonCodes or an errorCode is refused, so no lawful rewrite to success exists.
reset_attempts = {
    'optional failure rewriting indeterminate to success keeps the reasonCodes': {
        'class': 'success', 'runId': RUN, 'reasonCodes': ['VERDICT.INDETERMINATE']},
    'optional failure rewriting policy-failed to success keeps an errorCode': {
        'class': 'success', 'runId': RUN, 'errorCode': 'DELIVERY.REQUIRED_FAILED'},
}
for name, inst in reset_attempts.items():
    e = errs(inst)
    ck('no lawful reset: ' + name, bool(e), 'ACCEPTED but should be refused' if not e else '')

rep = {'control': 'c12-d9-projection',
       'commonSchema': 'docs/coop/design-corrections/workflows/schemas/common.schema.json',
       'stepTerminationRequired': st['required'],
       'domainDetailOptional': 'domainDetail' not in st['required'],
       'recoveryProjections': proj,
       'projectionNegativeControls': neg,
       'postPublicationOutcomes': post,
       'passed': sum(1 for c in checks if c['pass']),
       'failed': sum(1 for c in checks if not c['pass']),
       'checks': checks}
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(rep, indent=1) + '\n')
print('WROTE', OUT)
print('passed %d failed %d' % (rep['passed'], rep['failed']))
for c in checks:
    if not c['pass']:
        print('  FAIL', c['check'], '::', c['detail'])
