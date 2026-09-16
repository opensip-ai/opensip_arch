"""Phase 10 -- design-gap identification.

Each finding states the exact selector, what was attempted, what the kit says, and why it is
or is not a gap. The distinction the charter demands is applied explicitly:

  ALGORITHM FREEDOM   the kit deliberately leaves a STRATEGY open while pinning the OBSERVABLE
                      (an identity recipe, an admission rule, a refusal code). A consumer can
                      reconstruct it without inventing anything. NOT a gap.
  MISSING CONTRACT    a value a consumer MUST produce has no published derivation, or two
                      published statements disagree, or the authority is circular, so the
                      consumer is forced to invent. A gap.

Severity:
  MUST    reconstruction of a required observable is impossible or contradictory
  SHOULD  reconstruction is possible, but two conforming consumers can disagree on an
          outcome the kit treats as normative
  advisory  accounting, wording or ergonomics; no outcome depends on it
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import envelopes as EV

OUT = '/tmp/opensip-design-corrections/consumer-b.v17/output'

MUST = []

SHOULD = [
    {
        'id': 'V16-S1',
        'severity': 'SHOULD',
        'class': 'ambiguous default',
        'title': ('the repair descriptor\'s closedWorld projection names "that same Run\'s '
                  'ClosedWorldV2" without saying which Coverage entry owns it when a Run '
                  'carries several that differ'),
        'selectors': [
            'docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json'
            '#/$defs/RepairPlanDescriptor/properties/closedWorld (description)',
            'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
            '#/$defs/CoverageResultV3 entry.closedWorld',
        ],
        'whatWasAttempted': (
            'reconstructing RepairPlanDescriptor.closedWorld as "the five-field PROJECTION of '
            'the evidence Run\'s native ClosedWorldV2 ... each taken unchanged from that same '
            'Run\'s ClosedWorldV2". ClosedWorldV2 is a member of EVERY CoverageResultV3 entry, '
            'so a Run with N Coverage entries holds N of them.'),
        'whatTheKitSays': (
            'the clause is written in the singular ("the evidence Run\'s native '
            'ClosedWorldV2") and pins the projection, the seven-member closure, the two '
            'dropped members and the authority direction. It does not publish a selection '
            'rule over several entries, nor a requirement that they agree.'),
        'whyItIsNotAlgorithmFreedom': (
            'the five projected values enter repairPlanId, and deadCodeRepairEligible gates '
            'every unsafe edit. Two conforming hosts that pick different Coverage entries '
            'mint DIFFERENT repairplan2 identities for the same plan, and one may gate an '
            'unsafe edit that the other admits. That is an outcome the kit treats as '
            'normative, not a strategy it left open.'),
        'measuredOnThisReconstruction': (
            'the TypeScript Run used as the evidence Run carries several Coverage entries '
            'whose ClosedWorldV2 records reduce to ONE distinct canonical value, so this '
            'origin could project unambiguously and did NOT have to choose. The ambiguity was '
            'found by measuring the count, and is reported rather than worked around: see '
            'vectors/repair-descriptor.json evidenceRun.closedWorldNote.'),
        'smallestFix': (
            'one sentence naming the owner -- for example "the ClosedWorldV2 of the Coverage '
            'entry of the relation@rung each EvidenceRequirement names, which must agree '
            'across the requirements of one plan or REPAIR.CLOSED_WORLD_AMBIGUOUS" -- or a '
            'requirement that a Run\'s ClosedWorldV2 records be equal.'),
        'notAMustBecause': (
            'every other input to the gate and to the identity is published, and a host with '
            'agreeing entries (the common case, and this origin\'s case) reconstructs it '
            'exactly. Reconstruction is possible; agreement between hosts is not guaranteed.'),
    },
    {
        'id': 'V16-S2',
        'severity': 'SHOULD',
        'class': 'ambiguous default',
        'title': ('GlobPattern publishes a whole-segment `**` and one example, which does '
                  'not decide whether a TRAILING `**` matches the files of that directory'),
        'selectors': [
            'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json'
            '#/$defs/GlobPattern ("literal characters plus \'*\', \'?\' and a whole-segment '
            '\'**\'. No brace, class or escape syntax.")',
            'docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md:217 '
            '("`**/*.ts` matches root `a.ts`")',
            'docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md:109 '
            '(the same sentence, for rule include/exclude)',
        ],
        'whatWasAttempted': (
            'admitting a RepairPlanDescriptor whose permittedEditScope is `src/**` against an '
            'edit to `src/legacy.js`, and selecting rule subjects with include globs.'),
        'whatTheKitSays': (
            'the alphabet is closed and ONE semantic fact is published: `**/*.ts` matches root '
            '`a.ts`, i.e. a LEADING `**/` may match ZERO segments. Nothing states what a '
            'TRAILING `**` matches.'),
        'mathematicalCorrectionToThisOriginsV16Rationale': (
            'the v16 write-up said "Under \'zero or more segments\' `src/**` matches `src/` '
            'only; under \'one or more\' it matches `src/legacy.js`". The first clause is '
            'WRONG as stated: a zero-or-more set CONTAINS the nonzero lengths, so a '
            'zero-or-more reading of `src/**` matches `src/`, `src/legacy.js` AND '
            '`src/a/b.js`. Correcting that arithmetic does NOT dissolve the underspecification, '
            'and the two are kept separate here.'),
        'whyItIsNotAlgorithmFreedom': (
            'permittedEditScope decides whether a repair edit is admissible, and policy '
            'include/exclude decides subject enumeration and therefore which findings exist. '
            'Both are normative outcomes. Restated precisely: the published example forces '
            '`**` to be a SEGMENT-GROUP that is followed by a separator (that is what makes '
            '`**/*.ts` match root `a.ts`). Read that way, a TRAILING `**` -- with no following '
            'segment -- matches a path only if the path ends at a separator, so `src/**` '
            'matches NO file. Read instead as "any remaining suffix", `src/**` matches every '
            'descendant file. Both readings honour the closed alphabet and the one published '
            'example, and they disagree on whether the same plan is admissible. That is the '
            'gap: not which reading is right, but that the kit does not say.'),
        'measuredOnThisReconstruction': (
            'this origin writes a trailing wildcard as `**/*` so the final segment is matched '
            'explicitly, and recorded that choice at the site '
            '(lib/phase6_repair.py permittedEditScope). No reconstruction depended on the '
            'unstated reading, and NO glob law was invented to close it.'),
        'smallestFix': 'one sentence, or a second published example with a trailing `**`.',
        'notAMustBecause': ('a consumer can always avoid the unstated case by spelling the '
                           'final segment, so reconstruction is possible.'),
        'statusThisGeneration': (
            'STILL OPEN. No new normative bytes about globs were supplied in the v17 kit (the '
            '101 normative files are byte-identical to v16), and no oracle result for any glob '
            'was provided. The item remains pending source-author work; this origin has only '
            'corrected the arithmetic in its own rationale.'),
    },
]

ADVISORY = [
    {
        'id': 'V16-A3',
        'severity': 'advisory',
        'class': 'wording',
        'title': ('`traversalCoverage` and native CoverageResult share the word "coverage" '
                  'while being different obligations'),
        'selectors': [
            'docs/coop/design-corrections/workflows/schemas/evaluator3/'
            'graph-query.schema.json#/$defs/TraversalCoverage',
            'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
            '#/$defs/CoverageResultV3',
        ],
        'observation': (
            'the schema already says "Not native CoverageResult" in both places, which is why '
            'this is only advisory. The shared noun still invites a consumer to report a '
            'COMPLETE traversal over an INCOMPLETE evidence base as evidence completeness.'),
        'howThisOriginHandledIt': (
            'the two are carried in different required fields and reported separately, with '
            'an explicit statement of why: see '
            'query/graph-query-reconstruction.json '
            'evidenceLimitationsVersusStoredEdgeCompletion.'),
        'whyOnlyAdvisory': 'the distinction IS published; only the naming is inviting.',
    },
]

RESOLVED_BY_THIS_KIT = [
    {
        'id': 'V16-A2 (WITHDRAWN by this origin as factually wrong about the kit)',
        'wasReportedAs': ('advisory: "the execution-inputs inventory-kind equality rule does '
                          'not state the case where a cell binding is UNAVAILABLE", with the '
                          'further claim that an unavailable binding has no inventory to '
                          'produce, so the case is NOT-STATED'),
        'disposition': 'WITHDRAWN -- the clauses do state it, and they state the opposite',
        'why': (
            'three published clauses, read this generation: (1) enumeration-contract section 1, '
            'UNAVAILABLE binding -- "`extents` still populated from host membership so expected '
            'file/package paths are not lost", and the enumerator row requires "inventories '
            'empty `unavailable` matching that pair"; (2) enumeration-contract sections 3/4 -- '
            'EXACTLY ONE SubjectInventoryV1 per (cellOrdinal, programOrdinal, kind) of '
            'cell.kinds, with the `unavailable` shape given explicitly (rows=[], '
            'examinedPaths=[], deficiency non-null) and ENUMERATION_INVENTORY_MISSING_RECORD '
            'named for a whole missing expected inventory; (3) execution-inputs section 6 -- '
            '"Inventory digests: exactly one per kind, kinds set-equal to the cell" with NO '
            'available-only qualifier, plus "Unselected or `universe=null` DOES NOT DISCARD '
            'same-cell inventory items." A MISSING record is not a retained `unavailable` '
            'record.'),
        'whatThisOriginHadToFix': (
            'the advisory was not merely wording: this origin\'s own syntax-code graph carried '
            'NO inventory for its unavailable cell and an EMPTY extent on that binding, and the '
            'v16 checker had been weakened to make that pass. Both are corrected (V17-D5), the '
            'set-equality is now applied to every binding, and two controls now distinguish a '
            'missing record from a retained unavailable one.'),
        'notAnOracleClaim': (
            'no successor bytes answered this. The withdrawal follows from reading the three '
            'clauses in the kit this origin already held -- the 101 normative files are '
            'byte-identical to the v16 kit.'),
    },
    {
        'id': 'V15-S1 (withdrawn by this origin)',
        'wasReportedAs': ('SHOULD: the native retention catalogue omitted a `fragment` '
                          'entry'),
        'disposition': 'WITHDRAWN as over-broad',
        'why': ('no annotated site of the native document uses `fragment`, so declining to '
                'declare it there is correct. Measured: retention counts are preimage-frame '
                '31, preimage 21, owner-retained 11, closure-tree-member 10, derived 3, and '
                'ZERO fragment sites (notes/native-annotated-site-audit.json).'),
        'notAnOracleClaim': ('the withdrawal follows from measuring the document, not from '
                            'the successor agreeing or disagreeing with this origin.'),
    },
    {
        'id': 'V15-A1 (resolved in the new kit bytes)',
        'wasReportedAs': ('advisory: the native digest law carried a hand-maintained '
                          '`sites: 68` total beside the annotations it described'),
        'disposition': 'RESOLVED at the source',
        'why': ('the v16 native schema replaces it with `siteCountLaw`: "Count syntactic '
                'x-opensip-digest annotation occurrences in this schema document; the '
                'reference checker reports the measured count. No second hand-maintained '
                'total is normative." This origin now MEASURES 76 occurrences and asserts '
                'the absence of the old key.'),
    },
    {
        'id': 'V15-observation on the `derived` retention recipe',
        'wasReportedAs': ('the native retention vocabulary needed a declared recipe for the '
                          'derived sites this origin had independently derived'),
        'disposition': 'RESOLVED at the source',
        'why': ('the v16 native schema declares `derived` with the recipe this origin had '
                'already derived from the plan/run capabilityManifestId join; the closure now '
                'asserts the declared statement rather than this origin\'s inference '
                '(check_native_digest_law_vocabulary).'),
    },
]

FREEDOM_NOT_GAPS = [
    {'topic': 'how a host ENUMERATES subjects',
     'pinnedObservable': ('SubjectInventoryV1 rows, examinedPaths equal to the Plan census, '
                          'and the locator identity (planId, parameterDigest, cellOrdinal, '
                          'programOrdinal, kind)'),
     'left open': 'the traversal strategy, parallelism and caching',
     'why': 'the retained record is fully specified, so any strategy is checkable'},
    {'topic': 'how a normalizer computes an L1-L3 body',
     'pinnedObservable': ('the framed body identity, the retained level specification bytes, '
                          'and bodyIdentityJoin.recomputableAt = [L0-verbatim] only'),
     'left open': 'the normalisation algorithm itself',
     'why': ('the kit states in terms that it is NOT recomputable above L0 and demands exact '
             'retained preimage custody instead -- a deliberate, published limit, not a '
             'missing recipe')},
    {'topic': 'which shortest path a graph.path returns when several tie',
     'pinnedObservable': 'canonical fact2-id-sequence tie-break',
     'left open': 'the search algorithm',
     'why': 'the tie-break makes the RESULT total, so the algorithm is free'},
    {'topic': 'how a host stores and indexes the evidence store',
     'pinnedObservable': 'the exported object table plus every blob keyed by its digest',
     'left open': 'the storage engine, indexes and compaction',
     'why': 'a host index is explicitly never authority; resolution goes through digests'},
]


def main():
    doc = {'consumerId': 'consumer-b.v17', 'phase': 10, 'standing': __doc__,
           'distinctionApplied': {
               'algorithmFreedom': ('a strategy left open while the observable is pinned; '
                                    'reconstructible without invention'),
               'missingContract': ('a required observable with no published derivation, a '
                                   'contradiction, a circular authority, an ambiguous '
                                   'default that changes a normative outcome, or a forced '
                                   'invention')},
           'newMustIssues': MUST,
           'newShouldIssues': SHOULD,
           'advisories': ADVISORY,
           'itemsThisOriginWithdrewOrThatTheNewKitResolved': RESOLVED_BY_THIS_KIT,
           'algorithmFreedomNotGaps': FREEDOM_NOT_GAPS,
           'emptyMustJustification': (
               'newMustIssues is EMPTY because every observable this origin was required to '
               'produce had a published derivation that it could execute: the C/H recipes, '
               'the closing digest law and its four representations and retention modes, the '
               'capability-manifest gates, the relation/rung registry with its anchor, '
               'snapshot, totality and partition laws, the grammar-capability registry and '
               'its three enforcement boundaries, the section 1.2 mode table, the config '
               'node-kind law, the Rust context projection, the execution-inputs cell and '
               'account derivation, the composition section 9 proof/evidence/seal/Run '
               'joins, the repair descriptor and its two idempotency recipes, the comparison '
               'and baseline identities, the D9 class/exit table, and the graph-query '
               'operations with their bounds and mandatory disclosure. Where a value could '
               'not be recomputed (L1-L3 normalisation, symbol-to-path attribution, provider '
               'occupancy) the kit SAYS so and substitutes custody, which this origin '
               'executed rather than worked around.'),
           'v17ClauseToCodeAuditOfTheRECORDCONSTRUCTIONandADMISSIONfunctions': {
               'standing': (
                   'a second audit, run against BOTH the emitters and the admission/replay '
                   'functions. "A check saying that the emitter and replay agree does not '
                   'establish a normative clause that both omitted" -- so each area below '
                   'names a clause, what the code did instead, and the control that now '
                   'distinguishes it.'),
               'findingsInThisOriginsOwnWork': [
                   {'id': 'V17-D3', 'area': 'atom subject-kind / endpoint admission',
                    'clause': ('atom-evaluation-contract section 4 "Wrong `subject.kind` for '
                               'the relation/endpoint is ATOM_KIND_INCOMPATIBLE, never vacuous '
                               '`none`" + evaluator-projection-registry kindApplicability'),
                    'whatBothSidesOmitted': ('neither the emitter nor the checker compared the '
                                             'atom subject kind to the endpoint\'s registered '
                                             'kinds; only relation registration, ladder '
                                             'membership and tree shape were checked'),
                    'measuredConsequence': ('TWO of the five sealed graphs carried a DISABLED '
                                            'rule whose atom was kind-incompatible '
                                            '(literal@symbol with subjectKind file / package), '
                                            'and the `disabled` outcome hid it from every '
                                            'execution-side check'),
                    'nowDistinguishedBy': ('6 new policy controls reaching '
                                           'ATOM_KIND_INCOMPATIBLE / ATOM_ENDPOINT_UNAVAILABLE '
                                           '/ atom3:FILTER_FIELD_FORBIDDEN_AT_THE_REQUESTED_'
                                           'RUNG, plus a LAWFUL endpoint=target contrast')},
                   {'id': 'V17-D2', 'area': 'per-rung filter admissibility',
                    'clause': ('atom-evaluation-contract section 3 "Absent field at the '
                               'requested rung => filter forbidden at admission"'),
                    'whatBothSidesOmitted': ('the registry filter spec is EITHER a string or a '
                                             'PER-RUNG map; the checker compared the map to the '
                                             'string "forbidden", so every per-rung forbidden '
                                             'filter was admitted'),
                    'nowDistinguishedBy': 'the filter-forbidden-at-the-requested-rung control'},
                   {'id': 'V17-D4', 'area': 'enumeration plan and inventory totality',
                    'clause': ('enumeration-contract sections 1/3/4/5/8 + '
                               'x-opensip-file-membership-extent-law'),
                    'whatBothSidesOmitted': ('the v16 checker validated the enumeration plan '
                                             'NOT AT ALL -- it read the plan only to index '
                                             'cells -- so a compiler-filtered file extent, a '
                                             'consumer-chosen `kinds` subset and a missing '
                                             'expected inventory all passed'),
                    'measuredConsequence': ('four of five graphs declared a clones-fact FILE '
                                            'extent restricted to compiler/grammar-readable '
                                            'paths; one narrowed an `inventory` cell to '
                                            '[file]; one had a binding with no extents and no '
                                            'symbol inventory'),
                    'nowDistinguishedBy': ('8 enumeration controls, each reaching its intended '
                                           'law')},
                   {'id': 'V17-D5', 'area': 'unavailable bindings',
                    'clause': ('enumeration-contract sections 1/3/4 + execution-inputs '
                               'section 6'),
                    'whatBothSidesOmitted': ('the v16 checker was WEAKENED to make an '
                                             'unavailable cell with no inventory pass, and the '
                                             'gap was then published as advisory V16-A2'),
                    'nowDistinguishedBy': ('the unconditional kinds-set-equality plus the '
                                           'missing-record and dropped-extent controls')},
                   {'id': 'V17-D6', 'area': 'invocation step/result joins',
                    'clause': 'workflows-and-surfaces section 1 + invocation-record',
                    'whatBothSidesOmitted': ('the v16 envelope was schema-valid with ONE-based '
                                             'stepIds, no comparison step result and no '
                                             'attempt derivation binding; only the schema was '
                                             'checked'),
                    'nowDistinguishedBy': ('12 invocation controls, 10 of which the owning '
                                           'schema ADMITS and only the normative joins refuse')},
                   {'id': 'V17-D7', 'area': 'repair preimage / snapshot condition',
                    'clause': ('workflows-and-surfaces section 6 "preimage digest from the '
                               'snapshot inventory"'),
                    'whatBothSidesOmitted': ('only the local null/non-null image shape was '
                                             'checked, so the v16 "valid" descriptor asked to '
                                             'CREATE a path the selected snapshot already '
                                             'contained'),
                    'nowDistinguishedBy': ('4 snapshot-condition controls reaching '
                                           'REPAIR.CREATE_PATH_ALREADY_IN_THE_SELECTED_'
                                           'SNAPSHOT / REPAIR.SOURCE_MOVED / '
                                           'REPAIR.TARGET_PREIMAGE_MISMATCH / '
                                           'DELETE_HAS_NO_POSTIMAGE')},
                   {'id': 'V17-D1', 'area': 'helper rebinding',
                    'clause': 'n/a -- a helper defect, not a kit question',
                    'whatBothSidesOmitted': ('the v16->v17 path rebind rewrote an ancestry ROW '
                                             'LABEL while leaving the previous generation\'s '
                                             'digests beside it, so the table claimed the v17 '
                                             'manifest digest was the v16 value'),
                    'nowDistinguishedBy': ('digest constants are written beside their own '
                                           'generation and the current pair is asserted '
                                           'against the measured manifest')},
               ],
               'areasAuditedWithNoNewFinding': [
                   {'area': ('execution-inputs sections 4/5/6 coverage accounts and the '
                             'derived cell outcome'),
                    'result': ('the four applicability branches, the per-branch envelope '
                               'prohibitions, the matrix+cause-registry pair for '
                               'unsupported-typed, the per-universe attribution refusal and '
                               'the derived state table were already implemented and '
                               'independently recomputed from the retained Plan, inventories '
                               'and receipts. THREE additions were made rather than '
                               'corrections: the carrier must be a MEMBER of the owned source '
                               'pairs (not an unzipped combination), "empty kinds is not '
                               'complete-empty work", and an explicit record that complete '
                               'EXECUTION is not native capability support.')},
               ],
           },
           'blockerStatement': (
               'no blocker on this origin\'s side. Every promised vector was built and every '
               'acceptBlocking requirement was executed with a retained artifact. The two '
               'SHOULD items are ambiguous defaults that this origin measured around without '
               'inventing a rule, and both are reported with their exact selectors and '
               'smallest fix rather than with an adjusted meaning. They remain PENDING '
               'SOURCE-AUTHOR work: the v17 kit supplied no new normative bytes (its 101 '
               'normative files are byte-identical to v16), so neither can be closed here, '
               'and the verdict therefore stays CHANGES_REQUIRED.'),
           }
    EV.write('vectors/phase10-design-gaps.json', doc)
    print('phase10: %d MUST, %d SHOULD, %d advisories, %d withdrawn/resolved, '
          '%d freedom-not-gap topics'
          % (len(MUST), len(SHOULD), len(ADVISORY), len(RESOLVED_BY_THIS_KIT),
             len(FREEDOM_NOT_GAPS)))
    for r in SHOULD + ADVISORY:
        print('  %-8s %-9s %s' % (r['id'], r['severity'], r['title'][:84]))


main()
