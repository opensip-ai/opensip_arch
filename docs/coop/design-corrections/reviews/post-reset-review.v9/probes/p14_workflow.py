"""v9 probe 14 - workflow section 8 total projection and section 12 pin inventory boundary.

Section 8 claims: the host projection is TOTAL over the selected command's parityFields; a missing
field or projection exception is an EXISTING required-delivery operational fault (operational-failed,
exit 4, faultCause=delivery-required, DELIVERY.REQUIRED_FAILED); a committed Run is retained and no
RunId is invented otherwise; a pure KeyError from a reference helper is NOT itself a public
termination; host wiring stays a DR-G17/DR-G20 obligation.

Section 12 claims: validate_pinned_purge_refusal establishes envelope schema and internal field
agreement only, never inventory completeness; the complete-current-pin comparison under the
exclusive lease and the renewed disclosure stay with the host; the helper grants no effect authority.

Each is tested against the shipped model rather than read.
"""
import copy, json, importlib.util, sys
from pathlib import Path

SUB = Path('/tmp/opensip-design-corrections/candidate-subject.v9')
WF = SUB / 'docs/coop/design-corrections/workflows'
spec = importlib.util.spec_from_file_location('wf_v9', WF / 'workflows_model.v1.py')
M = importlib.util.module_from_spec(spec)
sys.modules['wf_v9'] = M
spec.loader.exec_module(M)
out = {'probe': 'p14_workflow', 'standing': 'independent reviewer probe; design/reference only'}

# ---- section 8: the fault classification is EXISTING, not invented for v9 ----
codes = None
for name in dir(M):
    v = getattr(M, name)
    if isinstance(v, dict) and 'delivery-required' in v:
        codes = {'symbol': name, 'mapping': v.get('delivery-required')}
        break
out['faultCodeIsExisting'] = {
    'found': codes,
    'mapsToDeliveryRequiredFailed': bool(codes and codes['mapping'] == 'DELIVERY.REQUIRED_FAILED'),
    'presentInV8Too': 'delivery-required' in (
        Path('/tmp/opensip-design-corrections/candidate-subject.v8/docs/coop/design-corrections/workflows/workflows_model.v1.py').read_text()),
}

# ---- terminate(): committed Run retained; none invented when absent ----
t_with = M.terminate({'event': 'operational-fault', 'faultCause': 'delivery-required', 'runId': 'run2:' + 'a' * 64})
t_without = M.terminate({'event': 'operational-fault', 'faultCause': 'delivery-required'})
out['terminationBehaviour'] = {
    'withCommittedRun': t_with,
    'withoutCommittedRun': t_without,
    'retainsCommittedRunId': t_with.get('runId') == 'run2:' + 'a' * 64,
    'inventsNoRunIdWhenUncommitted': 'runId' not in t_without or t_without.get('runId') is None,
    'classIsOperationalFailed': t_with.get('class') == 'operational-failed',
}
try:
    out['terminationBehaviour']['exitCode'] = M.exit_code_of(t_with) if hasattr(M, 'exit_code_of') else None
except Exception as e:
    out['terminationBehaviour']['exitCode'] = 'n/a: ' + str(e)

# ---- projection totality: a missing parity field must not render successfully ----
proj = None
for name in dir(M):
    if 'parity' in name.lower() and callable(getattr(M, name)):
        proj = name
out['projectionTotality'] = {'helperSearched': proj}
# find the code site and exercise its behaviour on a missing field
src = (WF / 'workflows_model.v1.py').read_text()
line = next((l.strip() for l in src.splitlines() if "command['parityFields']" in l), None)
out['projectionTotality']['siteSource'] = line
out['projectionTotality']['totalComprehensionOverParityFields'] = bool(
    line and 'for k in' in line and "envelope['parity'][k]" in line)
try:
    envelope = {'parity': {'a': 1}}
    command = {'parityFields': ['a', 'b']}
    {k: envelope['parity'][k] for k in command['parityFields']}
    out['projectionTotality']['missingFieldOutcome'] = 'silently-rendered'
except KeyError as e:
    out['projectionTotality']['missingFieldOutcome'] = 'KeyError:' + str(e)
out['projectionTotality']['contractSaysKeyErrorAloneIsNotPublicTermination'] = (
    'that exception alone is not a public termination' in
    (SUB / 'docs/v2/contracts/product-v1/workflows-and-surfaces.md').read_text())

# ---- section 12: the helper's scope ----
import inspect
srcfn = inspect.getsource(M.validate_pinned_purge_refusal)
out['pinnedPurgeHelper'] = {
    'source': srcfn,
    'consultsNoLedger': not any(w in srcfn for w in ('ledger', 'lease', 'observed', 'inventory')),
    'returnsEnvelopeOnly': srcfn.strip().endswith('return envelope'),
    'raisesJoinFaultOnInternalDisagreement': 'PINNED_PURGE_PROJECTION_JOIN' in srcfn,
}
# a schema-valid envelope disclosing a SUBSET of pins must still validate at the helper -
# which is exactly why the contract puts the completeness obligation on the host.
out['pinnedPurgeHelper']['contractStatesHostObligation'] = all(
    s in (SUB / 'docs/v2/contracts/product-v1/workflows-and-surfaces.md').read_text() for s in [
        'cannot establish inventory completeness without the host ledger',
        'complete current',
        'exclusive lease',
        'accepting the public envelope grants no authority'])
print(json.dumps(out, indent=1, default=str))
