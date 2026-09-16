"""Normative prose corrections (no Python is made law). Exact-once edits."""
import json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1/tools')
from textedit import apply  # noqa: E402

WS = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
WPC = 'docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md'
QPC = 'docs/coop/design-corrections/workflows/query-projection-contract.v3.md'
ECC = 'docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md'
SEC = 'docs/v2/contracts/product-v1/security-and-lifecycle.md'
NAT = 'docs/v2/contracts/product-v1/native-evidence.md'
rows = []

rows.append(apply('prose workflows-and-surfaces', WS, [
    ('Major-1 consumers are refused with `REQUEST.SCHEMA_MAJOR_UNSUPPORTED`, never reshaped. |',
     'Major-1 consumers are refused with `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` and detail `OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED`, never reshaped. |'),
    ('''policy/scope/waiver documents whose digests equal those context digests, rule
coverage, sorted unique matched entries and explicit unmatched occurrences.''',
     '''policy/scope/waiver documents whose digests equal those context digests, rule
coverage (including each rule's recorded absence knowledge, §3), sorted unique matched entries and explicit unmatched occurrences.'''),
    ('''`closureBundle` reference.

**Fresh CI.**''', '''`closureBundle` reference.

**Detector identity.** A detector is identified by its evaluator emission contribution.
`detectorClosure` has exactly one row per distinct `contributionId` of the origin Plan's
`EvaluatorEmissionPlanV1` rule rows, disabled rules included: `detectorId` equals that
`contributionId`, and `closureId` and `semanticsMajor` are that row's `detectorClosure` and
`semanticsMajor`, which equal the policy rule's `ruleProgramRef` major. Two rows for one
contribution with a different closure or major refuse (`CONFIG.INVALID` /
`EVALUATION.FINDING_JOIN_REFUSED`). `BaselineEntry.detectorId` is the `contributionId` of the
entry rule's emission binding and is a member of `detectorClosure`; comparison `detectorId`
values use the same identity. Baseline admission checks these joins after recomputing
`baselineId`, so a self-consistently reminted rename of a detector identity is refused rather
than accepted as a different baseline.

**Fresh CI.**'''),
    ('''no compatible peers; a present invalid, non-file or unavailable listing refuses
and cannot silently become absence.''', '''no compatible peers; a present invalid, non-file or unavailable listing refuses
(`REQUEST.PRECONDITION_FAILED` / `EVALUATION.PROJECTION_INPUT_INCOMPLETE`; the refusal
message is diagnostic only) and cannot silently become absence.'''),
    ('''not establish a negative result. Known hits remain usable in a partial result.

''', '''not establish a negative result. Known hits remain usable in a partial result.

**One presence-knowledge law on every side.** B, E0–E3 and E4 are each `true` (a known
matched occurrence), `false` (absence proved under the law above for that side's rule,
including the attested path extent) or `null` (not known). The absence of a matched current
hit is not by itself a known `false`: incomplete or unknown enumeration, unknown roots,
disabled evaluation and an exhausted budget leave E4 `null`. B is `false` for a non-entry only
when the baseline's `RuleCoverage.absenceKnowledge` for that rule is `complete-hit-set`,
recorded at adoption by the same law; the baseline artifact records per-rule knowledge, not a
per-path extent. An entry whose first attributable change along B→E4 would rest on a `null`
value is `INDETERMINATE` with `current-absence-unknown` (unknown E4) or
`baseline-absence-unknown` (unknown B), never `CODE-FIXED`, `UNCHANGED` or `CODE-NET-NEW` by
default. A change already established between known values before the unknown value keeps its
classification, so a known `CODE-NET-NEW` still fails. Rule coverage, evidence and execution
deficiencies remain independent of this knowledge.

'''),
    ('''A `CODE-NET-NEW` entry that is not live in current (hidden by a later policy/scope
change or by a waiver added in the same change) still gates under
`baseline-or-current` with `gateReason=code-net-new-policy-hidden`.''', '''A `CODE-NET-NEW` entry that is not live in current (hidden by a later detector, policy or scope
change, or by a waiver added in the same change; `subsequentDeltas` names the later axes) still gates under
`baseline-or-current` with `gateReason=code-net-new-policy-hidden`; that existing reason covers every
later hiding axis.'''),
    ('''the live tree still equals the `afterStep` snapshot. There is no shell string and no
interpolation anywhere in the schema.
''', '''the live tree still equals the `afterStep` snapshot. There is no shell string and no
interpolation anywhere in the schema.

**Argv digest.** `argvDigest` is the lowercase hexadecimal raw SHA-256 of `C(argv)`, where
`C` is product canonical JSON (identity-and-evidence §3) and `argv` is the exact ordered array
of argument strings actually selected for the spawn. Every element stays a separate array
member, preserving order, repeated elements and any empty string an owning schema admits; no
shell-joined, quoted, normalized or PATH-resolved surrogate is digested. The recipe is the same
wherever the digest binds, `RepoExecutionGrantV2.argvDigest` (security S10) and
`TestPayloadV1.argvDigest`: host test execution digests `TestExecutionStepParams.argv`, native
preparation digests the host-selected preparation argv of its grant, and an independently
prepared test payload digests the argument array its adapter recorded.
'''),
    ('''The step **discloses** and does not confine: `effects.network/subprocess/
filesystemWrite` are `DISCLOSURE-ONLY` unless the security unit's platform truth
table measures a primitive; a claimed enforcement without a measured primitive is
refused (`TEST.CONFINEMENT_CLAIM_REFUSED`).''', '''The step **discloses** and does not confine: `effects.network/subprocess/
filesystemWrite` are `DISCLOSURE-ONLY` unless the security unit's platform truth
table measures a primitive; a claimed enforcement without a measured primitive is
refused (`TEST.CONFINEMENT_CLAIM_REFUSED`). Every effect value must equal the selected
truth-table profile row (security S10). The selected `permission-truth-tables.v9` profile has
no measured platform-primitive row, so `ENFORCED-PLATFORM:<primitiveId>` cannot be claimed in
this profile and is not a member of `TestExecutionStepParams` `EnforcementValue`; security
`EnforcementV1` keeps that vocabulary for a future measured primitive, which requires a
successor truth-table profile and test-execution schema.'''),
    ('''committed, the termination retains its RunId and the after-commit detail below;
otherwise no RunId is invented.''', '''committed, the termination retains its RunId and the after-commit detail below;
otherwise no RunId is invented and the detail is `DELIVERY.REQUIRED_PROJECTION_FAILED`. The
termination schema enforces both directions: the after-commit detail requires a `runId`, the
no-Run detail forbids one.'''),
    ('''termination. The envelope and response must identify the same project. Missing
required query disclosure follows the existing required-delivery fault law.
''', '''termination. The envelope and response must identify the same project. Missing
required query disclosure follows the existing required-delivery fault law.

**Public query carrier.** Every `kind=query` envelope names `querySurface`. The query command,
whose inventory parity fields include `query-response`, selects `graph-query-response` and
carries that complete owner-admitted response in `CommandEnvelope.queryResponse`: the JSON
rendering is that envelope, the agent rendering is the same envelope plus `agentHints`, and
the human rendering prints every parity field; parity recovered from each rendering is
identical. `queryResponse` is required for that selector and forbidden for every other
selector and envelope kind, so a query-command envelope cannot omit it silently and no private
wrapper carries it. Every other query-class command (`recommend`, `baseline show`,
`policy show`, `policy test`, `candidates`, `inspect`, `review brief`, `repair preview`)
selects `command-owned-summary`; its compact `QueryResult` and parity fields keep their owners.
A query never commits a Run, so a query rendering that cannot deliver the carrier is
`DELIVERY.REQUIRED_FAILED` with `DELIVERY.REQUIRED_PROJECTION_FAILED` and no `runId`.
'''),
    ('Only an unproducible report is `HOST.IO_FAILURE` (4).',
     'Only an unproducible report is `HOST.IO_FAILURE` (4), with detail `DOCTOR.REPORT_NOT_PRODUCIBLE`.'),
    ('''detail so the two surfaces never disagree. Before a Plan or Run exists no run
envelope is fabricated.''', '''detail so the two surfaces never disagree. Before a Plan or Run exists no run
envelope is fabricated. A failure golden (request-rejected or operational-failed) carries its
actual `domainDetail`; only a golden whose `detailSuppliedBy` names that composition may omit
it. An unsupported envelope major is `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` with
`OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED`; an empty latest resolver is `IDENTITY.UNKNOWN` with the
query owner's `QUERY.VIEW_UNKNOWN`.'''),
    ('''| selected renderer fails after commit | operational-failed 4 | `DELIVERY.REQUIRED_FAILED` | `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`; runId retained |
''', '''| selected renderer fails after commit | operational-failed 4 | `DELIVERY.REQUIRED_FAILED` | `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`; runId retained |
| required projection or renderer fails with no committed Run | operational-failed 4 | `DELIVERY.REQUIRED_FAILED` | `DELIVERY.REQUIRED_PROJECTION_FAILED`; no runId |
'''),
    ('''| doctor report with defects | success 0 | — | `DOCTOR.DEFECTS_FOUND`; inspect typed outcome |
''', '''| doctor report with defects | success 0 | — | `DOCTOR.DEFECTS_FOUND`; inspect typed outcome |
| doctor report not producible | operational-failed 4 | `HOST.IO_FAILURE` | `DOCTOR.REPORT_NOT_PRODUCIBLE` |
| latest resolver on an empty domain | request-rejected 2 | `IDENTITY.UNKNOWN` | `QUERY.VIEW_UNKNOWN` |
| envelope major other than 3 requested | request-rejected 2 | `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` | `OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED` |
'''),
]))

