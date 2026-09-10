"""EDIT 4 (item 1): actual controls for the two now-registered scope-binding details.

These are not register-string assertions. They run the DIRECT verifier and the `adopt_baseline`
caller, take the REAL Refusal objects those calls raise, project them through the model's own
`termination()`, and validate the result against the owning unit's pinned public carrier and
against the full `kind=failure` CommandEnvelope - the same two surfaces the earlier CB-GAP-1
controls used for the ambiguity refusal. A live-validator negative keeps them non-vacuous.
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
F = ROOT / 'foundation/check-identity.py'

ANCHOR = """check('zero-selection-is-not-silently-filled-from-the-plan-scope-descriptor',
      _refusal(lambda:W.verify_scope_parameter_binding(
          _spec([]),{'schemaVersion':2,'workspaceRoots':['.'],'pathPrefixes':['.'],
                     'excludedPathPrefixes':[]})).detail=='BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER')
"""

ADDED = """
# --- V20-ROOT-3: the two PRESERVED details are now REGISTERED, so the real carrier can carry them.
# Before this correction both names were emitted straight into the public DomainDetail.code position
# while being members of NEITHER public-detail-registry.v1.json NOR the mirrored DomainDetailCode
# enum, so common.schema.json#/$defs/StepTermination REFUSED both terminations and these two
# refusals - the only two the verifier reaches for a well-formed single-row spec - had no public
# route at all. Registration preserves every emission exactly; what changes is admissibility.
_PUBLIC_REGISTRY=json.loads((H.parent/'public-detail-registry.v1.json').read_text())
_PUBLIC_RECORDS={r['code'] for r in _PUBLIC_REGISTRY['records']}
_SCOPE_DETAILS=('BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER','BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH')
check('both-scope-binding-details-are-members-of-the-closed-public-detail-registry',
      all(c in _PUBLIC_RECORDS for c in _SCOPE_DETAILS))
check('both-scope-binding-details-are-members-of-the-mirrored-closed-schema-enum',
      all(c in _COMMON_SCHEMA['$defs']['DomainDetailCode']['enum'] for c in _SCOPE_DETAILS))
check('the-registry-and-the-mirrored-enum-still-agree-exactly-after-the-registration',
      sorted(_PUBLIC_RECORDS)==_COMMON_SCHEMA['$defs']['DomainDetailCode']['enum'])
check('the-registration-added-exactly-these-two-members-and-nothing-else',
      len(_PUBLIC_RECORDS)==289 and
      {c for c in _PUBLIC_RECORDS if c.startswith('BASELINE.SCOPE')}==set(_SCOPE_DETAILS))
check('both-are-owned-by-workflows-and-carry-the-mirroring-selector',
      all(r['owner']=='workflows' and
          r['selector']=='workflows/schemas/common.schema.json#/$defs/DomainDetailCode'
          for r in _PUBLIC_REGISTRY['records'] if r['code'] in _SCOPE_DETAILS))
# They are NOT internal aliases: an alias normalizes an internal decision key that may not appear as
# a public DomainDetailCode, and these two are emitted by their owner directly into that position.
check('neither-scope-binding-detail-is-an-internal-alias',
      not ({a['internalCode'] for a in _PUBLIC_REGISTRY['internalAliases']}&set(_SCOPE_DETAILS)))
# THE DIRECT VERIFIER, on the ACTUAL Refusal objects - not on hand-written code strings.
_NOT_SELECTED_REF=_refusal(lambda:W.verify_scope_parameter_binding(_spec([]),SCOPE_DOCUMENT))
_MISMATCH_REF=_refusal(lambda:W.verify_scope_parameter_binding(_spec([_SCOPE_ROW_A]),SCOPE_DOCUMENT_B))
check('the-direct-verifier-refusals-keep-their-exact-preserved-error-code-and-detail',
      [(r.error_code,r.detail) for r in (_NOT_SELECTED_REF,_MISMATCH_REF)]==
      [('REQUEST.PRECONDITION_FAILED','BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER'),
       ('REQUEST.PRECONDITION_FAILED','BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH')])
check('the-two-conditions-stay-distinct-and-neither-collapses-onto-the-ambiguity-code',
      len({_NOT_SELECTED_REF.detail,_MISMATCH_REF.detail,'CONFIG.INVALID'})==3)
check('the-preserved-remedy-strings-are-unchanged-and-name-their-own-condition',
      _NOT_SELECTED_REF.remedy=='the analysis spec selects no ScopeDocumentV1 parameter' and
      _MISMATCH_REF.remedy=='the supplied scope document is not the selected scope parameter')
check('both-direct-verifier-terminations-are-admitted-by-the-real-public-carrier-schema',
      all(_step_termination_admits(r.termination()) for r in (_NOT_SELECTED_REF,_MISMATCH_REF)))
# and the full public FAILURE surface, not just the termination: a kind=failure CommandEnvelope
# REQUIRES a nonempty errors array of DomainDetail, so a detail the enum refuses breaks that too.
_ENVELOPE_SCHEMA='workflows/schemas/command-envelope.schema.json'
def _scope_failure_envelope(ref):
    t=ref.termination()
    return {'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'failure',
            'requestId':'req1_'+'b'*32,'termination':t,'exitCode':W.EXIT[t['class']],
            'errors':[t['domainDetail']]}
