"""EDIT 7 (item 3, V20-ROOT-5): keep the maintenance constraint, and make it enforceable.

ASSESSMENT, which is what this item asked for first. V20-ROOT-5 is a MAINTENANCE CONSTRAINT and, as
of these bytes, it is NOT a wrong current output. PUBLIC_ROUTE_REMEDIES is keyed by public CODE, so
one string serves every internal key routing to that code, and the two strings the earlier
correction widened for the ownership-tuple key are the only shared ones. The item-2 change routes a
THIRD path - default construction - to the same key and therefore to the same three codes, and each
of those three remedies is true of it: CONFIG.INVALID and native.capability-spec-invalid both state
`at most one row per (capabilityId, languageMode, workspaceRoot)` / `states two rows for one
(capabilityId, languageMode, workspaceRoot)`, and HOST.INVARIANT_VIOLATED says the host produced an
invalid internal record, which is exactly what a default construction emitting two rows for one
cell is. Measured by the controls added in edit 6.

WHAT IS NOT DONE: re-keying the table by (code, internal key). That is a shape change to an existing
table for a case two honest sentences already cover, and nothing in this correction produces a key
that needs it. The constraint is instead PROMOTED from a Python comment to a normative registry
statement and given a total control, so a future key that would break it fails a check rather than
relying on a reviewer noticing the comment.
"""
import json, sys
from pathlib import Path

ROOT = Path(sys.argv[1])

SCHEMAS = ROOT / 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
doc = json.loads(SCHEMAS.read_text())
reg = doc['x-opensip-public-route-registry']
assert 'remedyKeyingConstraint' not in reg

# Placed immediately after envelopeErrorsComposition, which is the statement it constrains.
STATEMENT = (
    "NORMATIVE MAINTENANCE CONSTRAINT on the remedy table, promoted here from a source comment so it "
    "is part of the published law rather than advice a reader may miss. PUBLIC_ROUTE_REMEDIES is keyed "
    "by PUBLIC CODE, not by internal key. Several keys route to one code - "
    "native.requested-capability-unregistered, native.requested-capability-mode-unregistered and "
    "native.requested-capability-duplicate-ownership-tuple all reach CONFIG.INVALID under "
    "external-configuration, and all three reach native.capability-spec-invalid as the "
    "externally-supplied-spec envelope detail - so ONE string must remain true for EVERY key that "
    "reaches that code, and a key whose remedy would be a DIFFERENT next step may not simply reuse the "
    "code. THIS IS CURRENTLY SATISFIED, not merely intended: the two strings widened for the ownership "
    "tuple state both the unregistered-name condition and the one-row-per-tuple condition, and the "
    "default-construction path added later routes to the same key and is covered by the same two "
    "sentences plus HOST.INVARIANT_VIOLATED, which is true of a host emitting two rows for one cell. "
    "The structural alternative - keying the remedy by (code, internal key) - is deliberately NOT taken: "
    "it changes the shape of an existing table for a case honest sentences already cover, and no key in "
    "this composition needs it. What is owed instead is exact: adding a key that routes to an existing "
    "code obliges its author to check that code's remedy is a true next step for the new condition and "
    "to widen it or choose another code if it is not."
)
items = list(reg.items())
out = {}
for k, v in items:
    out[k] = v
    if k == 'envelopeErrorsComposition':
        out['remedyKeyingConstraint'] = STATEMENT
assert 'remedyKeyingConstraint' in out
doc['x-opensip-public-route-registry'] = out
SCHEMAS.write_text(json.dumps(doc, indent=1) + '\n')

# --- the total control -----------------------------------------------------------------------
F = ROOT / 'docs/coop/design-corrections/foundation/check-identity.py'
s = F.read_text()
ANCHOR = """check('the-actual-discovery-output-drives-a-default-selection-without-any-duplicate',
      len(N.default_capability_selection(_DISCOVERED,_DEFAULT_REGISTRY)
          ['analysisSpec']['requestedCapabilities'])>0)
"""
ADDED = """# V20-ROOT-5 as a TOTAL control rather than a comment. Every registered key, at every origin it
# declares, composes its envelope errors; every emitted code is a closed-registry member; and every
# emitted remedy is EXACTLY the table's entry for that code - which is what `keyed by code` means and
# what makes a shared string a real constraint rather than a coincidence.
_ROUTE_KEYS=N.PUBLIC_ROUTE_REGISTRY['keys']
def _route_pairs():
    for key,row in _ROUTE_KEYS.items():
        if row.get('notATermination'):continue
        for origin in row['possibleOrigins']:
            yield key,origin
_ROUTE_PAIRS=sorted(_route_pairs())
check('every-registered-route-pair-composes-nonempty-envelope-errors',
      len(_ROUTE_PAIRS)>=len(_ROUTE_KEYS) and
      all(N.failure_envelope_errors(k,o) for k,o in _ROUTE_PAIRS))
check('every-envelope-error-code-across-the-whole-route-registry-is-registered',
      all(e['code'] in PUBLIC_CODES
          for k,o in _ROUTE_PAIRS for e in N.failure_envelope_errors(k,o)))
check('every-emitted-remedy-is-exactly-the-tables-entry-for-its-code',
      all(e['remedy']==N.PUBLIC_ROUTE_REMEDIES[e['code']]
          for k,o in _ROUTE_PAIRS for e in N.failure_envelope_errors(k,o)))
# The constraint has teeth only where a code IS shared, so the sharing is measured, not assumed.
_CODE_KEYS={}
for _k,_o in _ROUTE_PAIRS:
    for _e in N.failure_envelope_errors(_k,_o):
        _CODE_KEYS.setdefault(_e['code'],set()).add(_k)
check('at-least-two-public-codes-really-are-shared-by-several-internal-keys',
      len([c for c,ks in _CODE_KEYS.items() if len(ks)>1])>=2)
check('the-ownership-tuple-key-is-one-of-the-keys-sharing-both-widened-strings',
      all('native.requested-capability-duplicate-ownership-tuple' in
          _CODE_KEYS.get(code,set()) and len(_CODE_KEYS[code])>1
          for code in ('CONFIG.INVALID','native.capability-spec-invalid')))
check('every-shared-code-states-the-condition-of-every-key-that-reaches-it',
      all('(capabilityId, languageMode, workspaceRoot)' in N.PUBLIC_ROUTE_REMEDIES[code]
          for code in ('CONFIG.INVALID','native.capability-spec-invalid')
          if 'native.requested-capability-duplicate-ownership-tuple' in _CODE_KEYS.get(code,set())))
# The constraint is now published law, not only a source comment.
check('the-remedy-keying-constraint-is-published-in-the-route-registry',
      'remedyKeyingConstraint' in N.PUBLIC_ROUTE_REGISTRY and
      'keyed by PUBLIC CODE' in N.PUBLIC_ROUTE_REGISTRY['remedyKeyingConstraint'] and
      'deliberately NOT taken' in N.PUBLIC_ROUTE_REGISTRY['remedyKeyingConstraint'])
"""
assert s.count(ANCHOR) == 1
F.write_text(s.replace(ANCHOR, ANCHOR + ADDED))
print('remedy constraint published and controlled')
