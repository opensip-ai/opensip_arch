# CODEX2 — M3-I1 r1 review

**Verdict: REQUIRED-FINDINGS.** Three corrections are required before law acceptance: expected-importer totality, the authority for identity-enum widening, and population-only indeterminacy.

Reviewed `PROPOSAL.md` (38,187 bytes), SHA-256 `2226b14ff6778a22589d7602c23e2e0696d272221738f4411ad9110953592fc3`, and `UNITS.md` (6,915 bytes), SHA-256 `8fc877d49560995e97165d919b3121f9c73b91ec70efabe4a2ee40fbd0803eda`. All 13 pins in the request's `hashes.txt` matched on initial inspection and again before writing this review.

## Required findings

### I1-RF-1 — Close the expected imports source census

**Location:** PROPOSAL.md:129-141 (2.5(b), (d)); UNITS.md:26,36-64.

Graph completeness accounts retained partitions but does not establish that they cover every expected imports source. This can make an incompletely examined graph pass.

Item 2.5 checks every **retained** exact-rung scope and requires at least one per universe. It never establishes that those scopes cover every expected importer. Its population condition is the policy rule's **file** population. Imports independently enumerates **symbols** (`enumeration-plan.schema.v1.json:87-98`), and COMP:161-166 makes a file rule's relevant inventories kind=file only. Scopes are allowed to contain a subset of the source inventory (`enumeration-contract.v1.md:93`).

A static counterexample is enough:

1. One available universe U has a complete file inventory containing `a.ts` and `b.ts`, and a complete imports-symbol inventory containing opaque native IDs A and B, attributed to those files.
2. A lawful `required:false` imports cell returns one `imports@resolved-target` scope containing A only, with paired complete Coverage satisfying the fixed requirement. There are no retained import facts or unresolved edges.
3. B occurs in no returned scope. Native accounting correctly marks the account incomplete and the cell partial. This is an admitted semantic outcome, not a malformed record: execution-inputs:169 expressly covers missing expected subjects despite complete returned Coverage. Its missing-work carrier is (null, null), and only required cells create the independent required-cell deficiency (execution-inputs:190,198-211).
4. Nevertheless, 2.5(a)-(d) all hold. The selected graph is empty, both predicates are false, and COMP:56-58 permits pass. B's imports have never been examined, so sufficient graph Coverage has not been established (AQC:65-69).

Making the ordinary C4 request required would add a Run-level fallback, but would not make this atom's completeness law sound for lawful optional cells. A partial symbol inventory with complete file enumeration is another gap in the same predicate.

**Required fix:** Require completeness of the expected imports source-symbol census at every owed universe extent and exact-id coverage of every expected source by the returned exact imports/resolved-target scopes, in addition to the existing all-partition pairing and sufficiency checks. Retain a blocking population-unknown cause for an incomplete/unavailable source census and uncovered-expected-source-subject for a known uncovered source, using existing carrier rules without manufacturing provider-unavailable. This requirement must hold independently of the cell's required flag. Add I1-L/I1-b2 discriminating cases for a complete subset partition omitting another expected importer, partial symbol census with complete file population, complete broad partitions covering several importers, and complete-empty source populations.

### I1-RF-2 — Resolve the identity-law change explicitly

**Location:** PROPOSAL.md:180-214 (LD-3 and successor table); UNITS.md:22-24.

The in-place proof3/program-predicate enum widening is not authorized while the proposal expressly leaves the identity law unchanged.

IE:109-112 makes the closed identity schemas authoritative. IE:213-214 says schema/domain changes require a new identifier major and reviewed migration. It does not qualify that requirement to finding fingerprints or to reinterpretation of existing instances. The proposed additions change the accepted grammar of proof-bundle `predicateProofs[].operation` and the `program-predicate.operation` record (IDS:1221-1231,2781-2791).

COMP:7 permits an unchanged ancestor record to retain its domain when a committed parameter or schema **value** changes. It does not expressly permit changes to that record's own closed accepted vocabulary. IDS:4978 makes the same distinction between changed output domains and unchanged ancestors. “The fields remain the same” and “old readers reject the token” establish compatibility properties; they do not override the major/migration rule.

The placement of IE:213-214 after fingerprint prose is insufficient authority to narrow its unqualified requirement while item 4 declares IE unchanged. Under the cited unchanged law, LD-3 needs new majors and reviewed migration. An explicitly reviewed identity-law exception is a possible successor decision, but is absent from these bytes.

