Reading is complete. Both Codex findings corroborate against the frozen sources, and three of the four challenges to my classifications stand. Reconciliation follows.

```json
{
  "reviewer": "Claude (Anthropic), claude-fable-5-1; counter-review of Codex C-01/C-02 and reconciliation of PROD-02/03/07/10",
  "shippedVulnerabilityClaimed": false,
  "codexFindings": {
    "C-01": {
      "disposition": "CORROBORATED",
      "severity": "HIGH",
      "classification": "newly_discovered_defect (reference validator and its corpus; design evidence, not product)",
      "whatIsActuallyDefective": [
        "docs/coop/completion/host-foundation-model.v1.py:33 strict() uses json.loads with default parse_float, so 1.0 / 1e0 / 1.0000000000000001 become Python floats and fractional lexemes are rounded before any gate.",
        "host-foundation-model.v1.py:44 visit() deliberately tolerates finite floats although preview-configuration.schema.v1.json declares no float-typed field anywhere (limit :21-25 and schemaVersion :36-38 are type integer).",
        "host-foundation-model.v1.py:49-51 validate() delegates the type gate to Draft202012Validator, whose draft-2020 'integer' accepts integral floats and whose const equality treats 1.0 == 1; the schema therefore cannot enforce IMPLEMENTATION-FREEZE.md:1499-1508 law 18 ('a float is not an integer ... at any depth').",
        "The same validator path admits policySchema 1.0 for the permission-policy carrier (host-foundation-model.v1.py:208,213; security-schemas.v2/permission-policy.schema.json:4-5 is const 1 with no type). Untested by Codex's probes; same mechanism, so likely same result.",
        "host-foundation-cases.v1.json carries only integer literals for schemaVersion and limit (grep: no 1.0/1e0/float negatives), so 210/210 cannot detect the class; the omission propagates into whatever G12 fixture set is derived from it."
      ],
      "whatIsNotDefective": [
        "flag_budget() (host-foundation-model.v1.py:53-57) is exact: regex [1-9][0-9]*, length and uint53 bound.",
        "No product exists; a typed Rust deserializer (u64 from 1.0) refuses by construction. The risk is inheritance of the reference behavior or of the corpus gap, plus provenance: host-foundation-completion.v2.md:191-193 requires exact per-field values, which a rounding parser cannot supply."
      ],
      "distinction": "Reference-validator defect: yes, relative to law 18 and to host-foundation-completion.v2.md:171-175 ('required schemaVersion: 1', 'limit ... integer'). Unimplemented product acquisition: not applicable; this is an admission gate the reference model already claims to implement.",
      "correctTrustedInputBoundaryMustAdd": [
        "Lexical refusal before schema validation: parse_float hook that raises (carrier declares no float field), plus explicit rejection of exponent/fraction lexemes for every integer field, at every depth including nested pins/holds and any generated adapter carrier.",
        "Post-parse exact-type assertion for each closed scalar: type(v) is int and not bool for integers, type(v) is str for strings, type(v) is bool for booleans; never a mixed-type == comparison (law 18 'the assertion is the gate').",
        "Provenance: retain or round-trip the exact source lexeme; an admitted integer must re-serialize to the same canonical text.",
        "Retained negatives in host-foundation-cases for layers 2, 3 and 4 and for the policy carrier: 1.0, 1e0, 1E0, 1.0000000000000001, 9007199254740991.1, 9007199254740992, true, \"1\", 0, -1; positive control 1; expected reason carrier-schema or a new lexical reason.",
        "Apply the same gate to every carrier validated through Draft202012Validator in the accepted evidence set (policy, G13 result, doctor report reader, lock/manifest metadata profile); a JSON Schema is not the gate."
      ],
      "owners": "DR-103, DR-123, DR-125 (host admission/configuration carrier); G12 fixture derivation; law 18 (V1 freeze)",
      "confidence": "high"
    },
    "C-02": {
      "disposition": "CORROBORATED, with stronger evidence than Codex cited",
      "severity": "HIGH",
      "classification": "newly_discovered_defect (reference validator contradicts its own accepted contract text) plus integration_gap for producer attestation",
      "whatIsActuallyDefective": [
        "docs/coop/completion/check_g13_result_design_v4.py:35 compares runner.hostDigest/providerClosureDigest only to the candidate's own top-level fields; :20 HARDWARE trusted tuple omits both digests; :37 checks only HARDWARE keys against trusted_runners. Consistent relabeling of both copies passes; the 'wrong-subject' design case (:74) tests self-inconsistency only.",
        "check_g13_result_design_v4.py:56 accepts any fixture where the candidate declares expectationMatched=true and expectedCount==actualCount with zero missing/extra/duplicate; 0/0 passes. Yet :24 digest-pins quality-corpus-manifest.v1.json, and that manifest carries per-fixture expectations (expectedProjectImportEdges :12,40; expectedCycles :18,50; coverage :19,56; observations :20-33) that the validator never reads. The oracle exists in the pinned input and is ignored.",
        "g13-result-schema.v4.json:4-5 schemaMajor is const 1 with no type, so 1.0 passes for the same reason as C-01.",
        "Contract text the validator fails to encode: analysis-quality-completion.v2.md:126-130 ('exact set equality ... 100% expected members, zero extra'), :300 ('Result/fixture/subject digest joins are mandatory'), :304-306 (baseline existence from the authenticated record, 'not the candidate's self-declared'); analysis-performance-successor.v2.md:17-21 applies the separate trusted inventory to hardware/image fields only."
      ],
      "distinction": "Reference-validator defect: the trusted context already exists in the design (pinned corpus manifest, separately supplied runner inventory, baseline record) and the validator simply does not bind subject digests or per-fixture expectations to it. Unimplemented product acquisition: the actual-set truth and the producer attestation require the qualification wrapper to run the product; that remains G13 execution work and is not claimed defective here.",
      "correctTrustedInputBoundaryMustAdd": [
        "A trusted_subject context {hostDigest, providerClosureDigest} sourced from the signed release inventory or gate invocation; candidate top-level and every runner block must equal it. Add relabel-both-copies as a retained negative.",
        "Per-fixture oracle derived from the pinned corpus manifest: expected set digests and counts computed by the validator from the manifest, never taken from the candidate; a candidate expectedCount that disagrees is refused; zero expected only where the manifest says zero. Add zero-zero-matched and oracle-mismatch negatives.",
        "expectationMatched becomes a derived value: the report must carry actualSetDigest per fixture (computed by the trusted harness) and the validator recomputes match = actualSetDigest == expectedSetDigest and count consistency; a declared boolean is not evidence.",
        "Producer binding: the report is an untrusted artifact until the trusted wrapper's identity (harnessDigest alongside measurementToolDigest) and an attested report envelope are verified; the validator must refuse a report without that binding.",
        "Exact-type gate for schemaMajor and all integer fields per law 18; add schemaMajor-float negative."
      ],
      "owners": "DR-118, DR-121, DR-G13; language quality + product + release engineering",
      "confidence": "high"
    }
  },
  "claudeFindingReconciliation": {
    "PROD-02": {
      "codexChallenge": "honest known-open cell requirement, umbrella owner covers JS",
      "disposition": "AGREE; reclassify",
      "from": "HIGH newly_discovered_defect",
      "to": "MEDIUM known_open_contract",
      "retainedRequiredAcceptanceCase": "DR-118/119 must name JavaScript cells explicitly: no-tsconfig universe rule (resolved-inputs.v2.json:1708 keys the TypeScript universe on a tsconfig graph, so a JS project without one has no defined universe), ESM/CommonJS module systems, allowJs/checkJs, and the expected cycle-rule Coverage per cell. Register row 5 (08-decision-and-readiness-register.md:409) does not currently say 'JavaScript'; the D-371 act (D-371-design-target.v1.md:41-42) does. Naming it in the row prevents the cell from being closed with TypeScript-only evidence.",
      "strongestSources": ["docs/v2/architecture/10-mvp-and-future-scope.md:39", "docs/coop/unified-design-review/D-371-design-target.v1.md:41-42", "docs/coop/artifacts/resolved-inputs.v2.json:1696-1709", "language-quality-matrix.completed.v2.json (no JavaScript occurrence)"]
    },
    "PROD-03": {
      "codexChallenge": "row 4 maps machine projection parity to DR-122/123; chapter 13 requires each advertised adapter; the gap is the named surface/applicability/parity contract",
      "disposition": "AGREE in substance; reclassify",
      "from": "HIGH integration_gap ('unowned')",
      "to": "MEDIUM known_open_contract (owner inferable; acceptance cell and parity surface absent)",
      "retainedRequiredCorrection": "Row 4 text and the DR-122 successor must name HTML and the agent projection with applicability and parity field modes; operability.v10.json $.projectionParity.surfaces (json, exit-code, human-terminal, sarif, agent-mcp) has no html surface, and 13-evidence-workflows-and-product-contracts.md:259-261,263-268 requires adapter tests and typed-assessment-only report formatting without naming HTML. Agent surface: parity exists, register mention absent, v1-slice.md:172-173 exclusion unrevisited under D-371.",
      "strongestSources": ["docs/v2/architecture/10-mvp-and-future-scope.md:41", "docs/v2/architecture/08-decision-and-readiness-register.md:408", "docs/coop/artifacts/operability.v10.json:1231-1295", "docs/coop/architecture/08-surfaces-and-topology.md:371-384"]
    },
    "PROD-07": {
      "codexChallenge": "verify whether contracts already distinguish the provenance branches; do not claim three lawful outcomes for one request",
      "disposition": "PARTIALLY WITHDRAWN; reclassify",
      "from": "MEDIUM documentation_hazard ('three terminations for one journey')",
      "to": "LOW documentation_hazard plus one narrow known_open_contract",
      "branchTable": {
        "b_selected_closure_bytes_missing_or_corrupt_or_unspawnable": "DEFINED. delivery.v2.json:492-495 providerDeliveryFailure and :1170 map to faultCause delivery-required / DELIVERY.REQUIRED_FAILED (exit 4). The surfaces chapter (coop 08:211-212) cites that code correctly; my statement that it cited a golden with a different meaning is withdrawn. Residual hazard: d9-exit-contract.v1.14.json carries only the export-delivery instance of that code (:2279-2308), so a reader of D9 alone misreads provider delivery; the D9 successor should add the provider-delivery golden.",
        "c_provider_runs_and_returns_Unavailable": "DEFINED. d9-exit-contract.v1.14.json:1550-1575 indeterminate / COVERAGE.PROVIDER_UNAVAILABLE (exit 3); coop 08:209-211 clean typed Unavailable becomes Coverage provider-unavailable.",
        "a_core_only_install_no_selected_closure_in_local_registry": "NOT NAMED. distribution-runtime-completion.v2.md:196 says untrusted or missing dependencies refuse at resolution; host-foundation-completion.v2.md:164 makes the TypeScript request a compiled default, so analyze on a core-only install reaches a pre-admission resolver refusal; no D9 code or golden names it (host-foundation:200-201 covers authored invalid values, not an uninstalled dependency; security-completion.v8.md:354 lists OC-4 codes without a missing-dependency member). Correction owed: one golden and code selection at the DR-131/D9 successor; do not invent the code here."
      },
      "strongestSources": ["docs/coop/artifacts/delivery.v2.json:492-495,1170", "docs/coop/artifacts/d9-exit-contract.v1.14.json:1550-1575,2279-2308", "docs/coop/completion/distribution-runtime-completion.v2.md:196", "docs/coop/completion/host-foundation-completion.v2.md:164,200-201"]
    },
    "PROD-10": {
      "codexChallenge": "D-371 already requires every in-scope obligation to cite accepted contracts and forbids counting preview grades; this is traceability, not a proven loophole",
      "disposition": "AGREE; reclassify",
      "from": "MEDIUM documentation_hazard ('closure not measurable')",
      "to": "LOW documentation_hazard (traceability / primary accountable owner)",
      "retainedRequiredCorrection": "08-decision-and-readiness-register.md:414-420 states the per-obligation requirement; the condition-2 measurement (:431) remains per row and nothing binds an obligation to the row whose SATISFIED cell must cite its contract digest. Name one primary accountable row per obligation-table row. Table edit only.",
      "strongestSources": ["docs/v2/architecture/08-decision-and-readiness-register.md:403-420,428-434", "docs/coop/unified-design-review/D-371-design-target.v1.md:94-97"]
    }
  },
  "crossReferences": {
    "C-03": "Aligns with PROD-05; agree it is known open under row 2, not a broken accepted contract.",
    "C-04": "Aligns with condition 1 standing; PROD-06 (stage-to-stage trust-floor continuity) is a sub-case Codex's C-04 does not name and should be carried.",
    "C-05": "Consistent with the APFS/ext4 and birth-time refusals I read in host-foundation-completion.v2.md:121-127; the lease-versus-concurrent-agent-invocation question was not traced by me and stays an untested cross-contract concern."
  },
  "unchangedFromOriginalReport": ["PROD-01", "PROD-04", "PROD-05", "PROD-06", "PROD-08", "PROD-09", "PROD-11", "PROD-12"],
  "notVerifiedHere": [
    "Execution of any reference function; all statements rest on reading frozen source and on Codex's retained probe outputs.",
    "policySchema 1.0 admission (inferred from identical validator path; not probed).",
    "Whether serde-style typed deserialization is the selected Rust host approach; stated only as a bound on product consequence."
  ],
  "fullDesignAcceptanceRequested": false
}
```