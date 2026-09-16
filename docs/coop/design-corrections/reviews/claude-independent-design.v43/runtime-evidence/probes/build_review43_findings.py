# Executed by build_review43.py in its own globals (exec). Issues, observations, current dispositions of every prior finding,
# advisory and observation, charter item assessments and the named scope basis. Every claimed measurement is re-checked here.

def pick(rows, prefix, label):
    row = next((r for c, r in rows.items() if c.startswith(prefix)), None)
    if row is None:
        GAPS.append('%s row missing: %s' % (label, prefix))
        return {}
    if not row['ok']:
        GAPS.append('%s row not ok: %s' % (label, prefix))
    return row['observed']


def qx(prefix):
    return pick(Q43X, prefix, 'query43-x')


def qa(prefix):
    return pick(QAX, prefix, 'query-adapter43-x')


def qp(prefix):
    return pick(QPR, prefix, 'query-prose43')


MUST, SHOULD = [], []
V42ITEMS = {i['id']: i for i in V42['itemDispositions']}

# ------------------------------------------------------------------------------------------------ ADV42-01 (retained)
J1, J2, J3 = pick(CJ, 'J1-', 'capture-joins-on43'), pick(CJ, 'J2-', 'capture-joins-on43'), pick(CJ, 'J3-', 'capture-joins-on43')
adv_ok = (J1.get('admission', {}).get('refusals') == ['EXECUTION_INPUTS_PLAN_JOIN'] and J2.get('admission', {}).get('result') == 'ADMIT' and J3.get('admission', {}).get('result') == 'ADMIT'
          and 'CLOSURE_FIELD_KIND' in str(J2.get('fullRun')) and 'CLOSURE_FIELD_KIND' in str(J3.get('fullRun'))
          and not PORTED_EQUAL['P43-PORTED-CAPTURE-JOINS']['observedDifferFromSource42'])
adv_bytes = {k: U[k] for k in ('execution-inputs-contract.v1.md', 'execution_inputs_model.v1.py', 'execution_inputs_fixture.v3.py', 'identity-model.v3.py', 'identity-schemas.v3.json')}
if not adv_ok or not all(adv_bytes.values()):
    GAPS.append('ADV42-01 re-measurement or owner-byte identity not as recorded')
V42ADV = next(a for a in V42['advisories'] if a['id'] == 'ADV42-01')
ADVISORIES = [{
    'id': 'ADV42-01', 'severity': 'ADVISORY', 'origin': 'source42 review (retained; not new in source43)', 'title': V42ADV['title'],
    'selectors': V42ADV['selectors'], 'selectorOwnerBytesUnchanged42to43': adv_bytes,
    'measuredOnSource43': {'sameProviderForeignPlanId': J1, 'foreignProducerSamePlan': J2, 'foreignProducerForeignPlan': J3,
                           'observedEqualToSource42Receipt': not PORTED_EQUAL['P43-PORTED-CAPTURE-JOINS']['observedDifferFromSource42']},
    'detail': V42ADV['detail'],
    'currentStanding': 'RETAINED ADVISORY, NON-BLOCKING. Root routing as an implementation verification obligation for crates/host/src/analysis.rs is assessed as correctly scoped; it is not a containment proof and no control was executed for it.',
    'standingAssessment': ('Every selector owner is byte-identical 42->43 (%s), and the ported measurement re-observes the four source42 values on source43: J1 refuses EXECUTION_INPUTS_PLAN_JOIN; J2 and J3 admit, and close_run refuses them with CLOSURE_FIELD_KIND:view.producerClosure:provider. '
                           'The source-only note keeps the advisory with a verification obligation for crates/host/src/analysis.rs. Repository layout 14 (:475, search output) names that module as the service composing provider work, admission, evaluation and complete replay, which makes it the planned host capture. '
                           'Execution-inputs section 8 (:299, source42 read on byte-identical bytes) already binds the builder to place each explicit returned view on the view stage whose producerClosure it carries. A product verification that analysis.rs never lists a view on another producer\'s complete receipt therefore tests existing law and invents none. '
                           'This routing is carried by the root note, not by a source43 byte: the planning inputs and coverage are unchanged. Final application must carry it explicitly. '
                           'Scope limits: no two-stage two-provider Plan was minted by this review or by the note, so the unexercised shape stays argued from source. Execution-inputs admission still does not re-check receipt/view producer equality or apply PLAN_JOIN before the row filter, and those contract-level options stay optional owner improvements. '
                           'Nothing warrants reopening the advisory for wording: no measured world admits a contradictory Run, the refusal chain is closed by the Run owner, and TCB-SCOPE-01 is unchanged.') % json.dumps(adv_bytes),
    'consequence': V42ADV['consequence'],
    'disposition': 'ADVISORY, non-blocking; retained with owner routing (foundation execution-inputs owner for the optional contract clarifications; crates/host/src/analysis.rs implementation verification obligation at final application / implementation).',
    'owner': V42ADV['owner'],
    'receipts': ['receipts/probes/capture-joins-on43.json', 'claude-independent-design.v42/receipts/probes/capture-joins-42.json (historical)', 'claude-independent-design.v42/receipts/probes/view-attribution-x.json (historical)']}]

