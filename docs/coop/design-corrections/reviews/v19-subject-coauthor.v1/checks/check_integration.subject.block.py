# ============================================================================================
# PROPOSED DURABLE BLOCK for docs/coop/design-corrections/check-integration.py
# Insert beside the other cross-unit joins; it uses only names that file already binds
# (check, M -> integration-host-model, whose M.N is the native model and M.W the workflows
# model). Root integrates; nothing is inserted here.
# ============================================================================================
# ------------------- the exact bounded-selection subject survives the workflow envelope (H-join)
# Native OWNS the refusal and its subject; workflows OWNS the envelope a caller actually reads.
# Neither unit's own suite can see the seam, because each is correct on its own side: native
# projects `field:count>limit`, workflows carries a DomainDetail. The composition is where the
# promise "the subject always names which one overflowed" is either kept or silently lost, so it
# is asserted HERE, over the ACTUAL producer rather than a hand-written termination.
def scope_limit_observation(field, count, prefix):
    """Invoke the real native bounded-selection boundary and project its real typed refusal."""
    try:
        M.N.admit_plan_selection_cardinality({field: [prefix + ('%064x' % i) for i in range(count)]})
    except M.N.ScopeRefusal as exc:
        termination = M.N.scope_refusal_termination(exc)
        detail = termination['domainDetail']
        return detail, {'event': 'rejected', 'errorCode': termination['errorCode'],
                        'detail': detail['code'], 'subject': detail['subject'],
                        'remedy': detail['remedy']}
    raise AssertionError('expected an actual ScopeRefusal for ' + field)

for _field, _count, _prefix in (('semanticClosures', 129, 'closure2:'),
                                ('nativeContextDigests', 129, ''),
                                ('importIds', 257, 'import2:')):
    _detail, _obs = scope_limit_observation(_field, _count, _prefix)
    _term = M.W.terminate(dict(_obs))
    check('native-scope-limit-subject-survives-the-workflow-envelope.' + _field,
          _term['domainDetail'].get('subject') == _detail['subject']
          == _field + ':' + str(_count) + '>' + str(M.N.plan_selection_bound(_field)))
    check('native-scope-limit-public-route-is-unchanged-across-the-seam.' + _field,
          _term['class'] == 'request-rejected'
          and _term['errorCode'] == 'REQUEST.UNSATISFIABLE'
          and _term['domainDetail']['code'] == 'PROJECT.SCOPE_LIMIT'
          and _term['domainDetail']['remedy'] == M.N.SCOPE_LIMIT_REMEDY[_field]
          and M.W.exit_code(_term) == 2)
# The two bounded fields that predate the Plan arrays cross the same seam, so the join is a
# property of the shared law rather than of the three new fields.
for _field, _refuse in (('requestedCapabilities',
                         lambda: M.N.admit_requested_capability_cardinality(
                             [{'capabilityId': 'references', 'languageMode': 'ts-tsconfig',
                               'workspaceRoot': 'r%05d' % i, 'required': True}
                              for i in range(M.N.requested_capability_bound() + 1)])),
                        ('workspaceRoots',
                         lambda: M.N.unit_scope_descriptor(
                             [{'rootPath': 'r%05d' % i, 'languageMode': 'ts-tsconfig',
                               'languageFamily': 'tsjs'} for i in range(1025)], []))):
    try:
        _refuse()
        _observed = None
    except M.N.ScopeRefusal as _exc:
        _d = M.N.scope_refusal_termination(_exc)['domainDetail']
        _observed = M.W.terminate({'event': 'rejected', 'errorCode': 'REQUEST.UNSATISFIABLE',
                                   'detail': _d['code'], 'subject': _d['subject'],
                                   'remedy': _d['remedy']})['domainDetail'].get('subject')
    check('inherited-scope-limit-subject-survives-the-workflow-envelope.' + _field,
          _observed == _field + ':1025>1024')
