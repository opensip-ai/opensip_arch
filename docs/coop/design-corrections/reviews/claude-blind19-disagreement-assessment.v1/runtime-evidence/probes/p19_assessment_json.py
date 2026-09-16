"""P19: assemble assessment.json from the probe artifacts."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RT = os.path.dirname(HERE)


def L(n, root=HERE):
    return json.load(open(os.path.join(root, n)))


p1, p2 = L('p1-inventory.json'), L('p2-accounts.json')
p5, p7 = L('p5-outcomes.json'), L('p7-cellstate.json')
p13, p14 = L('p13-corrective-route.json'), L('p14-mutation-validate.json')
p17 = L('p17-clones-census.json')
rec = L('receipts.json', RT)

doc = {
    "sessionId": "919c766d-f2d0-4cfa-abaa-9d7425d9395f",
    "task": "bounded READ-ONLY diagnosis of blind19 ACCEPT vs root exact-replay REFUSE on frozen32",
    "standing": "source-coauthor origin performing diagnosis; NOT independent design, blind or application acceptance",
    "blindOriginContacted": False,
    "wroteOnlyToThisRuntime": True,
    "productImplementationOrCommit": False,

    "verification": {
        "manifestSha256": p1['manifestSha256'],
        "manifestMatches": p1['manifestMatches'],
        "manifestFileCount": p1['manifestFileCount'],
        "allFiveExportsRecomputedMatch": p1['allExportsMatch'],
        "ownersReadAllMatchManifest": all(o.get('manifestMatch') for o in p1['ownersRead'] if o['present']),
        "probeCount": len(rec['probeReceipts']),
        "allProbesExitZero": all(r['exitCode'] == 0 for r in rec['probeReceipts']),
    },

    "executionInputFindings": [
        {
            "id": "F1",
            "title": "inapplicable-vcs account sourceUniverse",
            "runsAffected": ["syntax-code", "typescript", "rust", "rust-partial", "syntax-data"],
            "observed": "applicability agrees (inapplicable-vcs both sides); consumer sourceUniverse=null, owner wants the binding universe",
            "ownerSelectors": [
                "foundation/execution_inputs_model.v1.py:1140 want_u = None if want_app in (unavailable-unselected, unavailable-null-universe) else uni",
                "foundation/execution_inputs_model.v1.py:1142 raises EXECUTION_INPUTS_COVERAGE_DERIVE",
                "foundation/execution_inputs_fixture.v3.py:273 same rule in the synthetic helper"
            ],
            "publishedOwnersConsulted": [
                "foundation/execution-inputs-contract.v1.md:81 (inapplicable-vcs row governs ENVELOPES only)",
                "foundation/execution-inputs.schema.v1.json#/$defs/NativeCoverageAccountV1 (sourceUniverse required+nullable; only conditional is coverageIds maxItems 0)",
                "foundation/execution-inputs-contract.v1.md:88-112 (per-universe clause constrains RESOLVED Coverage and NAMED scopes, not an account without Coverage)"
            ],
            "normativeSearchResult": "0 hits for any published tie between account sourceUniverse and applicability",
            "consumerRuleIsSelfConsistent": p5['consumerRuleApplicabilityToNullUniverse'],
            "classification": "genuinely missing normative law",
            "materiality": "this difference alone refuses all five runs",
            "correctionOwner": "execution-inputs contract section 5 table + NativeCoverageAccountV1 schema"
        },
        {
            "id": "F2",
            "title": "UNSUPPORTED-TYPED and unselected: which applicability token",
            "runsAffected": ["syntax-code"],
            "observed": "unresolved-edge@observed syntax-only, matrix UNSUPPORTED-TYPED, enumerator unselected; consumer unavailable-unselected, owner unsupported-typed; want_u None both ways so ONLY the token differs",
            "ownerSelectors": ["foundation/execution_inputs_model.v1.py:406-415 derived_applicability tests matrix at :409 BEFORE uni-null at :411 and unselected at :413"],
            "publishedOwnersConsulted": [
                "native-capability-matrix.v2.json#/capabilityIdLaw/releaseDeclarationRegistry/absenceProjectionAndPrecedence (orders the PAIR: language-tier-unsupported ahead of provider-unavailable)",
                "native-evidence.md:830 UNSUPPORTED-TYPED is requestable and answered, never refused",
                "admission-and-qualification.md:79 such cells are answered by disclosure rather than omitted",
                "enumeration-contract.v1.md:30 unselected+optional binding is lawful"
            ],
            "consumerDerivedPairMatchesPublishedPrecedence": True,
            "classification": "genuinely ambiguous on the token; arguably a consumer defect on choosing omission over disclosure",
            "note": "the consumer is internally inconsistent: syntax-data ANSWERS its UNSUPPORTED-TYPED cell while syntax-code OMITS its own"
        },
        {
            "id": "F3",
            "title": "UNSUPPORTED-TYPED, selected, with lawfully minted Coverage",
            "runsAffected": ["syntax-data"],
            "observed": "imports@resolved-target syntax-only; consumer declared supported-available WITH a real coverageId; owner wants unsupported-typed",
            "consumerNativeEvidenceIsCorrect": {
                "coverage": "unknown", "deficiency": "language-tier-unsupported",
                "nativeCause": "capability-missing", "resolutionCompletenessState": "not-attempted",
                "prescribedBy": ["native-evidence.md:3183", "native-evidence.md:534 matrix row imports@resolved-target under syntax-only = UNSUPPORTED-TYPED"]
            },
            "conformingShapeConfirmedExecutably": {
                "account": "applicability=unsupported-typed, coverageIds=[], sourceUniverse=<binding U>",
                "derivedOutcome": p13['deriveOutcomeUnderEachReading'],
                "consequence": "the lawfully minted Coverage is referenced by no account and the cell outcome discloses no carrier"
            },
            "classification": "consumer defect in the account token, plus a documentation gap",
            "derivative": "syntax-data EXECUTION_INPUTS_CAUSE_CARRIER is downstream of this (model :1415-1417), not an independent difference"
        },
        {
            "id": "F4",
            "title": "clones-fact carrier under census-driven incompleteness",
            "runsAffected": ["syntax-code", "typescript", "rust (two programs)"],
            "runsNotAffected": ["rust-partial", "syntax-data"],
            "observed": "state agrees (partial); the owner derives provider-unavailable where the consumer derives (null, null)",
            "computedCensus": p17,
            "ownerSelector": "foundation/execution_inputs_model.v1.py:614 deficiency = coverage_records[0].get('deficiency') or 'provider-unavailable'",
            "contractProhibition": [
                "execution-inputs-contract.v1.md:68 the row pair MUST ACTUALLY OCCUR ON A SOURCE RECORD, and not a rewrite as generic provider-unavailable",
                "execution-inputs-contract.v1.md:83 do not manufacture a carrier"
            ],
            "discriminator": "where the Coverage record carries a real pair (rust-partial, syntax-data) both sides agree exactly; the fault appears only where no source record carries a pair",
            "consumerRationaleRetained": "consumer-b.v19/output/helper-corrections.json V18-D7/V18-D8 cites EXECUTION_INPUTS_COVERAGE_DERIVE:MISSING_EXPECTED_SOURCE_SUBJECTS_MAKE_THE_ACCOUNT_INCOMPLETE and states the consequence is reported rather than engineered away",
            "classification": "reference defect",
            "correctionOwner": "execution-inputs contract section 5 (define the carrier) or _summarize_coverage_records (drop the invented fallback)"
        }
    ],

    "accountDifferencesPerRun": [
        {'run': r['run'], 'owedPairs': r.get('owedPairs'), 'accounts': r.get('accounts'),
         'differenceCount': r.get('differenceCount'), 'vcsKind': r.get('vcsKind'),
         'differences': r.get('differences')}
        for r in p2['runs']
    ],

    "queryAndMutationFindings": [
        {"id": "Q1", "item": "truncated-page vs truncated=true",
         "verdict": "CONFIRMED consumer defect",
         "owner": "workflows/query-projection-contract.v3.md section 5: 'Page fullness is truncated-page, truncated=false. It is not operation truncation.'",
         "observed": "truncated=true at operations 1 (page size 1), 5 and 6",
         "limit": "compared against the contract sentence; the reconstruction document was not validated against a response wire schema"},
        {"id": "Q2", "item": "cursor 'ord:1' lacking selection binding",
         "verdict": "CONFIRMED substantive (contract-level, not schema-level)",
         "owner": "graph-query.schema.json#/$defs/Page.cursor and query-projection-contract.v3.md section 5",
         "observed": "cursor 'ord:1' carries a position only; the published bind (project+Run+factViews+operation+params+order+position) and the QUERY.CURSOR_MISMATCH continuation check are unimplementable against it",
         "schemaValid": True},
        {"id": "Q3", "item": "external-import omission",
         "verdict": "CONFIRMED",
         "observed": "typescript Run holds resolvedTarget ts:node_modules/left-pad/index.d.ts (specifier left-pad); endpointMembership.admittedMembers lists 11 members and omits it",
         "owner": "query-projection-contract.v3.md: an external resolved target that is not first-party inventory remains a lawful vertex",
         "limit": "compared the artifact's declared membership against the Run's import facts for one Run; the projection was not re-derived"},
        {"id": "Q4", "item": "invalid request/step IDs",
         "verdict": "REFUTED in the query artifact; CONFIRMED in the mutation scope artifact",
         "queryArtifact": {"requestId": "req1_abababababababababababababababab",
                           "matchesPublishedPattern": True, "stepIdPresent": False},
         "mutationScope": {"preimage": p14['consumerPreimage'],
                           "schemaValidation": p14.get('validation'),
                           "sameRecordWithConformingIds": p14.get('validationFixed'),
                           "idVocabulary": p14.get('idVocabulary'),
                           "consequence": "the declared idempotency key is H over a preimage that cannot be admitted"}}
    ],

    "frozen32AcceptanceReopening": {
        "requiresReopening": ["F1", "F4"],
        "reason": "both are defects in frozen32 OWNERS, not in the consumer: F1 enforces an unpublished rule; F4 manufactures a carrier its own contract forbids",
        "documentationOnly": ["F3 gap: what becomes of Coverage lawfully minted for an UNSUPPORTED-TYPED pair"],
        "decisionNeeded": ["F2 applicability precedence and whether an UNSUPPORTED-TYPED cell may be left unselected"],
        "consumerSideCorrections": ["F3 account token", "Q1", "Q2", "Q3", "Q4 mutation preimage"]
    },

    "correctionRoute": [
        "F1: publish the sourceUniverse rule in the section 5 table and as a NativeCoverageAccountV1 conditional, choosing explicitly between 'binding U always' and 'null when no Coverage'",
        "F4: either name a deficiency for census-driven incompleteness or allow a (null,null) pair and delete the 'or provider-unavailable' fallback at _summarize_coverage_records:614; the latter is smaller and matches the existing must-occur-on-a-source-record rule",
        "F3: state in section 5 that Coverage minted for an UNSUPPORTED-TYPED pair is retained but unaccounted and that the token is the disclosure",
        "F2: publish the applicability precedence and reconcile enumeration-contract.v1.md:30 with 'answered by disclosure rather than omitted'",
        "Q1-Q4: consumer-side; the mutation-key vector must be regenerated from an admissible preimage"
    ],

    "unresolvedQuestions": [
        "F1: which sourceUniverse value is normative; the published text supports neither over the other",
        "F2: is the applicability enum ordered, and does 'answered by disclosure rather than omitted' forbid leaving an UNSUPPORTED-TYPED cell unselected",
        "F4: should census-driven incompleteness carry a deficiency at all; no existing member occurs on a source record for this case",
        "whether other capability/mode combinations outside these five runs hit the F1/F2/F3 shapes; not surveyed",
        "Q3 breadth: one omitted external vertex confirmed in one Run; the other four were not surveyed",
        "root's scope-enumerator / foreign-U filtering hypotheses: nothing I traced supports them; I make no claim either way"
    ],

    "limits": [
        "did not re-run the consumer engine, did not re-execute full reference suites, did not replay admit_execution_inputs end to end",
        "recomputed the disputed derivations by importing the frozen owner module and calling its own functions on the exact export bytes",
        "root supplied traces for syntax-code and syntax-data only; all five runs were recomputed here",
        "charter and requirement coverage were not assessed",
        "an early stub of mine wrongly suggested clones-fact derives complete; the frozen owner does implement the expected-subject census and the corrected derivation is in F4"
    ],

    "evidenceHashes": rec['evidenceHashes'],
    "probeReceipts": rec['probeReceipts']
}

out = os.path.join(RT, 'assessment.json')
json.dump(doc, open(out, 'w'), indent=2, default=str)
print('WROTE', out)
print('findings:', len(doc['executionInputFindings']), '+', len(doc['queryAndMutationFindings']))
print('probes:', doc['verification']['probeCount'], 'allZero', doc['verification']['allProbesExitZero'])
print('evidence hashes:', len(doc['evidenceHashes']))