# ------------------------------------------------------------------------------------------------ observations
omit_rows = [qx('availability-%s: omitted and retained report retained' % op) for op in ('neighbors', 'path', 'reach')]
OBSERVATIONS = [
    {'id': 'OBS43-01', 'text': ('Omitted reference observation. Contract section 7 (:162) says an omitted observation neither refuses nor grants ("not a grant and not a purge"), and it pins what an observed retained or partial state reports. The value a successful response reports for an omitted observation is not stated in contract prose. '
                                'It is stated by the model docstring (query_projection_model.v3.py:1483-1485: retained once close_run has admitted the closure) and pinned by the checker control host-availability-retained-and-omitted-report-retained. Measured: omitted reports retained on both trees for neighbors, path and reach. '
                                'A product adapter always supplies an observation, the admitted state of the retained record (:164, :166), so omission is a reference-harness case with no product surface. Not a defect; a one-clause prose pin is optional.'),
     'receipt': 'receipts/probes/query43-x.json'},
    {'id': 'OBS43-02', 'text': ('Current availability is not part of the cursor binding. selection_hash binds project, Run, fact-views, operation and effective params, and never availability (model :334-342). A continuation issued under one observation and presented under partial is admitted with the same page, and source43 discloses partial on that page. '
                                'This is consistent with availability being a current monotonic-generation record (identity :1722-1725) rather than a selection input. A refusing state still refuses.'),
     'receipt': 'receipts/probes/query43-x.json'},
    {'id': 'OBS43-03', 'text': ('Path rows carry no stored-orientation flag. Under incoming or both, a consumer recovers a hop\'s stored orientation only by its factId, for example from the neighbors row that keeps the projected fact\'s source->target. '
                                'This is the representation section 4 (:100) selects. GraphPathEdge (schema :817-836) has no orientation description, and GraphPathRow (:847) describes only zero-hop and the tie-break. It is not a defect.'),
     'receipt': 'receipts/probes/query43-x.json'},
    {'id': 'OBS43-04', 'text': ('Against root-source43-final-reference.v1 and codex final-reference.v43: all six group stdouts are byte-equal (%s); %d of %d child stdouts are byte-equal to root; enumeration and execution-inputs differ only in ownedHashes[].path/receiptPath (equal after removing only those fields, also against this origin\'s source42 receipts); '
                                'query-projection is byte-equal to root and differs from this origin\'s source42 receipt only by 204 -> 209 checks (added %s; none removed). The codex runner-original equals the root reference-checks (%s); codex adds the formal subject binding (changed top-level keys %s).')
     % (all(v['stdoutFileEqualRoot'] and v['stdoutFileEqualCodex'] for v in RC['groups'].values()), RC['childrenEqualRoot'], RC['childCount'],
        RCS['query-projection.stdout']['checkIdsAddedVs42'], RCS['codexRunnerOriginalEqualsRoot'], RCS['codexMinusRootTopLevelKeys']), 'receipt': 'receipts/reference-comparison.json; receipts/reference-children-stripped.json'},
    {'id': 'OBS43-05', 'text': ('The root reference and root planning verification were executed from a pre-freeze working tree (%s), not from the frozen archive. Their recorded script shas equal the frozen source43 bytes. '
                                'Their stdouts equal this review\'s own executions on verified archive copies: all six group stdouts are byte-equal, and the planning stdout sha is equal (%s). This review\'s own executions are the acceptance input.')
     % (RC['rootExecutionSourceRoots'], planning_stdout_equal_root), 'receipt': 'receipts/reference-comparison.json; receipts/planning-checks.json'},
    {'id': 'OBS43-06', 'text': ('Re-observed on source43 by the ten ported scope probes, every observed value identical to this origin\'s source42 receipts: %s. The source42 observation contents of OBS42-08 therefore stand on unchanged owner bytes.')
     % ', '.join('%s %d rows' % (k.replace('P43-PORTED-', '').lower(), v['rows']) for k, v in PORTED_EQUAL.items()), 'receipt': 'receipts/probes (ported43_*)'},
    {'id': 'OBS43-07', 'text': ('The model delta is three hunks (query_projection_model.v3.py diff): an observe_availability docstring, return avail replacing return "retained", and execute_graph_query passing that value to finish_operation in place of the literal "retained". '
                                'Refusal routes, observation order, cursor, traversal and every other context field are byte-identical in behaviour (P43-QUERY-X: omitted/retained responses and all orientation, route, cursor and bound responses are byte-identical across trees).'),
     'receipt': 'receipts/delta-diffs-42to43/docs__coop__design-corrections__workflows__query_projection_model.v3.py.diff; receipts/probes/query43-x.json'},
]
if not all(omit_rows):
    GAPS.append('omitted-observation rows missing')

