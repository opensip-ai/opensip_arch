"""P1 (SCHEMA + CLOSURE probe). Reproduce V20-ROOT-3 independently in MY disposable copy.

Kind: schema-membership probe (registry/enum set membership) PLUS a closure probe that runs the
owning unit's own pinned-closure validator `validate_import_record` against the REAL public carrier
`workflows/schemas/common.schema.json#/$defs/StepTermination`.

It does NOT prove product qualification and does NOT run the invocation path; see p3 for the
invocation/composition probe.
"""
import importlib.util, json, re, sys
from pathlib import Path

ROOT = Path(sys.argv[1])                      # .../work/docs/coop/design-corrections
spec = importlib.util.spec_from_file_location('w', ROOT / 'workflows/workflows_model.v1.py')
W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)

registry = json.loads((ROOT / 'public-detail-registry.v1.json').read_text())
common = json.loads((ROOT / 'workflows/schemas/common.schema.json').read_text())
enum = set(common['$defs']['DomainDetailCode']['enum'])
d9 = set(common['$defs']['D9ErrorCode']['enum'])
src = (ROOT / 'workflows/workflows_model.v1.py').read_text()

emitted = sorted(set(re.findall(r"Refusal\([^,]+,\s*'([A-Za-z0-9_.\-]+)'", src)))
reg_codes = {r['code'] for r in registry['records']}
alias_keys = {a['internalCode'] for a in registry['internalAliases']}


def carrier(code, error_code='REQUEST.PRECONDITION_FAILED'):
    term = {'class': 'request-rejected', 'errorCode': error_code,
            'domainDetail': {'code': code, 'remedy': 'x'}}
    try:
        W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/StepTermination', term)
        return 'ADMITS'
    except W.Refusal:
        return 'REFUSES'


rows = [{'code': c, 'inClosedSchemaEnum': c in enum, 'inPublicDetailRegistry': c in reg_codes,
         'inInternalAliases': c in alias_keys, 'realPublicCarrier': carrier(c)}
        for c in emitted if c not in enum]

# The two named codes, checked by name whether or not the regex found them.
named = {}
for c in ('BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER', 'BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH'):
    named[c] = {'emittedInSource': ("'" + c + "'") in src, 'inClosedSchemaEnum': c in enum,
                'inPublicDetailRegistry': c in reg_codes, 'inInternalAliases': c in alias_keys,
                'realPublicCarrier': carrier(c)}

# Live-validator control: a registered detail on the same shape must ADMIT, else the probe is vacuous.
control = {'CONFIG.INVALID(registered)': carrier('CONFIG.INVALID'),
           'BASELINE.SOURCE_EPHEMERAL(registered)': carrier('BASELINE.SOURCE_EPHEMERAL'),
           'ZZZ.NEVER_REGISTERED': carrier('ZZZ.NEVER_REGISTERED')}

# Registry/enum parity as check-integration.py enforces it.
parity = reg_codes == enum

print(json.dumps({'kind': 'schema-membership + carrier-closure probe',
                  'detailCodesEmitted': len(emitted), 'registryEnumParity': parity,
                  'registryRecords': len(reg_codes), 'enumMembers': len(enum),
                  'unregisteredEmitted': rows, 'namedByHand': named,
                  'liveValidatorControl': control,
                  'errorCodeRegistered': {'REQUEST.PRECONDITION_FAILED': 'REQUEST.PRECONDITION_FAILED' in d9}},
                 indent=1))
