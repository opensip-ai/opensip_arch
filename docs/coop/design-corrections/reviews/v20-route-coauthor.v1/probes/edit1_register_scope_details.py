"""EDIT 1 (item 1): register the two ALREADY-EMITTED scope-binding public details.

Behaviour-preserving by construction: `verify_scope_parameter_binding` is not touched, so both
refusals keep their exact error code, detail code, remedy string and reachability. What changes is
that the closed public vocabulary now CONTAINS the two names the function already publishes, so the
real carrier admits them instead of refusing them.

Mirrors are exact: `records` and `DomainDetailCode.enum` were byte-for-byte the same sorted code
list before this edit and remain so after it (check-integration.py enforces set equality).
"""
import json, sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REG = ROOT / 'public-detail-registry.v1.json'
COMMON = ROOT / 'workflows/schemas/common.schema.json'

NEW = ['BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER', 'BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH']
SELECTOR = 'workflows/schemas/common.schema.json#/$defs/DomainDetailCode'

STATEMENT = (
    "TWO EXISTING EMISSIONS WERE REGISTERED, and nothing new was invented. "
    "workflows_model.verify_scope_parameter_binding has always raised "
    "REQUEST.PRECONDITION_FAILED with BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER and with "
    "BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH, and neither name was a member of this registry, of "
    "the mirrored DomainDetailCode enum, or of internalAliases - so the REAL public carrier "
    "(workflows/schemas/common.schema.json#/$defs/StepTermination) REFUSED both terminations and "
    "the two refusals had no public route at all. They are registered here rather than renamed, "
    "because the emitting code, the owning normative prose (identity-and-evidence.md, `Where the "
    "binding is actually decided, and where it is only asserted`) and the existing controls all "
    "already use these exact names, and because the two conditions are DIFFERENT things for a "
    "caller to do next: NOT_A_SELECTED_PARAMETER says the analysis spec selects no ScopeDocumentV1 "
    "parameter at all - state one, or stop asking to be bound to a scope policy - while "
    "DIGEST_MISMATCH says exactly one IS selected and the supplied document is not it - supply the "
    "selected document. Collapsing them onto one existing code would delete that distinction and "
    "silently rename two published outputs. They are NOT internalAliases entries: an alias maps an "
    "internal decision key that may not appear as a public DomainDetailCode, and these two are "
    "emitted directly into the DomainDetail.code position by their own owner. The AMBIGUOUS "
    "selection introduced by the same correction keeps CONFIG.INVALID and is unchanged: it was "
    "already registered and no third BASELINE.SCOPE_* spelling is created. No D9 class, error code, "
    "exit code, faultCause, remedy string or reachability changes."
)


def main():
    reg = json.loads(REG.read_text())
    common = json.loads(COMMON.read_text())
    enum = common['$defs']['DomainDetailCode']['enum']
    codes = [r['code'] for r in reg['records']]

    assert codes == sorted(codes), 'records were not sorted before the edit'
    assert enum == codes, 'registry/enum mirror was not exact before the edit'
    for c in NEW:
        assert c not in codes, c + ' was already registered'

    reg['records'] = sorted(reg['records'] + [{'code': c, 'owner': 'workflows', 'selector': SELECTOR}
                                              for c in NEW],
                            key=lambda r: r['code'])
    # Recorded beside `newInThisCorrection` rather than inside it: that statement is the earlier
    # four-member account and stays exactly as written.
    assert 'scopeBindingDetailsRegistered' not in reg
    reg['scopeBindingDetailsRegistered'] = STATEMENT

    common['$defs']['DomainDetailCode']['enum'] = sorted(enum + NEW)

    after_codes = [r['code'] for r in reg['records']]
    assert after_codes == sorted(after_codes)
    assert after_codes == common['$defs']['DomainDetailCode']['enum'], 'mirror broke'
    assert len(after_codes) == 289, len(after_codes)

    REG.write_text(json.dumps(reg, indent=2) + '\n')
    COMMON.write_text(json.dumps(common, indent=2) + '\n')
    print(json.dumps({'registryRecords': len(after_codes), 'enumMembers': len(common['$defs']['DomainDetailCode']['enum']),
                      'added': NEW}, indent=1))


main()
