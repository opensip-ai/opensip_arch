# ============================================================================================
# PROPOSED DURABLE BLOCK for docs/coop/design-corrections/workflows/check_workflows.v1.py
# Insert anywhere after the `golden.*` termination checks; it uses only names that file already
# binds (check, must_valid, must_invalid, M, U). Root integrates; nothing is inserted here.
# ============================================================================================
# ------------------------------------------------- DomainDetail.subject survives `terminate`
# The public detail vocabulary is CLOSED, and this contract states what carries the rest:
# "Dynamic paths or refusal explanations travel in bounded `subject`/`remedy` fields, never as
# newly invented codes." `terminate` rebuilds a DomainDetail from an observation field by field
# and copied only two of the three, so a producer whose entire disclosure IS its subject lost it
# at the envelope. Native section 14's bounded selection refusal is the live case: it promises
# `field:count>limit` and that "the subject always names which one overflowed", yet every bounded
# field arrived as one indistinguishable PROJECT.SCOPE_LIMIT - leaving a caller who needs to know
# WHICH bound was hit only the newly invented code the sentence above forbids.
_SUBJECT_OBS = {'event': 'rejected', 'errorCode': 'REQUEST.UNSATISFIABLE',
                'detail': 'PROJECT.SCOPE_LIMIT', 'remedy': 'narrow the selection explicitly',
                'subject': 'importIds:257>256'}
_SUBJECT_TERM = M.terminate(dict(_SUBJECT_OBS))
check('termination.observed-subject-is-carried-exactly',
      _SUBJECT_TERM['domainDetail'].get('subject') == _SUBJECT_OBS['subject'],
      str(_SUBJECT_TERM))
must_valid('termination.subject-carrying-detail-is-schema-valid',
           U + 'common#/$defs/StepTermination', _SUBJECT_TERM)
# STRICTLY ADDITIVE: an observation with no subject yields exactly what it always yielded.
check('termination.absent-subject-adds-no-field',
      M.terminate({k: v for k, v in _SUBJECT_OBS.items() if k != 'subject'})
      == {'class': 'request-rejected', 'errorCode': 'REQUEST.UNSATISFIABLE',
          'domainDetail': {'code': 'PROJECT.SCOPE_LIMIT',
                           'remedy': 'narrow the selection explicitly'}})
check('termination.detailless-observation-still-has-no-domain-detail',
      'domainDetail' not in M.terminate({'event': 'rejected',
                                         'errorCode': 'REQUEST.UNSATISFIABLE'}))
# ONE record, ONE rule. `Refusal.termination()` already carried a subject onto this exact shape;
# two producers of one record disagreeing about one of its fields was the defect, so they are
# held equal on a present, an absent and an empty subject alike.
for _label, _subject in (('present', 'importIds:257>256'), ('absent', None), ('empty', '')):
    _obs = {k: v for k, v in _SUBJECT_OBS.items() if k != 'subject'}
    if _subject is not None:
        _obs['subject'] = _subject
    check('termination.both-producers-of-one-termination-agree.' + _label,
          M.terminate(_obs) == M.Refusal(_SUBJECT_OBS['errorCode'], _SUBJECT_OBS['detail'],
                                         _SUBJECT_OBS['remedy'], _subject).termination())
# The subject is COPIED, never ADMITTED. A malformed trusted observation is still the schema's to
# refuse, exactly as it is for a malformed `remedy` or `detail`; this makes no admission claim.
must_invalid('termination.over-length-observed-subject-is-still-refused-by-the-schema',
             U + 'common#/$defs/DomainDetail',
             M.terminate(dict(_SUBJECT_OBS, subject='x' * 2000))['domainDetail'])
