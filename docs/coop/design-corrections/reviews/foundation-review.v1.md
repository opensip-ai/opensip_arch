# Independent review — Codex foundation / identity / admission unit (subject v3)

Reviewer: actual Claude (claude-fable-5-1), authored none of the subject bytes.
Standing: independent substantive review of a FROZEN subject. Verdict below is
not self-acceptance by the author and does not change D-372 or register status.
Machine-readable twin: `foundation-review.v1.json`.

## Verdict: CHANGES_REQUIRED

Three MUST_FIX defects, nine SHOULD_FIX, ten advisory. The unit is close: the
canonical encoder, domain-framed identity, capability-manifest recipe, three-valued
predicate logic, G13 relabel/zero-oracle refusals, crash-state and purge
invariance are concrete and independently reproduced. What blocks ACCEPT is that
the reference closure admits cross-Plan/cross-Run references through typed `Ref`
fields, never admits the auxiliary typed payloads that v3 headlines as new, and
does not enforce the proof's own input-completeness rule. Those are exactly the
places where "no raw opaque hash silently stands for a missing producing rule"
has to be true for a Phase-1A packet.

## Subject pins

| Item | Value |
|---|---|
| Subject manifest | `docs/coop/design-corrections/reviews/foundation-subject.v3.json` sha256 `86c709e6c817034d2ea9cc0b9d0ed79731d1d09a5e4bd9fd90b29bbdb88ee4b2` |
| Snapshot root | `/tmp/opensip-design-corrections/foundation-subject.v3` (1066 files; 0 extra, 0 missing) |
| Live vs snapshot equality | 1066/1066 sha256 equal at review start and again after all probes |
| `identity-and-evidence.md` | `6b3be8a8ef674dd6fc8dc70faaa545ea47857da81843183e0dfc40c597a45ad1` |
| `admission-and-qualification.md` | `69ec96c875f9774a6aec195dffdd08e02250784a71385dbd3acd8cd0c802aa9a` |
| `foundation/source-pins.v1.json` | `1fbe604df8b9739d994f2d55fce4361b5d295a8cf6e86880f13bbc016a50a762` (1060 pinned sources, all valid) |
| Launcher run (from snapshot) | `/tmp/opensip-design-corrections/foundation-independent-execution.json` sha256 `f6ec0d736f3b500120781048ece7cbf4217fdb01d7b11ae3a9185f8556aa11ff`; byte-identical to committed `validation-report.json` |
| Environment | Python 3.12.13, jsonschema 4.25.1, OpenSSL 3.6.3, `-I -B` |

Older subject v1/v2 were never reviewed and are not adjudicated here.

## Checks run

1. Manifest verification: every manifest path hashed in live tree and snapshot; set equality of snapshot contents against manifest.
2. `run-reference-checks.py --report /tmp/...` executed from the snapshot: sourcePinsValid true; check-foundation 229/229, check-identity 71/71, check-product-quality 22/22, check-product-configuration 14/14; productQualification false. The four regenerated report files hash equal to their committed bytes (deterministic replay of the reports).
3. CAP-MANIFEST-ID-V1 recipe: recomputed `SHA256("opensip.capability-manifest.v1"||00||committedBytes)` over `delivery.v4.json` vector `DCM-1-core` = `508f24c7…881b`, equal to the vector's `capabilityManifestId`. Bare 64-hex form confirmed against schema `$defs.Hash`.
4. Independent probes (bounded, /tmp only): `claude-probes-v3.py` sha256 `4b523a40…6e1d` → `claude-probes-v3.json`; `claude-probes-v3b.py` sha256 `c93636b8…5291` → `claude-probes-v3b.json`. Probe ids below refer to those files.
5. Read in full: both contracts, all foundation `.py`/`.json`, `check_g13_result_design_v4.py::valid`, `delivery.v4.json` capabilityManifestIdentity op, JOINT-INTERFACES, D-372 proposed, register DR-004/006/011 sections and AR rows, product-v1 README. Not read: legacy evaluation-proof checker lineages (out of scope by instruction).

## MUST_FIX

### MF-1 Typed `Ref` fields admit foreign Run / Plan / source objects