# ------------------------------------------------------------------------------------------------ prior finding dispositions
PRIOR_DISPOSITIONS = [
    {'id': 'S40-01', 'priorSeverity': 'SHOULD (source40)', 'source42Disposition': 'RESOLVED-ON-COMPLETE-SOURCE42-BYTES', 'currentDisposition': 'REMAINS RESOLVED ON SOURCE43',
     'basis': ('unchanged-42 basis plus current corroboration. The execution-inputs contract, schema, model and fixture and the enumeration contract/model are byte-identical 42->43 (%s), so the section 3 attribution predicate and section 8 capture exactness assessed in CH42-ATTRIBUTION-LAW and CH42-CAPTURE stand. '
               'Current: the execution-inputs child runs 95 cases and the enumeration child 54, each equal to root and to this origin\'s source42 receipts after removing only path fields, and the capture-join measurement is identical.')
     % json.dumps({k: U[k] for k in ('execution-inputs-contract.v1.md', 'execution-inputs.schema.v1.json', 'execution_inputs_model.v1.py', 'execution_inputs_fixture.v3.py', 'enumeration-contract.v1.md', 'enumeration_model.v1.py')}),
     'evidence': ['receipts/reference-children-stripped.json', 'receipts/probes/capture-joins-on43.json', 'source42 review CH42-ATTRIBUTION-LAW / CH42-CAPTURE (historical)']},
    {'id': 'ADV40-01', 'priorSeverity': 'EDITORIAL (source40)', 'source42Disposition': 'RESOLVED', 'currentDisposition': 'REMAINS RESOLVED ON SOURCE43',
     'basis': ('implementation-planning-sources.v1.json and every docs/v2/architecture file (%d files) are byte-identical 42->43. The standing selects v11 (%s) as current, v8 stays a superseded intermediate (bytes %s, unchanged), and the prior-layer history digests match their bytes (%s). No historical layer was mutated.')
     % (PC['architectureDirFileCount'], PC['layerSha256']['11'][:12] + '...', PC['layerSha256']['8'][:12] + '...', PC['planningSourcesHistoryHashesMatchLayerBytes']),
     'evidence': ['receipts/planning-checks.json']},
    {'id': 'ADV42-01', 'priorSeverity': 'ADVISORY (source42)', 'source42Disposition': 'ADVISORY, non-blocking', 'currentDisposition': 'RETAINED ADVISORY (see advisories)',
     'basis': ADVISORIES[0]['currentStanding'], 'evidence': ADVISORIES[0]['receipts']},
    {'id': 'OBS42-01', 'currentDisposition': 'RETAINED OBSERVATION', 'basis': 'execution_inputs_fixture.v3.py and execution_inputs_model.v1.py byte-identical 42->43 (%s, %s); the reference builder\'s single-producer attribution limitation is unchanged.' % (U['execution_inputs_fixture.v3.py'], U['execution_inputs_model.v1.py']), 'evidence': ['mapSources']},
    {'id': 'OBS42-02', 'currentDisposition': 'RETAINED OBSERVATION', 'basis': 'enumeration-contract.v1.md and native_evidence_model.v2.py byte-identical 42->43 (%s, %s); the binder shorthand remains disambiguated within the same section.' % (U['enumeration-contract.v1.md'], U['native_evidence_model.v2.py']), 'evidence': ['mapSources']},
    {'id': 'OBS42-03', 'currentDisposition': 'RETAINED OBSERVATION (not re-probed)', 'basis': 'Capture owner bytes unchanged; the refs-only capture consequence measured by the source42 three-tree probe stands; the execution-inputs child cases are equal modulo paths.', 'evidence': ['receipts/reference-children-stripped.json', 'claude-independent-design.v42/receipts/probes/view-attribution-x.json (historical)']},
    {'id': 'OBS42-04', 'currentDisposition': 'RETAINED OBSERVATION (not re-probed)', 'basis': 'The same-scope re-encoding is a source40->42 identity change; source43 changes no execution-inputs byte, so no further re-encoding occurs.', 'evidence': ['mapSources', 'claude-independent-design.v42/receipts/probes/view-attribution-x.json (historical)']},
    {'id': 'OBS42-05', 'currentDisposition': 'RETAINED OBSERVATION', 'basis': 'enumeration_model.v1.py byte-identical 42->43 (%s); the explicit js-synthesized refusal stands; enumeration cases equal modulo paths.' % U['enumeration_model.v1.py'], 'evidence': ['receipts/reference-children-stripped.json', 'claude-independent-design.v42/receipts/probes/program-entry-x.json (historical)']},
    {'id': 'OBS42-06', 'currentDisposition': 'RETAINED OBSERVATION', 'basis': 'Enumeration bytes unchanged; unavailable-binding programEntry freedom stands, with no canonical encoding stated.', 'evidence': ['claude-independent-design.v42/receipts/probes/program-entry-x.json (historical)']},
    {'id': 'OBS42-07', 'currentDisposition': 'SUPERSEDED BY OBS43-04 (historical comparison not relabelled)', 'basis': 'The source42 reference comparison stays historical; the source43 comparison is OBS43-04.', 'evidence': ['receipts/reference-comparison.json']},
    {'id': 'OBS42-08', 'currentDisposition': 'RETAINED (OBS43-06)', 'basis': 'Ported probes re-observe every value on source43.', 'evidence': ['receipts/probes (ported43_*)']},
]
V42PRIOR = {d['id']: d for d in V42['source40FindingDispositions']}
for i, extra in (('OBS40-01', 'P43-PORTED-POLICY'), ('OBS40-02', 'P43-PORTED-POLICY'), ('OBS40-03', 'P43-PORTED-POLICY'), ('OBS40-04', 'P43-PORTED-NATIVE'), ('OBS40-05', 'P43-PORTED-NATIVE'),
                 ('OBS40-06', 'P43-PORTED-NATIVE'), ('OBS40-07', None), ('OBS40-08', None), ('OBS40-09', 'P43-PORTED-POLICY'), ('OBS40-10', None),
                 ('S39-01', 'P43-PORTED-POLICY'), ('S39-02', 'P43-PORTED-POLICY'), ('ADV39-01', 'P43-PORTED-RUNTERM'), ('ADV38-01', 'P43-PORTED-TERM7'), ('ADV38-02', 'P43-PORTED-CARRIER'), ('ADV38-03', None)):
    prior = V42PRIOR.get(i)
    if prior is None:
        GAPS.append('source42 prior disposition missing: ' + i)
        continue
    if extra:
        basis = 'Source42 disposition %s. On source43 the owning probe %s re-observes every row identically (%d rows).' % (prior['currentDisposition'], extra, PORTED_EQUAL[extra]['rows'])
    elif i == 'OBS40-07':
        basis = 'Source42 disposition CLOSED. The removed no-op continue stays removed (execution_inputs_model.v1.py byte-identical 42->43: %s).' % U['execution_inputs_model.v1.py']
    elif i == 'OBS40-08':
        basis = 'Source42 disposition SUPERSEDED. The historical comparisons stay historical; the source43 comparison is OBS43-04.'
    elif i == 'OBS40-10':
        basis = 'Source42 disposition HISTORICAL CORRECTION STANDS. The mapping population is 322 on source42 and source43 with 0 rows changed (measured).'
    else:
        basis = 'Source42 disposition %s. commit-recovery-readonly.v3.md is byte-identical 42->43 (%s).' % (prior['currentDisposition'], U['commit-recovery-readonly.v3.md'])
    PRIOR_DISPOSITIONS.append({'id': i, 'source42Disposition': prior['currentDisposition'], 'currentDisposition': prior['currentDisposition'] + ' (unchanged on source43)', 'basis': basis,
                               'evidence': ['receipts/probes/' + PBY[extra]['result']['receipt'].split('/')[-1]] if extra else ['mapSources', 'receipts/planning-checks.json']})