**Required fix:** Flip LD-3 to explicit new majors and a reviewed migration/dispatch plan for the affected identity records, retaining unchanged ancestors where COMP:7 permits it, and update I1-L, I1-a, pack pins and downstream joins consistently. If the lead instead chooses additive enum extension under existing majors, I1-L must explicitly include a narrowly scoped identity-law successor that authorizes it and defines compatibility/admission behavior; remove the claim that unchanged IE already permits it. Review that amendment rather than relying on paragraph placement.

### I1-RF-3 — Give population-only incompleteness a lawful result

**Location:** PROPOSAL.md:122-123,129-141 (2.5(d) versus cause derivation); UNITS.md:36-64.

Population-only incompleteness has no atom-cause derivation, so a valid partial file inventory can reach the stated host-invariant refusal instead of a semantic indeterminate result.

Item 2.5 makes complete **file-rule population** a necessary condition (d) of its graph-completeness result, while saying the op does not restate composition's population deficiency. The value table therefore returns indeterminate when (d) alone fails. Yet line 141 derives atom causes only from (a)-(c) and uncertain edges, then forbids emitting an indeterminate value with an empty cause set as a host-invariant defect.

Consider a lawful partial file inventory retaining `a.ts` while other extent paths remain unseen. Independently, its imports-symbol inventory and imports scopes/Coverage are complete and sufficient, with no facts, cycles or uncertain edges. Conditions (a)-(c) succeed; (d) alone fails. At the retained `a.ts` subject, the table returns indeterminate with no specified atom cause. The stated invariant rule refuses it before composition can publish its independent enumeration deficiency.

Partial inventories with known rows are valid semantic evidence (enumeration-contract:120; COMP:28,161-166). COMP:56 already makes their gating rule population indeterminate. The fault contract expressly excludes lawful partial inventories and ordinary unknown predicates from operational-fault treatment (evaluator-fault-contract:18,34-35). This gap is distinct from I1-RF-1: it occurs even when every imports source and partition is completely covered.

**Required fix:** Either define the existing blocking native population-unknown cause for failure of (d), retaining the real inventory/enumeration provenance and owner carriers, or keep file-rule population exclusively in composition and remove (d) from the atom's completeness/value decision. In either case a lawful partial file inventory must produce the existing semantic indeterminate rule outcome rather than a host-invariant fault. Add a population-only partial-file case with otherwise complete imports evidence to I1-L and I1-b2.

## Decisions requested by REQUEST.md

| Item | Assessment |
|---|---|
| 1. X12 r3 | Consistent. Item 7 amends only the M2 zero-row state and the corresponding NT-1/row-count tests. Byte-exact named admission, sole immutable release row/document, `Supplied` refusal, contribution membership, rows 1–4, admission order, `AdmittedPack`, Plan join and X12d remain in force. The original forbidden substitutes are preserved by incorporation and explicit restatement (X12:196-222; proposal:308-315,375-400). |
| 2. AQC / DR-131 | The root-only representative atom supplies one finding per admitted cyclic SCC, including self-edges; parallel facts do not multiply components. Only reconciled host occupancy drops external targets. Unresolved/unknown endpoints never become guessed edges. **LD-4 is sound:** a live unwaived known-cycle finding fails under COMP:56-58 while all deficiencies remain retained (COMP:34-36). Missing evidence does not erase a known cycle. The pass-only-with-sufficient-Coverage requirement remains blocked by I1-RF-1. |
| 3. IR | Exact-id inventory attribution avoids parsing opaque subject IDs. Skipping a known source outside V is sound because any cycle through it would need an outgoing edge from V, which is uncertain under the target rule. Existing `population-unknown` / `target-kind-unknown` carriers fit the semantic gaps; existing structural occupancy/inventory admission refusals still stand. The blocking-native-cause requirement is appropriate, but population-only incompleteness lacks its derivation (I1-RF-3). **LD-6 is confirmed:** ATOM:267 explicitly applies `target_exported/target_affected` only for endpoint=target; NE:2271's closed-world test does not add an incoming target obligation to this outgoing requirement. Forbid/forbid and all retained partition sufficiency are appropriate, but source-census totality is missing. Witness sets retain known/uncertain provenance, and the graph-once-per-rule design is consistent with the COMP:38 full-scan charge and existing output bounds. |
| 4. LD-3 | Blocked by I1-RF-2. No implicit identity-law exception is established. |
| 5. Bytes / digests | The proposed document is canonical ASCII JSON with no trailing newline. The contribution token is legal and distinct from the colon-bearing packId (COMMON:84-88). The registry row has X12a's exact six-key set. All three provisional digests independently match the proposed bytes and COMP:103's compilation recipe; details below. This verifies the current candidate, not acceptance of its proposed version dispatch. |
| 6. Feeds | C4 commits the admitted policy/program, enumeration and explicit detector binding; J admits before execution and obtains outcome from the core. I2 reuses the same reviewed semantics and stable namespace in harness documents without entering the release registry. LD-10 is correctly a recommendation for the C law, subject to the manifest/tree/role work noted below; COMP:9 and WS:277-281 remain mandatory. |
| 7. Units | UNITS.md's dependencies are sound: I1-L before I1-P/I1-a; I1-a before I1-b1; I1-b1 before I1-b2; I1-P plus I1-b1 before I1-c. **LD-11 is sound** while unsupported evaluation remains a structural refusal and J2 waits for I1-b2. Every product unit explicitly waits for integrated X9-6; design work is allowed earlier. The three required corrections must be reflected in I1-L and the affected implementation/fixture units. |

