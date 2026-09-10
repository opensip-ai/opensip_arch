"""EDIT 6 (item 2): update the two existing controls and add the composed public-route controls.

The two existing `rejects_because` controls asserted the bespoke key by name; they are the direct
consumers of the change and are updated to assert the registered key WITH its tuple subject, which
is strictly more specific than what they asserted before.

The added controls do not stop at the key string: they take the ACTUAL AdmissionError that
`default_capability_selection` raises, run it through `normalize_internal_key`,
`public_termination_for` and `failure_envelope_errors` for every possible origin, and validate the
composed terminations and failure envelopes against the real workflows carrier schemas.
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
F = ROOT / 'foundation/check-identity.py'
s = F.read_text()
applied = []


def sub(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, 'expected %d, found %d for %r' % (count, n, old[:100])
    s = s.replace(old, new)
    applied.append(n)


# --- the two existing consumers of the key ---------------------------------------------------
sub("""rejects_because('default-selection-refuses-a-duplicate-request-rather-than-deduping',
    lambda:N.default_capability_selection(_units+_units,[dict(r) for r in GOOD_REGISTRY]),
    'DUPLICATE_REQUESTED_CAPABILITY')""",
    """rejects_because('default-selection-refuses-a-duplicate-request-rather-than-deduping',
    lambda:N.default_capability_selection(_units+_units,[dict(r) for r in GOOD_REGISTRY]),
    'native.requested-capability-duplicate-ownership-tuple:')""")

sub("""rejects_because('two-co-located-units-in-one-mode-refuse-rather-than-silently-dedupe',
    lambda:N.default_capability_selection(
        [{'rootPath':'.','languageMode':'ts-tsconfig','languageFamily':'typescript'},
         {'rootPath':'.','languageMode':'ts-tsconfig','languageFamily':'typescript'}],_DEFAULT_REGISTRY),
    'DUPLICATE_REQUESTED_CAPABILITY')""",
    """rejects_because('two-co-located-units-in-one-mode-refuse-rather-than-silently-dedupe',
    lambda:N.default_capability_selection(
        [{'rootPath':'.','languageMode':'ts-tsconfig','languageFamily':'typescript'},
         {'rootPath':'.','languageMode':'ts-tsconfig','languageFamily':'typescript'}],_DEFAULT_REGISTRY),
    'native.requested-capability-duplicate-ownership-tuple:')
# V20-ROOT-4. That refusal is now PUBLICLY ROUTABLE, which it was not: the guard used to raise a
# bespoke DUPLICATE_REQUESTED_CAPABILITY with no row in x-opensip-public-route-registry, so
# public_termination_for and failure_envelope_errors both refused it and the one refusal the default
# path can reach had no derivable public termination at all. These controls take the ACTUAL error
# the ACTUAL call raises and carry it all the way to the real schemas.
def _default_dupe_key():
    try:N.default_capability_selection(
        [{'rootPath':'.','languageMode':'ts-tsconfig','languageFamily':'typescript'},
         {'rootPath':'.','languageMode':'ts-tsconfig','languageFamily':'typescript'}],_DEFAULT_REGISTRY)
    except N.AdmissionError as exc:return str(exc)
    raise AssertionError('two co-located units in one mode did not refuse')
_DUPE_RAW=_default_dupe_key()
check('the-default-construction-refusal-normalizes-to-the-registered-tuple-key',
      N.normalize_internal_key(_DUPE_RAW)[0]=='native.requested-capability-duplicate-ownership-tuple')
check('the-default-construction-refusal-names-the-offending-ownership-tuple-as-its-subject',
      N.normalize_internal_key(_DUPE_RAW)[1].endswith(':ts-tsconfig:.'))
check('the-bespoke-unregistered-key-is-gone-from-the-model-source',
      'DUPLICATE_REQUESTED_CAPABILITY' not in
      (H.parent/'native/native_evidence_model.v2.py').read_text())
# The SAME rows meet the SAME key at the shared vocabulary helper, so the default-construction path
# and the explicitly-supplied-spec path publish one vocabulary rather than two.
def _helper_dupe_key():
    try:N.admit_requested_capabilities(
        [{'capabilityId':'inventory','languageMode':'ts-tsconfig','workspaceRoot':'.','required':True}]*2)
    except N.AdmissionError as exc:return str(exc)
    raise AssertionError('the vocabulary helper did not refuse a duplicate ownership tuple')
check('the-default-path-and-the-vocabulary-helper-publish-one-vocabulary-not-two',
      N.normalize_internal_key(_DUPE_RAW)[0]==N.normalize_internal_key(_helper_dupe_key())[0]
      and _DUPE_RAW==_helper_dupe_key())
# Every possible origin now composes a real termination AND a real failure envelope for it.
def _dupe_terms():
    row=N.PUBLIC_ROUTE_REGISTRY['keys']['native.requested-capability-duplicate-ownership-tuple']
    return {o:N.public_termination_for(_DUPE_RAW,o) for o in row['possibleOrigins']}
_DUPE_TERMS=_dupe_terms()
check('every-origin-derives-a-public-termination-for-the-default-construction-refusal',
      len(_DUPE_TERMS)==3 and all(t is not None for t in _DUPE_TERMS.values()))
