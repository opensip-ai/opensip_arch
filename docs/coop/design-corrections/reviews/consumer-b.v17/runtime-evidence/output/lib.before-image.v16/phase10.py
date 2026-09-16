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

OUT = '/tmp/opensip-design-corrections/consumer-b.v16/output'

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
            'the alphabet is closed and ONE semantic fact is published: a LEADING `**/` may '
            'match zero segments. Nothing states whether `**` as the FINAL segment matches '
            'one-or-more segments, zero-or-more segments, or only directories.'),
        'whyItIsNotAlgorithmFreedom': (
            'permittedEditScope decides whether a repair edit is admissible, and policy '
            'include/exclude decides subject enumeration and therefore which findings exist. '
            'Both are normative outcomes. Under "zero or more segments" `src/**` matches '
            '`src/` only; under "one or more" it matches `src/legacy.js`. Two conforming '
            'consumers disagree on admission of the same plan.'),
        'measuredOnThisReconstruction': (
            'this origin writes a trailing wildcard as `**/*` so the final segment is matched '
            'explicitly, and recorded that choice at the site '
            '(lib/phase6_repair.py permittedEditScope). No reconstruction depended on the '
            'unstated reading.'),
        'smallestFix': 'one sentence, or a second published example with a trailing `**`.',
        'notAMustBecause': ('a consumer can always avoid the unstated case by spelling the '
                           'final segment, so reconstruction is possible.'),
    },
]

ADVISORY = [
    {
        'id': 'V16-A2',
        'severity': 'advisory',
        'class': 'case not stated',
        'title': ('the execution-inputs inventory-kind equality rule does not state the case '
                  'where a cell binding is UNAVAILABLE'),
        'selectors': [
            'docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md '
            'sections 5-6 (cell outcome / inventory obligations)',
        ],
        'observation': (
            'the rule that a cell\'s retained inventory KINDS are set-equal to the cell\'s '
            'declared kinds is stated for an available binding. For an unavailable binding '
            'there is no inventory to produce, and the clause does not say whether the '
            'equality still applies, is vacuous, or is replaced.'),
        'howThisOriginHandledIt': (
            'the check is applied only to an available binding, and the unavailable case is '
            'recorded as NOT-STATED rather than given an invented refusal or a fictional '
            'inventory. See the INVENTORY_KINDS_SET_EQUAL_TO_THE_CELL check and its '
            'not-applicable record in runs/*.closure.json.'),
        'whyOnlyAdvisory': (
            'no outcome of this reconstruction turns on it: an unavailable binding already '
            'carries its own published deficiency/cause pair, and the derived cell state is '
            'decided by the accounts, not by the inventory equality.'),
    },
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
    doc = {'consumerId': 'consumer-b.v16', 'phase': 10, 'standing': __doc__,
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
           'blockerStatement': (
               'no blocker. Every promised vector was built and every acceptBlocking '
               'requirement was executed with a retained artifact. The two SHOULD items are '
               'ambiguous defaults that this origin measured around without inventing a '
               'rule, and both are reported with their exact selectors and smallest fix '
               'rather than with an adjusted meaning.'),
           }
    EV.write('vectors/phase10-design-gaps.json', doc)
    print('phase10: %d MUST, %d SHOULD, %d advisories, %d withdrawn/resolved, '
          '%d freedom-not-gap topics'
          % (len(MUST), len(SHOULD), len(ADVISORY), len(RESOLVED_BY_THIS_KIT),
             len(FREEDOM_NOT_GAPS)))
    for r in SHOULD + ADVISORY:
        print('  %-8s %-9s %s' % (r['id'], r['severity'], r['title'][:84]))


main()