covered = {d['id'] for d in PRIOR_DISPOSITIONS}
for x in V42['newMustIssues'] + V42['newShouldIssues'] + V42['advisories'] + V42['observations'] + V42['source40FindingDispositions']:
    if x['id'] not in covered:
        GAPS.append('prior finding/advisory/observation without current disposition: ' + x['id'])

# ------------------------------------------------------------------------------------------------ items
AV = {op: qx('availability-%s: omitted and retained report retained' % op) for op in ('neighbors', 'path', 'reach')}
AV_SAME = {op: qx('availability-%s: identical semantic items' % op) for op in ('neighbors', 'path', 'reach')}
PARITY = qx('surface parity')
AD = {k: qa(k) for k in ('retained record:', 'record-partial:', 'record-partial-with-missing-ref:', 'record-purged', 'record-expired', 'record-corrupt:', 'record-unavailable',
                         'record-unparseable', 'record-unknown-state', 'record-other-run', 'record-missing-reason', 'record-partial-corrupt-bytes', 'record-partial-missing-bytes',
                         'record-retained-missing-bytes', 'adapter-invalid-null', 'adapter-invalid-unknown', 'a RequestId precondition')}
ITEMS = [
    {'id': 'CH43-AVAILABILITY-REPORTING', 'disposition': 'SUFFICIENT AND CONSISTENT; CORRECTS A SOURCE42 UNDER-DISCLOSURE',
     'assessment': ('Identity-and-evidence (:1715-1725) makes current availability a separate monotonic-generation record (retained, partial, expired, purged, corrupt, unavailable) and says a query reports both it and sealed assurance. '
                    'Its section 5 selector (:1753-1767) hands graph availability to query contract section 7. GraphOperationResponseContext requires availability over exactly that enum. '
                    'Workflows-and-surfaces (:1190, :1228-1229) makes availability a required query parity field projected from /queryResponse/context/availability, and query_surface_projection.v3.py (:47-53, :187-194, unchanged) copies ctx["availability"] verbatim. '
                    'Source42 passed the literal "retained" to finish_operation, so an admitted partial observation was reported as retained: the response under-disclosed current availability, contrary to "a query reports both". '
                    'Source43 section 7 (:162) requires reporting an observed retained or partial state exactly and never upgrading partial; the model returns the observed state. '
                    'Independently discriminated on one lawful closed Run with each tree\'s own modules. For neighbors, path and reach, omitted and retained report retained on both trees, and partial reports retained on source42 and partial on source43. '
                    'Items, termination and every other context field are identical across trees and observations. Omitted/retained responses are byte-identical across trees. '
                    'The trusted-latest join and a cursor continuation under partial also disclose partial on source43. '
                    'Through the reference adapter path, an admitted retained record with state partial reaches the response as partial on source43 (retained on source42); failing records are evidence.corrupt before any query. '
                    'Parity: the graph-query-response parity field is partial on source43, and human/json/agent renderings recover it with parity holding. '
                    'Omitted-observation behaviour is OBS43-01. The non-graph operations are unchanged (section 7: "It does not change the other seventeen operations").'),
     'evidence': {'perOperation': AV, 'semanticIdentity': AV_SAME, 'latestJoin': qx('route-latest-ok-partial'), 'cursorUnderPartial': qx('cursor continuation with a partial'),
                  'parity': PARITY, 'adapterRecords': {k: AD[k] for k in ('retained record:', 'record-partial:', 'record-partial-with-missing-ref:')}}},
    {'id': 'CH43-OBSERVATION-GRANTS-NOTHING', 'disposition': 'CONFIRMED (every refusal and precondition path)',
     'assessment': ('The observation is consumed before close_run (model :1563) but only refuses or selects the reported state. close_run remains the positive admission (:1583), and view join, selection, projection and traversal follow unchanged. '
                    'Measured identically on both trees: purged, expired, corrupt, unavailable and missing refuse HOST.IO_FAILURE with evidence.purged, expired, corrupt, missing and missing, operational-failed, exit 4, no run. A refusing observation routes before replay, even with missing bytes (evidence.purged). '
                    'Null, unknown and non-string values raise ReferenceCallPrecondition host.availability. Corrupt and missing retained bytes refuse evidence.corrupt and evidence.missing under omitted, retained and partial observations, and through the record path a partial record with corrupt or missing bytes and a retained record with missing bytes refuse the same way.'
                    'With a partial observation present, every public refusal keeps its route: schema major, malformed, project mismatch, relation, runId mismatch, missing latest, ambiguous snapshot, unavailable view, unknown endpoint and no retained Run. '
                    'Adapter law: an out-of-vocabulary observation projects SYSTEM.OUTCOME.ILLEGAL_STATE / HOST.INVARIANT_VIOLATED / host-invariant / exit 4 with subject host.availability, no run and no runId. Without a RequestId it stays a precondition, and a RequestId precondition is never projected. '
                    'Failing retained records (unparseable, unknown state, other Run, missing reason) are evidence.corrupt. No new public code is involved.'),
     'evidence': {'refusingStates': {s: qx('avail-refuse-' + s) for s in ('purged', 'expired', 'corrupt', 'unavailable', 'missing')},
                  'preconditions': {s: qx('avail-precondition-' + s) for s in ('null', 'unknown', 'number')},
                  'bytes': {k: qx(k) for k in ('bytes-corrupt-omitted', 'bytes-corrupt-retained', 'bytes-corrupt-partial', 'bytes-missing-omitted', 'bytes-missing-retained', 'bytes-missing-partial', 'bytes-missing-purged')},
                  'routesWithPartial': {k: qx(k) for k in ('route-major2-partial', 'route-malformed-partial', 'route-project-mismatch-partial', 'route-relation-unsupported-partial', 'route-runid-mismatch-partial',
                                                          'route-latest-missing-partial', 'route-snapshot-ambiguous-partial', 'route-view-unavailable-partial', 'route-endpoint-unknown-partial', 'route-purged-before-view-join', 'route-no-retained-run-partial')},
                  'adapter': {k: AD[k] for k in AD if not k.startswith(('retained record:', 'record-partial:', 'record-partial-with-missing-ref:'))}}},
    {'id': 'CH43-PATH-EDGE-ORIENTATION', 'disposition': 'REPRESENTATION SELECTED FOR A PREVIOUSLY UNSPECIFIED FIELD; MODEL BEHAVIOUR PRESERVED; CONSISTENT',
     'assessment': ('Source42 specified GraphPathEdge {factId, source, target} without an orientation (schema :817-836; GraphPathRow :847 fixes only zero-hop and the canonical fact2-id-sequence tie-break). Either reading of source/target was therefore open, and the earlier stored-orientation reading was not a defect under that law. '
                    'Section 4 (:100) now selects the walk representation: edges[i] is the hop nodes[i]->nodes[i+1] under outgoing, incoming and both; factId still names the stored fact; neighbors rows keep the projected fact\'s source->target. '
                    'path_unit already emitted traversal-oriented hops, and every orientation response is byte-identical across trees. On the real Run, the incoming and both paths bar->foo emit one hop bar->foo, the reverse of the stored fact, with the stored factId, while incoming neighbors of bar keep source foo/target bar. '
                    'Incoming from the fact source finds no path. Zero-hop has nodes [start], edges [] and hopCount 0. '
                    'Goldens: both s->t yields the shortest two-hop path with the lex-least fact2 sequence (1,3) and hops against both stored facts; incoming t->s yields (4,2) with hops t->y, y->s; outgoing uses stored directions (2,4); depth 1 finds no path; all goldens are identical across trees. '
                    'hopCount equals len(edges) and nodes has hopCount+1 members within schema bounds (nodes 1-65, edges <=64). Order (:86) and bounds (section 5) are unchanged. '
                    'No other owner consumes path edge orientation: identity :1754 and workflows :1151 hand graph law to the query contract, and the historical non-evaluator3 schema only names the operation (search output). Consequence: OBS43-03.'),
     'evidence': {k: qx(k) for k in ('real-Run path under incoming and both', 'real-Run neighbors under incoming', 'real-Run incoming path from the fact source', 'golden both s->t', 'golden incoming t->s',
                                     'golden outgoing s->t', 'goldens identical', 'orient-path-incoming-bar-foo', 'orient-path-both-bar-foo', 'orient-neighbors-both-bar', 'orient-reach-incoming-bar')}},
    {'id': 'CH43-CURSOR-BOUNDS-AND-PROSE', 'disposition': 'CONSISTENT; OPAQUE TOKEN FREEDOM RESPECTED',
     'assessment': ('Section 5 (:138) and schema Page.cursor (:274-278) make the cursor an opaque host token of at most 256 characters, with a reference form, that grants no authority. This review claims no cross-host portability and requires no new canonical preimage; it checks only the same-host laws. '
                    'Measured identically on both trees on the lawful Run: a two-row reach page issues the same token, and continuation returns the same second page. Cache loss ({}) and cache poison change nothing. '
                    'Re-resolving latest, another runId, changed params, a position past the produced prefix and a malformed token each refuse QUERY.CURSOR_MISMATCH (request-rejected, exit 2). Historical selection by runId is the only continuation view. '
                    'Bound admission: testBounds above a public cap refuses QUERY.PARAMS_MALFORMED, and a lowered visited cap under best-effort truncates with truncated-bound and lower-bound disclosure, identically. '
                    'Prose law (source43 probe): a limitation note is any BoundedText (<=1024). Rewording it keeps GraphQueryResponseV1 admission and renderer parity, the note travels verbatim inside query-response parity, and an over-long note is refused. '
                    'A success StepTermination admits no errorCode/reasonCodes/signal/faultCause. Refusal diagnostic prose is private: envelopes are identical for different diagnostics. Remedy wording changes only domainDetail.remedy, never class, errorCode, faultCause, detail or exit. '
                    'Section 7 (:158) keeps refusal messages diagnostic while the table selects every route. No canonical wording is required or invented.'),
     'evidence': {'cursor': {k: qx(k) for k in ('cursor issued', 'cursor continuation (same host)', 'cursor-latest-reresolve', 'cursor-other-run', 'cursor-params-changed', 'cursor-position-past-prefix', 'cursor-malformed')},
                  'bounds': {k: qx(k) for k in ('bound-raise-refused', 'bound-lower-admitted')}, 'prose': {r['case']: r['observed'] for r in QPR.values()}}},
    {'id': 'CH43-NO-NEW-PUBLIC-SURFACE', 'disposition': 'CONFIRMED',
     'assessment': ('The 42->43 delta is exactly nine files: the query contract, model and checker, the five source-pin ledgers and the workflows report. No schema, public-detail registry, identity, native, command inventory, surface projection or envelope byte changed (%s). '
                    'No new public identity, error code or schema major exists: graph-query:3 is unchanged, and the adapter and refusal routes reuse existing codes. The same lawful Run closes to the same RunId on both trees, and package export stores are byte-equal to package19, so byte-derived identities are unchanged and nothing was reminted.')
     % json.dumps({os.path.basename(p): MAP[p]['unchanged42to43'] for p in MAP_FILES if p.endswith(('.schema.json', 'public-detail-registry.v1.json', 'identity-model.v3.py', 'identity-schemas.v3.json', 'native-evidence.schemas.v2.json', 'command-inventory.v3.json', 'query_surface_projection.v3.py'))}),
     'evidence': {'deltaPaths': sorted(paths42to43), 'sameRun': qx('same lawful closed Run on both trees')}},
    {'id': 'CH43-PINS-AND-REPORT', 'disposition': 'CONFIRMED',
     'assessment': ('Every entry of the five ledgers matches the formal manifest (foundation %d, evaluator3 %d, native %d, security %d, workflows %d; none added or removed). The four sibling ledgers repin exactly the three query owner files. The evaluator3 ledger additionally repins the four sibling ledgers. '
                    'The workflows report updates only the checker, model and workflows source-pins digests. The evaluator3 pins sha equals the root and codex currentProfilePinsSha256 (%s).')
     % tuple([PINS['ledgers'][l]['entries'] for l in ('docs/coop/design-corrections/foundation/source-pins.v1.json', 'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json',
                                                     'docs/coop/design-corrections/native/source-pins.v2.json', 'docs/coop/design-corrections/security/source-pins.v1.json',
                                                     'docs/coop/design-corrections/workflows/source-pins.v1.json')] + [CODEXD.get('currentProfilePinsSha256') == PINS['ledgers']['docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json']['ledgerSha256']]),
     'evidence': {'changedPinUnion': PINS['changedPinUnion']}},
    {'id': 'CH43-PLANNING-V11', 'disposition': 'CONFIRMED (population measured; layer retained, not relabelled)',
     'assessment': ('v11 (%s...) binds %d inputs with no mismatch; none of them and none of the %d coverage sources is among the nine changed files. Layers v8-v11 and all %d docs/v2/architecture files are byte-identical to source42, so no layer12 is required and none is claimed. '
                    'The planning checker reports 322 source-bound mappings and 54 planned failure cases (stdout sha equals the root verification: %s); the inventory checker reports 198 unique paths in 20 packages. There are 0 mapping rows changed versus source42, 24 report features, M0-M6, and 54 recovery cases, none executed.')
     % (PC['layerSha256']['11'][:12], PC['layerInputs']['11'], PC['coverageSourceKeys'], PC['architectureDirFileCount'], planning_stdout_equal_root),
     'evidence': {k: PC[k] for k in ('layerSha256', 'layerInputs', 'layersByteEqualToSource42', 'v11InputsIntersectingThe9ChangedFiles', 'coverageSourcesIntersectingThe9ChangedFiles', 'coverageMappings',
                                     'coverageMappingsSource42', 'coverageRowsChangedVs42', 'coverageGroups', 'inventoryPaths', 'inventoryPackages', 'recoveryCases', 'recoveryCasesNotExecuted', 'milestoneOrder')}},
    {'id': 'CH43-PACKAGE20', 'disposition': 'VERIFIED AS AUTHOR EVIDENCE', 'assessment': 'See packageAssessment.', 'evidence': {k: v['ok'] for k, v in PK.items()}},
    {'id': 'CH43-CURRENT-REFERENCE', 'disposition': 'OWN EXECUTION PASSES; ROOT RECEIPTS CONSISTENT',
     'assessment': ('This review\'s six groups and 17 children pass on its own verified copy, which is unchanged before and after every group. Query-projection runs 209 checks with 0 failed, execution-inputs 95 cases and enumeration 54. '
                    'The comparison with root and codex is OBS43-04 and OBS43-05. The historical source42 receipts of this origin are preserved and not relabelled.'),
     'evidence': {k: RC[k] for k in ('codexReferenceChecks', 'codexPassed', 'codexSubjectManifestSha256', 'rootPassed', 'childrenEqualRoot', 'childrenDifferingFromHistoricalMine42')}},
]