Evidence: P2a — a proof whose `evaluationInputRefs` names a foreign committed
Run (`{"domain":"run",…}`) closes successfully through `close_run` when that Run
is in the object set. P2a2 — a finding whose `evidenceRefs` names a foreign
`evaluation-seal` closes. P2b — a finding whose `evidenceRefs` names a `fact`
bound to a different `snapshot2` closes. In each case only the fixture replay
callback (a TCB assumption, not a closure rule) would notice.

Contract text violated: `identity-and-evidence.md` L121–122 ("proof does not
include EvidenceId or RunId"), L180–183 ("rejects … wrong-kind, cross-Plan/
cross-source or unresolved references").

Selectors: `identity-schemas.v2.json` `$defs.Ref.properties.domain.enum` (one
35-member enum shared by `proof-bundle.evaluationInputRefs`,
`predicateProofs[].inputRefs`, `finding.evidenceRefs`, `cache-key`/
`regeneration-key.inputRefs`, `availability.missingRefs`);
`identity-model.py` L47–62 (`walk`) and L74–110 (joins only for objects reached
via view/scope/fact fields).

Required: per-field allowed-domain sets in the schema (proof inputs: view,
import, coverage, rule-program, policy, waiver, schema, blob…; finding evidence:
fact, coverage, import, predicate-witness, blob; never run/semantic-evidence/
evaluation-seal/proof-bundle from inside proof or finding). In `close_run`,
every visited typed object must join the Run: fact/scope → `run.snapshotId`;
view/proof/evidence/seal/execution-plan → `run.planId`; any Ref to a run or seal
domain from proof/finding is `REFERENCE_KIND`. Add negative cases for all three
probes to `check-identity.py`.

### MF-2 Auxiliary typed payloads are declared, never admitted

Evidence: P2c — `scopeDigest` and `semanticGrantDigest` replaced by the digest of
`\x00not-json` bytes; `close_run` accepts. P2c-* — the fixture's own payload
`{}` (used for `scopeDigest`, `resolvedConfigDigest`, `policyDigest`,
`waiverDigest`, `semanticGrantDigest`, `payloadSchemaDigest`, `manifestDigest`,
`check-identity.py` L23) fails every declared schema (`scope-descriptor`,
`analysis-spec`, `semantic-grant`, `predicate-witness`). P2c-identifier — those
`$defs` are unreachable through `identifier()` (`PREFIX`, L7). P2j — a
schema-valid `semantic-grant` with a wrong `projectId` and wrong `scopeDigest`
closes. P2f — a non-JSON witness blob closes (`witnessDigest` is only required
to exist, L62).

Contract text violated: `identity-and-evidence.md` L141–158 (producing rules for
`resolvedConfigDigest`, `scopeDigest`, `analysisSpecDigest`,
`semanticGrantDigest`, grant binds ProjectId and scope), L180–183 ("validates
each payload with the exact admitted schema and its semantic admission rules"),
L201–209 (closed witness record). The v3 headline "typed auxiliary
scope/analysis-spec/semantic-grant payloads" is currently schema-only.

Required: a digest-field → schema map in `identity-model.py` (`scopeDigest`→
`scope-descriptor`, `analysisSpecDigest`→`analysis-spec`, `semanticGrantDigest`→
`semantic-grant`, `witnessDigest`→`predicate-witness`, `resolvedConfigDigest`→
canonical semantic value produced by `product-configuration-model.resolve`) that
parses with `canonical.parse`, validates with `ExactValidator`, applies
`ordered`, and enforces: `grant.projectId == run.projectId`,
`grant.scopeDigest == plan.scopeDigest`, `witness.programPredicateDigest` is a
retained blob, `witness.matchingFactIds ⊆` facts of the views named by the
predicate's `inputRefs`, `witness.coverageIds ⊆` those views' coverage. The
fixture must use schema-valid payloads (its `analysisSpecDigest` currently
doubles as the rule program, L30–31). Native/workflow-owned payload schemas
(native-context, policy, waiver, rule-program, coverage payload, fact payload,
import payload) should be named as joins, not validated here.

### MF-3 Proof input-completeness ("no hidden lookup") is not a closure rule

Evidence: P2d — `evaluationInputRefs` emptied while `predicateProofs[].inputRefs`
still name the view: closes. P2e — `evidence.coverageIds` carrying a coverage
no view references: closes. The fixture replay (`check-identity.py` L54)
selects views by scanning all objects for the Plan rather than through
`evaluationInputRefs`, so it cannot detect this either.

Contract text violated: `identity-and-evidence.md` L197–199, L181–182 ("extra
authoritative roots").

Required in `close_run`: `predicateProofs[].inputRefs ⊆ evaluationInputRefs`;
`predicateProofs[].scopeIds ⊆` scopes of the views named in its `inputRefs`;
`evidence.viewIds` set-equal to the view refs in `evaluationInputRefs`;
`evidence.coverageIds` equal to the union of referenced views' `coverageIds`.
The reference replay should read only through `evaluationInputRefs`. Add cases.

## SHOULD_FIX

- **SF-1 Depth bound disagreement.** P1d-33: `canonical.parse` admits 33 nested objects (`typed`, root depth 0, `depth > 32`), `host-foundation-model.v2.strict` refuses 33 (root depth 1). Contract L75 says "nesting depth 32". Define the count (root container = 1) and align both; add 32/33 vectors to `check-foundation.py`.
- **SF-2 Stale matrix selector.** `admission-and-qualification.md` L133 names `native/native-capability-matrix.v1.json`; only `v2.json` exists, `native/README.md` L25 calls v1 incomplete, `native-evidence.md` L67 names v2. Pin exact file and digest at integration. Cross-owner join (native).
- **SF-3 Missing baseline passes performance.** P5a: `product-quality-validator.py` L29–32 pass a cell on absolute bounds alone when `baselineMedianNanos` is null. Contract L169–171 says a new supported cell needs an explicitly reviewed initial baseline; absence is not an automatic pass. Either refuse null baseline for release-selected cells (first-baseline lanes admitted but not promotable) or correct the prose; also define both-or-neither for `baselineMedianNanos`/`baselinePeakRssBytes` (L31–32 read the second only when the first is set). Add a case.
- **SF-4 Waiver IDs not registry-checked.** P3a: `product-configuration-model.py` L29 checks `packIds` only; contract §1.1 L44 and L65 require registered pack and waiver IDs. Add check and case. (`evidence.importIds` admission is a disclosed native/workflow join; fine.)
- **SF-5 DR-006-named digests still lack an exact recipe.** L135–139 say `typescriptStdlibMerkleRoot` and `rustcDevLlvmDigest` are "generated from byte-complete signed closure inventories" but not that they are the `closure2` identities of `kind: stdlib` / `kind: rust-dev-llvm` closure descriptors (the schema has those kinds), nor which native recipe otherwise applies. `snapshot.vcsDigest` has no producing rule at all and `walk` (L62) forces it to be a retained blob. `closure.manifestDigest` should name the security unit's signed-manifest selector. State the rules.
- **SF-6 ProjectId first-use table untested.** Contract §2 L43–47 (missing/agree/unilateral/contradictory) and L50–56 (adoption, fork, move) have no reference transition or negative case; AR-09 names the ProjectId/storage join. Add a small decision-table reference and cases, including adoption that preserves ProjectId without importing credentials/leases/receipts.
- **SF-7 Recovery and availability not modeled.** P2h/P2i: no read-only `recover(executionId)` returning committed/failed after `durability-undetermined`; availability is a bare string with no generation, no partial/corrupt/expired/regeneration-mismatch/restoration transitions; `availability` and `commit-receipt` `$defs` are never instantiated; sealed-assurance immutability has no case. These are DR-004 Phase-1A bullets ("retained verification or regeneration objects", "immutable sealed assurance versus mutable availability", "typed expiry/purge degradation").
- **SF-8 Finding-fingerprint discriminator.** L122–125: who computes `subjectKey.discriminator`, from what, and the "refuses an ambiguous key" behavior are unspecified and untested; the schema allows any Text. Specify or delegate by named join to the native subject-correspondence contract; add a refusal case.
- **SF-9 Unlisted identity domain.** `g13-validator.v5.py` L85 mints `quality-difference` under the product frame; it is absent from the §3 domain table (L101–119). Add it as an operational artifact domain or replace with a raw digest.

## Advisory

- AD-1 Integer set arrays sort by canonical bytes (P2g: `requires: [9,10]` rejected, `[10,9]` accepted). Contract-consistent (L82–83) but surprising; document or declare ordinal arrays numerically sorted.
- AD-2 `Ref.domain` enum has overlapping/untyped members (`witness` vs `predicate-witness`; `blob`, `coverage-payload`, `fact-payload`, `legacy-fact`). Collapse or define each.
- AD-3 `check-foundation.py` L101 embeds the Python version in the report, so a manifest-covered file is interpreter-fragile.
- AD-4 RequestId minting source (bytes/CSPRNG) and the "existing execution recipe" for ExecutionId are not pinned by selector; `commit-receipt.executionId` is free Text.
- AD-5 Fixture replay uses `assert` (`check-identity.py` L55); `AssertionError` escapes `rejects()`.
- AD-6 `CONFIG_PROFILE_UNREGISTERED` is raised for an absent profile (P3c); distinguish absent from unregistered.
- AD-7 The launcher writes reports into the subject directory, mutating manifest-covered files on every run; deterministic today, but a `--report-dir` would keep the subject read-only.
- AD-8 `Text.maxLength` is counted in code points (P1i: 4096 × U+10000 = 16 KiB admitted). Fine under the 4 MiB cap; state the unit.
- AD-9 Contract §1.1 L50–56 describes a discovery layer with recognizer provenance; `product-configuration-model.resolve` has no such layer (folded into `defaults`). Document or add.
- AD-10 U+007F and U+2028 are emitted unescaped (P1b). Matches L80–82; note it explicitly since some consumers escape them.

## Things verified as correct

Canonical byte vectors and UR-1..5 goldens; lone-surrogate, BOM, `01`, `+1`, `1E400`, `-0`, nested `1.0`, bool-vs-integer and bool-vs-const refusals (P1a, P1e–P1g); UTF-8 key order across BMP/PUA/supplementary (P1h); capability-manifest recipe vector; strong-Kleene table and incomplete-resolution `none`→indeterminate; G13 v5 refuses missing/duplicate fixtures (P4a/b), refuses PASS flags over failing counters (P4d) while admitting an honest self-consistent FAIL report (P4c); product report v3 refuses absent absolute budget (P5b); crash states and purge invariance; report determinism.

## Cross-unit joins this unit depends on (name, do not self-close)

Native: coverage "complete" derivation from CoverageResultV3; fact/coverage/import payload schema admission; universe-key recipe; stdlib/LLVM closure recipe (SF-5); subject correspondence/discriminator (SF-8); matrix v2 pin (SF-2). Security: root boundary for ProjectId discovery; signed closure manifest digest; storage classifications feeding `storage_admission`; platform profiles for cells. Workflow: policy pack → rule program join (plan carries `policyDigest`, proof carries `ruleProgramDigest`; no join between them is checked), waiver resolution provenance, import2 admission for `evidence.importIds`, D9 code mapping for `evidence.{expired,purged,missing,corrupt}`.

## Coverage of the assigned audit rows

AR-01 exact scalar admission: concrete (SF-1 boundary). AR-02 independently bound subject/oracle/producer: concrete (SF-3). AR-09 identity-input closure and custody: concrete for the graph, defective at the closure rules (MF-1..3), thin for ProjectId/recovery (SF-6/7). AR-15 crosswalk: integration record, not adjudicated here. DR-004 eight bullets: proof match/no-match/indeterminate and purge-not-rewrite are evidenced; verification/regeneration objects and typed degradation are prose only (SF-7); reconciliation bullet is integration. DR-006: every §7.1 member has a `*2` domain; capabilityManifestId inherited and verified; the two freeze-named Plan digests still need an exact rule (SF-5). DR-011-R15: RequestId grammar given, minting and ExecutionId selector not pinned (AD-4).

## Limitations of this review

Reference code was executed only under the fixture adapter's finite relation; no native provider, OS durability, or hostile-TCB behavior was measured, and none is claimed. The replay callback is accepted as an authenticated host/evaluator TCB assumption per instruction. Sibling contracts (native, security, workflows) were read only to name joins; they are under authoring and not part of this verdict. Legacy evaluation-proof checker lineages were not re-read. All probes are in /tmp and are not part of the subject.