rows.append(apply('prose workflow-projection-contract', WPC, [
    ('- `emissionBindings` keyed by ruleId (contributionId, ruleStableId, semanticsMajor, detectorClosure, stabilityClass, emissionProfile)',
     '- `emissionBindings` keyed by ruleId (contributionId, ruleStableId, semanticsMajor, detectorClosure, stabilityClass, emissionProfile); every `detectorId` in this projection is the binding `contributionId`'),
    ('`verify_baseline_artifact_v3` enforces schemaMajor 2, H(baselineId), context-document digest bindings, `side=baseline` unmatched, and `run3|closure2` retention pins.',
     '`verify_baseline_artifact_v3` enforces schemaMajor 2, H(baselineId), context-document digest bindings, `side=baseline` unmatched, `run3|closure2` retention pins, and the detector identity joins of workflows-and-surfaces §2 (one `detectorClosure` row per embedded policy rule contribution with `detectorId = contributionId` and the rule `semanticsMajor`; every entry `detectorId` equal to its rule contribution), refusing `CONFIG.INVALID` / `EVALUATION.FINDING_JOIN_REFUSED` also for a self-consistently reminted rename.'),
    ('- E0 detector join is the exact baseline selected `{detectorId → (closureId, semanticsMajor)}` map, not a subset of common IDs. Extra, missing, or major-disagreeing detectors refuse.',
     '- E0 detector join is the exact baseline selected `{detectorId → (closureId, semanticsMajor)}` map, not a subset of common IDs. Extra, missing, or major-disagreeing detectors refuse. `detectorId` is the emission `contributionId`.'),
    ('''Unrelated unknown must not erase a known CODE-NET-NEW fail.
''', '''Unrelated unknown must not erase a known CODE-NET-NEW fail.
- Current E4 and baseline B use that same law (workflows-and-surfaces §3). E4 is `true` for a matched current occurrence, `false` only when the current rule proves absence under the pivot predicate including the attested path extent, else `null`. B is `false` for a non-entry only when the baseline RuleCoverage records `absenceKnowledge=complete-hit-set` (recorded at adoption by the same predicate), else `null`. An entry whose first attributable change rests on `null` is `INDETERMINATE` (`current-absence-unknown` / `baseline-absence-unknown`); an earlier known change keeps its classification. A `compare_v3` projection without admitted root predicate proofs and an absence extent has no absence knowledge; caller presence maps remain refused.
'''),
    ('Present malformed / unrecognized / missing / hash-or-length mismatch refuses (never silent no-declaration).',
     'Present malformed / unrecognized / missing / hash-or-length mismatch refuses `REQUEST.PRECONDITION_FAILED` / `EVALUATION.PROJECTION_INPUT_INCOMPLETE` (never silent no-declaration).'),
]))