def _envelope_admits(env):
    try:W.validate_import_record(_ENVELOPE_SCHEMA,'',env)
    except W.Refusal:return False
    return True
check('both-scope-binding-refusals-compose-a-schema-admitted-failure-envelope',
      all(_envelope_admits(_scope_failure_envelope(r)) for r in (_NOT_SELECTED_REF,_MISMATCH_REF)))
check('the-composed-envelopes-carry-exit-code-2-for-request-rejected',
      all(_scope_failure_envelope(r)['exitCode']==2 for r in (_NOT_SELECTED_REF,_MISMATCH_REF)))
# NON-VACUITY, on both surfaces: an UNREGISTERED detail on the same two shapes still refuses. The
# probe name is deliberately one this correction did NOT register.
_UNREGISTERED='BASELINE.SCOPE_PARAMETER_AMBIGUOUS'
check('the-unregistered-probe-name-really-is-outside-both-closed-registries',
      _UNREGISTERED not in _PUBLIC_RECORDS and
      _UNREGISTERED not in _COMMON_SCHEMA['$defs']['DomainDetailCode']['enum'])
def _with_detail(ref,code):
    t=ref.termination();t['domainDetail']=dict(t['domainDetail'],code=code);return t
check('an-unregistered-detail-on-the-same-termination-shape-is-still-refused-by-the-carrier',
      not any(_step_termination_admits(_with_detail(r,_UNREGISTERED))
              for r in (_NOT_SELECTED_REF,_MISMATCH_REF)))
check('an-unregistered-detail-on-the-same-envelope-shape-is-still-refused',
      not any(_envelope_admits({**_scope_failure_envelope(r),
                                'termination':_with_detail(r,_UNREGISTERED),
                                'errors':[_with_detail(r,_UNREGISTERED)['domainDetail']]})
              for r in (_NOT_SELECTED_REF,_MISMATCH_REF)))
# THE CALLER. `adopt_baseline` is the caller the contract names, and it reaches the verifier only
# when the retained analysis-spec is supplied. These run it for real and take what it raises: the
# refusal must PROPAGATE out of the caller with its detail intact and reach the public carrier from
# there, which is the actual public path rather than a helper-only claim.
_ADOPT_RUN={'authority':'authoritative','availability':'retained','snapshotId':'snap1','runId':'run2:x'}
def _adopt(spec_rows,document):
    return W.adopt_baseline(_ADOPT_RUN,'plan2:x','proj',{'schemaVersion':1,'rules':[]},document,
                            {'schemaVersion':1,'waivers':[]},[],[],[],[],{},'0.0.0',
                            analysis_spec=_spec(spec_rows))
_ADOPT_NOT_SELECTED=_refusal(lambda:_adopt([],SCOPE_DOCUMENT))
_ADOPT_MISMATCH=_refusal(lambda:_adopt([_SCOPE_ROW_A],SCOPE_DOCUMENT_B))
check('adopt_baseline-propagates-the-missing-selection-refusal-unchanged',
      (_ADOPT_NOT_SELECTED.error_code,_ADOPT_NOT_SELECTED.detail)==
      ('REQUEST.PRECONDITION_FAILED','BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER'))
check('adopt_baseline-propagates-the-digest-mismatch-refusal-unchanged',
      (_ADOPT_MISMATCH.error_code,_ADOPT_MISMATCH.detail)==
      ('REQUEST.PRECONDITION_FAILED','BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH'))
check('both-adopt_baseline-refusals-reach-the-real-carrier-and-the-failure-envelope',
      all(_step_termination_admits(r.termination()) and _envelope_admits(_scope_failure_envelope(r))
          for r in (_ADOPT_NOT_SELECTED,_ADOPT_MISMATCH)))
# NOT VACUOUS: the same caller with the SELECTED document does not raise either scope refusal, so
# the two controls above are measuring the binding and not some unrelated precondition.
def _adopt_scope_detail(spec_rows,document):
    try:_adopt(spec_rows,document)
    except W.Refusal as exc:return exc.detail
    return None
check('adopt_baseline-with-the-selected-document-raises-neither-scope-binding-refusal',
      _adopt_scope_detail([_SCOPE_ROW_A],SCOPE_DOCUMENT) not in _SCOPE_DETAILS)
# And the ambiguity refusal introduced by the earlier correction is untouched by the registration.
check('the-ambiguity-refusal-still-uses-config-invalid-after-the-registration',
      _refusal(lambda:W.verify_scope_parameter_binding(
          _spec([_SCOPE_ROW_A,_SCOPE_ROW_B]),SCOPE_DOCUMENT)).detail=='CONFIG.INVALID')
"""

s = F.read_text()
assert s.count(ANCHOR) == 1, s.count(ANCHOR)
F.write_text(s.replace(ANCHOR, ANCHOR + ADDED))
print('controls added')