# ------------------------------------------------------------------------------------------------ scope basis (source42 scope retained)
UNCH42 = ['CH42-ATTRIBUTION-LAW', 'CH42-CAPTURE', 'CH42-HISTORICAL-POPULATIONS', 'CH42-PROGRAM-ENTRY-CLARIFICATION', 'CH42-PROGRAM-ENTRY-ENFORCEMENT', 'CH42-IDENTITY-DIGEST-SCOPE', 'CH42-COMPOSITION7-AND-POLICY-DERIVATION3']
ch = lambda n: {'stdoutEqualRoot': RC['children'][n + '.stdout']['equalRoot'], 'stdoutEqualHistoricalMine42': RC['children'][n + '.stdout']['equalHistoricalMine42']}
SCOPE_BASIS = [
    {'scope': 'five product contracts and incorporated schemas', 'basis': 'unchanged-42-basis + current execution',
     'current43': 'identity, security, native, workflows and admission contracts and the README index byte-identical (%s); the incorporated query contract changed and was fully read; all six groups pass' % json.dumps({k: U[k] for k in ('identity-and-evidence.md', 'security-and-lifecycle.md', 'native-evidence.md', 'workflows-and-surfaces.md', 'admission-and-qualification.md', 'README.md')}),
     'unchanged42': 'source42 AR-01..AR-16 row assessments and inheritedUnchanged42Read whole-file reads'},
    {'scope': 'architecture, tool, layout and report decisions', 'basis': 'unchanged-42-basis + current execution', 'current43': 'all %d docs/v2/architecture files byte-identical; planning and inventory checks pass' % PC['architectureDirFileCount'], 'unchanged42': 'CH42-PLANNING-V11'},
    {'scope': '198 files in 20 packages; 322 mappings; M0-M6; 24 report features; 54 recovery cases', 'basis': 'current execution', 'current43': 'measured: %d paths, %d packages, %d mappings (0 changed), %s, %d report features, %d recovery cases not executed' % (PC['inventoryPaths'], PC['inventoryPackages'], PC['coverageMappings'], '-'.join([PC['milestoneOrder'][0], PC['milestoneOrder'][-1]]), PC['coverageGroups']['reportFeatures'], PC['recoveryCasesNotExecuted']), 'unchanged42': None},
    {'scope': 'native discovery, config, unitKind, allowJs, nested Cargo, clone normalization, custody', 'basis': 'unchanged-42-basis + current execution',
     'current43': 'native group stdout equal root and own source42; native-consumer24-corrections and native-replay children %s / %s; ported native (%d rows) and custody (%d rows) identical to source42; nine native-v2 membership probes content-equal to root' % (ch('native-consumer24-corrections'), ch('native-replay'), PORTED_EQUAL['P43-PORTED-NATIVE']['rows'], PORTED_EQUAL['P43-PORTED-CUSTODY']['rows']),
     'unchanged42': 'native bytes unchanged (native_evidence_model.v2.py %s); source42 AR-07/AR-13 and OBS42-02' % U['native_evidence_model.v2.py']},
    {'scope': 'enumeration default-vs-explicit binding, attribution and capture', 'basis': 'unchanged-42-basis + current execution',
     'current43': 'enumeration (54) and execution-inputs (95) children equal to root and own source42 after removing path fields only; capture-join measurement identical; package binding-controls content-equal to root',
     'unchanged42': 'CH42-ATTRIBUTION-LAW, CH42-CAPTURE, CH42-PROGRAM-ENTRY-CLARIFICATION, CH42-PROGRAM-ENTRY-ENFORCEMENT, CH42-HISTORICAL-POPULATIONS on byte-identical owners; the source42 three-tree view-attribution and program-entry probes were not re-run'},
    {'scope': 'policy.test known-hit, universe and import', 'basis': 'unchanged-42-basis + current execution', 'current43': 'ported policy probe %d rows identical; policy-derivation child %s' % (PORTED_EQUAL['P43-PORTED-POLICY']['rows'], ch('policy-derivation')), 'unchanged42': 'policy_test_model.v3.py unchanged (%s); S39-01/S39-02 closed' % U['policy_test_model.v3.py']},
    {'scope': 'comparison counterfactuals, knowledge and identities', 'basis': 'unchanged-42-basis + current execution', 'current43': 'ported comparison probe %d rows identical; comparison-knowledge child %s' % (PORTED_EQUAL['P43-PORTED-COMPARISON']['rows'], ch('comparison-knowledge')), 'unchanged42': 'source42 AR-10/AR-11'},
    {'scope': 'nine command carriers and twenty operations', 'basis': 'current execution', 'current43': 'ported query carriers %d rows identical; query-projection checker twenty-operation-names passes; command-inventory unchanged (%s)' % (PORTED_EQUAL['P43-PORTED-QUERY']['rows'], U['command-inventory.v3.json']), 'unchanged42': None},
    {'scope': 'repair2', 'basis': 'unchanged-42-basis + current execution', 'current43': 'ported repair:2 probe %d rows identical' % PORTED_EQUAL['P43-PORTED-REPAIR2']['rows'], 'unchanged42': 'repair_closed_world_selection.v1.py unchanged (%s)' % U['repair_closed_world_selection.v1.py']},
    {'scope': 'security, discovery, commit, recovery and read-only carrier boundaries', 'basis': 'unchanged-42-basis + current execution',
     'current43': 'security group stdout equal root and own source42; ported read-only carrier %d rows and run-termination/commit-inventory %d rows identical' % (PORTED_EQUAL['P43-PORTED-CARRIER']['rows'], PORTED_EQUAL['P43-PORTED-RUNTERM']['rows']),
     'unchanged42': 'carrier-dispatch.v3.json (%s) and commit-recovery-readonly.v3.md (%s) unchanged; ADV38-02/ADV38-03' % (U['carrier-dispatch.v3.json'], U['commit-recovery-readonly.v3.md'])},
    {'scope': 'evaluator, import and termination bridges', 'basis': 'unchanged-42-basis + current execution',
     'current43': 'children full-replay %s, execution-replay %s, candidate-replay %s, composition %s, analysis-seal %s, provider-attribution-return %s, faults %s, atoms %s; ported section 7 termination %d rows identical; query checker imports@resolved-target controls pass inside the 209 checks'
                  % (ch('full-replay'), ch('execution-replay'), ch('candidate-replay'), ch('composition'), ch('analysis-seal'), ch('provider-attribution-return'), ch('faults'), ch('atoms'), PORTED_EQUAL['P43-PORTED-TERM7']['rows']),
     'unchanged42': 'CH42-COMPOSITION7-AND-POLICY-DERIVATION3 and CH42-IDENTITY-DIGEST-SCOPE on byte-identical owners (composition %s, replay %s, identity model %s)' % (U['evaluator-composition-contract.v3.md'], U['evaluator_replay_model.v3.py'], U['identity-model.v3.py'])},
]
UNCHANGED42_ITEMS = [{'id': i, 'source42Disposition': V42ITEMS[i]['disposition'], 'standsOnSource43': True, 'note': 'Owner bytes named by the source42 item are byte-identical 42->43; the conclusion is this origin\'s source42 assessment, not a new read.'} for i in UNCH42]
for i in UNCH42:
    if i not in V42ITEMS:
        GAPS.append('source42 item not found: ' + i)
ITEMS.append({'id': 'CH43-SCOPE-PRESERVATION', 'disposition': 'SOURCE42 SCOPE RETAINED; NAMED BASIS',
              'assessment': 'Each retained scope names its current source43 execution and, where applicable, its individually named unchanged-42 basis. Passing suites are corroboration, not assessment. Query changes reach the read-only response, availability and parity owners, which are assessed in CH43-AVAILABILITY-REPORTING although their bytes are unchanged.',
              'scopeBasis': SCOPE_BASIS, 'unchanged42Items': UNCHANGED42_ITEMS, 'portedProbes': PORTED_EQUAL})
