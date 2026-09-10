"""CB7-SHOULD-2: the new control set, appended beside the existing bounded-selection controls."""
import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/v19-native-coauthor.v1/work')
P = W / 'docs/coop/design-corrections/foundation/check-identity.py'
s = P.read_text(encoding='utf-8')

ANCHOR = """# the widened published meaning is stated, not silently stretched
"""
NEW = '''# ------------------------------------------------- CB7-SHOULD-2: the PLAN's own bounded selections.
# Three arrays a valid ordinary request can overflow, whose only previous outcome was a generic
# jsonschema maxItems error naming no field, count, limit or public route.
_PLAN_BOUNDS={f:N.plan_selection_bound(f) for f in N.PLAN_SELECTION_FIELDS}
check('the-plan-bounds-are-read-from-the-published-schema-not-restated',
      _PLAN_BOUNDS=={f:M.SCHEMA['$defs']['plan']['properties'][f]['maxItems']
                     for f in N.PLAN_SELECTION_FIELDS} and
      _PLAN_BOUNDS=={'semanticClosures':128,'nativeContextDigests':128,'importIds':256})
# ORDER is the published declaration order of $defs/plan, so a request overflowing two arrays always
# yields the same first subject. A hand-kept tuple that drifted from the document would silently
# change which field a caller is told to narrow.
check('the-plan-selection-order-is-the-published-declaration-order',
      list(N.PLAN_SELECTION_FIELDS)==[f for f in M.SCHEMA['$defs']['plan']['properties']
                                      if f in set(N.PLAN_SELECTION_FIELDS)])
def _plan_over(**fields):
    base={f:[] for f in N.PLAN_SELECTION_FIELDS}
    base.update(fields)
    return base
_ID=lambda prefix,n:[prefix+'%064x'%i for i in range(n)]
# BOUNDARY: exactly at the bound admits, one over refuses. An off-by-one here would either reject a
# lawful maximal selection or let an unrepresentable one through to a generic schema error.
for _field,_prefix in (('semanticClosures','closure2:'),('nativeContextDigests',''),
                       ('importIds','import2:')):
    _limit=_PLAN_BOUNDS[_field]
    check('a-plan-selection-exactly-at-its-bound-is-admitted.'+_field,
          N.admit_plan_selection_cardinality(_plan_over(**{_field:_ID(_prefix,_limit)}))[_field]
          ==_ID(_prefix,_limit))
    rejects_because('a-plan-selection-one-over-its-bound-refuses-typed.'+_field,
        lambda f=_field,p=_prefix,l=_limit:N.admit_plan_selection_cardinality(
            _plan_over(**{f:_ID(p,l+1)})),
        'PROJECT.SCOPE_LIMIT:'+_field+':'+str(_limit+1)+'>'+str(_limit))
# The typed refusal carries the field, the exact observed bound and this field's OWN remedy.
def _plan_refusal(field,count):
    try:N.admit_plan_selection_cardinality(_plan_over(**{field:_ID('',count)}))
    except N.ScopeRefusal as exc:return exc
    raise AssertionError('the plan selection did not refuse')
_IMPORT_REFUSAL=_plan_refusal('importIds',257)
check('the-plan-selection-refusal-carries-field-count-limit-and-its-own-remedy',
      _IMPORT_REFUSAL.detail=='PROJECT.SCOPE_LIMIT' and
      _IMPORT_REFUSAL.subject=={'field':'importIds','count':257,'limit':256} and
      N.SCOPE_LIMIT_REMEDY['importIds']!=N.SCOPE_LIMIT_REMEDY['workspaceRoots'])
# PUBLIC ENVELOPE: request-rejected, exit 2, REQUEST.UNSATISFIABLE, PROJECT.SCOPE_LIMIT, exact subject.
_PLAN_TERMINATION=N.scope_refusal_termination(_IMPORT_REFUSAL)
check('an-oversized-plan-selection-projects-the-existing-public-route',
      _PLAN_TERMINATION['class']=='request-rejected' and
      _PLAN_TERMINATION['errorCode']=='REQUEST.UNSATISFIABLE' and
      _PLAN_TERMINATION['domainDetail']['code']=='PROJECT.SCOPE_LIMIT' and
      _PLAN_TERMINATION['domainDetail']['subject']=='importIds:257>256' and
      _PLAN_TERMINATION['domainDetail']['remedy']==N.SCOPE_LIMIT_REMEDY['importIds'])
check('the-oversized-plan-selection-route-adds-no-public-code',
      N.d9_map('PROJECT.SCOPE_LIMIT')['exitCode']==2 and
      'PROJECT.SCOPE_LIMIT' in {r['code'] for r in
          json.loads((H.parent/'public-detail-registry.v1.json').read_text())['records']})
# DETERMINISTIC ORDER when more than one overflows at once.
rejects_because('two-oversized-plan-selections-refuse-on-the-first-published-field',
    lambda:N.admit_plan_selection_cardinality(_plan_over(
        semanticClosures=_ID('closure2:',129),importIds=_ID('import2:',257))),
    'PROJECT.SCOPE_LIMIT:semanticClosures:129>128')
rejects_because('the-second-published-field-is-reported-once-the-first-is-narrowed',
    lambda:N.admit_plan_selection_cardinality(_plan_over(
        nativeContextDigests=_ID('',129),importIds=_ID('import2:',257))),
    'PROJECT.SCOPE_LIMIT:nativeContextDigests:129>128')
# MALFORMED SHAPES stay the schema's. Nothing is coerced, and a 300-character STRING is never
# reported as 300 members - the misclassification the analysis-spec boundary already had to fix.
def _no_scope_refusal(value):
    """True when this shape passes the cardinality boundary untouched, so the SCHEMA gets to own it."""
    try:return N.admit_plan_selection_cardinality(value) is value
    except N.ScopeRefusal:return False
for _label,_value in (('null',None),('true',True),('false',False),('number',300),
                      ('string','x'*300),('object',{'a':1}),('nested-list',[['a']*300])):
    _probe=_plan_over(importIds=_value)
    check('a-malformed-plan-selection-shape-raises-no-scope-refusal.'+_label,_no_scope_refusal(_probe))
_MISSING=_plan_over();_MISSING.pop('importIds')
check('a-missing-plan-selection-field-raises-no-scope-refusal',_no_scope_refusal(_MISSING))
check('a-non-object-prospective-plan-raises-no-scope-refusal',
      _no_scope_refusal(None) and _no_scope_refusal([1,2,3]))
# The string case is the one that was PUBLICLY MISCLASSIFIED for the analysis spec: a 300-character
# string must never be reported as 300 members with a typed scope refusal.
check('an-oversized-string-is-never-reported-as-a-member-count',
      _no_scope_refusal(_plan_over(importIds='x'*300)))
# CARDINALITY-FIRST only where an ACTUAL array exceeds: an in-bound array that is malformed some
# other way passes through untouched.
check('an-in-bound-but-malformed-plan-selection-passes-through-to-the-schema',
      N.admit_plan_selection_cardinality(_plan_over(importIds=[7,8,9]))['importIds']==[7,8,9])

# THE REACHABLE CASES, through published bounds rather than assertion.
check('a-narrow-capability-workspace-reaches-the-plan-context-bound-through-admitted-bounds',
      129<=M.SCHEMA['$defs']['scope-descriptor']['properties']['workspaceRoots']['maxItems'] and
      129<=N.requested_capability_bound() and 129>_PLAN_BOUNDS['nativeContextDigests'])
# ...and through the ACTUAL producer of that field, which is where the deduplicated count first exists.
rejects_because('the-native-context-digest-producer-accounts-for-its-own-field',
    lambda:N.plan_native_context_digests(
        [{'refusals':[],'planNativeContextDigest':'%064x'%i} for i in range(129)]),
    'PROJECT.SCOPE_LIMIT:nativeContextDigests:129>128')
check('the-native-context-digest-producer-still-returns-a-lawful-deduplicated-set',
      N.plan_native_context_digests(
          [{'refusals':[],'planNativeContextDigest':'a'*64},
           {'refusals':[],'planNativeContextDigest':'a'*64}])==['a'*64])
check('the-configuration-import-selection-outranges-the-plan-import-array',
      M.SCHEMA['$defs']['semantic-configuration']['properties']['evidence']['properties'][
          'importIds']['maxItems']==1024 and _PLAN_BOUNDS['importIds']==256)

# THE REAL CONSTRUCTION PATH: an oversized ordinary selection refuses BEFORE plan2 is minted, so the
# refused step has no Plan and no Run at all. This drives `build`, not the helper.
rejects_because('an-oversized-plan-import-selection-on-the-construction-path-mints-no-plan',
    lambda:build(plan_import_ids=_ID('import2:',257)),
    'PROJECT.SCOPE_LIMIT:importIds:257>256')
rejects_because('an-oversized-plan-closure-selection-on-the-construction-path-mints-no-plan',
    lambda:build(plan_semantic_closures=_ID('closure2:',129)),
    'PROJECT.SCOPE_LIMIT:semanticClosures:129>128')
check('an-in-bound-plan-import-selection-on-the-construction-path-still-closes-a-run',
      M.close_run(*build(resolved=True,has_match=True,
                         plan_import_ids=[])).startswith('run2:'))
_AT_BOUND_PLAN=build(plan_import_ids=_ID('import2:',256))[1]
check('a-plan-import-selection-exactly-at-its-bound-is-still-minted',
      len(next(v for k,(d,v) in _AT_BOUND_PLAN.items() if d=='plan')['importIds'])==256)

# A RETAINED Plan over its bound stays a CORRUPT/malformed retained record: schema-first, not a
# request-scope rewrite. Re-deriving a caller's remedy from committed bytes would misreport a
# corrupt store as an oversized request.
def _retained_plan_over_bound():
    run,objects,blobs=build(resolved=True,has_match=True)
    plan=copy.deepcopy(objects[run['planId']][1])
    plan['importIds']=_ID('import2:',257)
    rekey_plan(objects,blobs,run,plan)
    return M.close_run(run,objects,blobs)
check('a-retained-plan-over-its-bound-refuses-at-retained-closure',
      not_admitted(_retained_plan_over_bound))
def _raised(fn):
    try:fn()
    except BaseException as exc:return exc
    return None
check('a-retained-plan-over-its-bound-is-not-reclassified-as-a-request-scope-refusal',
      not isinstance(_raised(_retained_plan_over_bound),N.ScopeRefusal))

# the widened published meaning is stated, not silently stretched
'''
assert s.count(ANCHOR) == 1
s = s.replace(ANCHOR, NEW)
P.write_text(s, encoding='utf-8')
print('ok')