check('the-host-generated-origin-is-the-host-invariant-fault-the-route-was-written-for',
      _DUPE_TERMS['host-generated-internal-layer']==
      {'class':'operational-failed','errorCode':'SYSTEM.OUTCOME.ILLEGAL_STATE',
       'faultCause':'host-invariant'})
check('the-configured-origin-carries-the-config-invalid-detail-with-the-tuple-subject',
      _DUPE_TERMS['external-configuration']['domainDetail']['code']=='CONFIG.INVALID' and
      _DUPE_TERMS['external-configuration']['domainDetail']['subject'].endswith(':ts-tsconfig:.'))
check('a-caller-still-cannot-launder-this-refusal-into-an-origin-it-cannot-have',
      not_admitted(lambda:N.public_termination_for(_DUPE_RAW,'authenticated-release-declaration'))
      and not_admitted(lambda:N.public_termination_for(_DUPE_RAW)))""")

# --- envelope + carrier composition, placed after the existing tuple-key block ----------------
sub("""check('an-origin-dependent-key-is-correctly-absent-from-the-context-free-alias-map',
      'native.requested-capability-duplicate-ownership-tuple' not in
      {a['internalCode'] for a in
       json.loads((H.parent/'public-detail-registry.v1.json').read_text())['internalAliases']})
""",
    """check('an-origin-dependent-key-is-correctly-absent-from-the-context-free-alias-map',
      'native.requested-capability-duplicate-ownership-tuple' not in
      {a['internalCode'] for a in
       json.loads((H.parent/'public-detail-registry.v1.json').read_text())['internalAliases']})
# V20-ROOT-4, the COMPOSED public surface for the DEFAULT-CONSTRUCTION refusal specifically: not the
# synthetic tuple string the block above uses, but the string the real call actually raised.
check('the-default-construction-terminations-are-admitted-by-the-real-carrier-schema',
      all(admits(COMMON,'#/$defs/StepTermination',t) for t in _DUPE_TERMS.values()))
check('every-origin-composes-a-nonempty-registered-errors-array-for-it',
      all(N.failure_envelope_errors(_DUPE_RAW,o) and
          all(e['code'] in PUBLIC_CODES for e in N.failure_envelope_errors(_DUPE_RAW,o))
          for o in _DUPE_TERMS))
check('every-origin-composes-a-schema-admitted-failure-envelope-for-it',
      all(admits(ENVELOPE,'',{'schemaFamily':'opensip.product.envelope','schemaMajor':2,
                              'kind':'failure','requestId':'req1_'+'c'*32,
                              'termination':_DUPE_TERMS[o],'exitCode':W.EXIT[_DUPE_TERMS[o]['class']],
                              'errors':N.failure_envelope_errors(_DUPE_RAW,o)})
          for o in _DUPE_TERMS))
# V20-ROOT-5 assessed, not redesigned. PUBLIC_ROUTE_REMEDIES is keyed by CODE, so every remedy a key
# reaches must stay true for EVERY key that reaches it. This is the maintenance constraint stated as
# a control over the codes THIS key reaches, including from the default-construction path.
check('every-remedy-reachable-from-the-duplicate-tuple-key-states-the-tuple-condition',
      all('(capabilityId, languageMode, workspaceRoot)' in
          N.PUBLIC_ROUTE_REMEDIES[e['code']]
          for o in _DUPE_TERMS for e in N.failure_envelope_errors(_DUPE_RAW,o)
          if e['code'] in ('CONFIG.INVALID','native.capability-spec-invalid')))
check('the-host-invariant-remedy-is-true-of-a-host-built-default-selection',
      'the host produced an invalid internal record'
      in N.PUBLIC_ROUTE_REMEDIES['HOST.INVARIANT_VIOLATED'] and
      N.failure_envelope_errors(_DUPE_RAW,'host-generated-internal-layer')[0]['code']
      =='HOST.INVARIANT_VIOLATED')
# REACHABILITY, stated honestly and measured rather than asserted: the ACTUAL discovery instrument
# cannot emit two units sharing (rootPath, languageMode) - one rust unit and one tsjs unit per
# directory, and their modes are disjoint - so this refusal is a HOST INVARIANT over the default
# path, not something an admitted repository can provoke. The guard is kept because a host bug of
# that shape must refuse publicly rather than dedupe silently or die in a generic schema error.
_DISCOVERED=N.discover_units({'Cargo.toml':{'sha256':'a'*64},'package.json':{'sha256':'b'*64},
                              'apps/x/tsconfig.json':{'sha256':'c'*64},
                              'apps/x/jsconfig.json':{'sha256':'d'*64},
                              'apps/x/package.json':{'sha256':'e'*64},
                              'apps/y/tsconfig.json':{'sha256':'f'*64,'allowJs':True},
                              'apps/z/jsconfig.json':{'sha256':'0'*64}})['units']
check('co-located-markers-discover-one-unit-per-family-with-disjoint-language-modes',
      len({(u['rootPath'],u['languageMode']) for u in _DISCOVERED})==len(_DISCOVERED))
check('the-actual-discovery-output-drives-a-default-selection-without-any-duplicate',
      len(N.default_capability_selection(_DISCOVERED,_DEFAULT_REGISTRY)
          ['analysisSpec']['requestedCapabilities'])>0)
""")

F.write_text(s)
print({'applied': applied})