rows.append(apply('prose query-projection-contract', QPC, [
    ('The public failure carrier is CommandEnvelope major 3, `kind=failure`, nonempty `errors` of registered DomainDetail, and **no** `run` field.',
     'The public failure carrier is CommandEnvelope major 3, `kind=failure`, nonempty `errors` of registered DomainDetail, and **no** `run` field. The public success carrier is CommandEnvelope major 3 `kind=query` with `querySurface=graph-query-response` and the complete response in `queryResponse` (workflows-and-surfaces §8). Refusal messages are diagnostic; the table below selects every public route.'),
    ('''| unsupported relation or non-projectable request rung |''', '''| request `projectId` differs from the admitted Run's project | request-rejected | `REQUEST.PRECONDITION_FAILED` | `QUERY.PARAMS_MALFORMED` |
| unsupported relation or non-projectable request rung |'''),
]))

rows.append(apply('prose evaluator-composition-contract', ECC, [
    ('Identical projected signatures among distinct native IDs, empty/missing projection, anonymous unavailable name, or incomplete collision-class population cannot establish stable correspondence.',
     'Identical projected signatures among distinct native IDs, empty/missing projection, anonymous unavailable name, or incomplete collision-class population cannot establish stable correspondence. When several of these hold for one emitted subject, exactly one correspondence cause is published, the first applicable in this order: (1) `projection-unavailable`, the symbol has no projection for the binding `detectorClosure` or its `signatureTokens` are empty; (2) `population-incomplete`, its collision-class population is incomplete; (3) `signature-ambiguous`, the complete collision class holds another distinct subject3 with equal projected tokens. More than one projection for one detectorClosure is an admission refusal (`EVALUATOR_DUPLICATE_DETECTOR_PROJECTION`) before any cause. An anonymous subject is not a separate published cause: without a unique enclosing name or signature it has empty projected tokens or shares its projection, so one of the three causes keeps it unmatched (identity-and-evidence §3); registry member `anonymous-subject` remains closed membership and is not emitted. File and package subjects have no correspondence cause.'),
    ('Otherwise a gating rule is indeterminate if its population is incomplete/unresolved or its root truth is indeterminate with at least one blocking native or required imported cause.',
     'Otherwise a gating rule is indeterminate if its population is incomplete/unresolved, if it carries a required-import deficiency (§9.5 `evidence-kind-unavailable`: a `required` declared `evidenceUse` kind absent from the Plan-selected imports) whatever its root value, or if its root truth is indeterminate with at least one blocking native or required imported cause.'),
    ('No import pointer is required. Optional `evidenceUse` entries emit nothing here.',
     'No import pointer is required. Optional `evidenceUse` entries emit nothing here. The deficiency makes an enabled gating rule `indeterminate` independently of its root value unless a live unwaived finding makes it `fail` (§5); an advisory rule stays `pass`.'),
    ('Registry member `anonymous-subject` remains closed membership; the current correspondence algorithm classifies empty symbol tokens as `projection-unavailable`.',
     'Registry member `anonymous-subject` remains closed membership; the current correspondence algorithm classifies empty symbol tokens as `projection-unavailable`. Precedence is §4 first-applicable: each unmatched finding has exactly one correspondence deficiency, and its `correspondence.reason` (§9.7) is that deficiency `cause`; co-occurring conditions never add a second correspondence row.'),
    ('| `correspondence.reason` | null if matched; else the correspondence cause of §9.5 |',
     '| `correspondence.reason` | null if matched; else the single first-applicable correspondence cause of §4 / §9.5 |'),
]))

rows.append(apply('prose security-and-lifecycle', SEC, [
    ('projectId, snapshotId (`snapshot2:`) and argv digest equal the invocation\'s;',
     'projectId, snapshotId (`snapshot2:`) and argv digest (`argvDigest`: lowercase hex raw SHA-256 of `C` of the exact ordered argument array selected for the spawn, every element preserved, no shell-joined surrogate; workflows-and-surfaces §7) equal the invocation\'s;'),
]))

rows.append(apply('prose native-evidence', NAT, [
    ('the actual host-selected argv/runner, class, project,', 'the actual host-selected argv (`argvDigest` per security S10) and runner, class, project,'),
]))
print(json.dumps(rows, indent=1))