## Digest evidence

Recomputed with `inspect_digests.py`, a read-only scratch script importing only Python standard-library modules. It neither imports nor runs repository code.

| Value | Recomputed SHA-256 |
|---|---|
| SHA-256 of C(emitWhen), `programDigest` | `8e8936af513ae93eeb8227fb991330b523761930d85d077b044f4312706a57de` |
| SHA-256 of the canonical 574-byte document, `policySha256` | `96675a5e20fcfd8ba6501f20b9017aa205e300b9f1984d7e74ad534996acdcd1` |
| SHA-256 of the canonical 457-byte RuleProgramV2, `ruleProgramDigest` | `e796f81764d0ee452c591c852e98f59647518a1894d4bd0fd5c70b674ecc3ecb` |

The compiled record is constructed from `schemaVersion:2`, the policy digest, and each rule's `ruleId`, `ruleProgramRef` and `emitWhen` in policy order (COMP:103; pinned product `policy.rs:584-606`). I1-P's design-encoder check and I1-c's product-encoder check remain their later acceptance obligations. If the resolution of I1-RF-2 changes these bytes, recompute the affected pins.

## Non-blocking observations

- **I1-NB-1 (PROPOSAL.md:120,169; UNITS.md:58).** The admitted-SCC semantics and the documented possibility of later component merging support the chosen transient representative. The truth-table explanation only proves persistence of a cycle, not persistence of its least-member representative. Say that true identifies the representative of the current admitted component. Adding edges can merge it with an earlier-path component and make the former representative false; avoid claiming monotonicity of the whole representative proposition.
- **I1-NB-2 (PROPOSAL.md:373; UNITS.md:26,29-34).** The authoritative detailed unit breakdown makes I1-b2 depend on I1-b1. The proposal's short order summary instead lists only I1-a -> I1-b2. Make the short summary include I1-b1 -> I1-b2 so the two dependency presentations agree.
- **I1-NB-3 (PROPOSAL.md:321,355; UNITS.md:68).** LD-10 is explicitly deferred to the C law. A distinct selected kind=detector closure is the right emission binding, but a signed core manifest cannot automatically be reused for an arbitrary one-document detector tree. C2/C4 must define and review the host-derived detector tree's exact signed-core provenance and component/role joins, retain its bytes and descriptor, and select it in Plan. Treat LD-10 as a recommendation, not a completed closure-admission law.

## Review boundary

This is a law and contract-soundness verdict, not `ACCEPT-DESIGN-UNIT`, `ACCEPT-UNIT`, harness qualification, or live-provider evidence. I1-L and I1-P still need their own reviews.

Product source was inspected at the requested commit `2967905d8152a5f2e431cd8006e1b82f898c3fe2` using `git show`. The live checkout already had HEAD `3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f`; no source-pin conclusions depend on that moving checkout.

No cargo, product builds, tests, reference-model runs, delegation, repository edits or commits were performed. No application runtime/home state or 413 fixture was read. All written artifacts are under the requested review directory.
