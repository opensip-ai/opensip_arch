# Decision packet C (part 2) — C5–C9: reserved encodings, OD-1/OD-2 owner and fold, OD-101-1/2, D-006 unit and tree-accounting

Prepared by the D-000 orchestrator (Claude) for the human owner, 2026-08-27.
Measured at HEAD `4abb961aad98525ca8b992a24609a6286964a451` (D-292; COORD carries 277 `## D-NNN` headings; file 08 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`).

**This packet decides nothing.** Every factual claim below carries a citation to a file path plus heading/field/line, with sha256 for artifacts. Quoted bytes are verbatim. Where the record contains no value, the packet says "none in the record". Editorial judgment is confined to the lines labelled **Orchestrator recommendation** and to the consequence sentences inside each option form; none of it decides anything on the owner's behalf.

Items covered (numbering from `DECISIONS-NEEDED.md` section C):

| Item | Subject | Row | Row lead label today |
|---|---|---|---|
| C5 | Monorepo CI encodings (provider, YAML, path filters, caches, commands) | DR-121 | `OPEN` |
| C6 | Lifecycle encodings (atomic-rename equivalent, quarantine/journal format, lock grammar) | DR-107 | `PROPOSED-CLOSED-FOR-REVIEW` |
| C7 | OD-1 owner (DR-115 vs DR-120) and size caps; OD-2 fold (schema shape) | DR-103 | `OPEN` |
| C8 | OD-101-1 core implementation language; OD-101-2 signing/notarization ceremony | DR-101 | `OPEN` |
| C9 | D-006 unit (MB-to-bytes) and G02 tree-accounting | DR-115 / D-006 | `SATISFIED` (DR-115); DR-101 carries the leftover |

Lead labels: file 08 rows at lines 303, 289, 285, 283, 297 respectively (`docs/v2/architecture/08-decision-and-readiness-register.md`).

---

## 0. What the record does — and does not — reserve to "after Condition 5"

`STATUS.2026-08-26.md` §3.C says: "DR-120 adapter implementations, DR-125 SDK APIs, DR-107/121 encodings are reserved to *after Condition 5* — implementation, not design". `DECISIONS-NEEDED.md` C5 (line 46) asks "or explicitly post-Condition-5"; C6 (line 47) asks "or post-Condition-5". Those two files are the orchestrator's working documents, not the record. Measured against bytes:

**Where the literal phrase "after condition 5" occurs (repo-wide grep over `docs/`, `HANDOFF.D-000-orchestrator-live.txt`, `PROPOSAL.cross-citation-convention.md`):**

- `docs/coop/artifacts/packaging-leftover-join.v4.json` (`03251cc80cc774c12335ad038eedbb38ce73431623306f11fa1e75e40db61d07`, DR-120, current at D-266), `obligations[OBL-ADAPTER-IMPL].reason`: "D-108 records adapter implementations remain reserved. v14 namedOpenDecisions OD-P1 is 'Concrete packager, build tool, language toolchain, and command line', notDecidedHere true, owner after condition 5. …"; and `proposedLaterWork`: "A later leftover-design cycle may author an adapter implementation only after condition 5. This join does not invent that implementation."
- `docs/coop/artifacts/sdk-leftover-join.v6.json` (`e91d6e926830833d563bb89f3693d65328173af6f0d42275ad5339ef73880341`, DR-125, current at D-267), `proposedLaterWork`: "A later implementation successor after condition 5 may choose an SDK language, framework, or API surface. This join chooses none."
- Earlier versions of those same two lineages carry the phrase too, not identically: packaging v1–v3 `obligations[OBL-ADAPTER-IMPL].reason` is byte-identical to v4 ("owner after condition 5"), but their `proposedLaterWork` sentence is worded differently — "A later D-000 cycle may author an adapter implementation after condition 5. This join does not invent that implementation." — whereas v4 reads "only after condition 5"; sdk v1–v5 `proposedLaterWork` carry the sentence identical to v6. Three Claude review files of the packaging lineage (v2, v3, v4 `.review-independent.claude2.json`) quote them. Outside those two lineages and their reviews, no artifact and no COORD heading contains the phrase. No `COORDINATOR-DECISIONS.md` entry contains "after condition 5" or "after Condition 5" (grep: zero hits). Every COORD occurrence of "Condition 5" is either a readiness-formula sentence (forms include: "Condition 5 last", "Condition 5 remains the only implementation authorization", "Condition 5 remains NOT MET and last", "Condition 5 stays last", "Condition 5 is unchanged.", "Condition 5 is the only implementation", "Condition 5 still forbids", "Condition 5 remains the only authorization for `docs/v2/implementation/`." (lines 1546–1547, wrapped), "Condition 5 remains last." (lines 3464–3465, wrapped)) or D-001's definition sentence "**Condition 5:** the final authorization is a separate PREFERENCE-LADEN act, taken under D-000, adversarially reviewed, staged as the last commit so reverting it costs one `git revert`." (D-001, `## D-001 — Definition of "completed" for the V2 design`, line 287) — none is an encoding reservation.

**What the record says for DR-121 and DR-107 instead** (no "Condition 5" wording):

- DR-121 contract: `docs/coop/artifacts/monorepo-ci-contract.v16.json` (`67ca501660a2ba515ce37adc799c5418e4ffd156308189662245e5a5e45a2ddb`, recorded D-124) field `reservedForBlueprint`: `["CI provider", "YAML", "repository path filters", "caches", "commands", "implementation tooling"]`; and `selector.ownershipRecord.unitIdentity`: "… Concrete path encoding is reserved for the later blueprint; …".
- DR-121 join: `docs/coop/artifacts/monorepo-leftover-join.v4.json` (`03d4478c3ce6ea843f8a4ee3ea1dcc6d8c06bd661f71970fe836ce107b611481`, recorded D-277) `proposedLaterWork[2]`: "A later implementation successor may choose a CI provider, YAML, path filter, cache, command, or tooling. That successor must still prove the live file 02 properties. This join chooses none."
- DR-107 contract: `docs/coop/artifacts/lifecycle-generation-contract.v2.json` (`a5f9d6a35f83d64687cdd2a00ec3106251ae407e54a5538727c086dd8f9ab77b`, recorded D-107) `mechanismReservation.failureRule`: "A later implementation successor that cannot prove P-1..P-8 fails DR-107, regardless of mechanism choice."
- DR-107 join: `docs/coop/artifacts/lifecycle-leftover-join.v4.json` (`bcc76ee3d99c88c258496dcc5591682d4ad655e06049b802a383ba03d3f1ddfb`, recorded D-275) `proposedLaterWork[2]`: "A later implementation successor may choose a journal/lock/lease mechanism. That successor must still prove the live file 04 properties. This join chooses none."
- COORD D-107 Decision: "Concrete journal/lock/lease encoding remains reserved." COORD D-108 Decision: "Adapter implementations remain reserved." COORD D-110 Decision: "Exact SDK APIs/frameworks remain reserved."

**Consequence the owner should weigh before C5/C6.** For DR-120 and DR-125 the record itself places the reserved implementation "after condition 5". For DR-121 and DR-107 the record reserves the encodings to "a later implementation successor" / "the later blueprint" but never ties that to Condition 5 by name; the "after Condition 5" reading is the orchestrator's summary. Independently of which reading applies, both current joins classify the encoding obligation as `leftoverDesign: true`, `rideStanding: "not-capable-of-riding"`, with the reason "Undecided encodings are leftover-design (D-056)" (monorepo v4 `OBL-CI-ENCODING-RESERVED`) / "Those mechanisms remain reserved." (lifecycle v4 `OBL-ENCODING-RESERVED`). D-056's pinned subject (`docs/coop/artifacts/coordinator-decisions.D-056.turn2.draft.md`, `dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82`, `## Eligibility (narrow)`, gate 2) reads: "Every remaining acceptance-evidence member is **only** harness *execution*, fixture *execution*, or qualification *measurement*. Authoring of fixtures, schemas, successors, actor-joins, missing design, or still-UNDECIDED numbers is **not** a remainder this amendment may split." So, as the record stands, neither row can reach D-056 gate 2 while its encoding obligation is measured `leftoverDesign: true`. A "post-Condition-5" disposition, if that is the owner's choice, has to be recorded (a D-000 act plus a successor leftover-join that re-measures the obligation), not assumed.

---

## C5 — DR-121: monorepo CI encodings

### File 08 cells (line 303, verbatim)

`| DR-121 | Monorepo isolated component CI and independent release qualification | Release engineering + component owners + core/protocol/integration owners | [Monorepo CI model](02-distribution-and-components.md#monorepo-ci-and-independent-component-releases); DR-103/111/118/120 | Ownership/dependency selection model; per-component relevant-platform lane contract for build/test/package/sign/attest/SBOM/quality; shared-core lane; cross-component protocol/authority/lock/offline/bundle gates; change-impact and missed-dependency negative tests; independent release evidence | OPEN | Hard blocker for release architecture; does not require separate repositories or lockstep versions |`

Companion gate row DR-G16 (line 352): claim "Monorepo changes run all and only required component/core/integration qualification lanes from declared ownership/dependencies"; harness "named: harness.DR-G16.ci-isolation-integration (D-086; not authored; not QUALIFIED). change-impact corpus × component/language/platform matrix; forced dependency/ownership mutations; aggregate release selection"; owner "Release engineering + component/core/protocol/integration owners (owner cell made concrete 2026-08-13, C4)"; status `OPEN`.

### Current leftover-join and its obligations

`docs/coop/artifacts/monorepo-leftover-join.v4.json`, sha256 `03d4478c3ce6ea843f8a4ee3ea1dcc6d8c06bd661f71970fe836ce107b611481`, recorded at `## D-277 — Record monorepo leftover-join.v4 as DR-121 leftover remasurement` (ADOPTED 2026-08-24; Stage A dual ACCEPT 0/0; Stage B dual CONSENT 0/0). `summary.leftoverDesign` = `["OBL-G16-FX-AUTHORING", "OBL-CI-ENCODING-RESERVED"]`. `file08StatusToken` = `"OPEN"`.

- `OBL-CI-ENCODING-RESERVED` — `leftoverDesign: true`, `existingGate: "none"`, `executionObligationOwnerToday: "none"`, `rideStanding: "not-capable-of-riding"`. Reason (verbatim): "v16 reservedForBlueprint is CI provider, YAML, repository path filters, caches, commands, implementation tooling. G16 occupancy does not choose those encodings. Undecided encodings are leftover-design (D-056). This join does not invent them. g16 leftover-join.v4 does not steal OBL-CI-ENCODING-RESERVED. This join does not close it."
- `OBL-G16-FX-AUTHORING` — `leftoverDesign: true`, `namedCorpusNotAuthored`: `["change-impact corpus × component/language/platform matrix", "forced dependency/ownership mutations", "aggregate release selection"]`. Reason (excerpt): "G16 occupancy namedCorpusNotAuthored carries three live harness-cell corpus classes. Fixtures are unauthored. D-056 Decision clause 5: authoring fixtures remains design work …". (This obligation is packet D's delegation question, not C5; it is listed because it keeps DR-121 ineligible even if C5 is decided.)
- Not leftover: `OBL-CONTRACT-V16` (recorded-candidate-not-applied), `OBL-G16-HARNESS-SPEC`, `OBL-G16-EXECUTION` (qualification at G16), `OBL-G16-NAMED-CATALOG` (specified), `OBL-WINDOWS` (rides DR-111), `OBL-EE-7E` (rides G16), `OBL-HOSTILE-GOLDENS` (rides DR-127), `OBL-G13` (rides DR-118).

The join's `reservedForBlueprintVerbatim` field: `["CI provider", "YAML", "repository path filters", "caches", "commands", "implementation tooling"]` — six members.

### Candidate value in the record

**None in the record.** No artifact or COORD entry names a CI provider, a YAML shape, a path-filter table, a cache key/strategy, or a command line for DR-121. The contract is explicit that path filters are not authority: monorepo-ci-contract.v16 `selector.ownershipRecord.standing`: "AUTHORITATIVE committed design record. Not CI YAML. Not a path-filter table as authority."; and its `honestyRepairsFromV1[1]` (CODEX-V1-B2): "… Path filters are not authority."

### Constraints found in the record

1. Any later encoding "must still prove the live file 02 properties" (monorepo-leftover-join.v4 `proposedLaterWork[2]`).
2. The ownership record, not CI YAML, is the impact authority: v16 `selector.authority`: "The ownership record is the only impact authority. It includes: unit→owner maps, shared-surface→consumer-component edges, multiComponentSharedLaneSelection, roleApplicability (custodied DR-118 component→role map), validated platform sets, and the previous/current comparison basis. …"
3. Concrete path encoding is reserved: v16 `selector.ownershipRecord.unitIdentity` (quoted in §0).
4. Grok's standing instruction (`HANDOFF.D-000-orchestrator-live.txt`, `## Do not invent / do not SATISFY`): "… Do not invent … adapter implementations, reserved CI encodings, a journal, reserved SDK APIs, or Rosetta. …" and "Do not steal … OBL-CI-ENCODING-RESERVED / OBL-ENCODING-RESERVED …".
5. D-001 classes DR-121 as "Rule-governed architecture authoring with review" (D-001, "**Condition 2 — all 29 rows classified**" paragraph), not as a route-C product decision. Choosing a vendor/provider is nonetheless a preference no rule derives; the record does not classify that sub-choice.
6. D-056 gate 1 for DR-121 is also unopened: D-124 recorded monorepo-ci-contract.v16 as "DR-121's leftover T2-02 successor candidate … The candidate binds NOTHING. D-056 Class A is not opened." A later application-grade, no-express-reservation acceptance recording (the same form as B1–B3) would be required in addition to closing both leftover obligations.

### Owner cell

DR-121: "Release engineering + component owners + core/protocol/integration owners". DR-G16: "Release engineering + component/core/protocol/integration owners (owner cell made concrete 2026-08-13, C4)". Decision authority as the record states it: D-000 clause 1 — "Any decision that would have needed the user is put to an ADVERSARIAL subagent review (prompted to refute, not confirm), iterating to consensus." — routes user-needed decisions through adversarial review on the user's behalf; D-132 (`## D-132 — User Route C grant: complete the architecture`, user words item 9) records the user's delegation: "use them to answer questions and not me. between the 3 of you, decide."; the owner may nonetheless decide any item directly, in the user-made entry form D-132 itself takes ("PREFERENCE-LADEN user amendment").

### Decision form

**Option A — set the encodings now (design act).** You name the six members (or a subset, with the rest explicitly deferred). Consequences: a successor artifact (monorepo-ci-contract.v17 or a dedicated encoding contract) authored under D-000 dual review; a successor monorepo leftover-join re-measures `OBL-CI-ENCODING-RESERVED` `leftoverDesign: false`; `OBL-G16-FX-AUTHORING` still keeps DR-121 D-056-ineligible until packet D resolves fixture authoring; Class A must still be opened separately. The six members are vendor-specific choices the record does not derive; per D-000 clause 5 the entry would carry `PREFERENCE-LADEN` and a cheap overturn.

**Option B — defer with an explicit disposition (post-implementation-authorization).** You record that the six members are implementation, decided by the first blueprint-phase act after Condition 5, and direct the orchestrator to re-measure the obligation accordingly. Consequences: a D-000 entry records the disposition; a successor leftover-join moves `OBL-CI-ENCODING-RESERVED` from `not-capable-of-riding` to an explicit deferred standing (precedents in form: `OBL-WINDOWS` `rideStanding: "deferred-to-DR-111"` in the same join; DR-G05 row "caps deferred by explicit disposition (D-006)"; packaging v4's OD-P1 "owner after condition 5"). Whether a deferred-by-disposition encoding still counts as "missing design" under D-056 gate 2 is not settled by any byte — see Open questions. The row stays `OPEN` regardless until fixtures and Class A are resolved.

**Option C — delegate the choice to the orchestrator under D-000 review.** Same output as A but the choice is made on your behalf; because it is a vendor preference, expect CONTESTED risk under D-000 clause 2.

**Orchestrator recommendation:** Option B. The contract already treats CI YAML and path filters as non-authority and reserves the encodings to the blueprint; setting a provider now adds no readiness (gate 1 and fixtures still block) and would be the only vendor selection in the register.

### COORD-entry skeleton (DRAFT — not dispatched, not numbered)

```
## D-29x — DR-121 CI-encoding disposition: [SET | DEFERRED-TO-IMPLEMENTATION]

- **Date:** 2026-08-[dd]
- **Status:** DRAFT. Not reviewed. Requires Stage B dual CONSENT 0/0.
- **Decision type:** PREFERENCE-LADEN (route C; owner-made). [If Option B: RULE-GOVERNED
  recording of the owner's disposition.]
- **Subject:** [Option A: docs/coop/artifacts/monorepo-ci-contract.v17.json `<sha256>` |
  Option B: this entry; successor monorepo-leftover-join.v5 `<sha256>` re-measures the obligation]
- **Decision:** The owner [sets | defers] the six `reservedForBlueprint` members of
  monorepo-ci-contract.v16 (`67ca5016…`): CI provider, YAML, repository path filters, caches,
  commands, implementation tooling. [Option A: values <owner-supplied, verbatim>.] [Option B:
  each member is implementation, decided by the first blueprint-phase act after Condition 5;
  OBL-CI-ENCODING-RESERVED re-measures as `deferred-to-implementation` on the successor join.]
  Ownership record remains the only impact authority (v16 selector.authority). Does not SATISFY
  DR-121. Does not close OBL-G16-FX-AUTHORING. Does not open D-056 Class A. Does not edit file 08.
  Does not authorize `docs/v2/implementation/`.
- **Readiness effect:** Zero SATISFIED. Condition 2 stays 5 of 32. Condition 5 last.
- **Reversibility:** Total. Overturn: one supersession line + revert of C-D29x.
- **Commit:** C-D29x.
```

---

## C6 — DR-107: lifecycle encodings

### File 08 cells (line 289, verbatim)

`| DR-107 | Project/operation lock and multi-version generation semantics | Lifecycle + versioning | [Operations](04-lifecycle-delivery-and-operations.md) | DR-G18 crash-point harness; concurrent conflicting locks; immutable installs; leases/refcounts; reference-safe GC/removal; atomic dependency/state closure and migration | PROPOSED-CLOSED-FOR-REVIEW | Still hard blocker until reviewed successor and DR-G18 harness acceptance |`

Legend for the label (file 08 `## How to use the register`): "`PROPOSED-CLOSED-FOR-REVIEW` — V2 prose now addresses the review finding, but no binding successor or qualification is implied." Standing instruction (`HANDOFF.D-000-orchestrator-live.txt` line 25): "DR-107 remains `PROPOSED-CLOSED-FOR-REVIEW`. Do not flatten to OPEN."

Companion gate row DR-G18 (line 354): claim "Activation, migration, rollback, locks, leases, and removal are journaled and crash-safe"; harness "named: harness.DR-G18.lifecycle-generation-recovery (D-086; not authored; not QUALIFIED). crash at every journal write/fsync/rename/pointer and migration prepare/commit/abort/no-return transition; conflicting project locks; process death"; owner "Lifecycle + storage + versioning"; status `OPEN`.

### Current leftover-join and its obligations

`docs/coop/artifacts/lifecycle-leftover-join.v4.json`, sha256 `bcc76ee3d99c88c258496dcc5591682d4ad655e06049b802a383ba03d3f1ddfb`, recorded at `## D-275 — Record lifecycle leftover-join.v4 as DR-107 leftover remasurement` (ADOPTED 2026-08-24; Stage A dual ACCEPT 0/0; Stage B dual CONSENT 0/0). `summary.leftoverDesign` = `["OBL-G18-FX-AUTHORING", "OBL-ENCODING-RESERVED"]`. `file08StatusToken` = `"PROPOSED-CLOSED-FOR-REVIEW"`.

- `OBL-ENCODING-RESERVED` — `leftoverDesign: true`, `existingGate: "none"`, `executionObligationOwnerToday: "none"`, `rideStanding: "not-capable-of-riding"`. Reason (verbatim): "Contract v2 reserves the reviewed equivalent of atomic rename and the on-disk quarantine format. G18 occupancy names crash-injection sites and does not choose an on-disk journal format, lock-file grammar, lease API, solver, filesystem layout, or reviewed-equivalent of atomic rename. Those mechanisms remain reserved. This join does not invent them. g18 leftover-join.v5 does not steal OBL-ENCODING-RESERVED. This join does not close it."
- `OBL-G18-FX-AUTHORING` — `leftoverDesign: true`, `namedCorpusNotAuthored`: `["crash at every journal write/fsync/rename/pointer and migration prepare/commit/abort/no-return transition", "conflicting project locks", "process death"]` (packet D scope; listed because it independently keeps DR-107 ineligible).
- Not leftover: `OBL-CONTRACT-V2` (recorded-candidate-not-applied), `OBL-G18-HARNESS-SPEC`, `OBL-G18-EXECUTION` (qualification at G18), `OBL-G18-NAMED-CATALOG` (specified), `OBL-DR110-BOUNDARY` (rides DR-110).

### What exactly is reserved (contract bytes)

`docs/coop/artifacts/lifecycle-generation-contract.v2.json` (`a5f9d6a3…`), `mechanismReservation`:
- `file04Verbatim`: "The concrete lock/journal/lease mechanism is open, but a successor that cannot\nprove every property fails DR-107."
- `reserved`: `["on-disk journal format", "lock file grammar beyond DR-103 lockSchema", "lease implementation (fcntl, sqlite, custom)", "solver algorithm", "filesystem layout"]` — five members.
- `crashSafety.doesNotChoose`: "The reviewed equivalent of atomic rename is reserved. Fail-closed quarantine is required; the on-disk quarantine format is reserved."
- `crashSafety.rules[1]`: "Publication requires durable staged files/directories/journal, same-filesystem atomic rename or a reviewed equivalent, and recovery at each write/fsync/rename/pointer transition."

So the reserved set the owner would be setting is: (i) the reviewed equivalent of atomic rename, (ii) the on-disk quarantine format, and (iii) the five `mechanismReservation.reserved` members. Note "lock file grammar beyond DR-103 lockSchema": the lock's schema is DR-103's (component-manifest-schemas.v11 `lockSchema`, recorded D-104); the grammar reserved here is whatever lies beyond that schema. Also note D-106: "Locks remain deferred to DR-111." — no lock is producible until DR-111 closes (schemas.v11 `lockSchema.purpose`: "NO lock is producible until DR-111 closes").

### Candidate value in the record

**None in the record.** The contract names example lease implementations only as a parenthetical enumeration — "(fcntl, sqlite, custom)" — inside the *reserved* member; that is not a candidate. No journal format, quarantine format, or atomic-rename equivalent is named anywhere.

### Constraints found in the record

1. "A later implementation successor that cannot prove P-1..P-8 fails DR-107, regardless of mechanism choice." (contract v2 `mechanismReservation.failureRule`).
2. "That successor must still prove the live file 04 properties." (lifecycle-leftover-join.v4 `proposedLaterWork[2]`).
3. D-107 Decision: "Concrete journal/lock/lease encoding remains reserved. Generation-rollback remains distinct from DR-110 self-update rollback. No lock is producible."
4. Grok's standing instruction: "Do not invent … a journal …" (HANDOFF, `## Do not invent / do not SATISFY`).
5. D-001 classes DR-107 as "Rule-governed architecture authoring with review" ("DR-107 (+DR-G18)").
6. D-056 gate 1 is unopened for DR-107 as for DR-121 (D-107 recorded "v2 as DR-107's accepted design-contract candidate … DR-107 stays PROPOSED-CLOSED-FOR-REVIEW / OPEN. No SATISFIED."). DR-107's blueprint-impact cell adds a second bar: "Still hard blocker until reviewed successor and DR-G18 harness acceptance".

### Owner cell

DR-107: "Lifecycle + versioning". DR-G18: "Lifecycle + storage + versioning".

### Decision form

**Option A — set now.** You choose the atomic-rename equivalent, quarantine format, journal format, lock grammar, lease implementation, solver, and layout (or a subset, remainder deferred). Consequences: lifecycle-generation-contract.v3 under D-000 dual review, proving P-1..P-8 for the chosen mechanism; successor lifecycle leftover-join re-measures `OBL-ENCODING-RESERVED`; `OBL-G18-FX-AUTHORING`, Class A, and the "DR-G18 harness acceptance" bar remain. These are engineering-mechanism choices with security consequences (fail-closed quarantine, crash atomicity); D-001 treats the row as rule-governed, so an orchestrator-authored candidate is lawful, but any choice among named alternatives is a preference.

**Option B — defer with explicit disposition.** As C5 Option B: record that mechanisms are implementation, re-measure the obligation to a deferred standing. Same open question about D-056 gate 2.

**Option C — delegate to the orchestrator under D-000 review.** Lawful under D-001's classification; CONTESTED risk where reviewers disagree on mechanism.

**Orchestrator recommendation:** Option B for the on-disk formats and lease/solver/layout (pure implementation, contract already says "regardless of mechanism choice"); but consider setting only the *atomic-rename equivalent* policy now, because file 04's rule ("same-filesystem atomic rename or a reviewed equivalent") leaves open whether any equivalent is admissible on the D-002 platforms, and that is a design boundary G18 fixtures will need.

### COORD-entry skeleton (DRAFT — not dispatched, not numbered)

```
## D-29x — DR-107 mechanism-encoding disposition: [SET | DEFERRED-TO-IMPLEMENTATION]

- **Date:** 2026-08-[dd]
- **Status:** DRAFT. Not reviewed. Requires Stage B dual CONSENT 0/0.
- **Decision type:** [PREFERENCE-LADEN (route C; owner-made) | RULE-GOVERNED recording of the
  owner's disposition]
- **Subject:** [Option A: docs/coop/artifacts/lifecycle-generation-contract.v3.json `<sha256>` |
  Option B: this entry; successor lifecycle-leftover-join.v5 `<sha256>`]
- **Decision:** The owner [sets | defers] the reserved members of lifecycle-generation-contract.v2
  (`a5f9d6a3…`): the reviewed equivalent of atomic rename; the on-disk quarantine format; and
  mechanismReservation.reserved = on-disk journal format, lock file grammar beyond DR-103
  lockSchema, lease implementation (fcntl, sqlite, custom), solver algorithm, filesystem layout.
  [values or deferral standing <owner-supplied>]. P-1..P-8 remain the acceptance bar regardless
  of mechanism (failureRule). DR-107 stays `PROPOSED-CLOSED-FOR-REVIEW`; not flattened to OPEN.
  Does not SATISFY DR-107. Does not close OBL-G18-FX-AUTHORING. No lock is producible (DR-111).
  Does not open D-056 Class A. Does not edit file 08. Does not authorize `docs/v2/implementation/`.
- **Readiness effect:** Zero SATISFIED. Condition 2 stays 5 of 32. Condition 5 last.
- **Reversibility:** Total. Overturn: C-D29x.
- **Commit:** C-D29x.
```

---

## C7 — DR-103: OD-1 owner and size caps; OD-2 fold

### File 08 cells (line 285, status cell excerpt — verbatim)

Row head: `| DR-103 | Canonical component manifest/index/lock schemas, delegated roles, IDs, provenance/SBOM/attestation binding | Delivery + security | [Distribution](02-distribution-and-components.md), [Security](03-configuration-and-security.md) | Reviewed canonical schemas, duplicate/path rejection, signatures, exact-byte test corpus | **OPEN — design contract ACCEPTED 2026-08-13 (D-013); the fixture-corpus half remains open.** …`

The OD-1 sentence inside the status cell: "… named open decision **OD-1** (manifest byte size / tree entry count / path length / alias count caps — an unbounded-input surface at metadata-only admission; oversized-input refusal UNSPECIFIED, not implied) remains OPEN with its owner UNASSIGNED between DR-115 and DR-120, and choosing that owner is a separate decision — DR-115's `DECIDED-V1-NOT-INTEGRATED` annotation does not cover these numbers, because D-006 decided DR-G01..G05 only."

Blueprint-impact cell: "Hard blocker — design contract ACCEPTED (D-013); the exact-byte fixture-corpus half remains, at DR-120/DR-G15".

Observation (bytes, not a decision): the DR-103 cell still refers to "DR-115's `DECIDED-V1-NOT-INTEGRATED` annotation", while the DR-115 row's lead label is now "**SATISFIED 2026-08-14 (D-089 / D-056 Class B).**" (line 297). The DR-103 cell was written at D-013 (2026-08-13), before D-089. OD-2 is not named in the DR-103 cell; file 08 names it only once, in the DR-G31 row (line 367: "… not DR-103 leftover Windows-path/envelope/unicode/OD-1/OD-2; …"). schemas.v11 says the DR-103 row must name it at application time (below).

### Current leftover-join and its obligations

`docs/coop/artifacts/component-manifest-leftover-join.v9.json`, sha256 `e71dca64c78a8feea9e72df5ae846eb2843be50fb10d01d54d5b65714ed1d2c4`, recorded at `## D-282 — Record component-manifest leftover-join.v9 as DR-103 leftover remasurement` (ADOPTED 2026-08-26, turn 2; Stage A dual ACCEPT 0/0). `summary.leftoverDesign` = `["OBL-WINDOWS-PATH", "OBL-ENVELOPE-MISMATCH", "OBL-UNICODE-NORM", "OBL-OD-1", "OBL-OD-2"]`. `file08StatusToken` = `"OPEN"`. `authoredFixtureAudit`: `v6AuthoredCount: 51`, `filesPresent: 51`, `sha256Mismatches: 0`.

- `OBL-OD-1` — `leftoverDesign: true`, `existingGate: "none"`, `executionObligationOwnerToday: "none"`, `rideStanding: "not-capable-of-riding"`. Reason (verbatim): "File 08 named open decision OD-1: manifest byte size / tree entry count / path length / alias count caps. Owner UNASSIGNED between DR-115 and DR-120. UNDECIDED numbers are leftover-design (D-056). This join does not assign the owner and does not invent the numbers."
- `OBL-OD-2` — `leftoverDesign: true`, `rideStanding: "not-capable-of-riding"`. Reason (verbatim): "schemas.v11 namedOpenDecisions OD-2 is OPEN, still not folded at v11: whether to normalize TC-ACCEPT/TC-SIG/TC-BYTE-EXACT lock deferral onto a single conditionalRequires array-of-{member,gate} shape (Claude advisories CLAUDE-V6-A2/A3 on component-manifest-schemas.v6, carried as OD-2 into schemas.v11 namedOpenDecisions). Candidate owner is this schema surface (DR-103). Activation is a later successor of that artifact. registerEchoAtApplication: any later application/MF-6 of this surface must name OD-2 alongside OD-1 on the live DR-103 row. This join does not fold OD-2 and does not edit file 08."
- Other leftover (packet D scope): `OBL-WINDOWS-PATH` (three named Windows-only TC-PATH members: reserved device names, trailing dot, trailing space — fixture bytes unauthored), `OBL-ENVELOPE-MISMATCH` (TC-SIG conditional, unauthored), `OBL-UNICODE-NORM` ("BLOCKED on schemas.v11 pathRule / RJ-3. A later schema successor is required before this member can be scored.").
- `proposedLaterWork[4]`: "A later D-000 cycle may assign OD-1's owner and decide the numbers. This join does neither." `proposedLaterWork[6]`: "A later schemas successor may fold OD-2 (conditionalRequires shape). This join does not fold it."

### OD-1 as stated by the schema artifact (candidate owners)

`docs/coop/artifacts/component-manifest-schemas.v11.json` (`1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005`, recorded D-104), `namedOpenDecisions[OD-1]`:
- `decision`: "Size caps: manifest byte size, tree entry count, path length, alias count"
- `standing`: "NO caps are stated in these schemas, and that absence is a NAMED OPEN DECISION, not a default. Unbounded manifests are a denial-of-service surface at metadata-only admission - the treeCommitmentShape alternatives note's own self-flag, answered here with an owner rather than left rhetorical."
- `candidateOwners`: "DR-115's numeric-threshold machinery (which already owns the core's size/startup/memory numbers, DECIDED at D-006, with the measurement half at qualification) or DR-120's packaging contract (which owns what an adapter may emit). This artifact declines to mint the numbers: a cap is a product threshold, and thresholds in this corpus are product-owned, measured, and waiver-formed (the D-006 pattern)."
- `consequence`: "Until an owner states caps, admission enforces structural rules only, and oversized-input refusal is UNSPECIFIED, not implied - a fixture author must not assume it."

Candidate owners: exactly two are named — DR-115 and DR-120. Candidate cap values: **none in the record** (four cap quantities are named; no number for any of them).

Owner cells of the two candidates: DR-115 "Product + release engineering" (line 297; route C PREFERENCE-LADEN per D-001; lead label `SATISFIED` under D-056 Class B since D-089). DR-120 "Component architecture + release/developer-experience + language owners" (line 302; "Rule-governed architecture authoring with review" per D-001; lead label `OPEN`; accepted design-contract candidate component-packaging-contract.v14 at D-108, "Adapter implementations remain reserved").

### OD-2 as stated by the schema artifact

schemas.v11 `namedOpenDecisions[OD-2]`: `decision`: "Whether to normalize TC-ACCEPT/TC-SIG/TC-BYTE-EXACT lock deferral onto a single conditionalRequires array-of-{member,gate} shape (carried Claude v6 advisories V6-A2 and V6-A3)."; `standing`: "OPEN. Still not folded at v11. Previously recorded at v8 /openDecisions[OD-V8-1]; moved to namedOpenDecisions at v9."; `candidateOwners`: `["this schema surface (DR-103)"]`; `consequence`: "Each class already states the DR-111 gate unambiguously. Normalization is findability/shape, not a change to the no-lock-until-DR-111 rule. Activation is a later successor of this artifact, not a SATISFIED-GRADE corpus review by itself."; `registerEchoAtApplication`: "On any later application/MF-6 of this surface, the live DR-103 row must name OD-2 alongside OD-1. This artifact binds NOTHING and does not edit file 08."; `corpusAdvance`: "Corpus v2 is process-frozen against schemas.v9 so the v10/v11 digest citation stays resolvable. Advancing that draft to pin a later schema requires a corpus v3 or an explicit unfreeze-and-recite, not a silent retarget."

Candidate shape: exactly one is named — "a single conditionalRequires array-of-{member,gate} shape". The alternative is the status quo ("Each class already states the DR-111 gate unambiguously").

### Constraints found in the record

1. File 08: "choosing that owner is a separate decision" (DR-103 cell) — so the owner assignment is its own D-000 act, not a rider.
2. D-006 pattern for caps: "product-owned, measured, and waiver-formed" (schemas.v11 OD-1 candidateOwners); D-006's own G05 precedent: "caps become product decisions at the first component-acceptance decision under DR-G05's own evidence column" (`## D-006`, Proposed thresholds item 5).
3. D-006 turn-2 NOTE-03, quoted at D-013 Alternatives (b): "the closed status vocabulary stays closed; coining an analog would itself be a register-content decision" — any file 08 wording change is an MF-6 under its own cycle.
4. Fixture consequence: until caps exist "a fixture author must not assume" oversized-input refusal — so OD-1 gates any oversized-input fixture in packet D.
5. OD-2 fold requires a schemas successor (v12) and, per `corpusAdvance`, either a corpus v3 or an explicit unfreeze-and-recite of the corpus's schema pin.
6. Standing instruction: "Do not steal … OBL-OD-1 / OBL-OD-2" (HANDOFF).

### Owner cell

DR-103: "Delivery + security".

### Decision form — OD-1 (two decisions: owner, then numbers)

**A1 — assign to DR-115.** Caps join the D-006 threshold family as a scoped D-006 successor (form precedent: D-102 "PREFERENCE-LADEN scoped D-006 successor"). Consequence: consistent with "a cap is a product threshold"; but DR-115 is already `SATISFIED` (D-089) and its acceptance cell reads "Reproducible measurements and product-owned threshold decision" — adding caps means either (i) a D-006 successor with no file-08 status change (numbers decided, measurement at qualification, same as the existing thresholds), or (ii) an MF-6 note on DR-115; the record does not say which. Owner cell that would decide: "Product + release engineering".

**A2 — assign to DR-120.** Caps land in a component-packaging-contract successor (v15) as what an adapter may emit. Consequence: DR-120 is OPEN with reserved adapter implementations; the cap becomes an adapter-emission rule rather than a product threshold; measured at DR-G15. Owner cell: "Component architecture + release/developer-experience + language owners".

**A3 — set the four numbers now (with A1 or A2).** Values: none in the record; you would supply manifest byte size, tree entry count, path length, alias count. PREFERENCE-LADEN. Consequence: `OBL-OD-1` re-measures `leftoverDesign: false`; oversized-input refusal becomes specifiable and fixture-able.

**A4 — assign the owner now, defer the numbers with explicit disposition** (e.g. to first component acceptance, mirroring D-006's G05 clause). Consequence: owner assigned; `OBL-OD-1` could re-measure to a deferred standing; same D-056 gate 2 open question as C5/C6 ("still-UNDECIDED numbers is not a remainder this amendment may split").

**A5 — delegate owner choice and/or numbers to the orchestrator** (DECISIONS-NEEDED C7 says this "may be delegated"). Owner choice is rule-shaped enough to delegate (two named candidates, criteria quoted above); the numbers are product thresholds and would be decided on your behalf under D-000 with CONTESTED risk.

**Orchestrator recommendation:** A1 for the owner (the artifact's own words call a cap "a product threshold", and DR-115's D-006 machinery already carries the waiver form), combined with A4 (defer the four numbers to the first component-acceptance decision, D-006's G05 precedent), unless you want oversized-input fixtures authored in packet D — in which case A3 is needed first.

### Decision form — OD-2

**B1 — fold now.** Direct a schemas.v12 successor normalizing the three classes onto the named `conditionalRequires` array-of-{member,gate} shape, under D-000 dual review, plus the corpus v3 / unfreeze-and-recite step. RULE-GOVERNED (DR-103 is rule-governed per D-001; the shape is already named in the record). Delegable.

**B2 — record an explicit "do not fold" disposition.** The record itself says the status quo is unambiguous ("Each class already states the DR-111 gate unambiguously"). Consequence: `OBL-OD-2` re-measures closed-by-disposition on a successor join; the DR-103 row must still name OD-2 at the next MF-6 (`registerEchoAtApplication`).

**B3 — leave open** (no act). Consequence: `OBL-OD-2` stays `leftoverDesign: true` and continues to block D-056 gate 2 for DR-103.

**Orchestrator recommendation:** B1, delegated — the shape is uniquely named, the change is "findability/shape, not a change to the no-lock-until-DR-111 rule", and it removes one of five leftover obligations on DR-103 at zero product cost.

### COORD-entry skeleton (DRAFT — not dispatched, not numbered)

```
## D-29x — DR-103 OD-1 owner assignment [and caps] ; OD-2 [fold | disposition]

- **Date:** 2026-08-[dd]
- **Status:** DRAFT. Not reviewed. Requires Stage B dual CONSENT 0/0.
- **Decision type:** PREFERENCE-LADEN (route C; owner-made) for OD-1 owner/caps;
  RULE-GOVERNED for the OD-2 fold.
- **Subject:** [OD-1: this entry (owner) + <D-006 successor | component-packaging-contract.v15>
  `<sha256>` (numbers)] [OD-2: docs/coop/artifacts/component-manifest-schemas.v12.json
  `<sha256>`; corpus v3 or unfreeze-and-recite `<sha256>`]
- **Decision:** OD-1 (schemas.v11 `1c0b8868…` namedOpenDecisions[OD-1]; file 08 DR-103 cell
  "owner UNASSIGNED between DR-115 and DR-120") is assigned to [DR-115 | DR-120]. The four caps
  (manifest byte size, tree entry count, path length, alias count) are [set: <owner-supplied
  values> | deferred by explicit disposition to <trigger>]. OD-2 is [folded onto the single
  conditionalRequires array-of-{member,gate} shape at schemas.v12 | left as-is by explicit
  disposition]. A successor component-manifest leftover-join re-measures OBL-OD-1 / OBL-OD-2.
  Does not SATISFY DR-103. D-013's SATISFIED-refusal stands. Does not close OBL-WINDOWS-PATH,
  OBL-ENVELOPE-MISMATCH, or OBL-UNICODE-NORM. Does not edit file 08 (a later MF-6 names OD-2
  alongside OD-1 per registerEchoAtApplication). Does not authorize `docs/v2/implementation/`.
- **Readiness effect:** Zero SATISFIED. Condition 2 stays 5 of 32. Condition 5 last.
- **Reversibility:** Total. Overturn: C-D29x.
- **Commit:** C-D29x.
```

---

## C8 — DR-101: OD-101-1 core implementation language; OD-101-2 signing/notarization ceremony

### File 08 cells (line 283, verbatim)

`| DR-101 | Native signed distribution-core language, mandatory closure/TCB inventory, layering, signing/notarization, platforms | Architecture + release engineering | [Distribution](02-distribution-and-components.md) | Reviewed closure inventory and dependency graph; gate harnesses DR-G01–G05 | OPEN | Hard blocker for core implementation blueprint |`

Related cells: DR-118 blueprint impact (line 300): "Hard blocker for every slice-1 language role; does not mandate implementation language". DR-102 status cell (line 284) contains the phrase "a false measurement attributing the Rust substrate's handshake list to TypeScript major 1" — this is a description of a rejected v1 finding, not a language decision; it is quoted here for completeness. "Rust" occurs three times in file 08 (line 80, DR-011-R05 "Rust provider base v2"; line 284, DR-102 "Rust substrate's handshake list"; line 346, DR-G10 "TS major 1 and Rust merged major 2"), all naming the Rust provider/subprotocol, none as a core implementation-language selection.

### Current leftover-join and its obligations

`docs/coop/artifacts/distribution-core-leftover-join.v9.json`, sha256 `e6b235d3330a03e62acede6770919a413791c958a3e791eca5f677e822100bc7`, recorded at `## D-287 — Record distribution-core leftover-join.v9 as DR-101 leftover remasurement` (ADOPTED 2026-08-27; Stage A dual ACCEPT 0/0; Stage B dual CONSENT 0/0). `summary.leftoverDesign` = `["OBL-2", "OBL-D1", "OBL-D2"]`; `summary.languageNotDecided: true`, `ceremonyNotDecided: true`, `harnessSpecificationsNotAuthored: false`, `d006UnitUndecided: true`. `file08StatusToken` = `"OPEN"`.

- `OBL-D1` (`alias: "OD-101-1"`) — `leftoverDesign: true`, `existingGate: "none"`, `rideStanding: "not-capable-of-riding"`, `registerRowOwner: "Architecture + release engineering"`. Reason (verbatim): "Core implementation language is RESERVED on distribution-core-inventory-contract.v16. G01-G05 measure size, startup, memory, and component delta. They do not own a language choice. G13 is language-quality for supported analyzer roles, not core-language selection. This join does not mint Rust-as-core."
- `OBL-D2` (`alias: "OD-101-2"`) — `leftoverDesign: true`, `existingGate: "none"`, `rideStanding: "not-capable-of-riding"`. Reason (verbatim): "distribution-core-inventory-contract.v16 extracts signing ROLES and reserves ceremony/thresholds/notarization. G01-G05 do not own OS notarization or code-signing ceremony. DR-112 recovery ceremony and DR-110 repair-media trust remain adjacent, not owners."
- `OBL-2` — see C9.
- Not leftover: `OBL-1`, `OBL-D-INV`, `OBL-D-LAY`, `OBL-D3` (capable-of-riding named G01–G05).

D-287 Decision (excerpt): "OBL-2 remains leftover-design on the D-006 unit/accounting limb; OD-101-1 and OD-101-2 remain leftover-design; harness-spec authoring is measured closed against the current G01-G05 occupancy remasurements; execution remains qualification (D-056). … Does not mint Rust-as-core. Does not decide OD-101-2."

### The named open decisions as stated by the contract

`docs/coop/artifacts/distribution-core-inventory-contract.v16.json` (`429b8c7a9cd5c8f2b495337c055ccbd262e796ba1cc42efb173779c72018fb5b`, recorded D-114), `namedOpenDecisions`:
- `OD-101-1` — `decision`: "Core implementation language (the decision-column word 'language')"; `standing`: "RESERVED. File 02 says 'small native executable' and later uses native/Rust as quality framing, not a recorded language selection. This artifact does not mint Rust-as-core."; `owner`: "A later Route-C or rule-governed successor, not this extraction."
- `OD-101-2` — `decision`: "OS notarization ceremony and signing ceremony details"; `standing`: "RESERVED. Signing ROLES are listed (inventory/identity). Ceremony/thresholds/notarization remain a DR-101 decision. DR-112 recovery ceremony and DR-110 repair-media trust are adjacent input mechanics, not owners of core code-signing or OS notarization."; `owner`: "A later DR-101 successor, not this extraction. Same form as OD-101-1."
- `signingRolesNote`: "Role list is inventory/identity (file 03 proposed independent-release trust). Ceremony, thresholds, and OS notarization remain OD-101-2 on this row. DR-112 / DR-110 supply adjacent ceremony/repair-media mechanics; they do not own this fragment."
- Eligibility statement inside the contract (`recordedInputs.governingSources[1].role`, the COORD pin): "… DR-101 is ineligible under D-056 and remains so while OD-101-1 and OD-101-2 are open design reservations: the remainder is not only execution/measurement (gate 2) and is not already named at a condition-4 / DR-G* obligation (gate 3). A T2-02 contract alone does not unlock SATISFIED. …" and `whatThisDoesNotDo[0]`: "Does not SATISFY DR-101 until independently reviewed at SATISFIED-GRADE and recorded by a later D-000 MF-6. A T2-02 contract alone does not make the row D-056-eligible while OD-101-1 and OD-101-2 remain design reservations."

### Candidate values in the record

- OD-101-1: **none in the record** as a decision. The only language-shaped bytes are file 02's "small native executable" and "native/Rust as quality framing" (as characterised by v16's own standing sentence). The guard recurs in substance across the DR-101 lineage and its COORD recordings — dclj v9 `registerRowNote` "does not mint Rust-as-core" and `doesNot[6]` "Does not decide OD-101-1 or mint Rust-as-core."; COORD D-231, D-232, D-287 Decision paragraphs "Does not mint Rust-as-core" (line-wrapped in D-231 and D-287; on one line in D-232); packaging-leftover-join.v4 `obligations[OBL-ADAPTER-IMPL].reason` "and does not mint Rust-as-core." — and does not appear in monorepo-leftover-join.v4.
- OD-101-2: **none in the record.** Signing ROLES exist (v16 `inventorySchema.signingRolesNote`, inventory/identity only); no ceremony, threshold, or notarization procedure is named. Boundary with packet C1 (DR-112): schemas.v11 `whatThisDoesNotDo[2]`: "Does NOT define the signing ceremony: key custody, thresholds, rotation, expiry, revocation, quorum loss, recovery, and envelope validity are DR-112's surface." — that is the *index/component* signing ceremony. OD-101-2 is the *distribution-core code-signing and OS notarization* ceremony; v16 says DR-112 is "adjacent", not owner.

### Constraints found in the record

1. D-001 classes DR-101 as "Rule-governed architecture authoring with review"; v16's OD-101-1 owner sentence nonetheless names "A later Route-C or rule-governed successor" — the record leaves open whether the language choice is route C (preference) or rule-derived. A language selection is not derivable from any rule in the record.
2. DR-118's blueprint-impact cell: "does not mandate implementation language" — the analyzer-role decision (D-002 TypeScript) does not decide the core language.
3. Both OD-101-1 and OD-101-2 are named leftover on every current G01–G05 occupancy (`whatThisCloses.leftoverDesignRemainingOnDR101` = `[OBL-2, OBL-D1, OBL-D2]` per dclj v9 basedOn roles).
4. Deciding either OD alone does not make DR-101 eligible: v16 `recordedInputs.governingSources[1].role` (quoted above) requires both closed, plus OBL-2's unit/accounting limb (C9), plus Class A opening.
5. OS notarization is platform-bound: D-002 platforms are `macos/arm64`, `macos/x86_64`, `linux/x86_64`, `linux/arm64` (HANDOFF line 85; G01 v9 `basedOn.d002.role`: "Platforms: macOS (arm64, x86_64) and Linux (x86_64, arm64). Windows deferred with explicit disposition.").

### Owner cell

DR-101: "Architecture + release engineering". Gate owners (dclj v9 `liveGateOwners`): DR-G01 "Release engineering", DR-G02 "Architecture + release", DR-G03 "Release engineering", DR-G04 "Release engineering", DR-G05 "Component publisher + release".

### Decision form — OD-101-1

**A — set the core implementation language now.** You name it. Consequence: a distribution-core-inventory-contract.v17 (or a dedicated D-000 entry) records the selection as PREFERENCE-LADEN; `OBL-D1` re-measures `leftoverDesign: false`; the register's repeated "Does not mint Rust-as-core" guard becomes moot for that language; the "core implementation blueprint" hard blocker (DR-101 blueprint-impact cell) narrows to OD-101-2 + OBL-2 + Class A.

**B — defer with explicit disposition.** Record that the language is decided at the first core-implementation blueprint act (after Condition 5) and direct re-measurement. Consequence: DR-101 stays D-056-ineligible unless reviewers accept a deferred design reservation under gate 2 (open question); the row's own blueprint-impact cell says it is a "Hard blocker for core implementation blueprint", so a deferral pushes a blocker into the phase it blocks — reviewers may object.

**C — delegate.** Grok's and this orchestrator's standing rule is "does not mint Rust-as-core"; delegation would need your express lift of that rule, and the choice is a preference (CONTESTED risk).

**Orchestrator recommendation:** A. It is the one item in this packet that no later act can lawfully take on your behalf without a rule lift, it blocks the core blueprint by the row's own words, and every downstream artifact (G01–G05 fixtures, TCB inventory at DR-126, signing ceremony) depends on it.

### Decision form — OD-101-2

**A — set the ceremony now.** You specify code-signing ceremony (key custody, thresholds, rotation) and OS notarization per D-002 platform. Consequence: a DR-101 successor artifact under D-000 review; `OBL-D2` re-measures closed. Note the split: index/component signing ceremony numbers are packet C1 (DR-112 OD-112-1..4); OD-101-2 is core binary signing + notarization only.

**B — defer with explicit disposition** (e.g. "decided with OD-101-1 at the core-implementation blueprint act" or "decided jointly with DR-112 OD-112-1..4"). Consequence: same gate 2 open question; keeps DR-101 ineligible.

**C — delegate.** The ceremony is security-sensitive; DECISIONS-NEEDED D1 already invites you to reserve security-sensitive classes.

**Orchestrator recommendation:** B, tied to your C1 (DR-112) answer — a single signing ceremony decision covering index, component, and core binary signing is cheaper to review than two, and notarization is platform-mechanical once the language and toolchain exist.

### COORD-entry skeleton (DRAFT — not dispatched, not numbered)

```
## D-29x — DR-101 OD-101-1 core implementation language [SET | DEFERRED]; OD-101-2 [SET | DEFERRED]

- **Date:** 2026-08-[dd]
- **Status:** DRAFT. Not reviewed. Requires Stage B dual CONSENT 0/0.
- **Decision type:** PREFERENCE-LADEN (route C; owner-made). Overturn is one supersession line
  + one revert (D-000 clause 5).
- **Subject:** [docs/coop/artifacts/distribution-core-inventory-contract.v17.json `<sha256>` |
  this entry]; successor distribution-core-leftover-join.v10 `<sha256>` re-measures OBL-D1/OBL-D2.
- **Decision:** OD-101-1 (distribution-core-inventory-contract.v16 `429b8c7a…`
  namedOpenDecisions[OD-101-1], "Core implementation language") is [set to <owner-supplied> |
  deferred to <trigger>]. OD-101-2 ("OS notarization ceremony and signing ceremony details") is
  [set: <owner-supplied ceremony> | deferred to <trigger>]. DR-112 recovery ceremony and DR-110
  repair-media trust remain adjacent, not owners. Does not SATISFY DR-101 (OBL-2 unit/accounting
  limb and Class A remain). Does not change D-002 platforms. Does not edit file 08. Does not
  authorize `docs/v2/implementation/`.
- **Readiness effect:** Zero SATISFIED. Condition 2 stays 5 of 32. Condition 5 last.
- **Reversibility:** Total. Overturn: C-D29x.
- **Commit:** C-D29x.
```

---

## C9 — DR-115 / D-006: unit (MB-to-bytes) and G02 tree-accounting

### File 08 cells

DR-115 (line 297, verbatim): `| DR-115 | Numeric size/startup/memory thresholds and regression tolerances | Product + release engineering | release gates below; thresholds at `COORDINATOR-DECISIONS.md` D-006 (three-turn adversarial consensus, CONSENT `bfd8a758…`) | Reproducible measurements and product-owned threshold decision | **SATISFIED 2026-08-14 (D-089 / D-056 Class B).** — thresholds DECIDED 2026-08-13 (D-006: core ≤25 MB compressed / ≤80 MB installed; help/version cold p50/p95/p99 100/150/250 ms, warm p95/p99 50/100 ms; RSS steady/peak 40/50 MB help-version, 60/100 MB doctor read-only; named runner classes incl. native-Intel macOS x86_64, never Rosetta; G05 measurement-mandatory with caps at first component acceptance; regress-only 10% rule from the second qualified release; full waiver form); the MEASUREMENT half is discharged at qualification under the D-006 scope disposition | Architecture-preview SATISFIED under D-056 Class B (D-089). Measurement remains condition 4 / DR-G01..G05 / DR-012 qualification, not an architecture hard blocker. Not QUALIFIED. |`

Gate rows (lines 337–338): DR-G01 "threshold DECIDED (D-006); expiring waiver only"; DR-G02 "threshold DECIDED (D-006)"; DR-G02 required evidence "immutable tree inventory, dependency/TCB classification, size"; DR-G02 owner "Architecture + release".

### Where the leftover lives

The unit/accounting limb is measured on DR-101's join, not DR-115's (DR-115 has no leftover-join; it is `SATISFIED` Class B). `distribution-core-leftover-join.v9.json` (`e6b235d3…`, D-287) `obligations[OBL-2]` — `leftoverDesign: true`, `rideStanding: "not-capable-of-riding"`, `existingGate: "DR-G01, DR-G02, DR-G03, DR-G04, DR-G05"`. Reason (verbatim): "Independently reviewed G01-G05 occupancy remasurements now exist: G01 occupancy v9 (D-231), G02 occupancy v4 (D-232), G03 occupancy v5 (D-233), G04 occupancy v4 (D-234), G05 occupancy v4 (D-235), each dual ACCEPT 0/0, CANDIDATE-NOT-APPLIED, not QUALIFIED, live assurance stage SPECIFIED. Their frozen predecessors (G01 occupancy v1, G02 occupancy v1, G03 occupancy v4, G04 occupancy v1, G05 occupancy v1; CGHS v4 promised-path occupancies; Claude ACCEPT 0/0; Codex not reviewed) are not current. The authoring-of-specifications limb of OBL-2 is stale as an authoring claim. Remainder is (a) D-006 unit and G02 tree-accounting UNDECIDED, so size comparison cannot be scored, and (b) G01-G05 execution, which remains qualification (D-056). This join does not invent a D-006 unit and does not execute G01-G05."

COORD D-231 (G01 occupancy v9): "… Does not invent a D-006 unit or authorize 26214400 as the bound. …". COORD D-232 (G02 occupancy v4): "… Does not invent a D-006 unit or authorize 83886080 as the bound. Does not invent G02 tree-accounting. …".

### How the question is stated (verbatim; source is an unrecorded candidate)

`docs/coop/artifacts/core-gate-harness-specifications.v4.json` (`59f47a612f5f7b9ee073caec063a0dd336ca427a40a4aef2f08a174a44284b1b`). Standing of that file before anything is quoted from it: `status` "CANDIDATE-NOT-APPLIED", `reviewStatus` "AWAITING-INDEPENDENT-REVIEW", `binds` "NOTHING"; no COORD heading or entry names `core-gate-harness-specifications.v4` (grep over `COORDINATOR-DECISIONS.md`: zero hits); it reaches the record only as a digest pin in dclj v9 `recordedInputs`, and dclj v9 `obligations[OBL-2].reason` calls the "CGHS v4 promised-path occupancies" "not current". The five-alternative accounting list and the "1e6 or 2^20" readings below are sourced from this candidate, not from a recorded artifact; the recorded G02 v4 occupancy says only "accounting method named but not invented here" (EV-3 `exactByteIntent`). Field `d006UnitStanding`:
- `numerals`: "25 / 80 / 40 / 50 / 60 / 100 MB as written in D-006. Not restated as a byte constant here."
2. D-102's pinned subject (`docs/coop/artifacts/coordinator-decisions.D-102.turn2.draft.md`, item 5, line 178) defines "GiB = bytes/1024³" for fleet-class RAM matching ("RAM: macos `sysctl -n hw.memsize` bytes; Linux `MemTotal` kB × 1024. GiB = bytes/1024³. Match 7/14/16 ±0.75 GiB"); core-gate-harness-specifications.v4 `d006UnitStanding.byteMeaning` characterises this as "D-102 defines GiB as bytes/1024^3 only for RAM matching, not for these thresholds." — a candidate's (CANDIDATE-NOT-APPLIED, unrecorded) inference, not a D-102 statement. So the record holds one binary-unit definition, in a different domain, and no unit for the D-006 thresholds.
- `g02InstalledTreeAccounting`: "UNDECIDED. Logical file lengths vs allocated blocks vs metadata/xattrs vs links vs deduplicated inventory nodes is not decided here."
- `comparisonRule`: "A later D-006 unit/accounting successor decides the conversion and G02 domain. Until then a job records raw bytes and the D-006 numeral but cannot claim pass/fail against a byte constant invented here."
- `proposedLaterWork[0]`: "A later D-006 successor may define MB-to-bytes and G02 installed-tree accounting for G01/G02/G04. This artifact invents neither."
- `whatThisCloses.obl2Standing`: "Protocol authoring for G01-G05 advanced. OBL-2 is not closed while D-006 MB unit and G02 tree accounting remain UNDECIDED (CGHS-V1-SF1)."

Current occupancies: G01 v9 (`f28b0d97723550c8690eec2a6ac7803efba93fd797f266600b038b14e269277b`) `basedOn.d006.role`: "Threshold DECIDED: signed compressed distribution-core ≤ 25 MB per platform. Unit standing remains UNDECIDED. This occupancy does not invent 26214400 as an authorized bound …"; EV-2 `passProperty`: "… Size comparison to 25 MB is scored only after a D-006 unit successor. Exclusion membership is scored now." G02 v4 (`1bc247f779fa980ecde7d7a244effa6116f02a79be4a0ee74e0cedb168ccf360`) `basedOn.d006.role`: "Threshold DECIDED: immutable installed tree ≤ 80 MB; mandatory-closure inventory enumerated. Unit standing remains UNDECIDED. G02 tree-accounting remains UNDECIDED. This occupancy does not invent 83886080 as an authorized bound …"; EV-3 `exactByteIntent`: "Once authored: digest-pinned installed-tree raw byte count with accounting method named but not invented here. …"; EV-3 `passProperty`: "Raw installed-tree measurement is recorded. Size comparison to 80 MB is scored only after a D-006 unit-and-accounting successor. …"

D-006 itself (`## D-006 — DR-115: numeric size/startup/memory thresholds`): decision type "PREFERENCE-LADEN (route C). Numbers are not derivable from any rule; … Decided on the user's behalf; overturn is one supersession line + one revert." Thresholds: "signed compressed distribution-core ≤ 25 MB per platform"; "immutable installed tree ≤ 80 MB"; G04 "`--help`/`--version` RSS: steady baseline ≤ 40 MB, peak ≤ 50 MB … `doctor` read-only RSS: steady baseline ≤ 60 MB, peak ≤ 100 MB". Falsifiability note: "If early implementation shows a number infeasible, the lawful path is a successor decision with the measurement attached — never a silent waiver." A grep of the D-006 entry finds no "unit", "MiB", "1024", "decimal", or "accounting" token; the ambiguity is real in D-006's bytes.

### Candidate values in the record

- Unit: two readings are named, both by refusal, and only in the unrecorded CGHS v4 candidate — "1e6 or 2^20" (`d006UnitStanding.byteMeaning`); no recorded artifact names either. The constants `26214400` (G01) and `83886080` (G02) appear only as refused bounds; the Claude reviewer characterises 83886080 as "80 MiB in bytes" (`harness.DR-G02.core-installed.v3.review-independent.claude2.json` line 132: "The constant is 80 MiB in bytes, which is exactly the conversion D-006 has not authorized …"), and the Codex review of CGHS v2 (`core-gate-harness-specifications.v2.review-independent.codex.json`) reads the same constants as "25×2^20 and 80×2^20". No value is decided.
- Accounting: five alternatives named in one sentence of the unrecorded CGHS v4 candidate (`d006UnitStanding.g02InstalledTreeAccounting`) — "Logical file lengths vs allocated blocks vs metadata/xattrs vs links vs deduplicated inventory nodes" — none chosen; no recorded artifact names them (G02 v4 occupancy: "accounting method named but not invented here").
- Scope: the unit successor is said to cover "G01/G02/G04" (CGHS v4 `proposedLaterWork[0]`); G04's RSS numerals (40/50/60/100 MB) share the same undecided unit (CGHS v4 line 194: "Comparison to D-006 40/50/60/100 MB is scored only after the same D-006 unit successor named at d006UnitStanding.").

### Constraints found in the record

1. D-006 is PREFERENCE-LADEN; a unit/accounting decision is a *scoped D-006 successor* — form precedent D-102 ("PREFERENCE-LADEN scoped D-006 successor plus RULE-GOVERNED naming …"; note D-094/D-098/D-099/D-101 were CONTESTED attempts at that same successor before D-102 landed, which is why DECISIONS-NEEDED A2 lists them).
2. D-102's pinned subject (`docs/coop/artifacts/coordinator-decisions.D-102.turn2.draft.md`, item 5, line 178) defines "GiB = bytes/1024³" for fleet-class RAM matching ("RAM: macos `sysctl -n hw.memsize` bytes; Linux `MemTotal` kB × 1024. GiB = bytes/1024³. Match 7/14/16 ±0.75 GiB"); core-gate-harness-specifications.v4 `d006UnitStanding.byteMeaning` characterises this as "D-102 defines GiB as bytes/1024^3 only for RAM matching, not for these thresholds" — the candidate's (CANDIDATE-NOT-APPLIED, unrecorded) inference, not a D-102 statement. So the register already holds one binary-unit definition in a different domain; the record does not say whether consistency is required.
3. DR-115 is `SATISFIED` (D-089); the unit decision changes no DR-115 label. It changes DR-101's OBL-2 remainder (a). Even with unit and accounting decided, OBL-2's remainder (b) is execution (rides G01–G05, qualification) and DR-101 still carries OD-101-1/OD-101-2 (C8).
4. D-006's regression rule domain ("the CORE quantities of clauses 1–4 only") is unaffected by the unit choice but its 10% comparison is also unscorable until a unit exists (by the same `comparisonRule`).
5. Standing instruction: "Do not invent … UNDECIDED numbers …" (HANDOFF).

### Owner cell

DR-115: "Product + release engineering" (D-006 is route C; the human owner). DR-G02: "Architecture + release". DR-G01/G03/G04: "Release engineering".

### Decision form

**A — set both now (scoped D-006 successor).** You state (i) the MB-to-bytes conversion for the D-006 numerals (the unrecorded CGHS v4 candidate names the two readings: 1e6 or 2^20), scope G01/G02/G04, and (ii) the G02 installed-tree accounting rule (the same candidate names: logical file lengths, allocated blocks, metadata/xattrs, links, deduplicated inventory nodes — you pick the domain and the treatment of each). Consequences: one COORD entry, PREFERENCE-LADEN, cheap overturn; a successor dclj re-measures OBL-2 remainder (a) closed, leaving OBL-2 as execution-only; G01/G02/G04 occupancies become scorable once fixtures exist; no file 08 cell needs to change (thresholds remain "DECIDED (D-006)" — the successor is cited from the occupancies, not the cells), unless you want the DR-115 cell's D-006 parenthetical to name the successor (an MF-6).

**B — set the unit only, defer accounting with disposition** (e.g. "accounting fixed by the first G02 measurement act with product sign-off", mirroring D-006's "EXACT machine identifiers … are pinned by the G03/G04 harness-naming" pattern). Consequence: G01 and G04 become scorable; G02 stays unscorable; OBL-2 remainder (a) narrows but stays leftover.

**C — defer both with explicit disposition.** Consequence: G01/G02/G04 stay unscorable; DR-101 keeps three leftover obligations; no readiness change either way (DR-115 already SATISFIED).

**D — delegate to the orchestrator.** The unit choice is binary between two readings named in the CGHS v4 candidate and could be decided under D-000 review; accounting has five named components and is closer to a product/measurement preference.

**Orchestrator recommendation:** A. It is the cheapest item in the packet (one entry, two sentences, two candidate-named alternatives for the unit — CGHS v4, unrecorded), it unblocks scoring for three gates, and it is the only item here that the reviewers have repeatedly flagged as a defect in D-006's own bytes rather than a reservation by design.

### COORD-entry skeleton (DRAFT — not dispatched, not numbered)

```
## D-29x — D-006 successor: unit and G02 installed-tree accounting for G01/G02/G04

- **Date:** 2026-08-[dd]
- **Status:** DRAFT. Not reviewed. Requires Stage B dual CONSENT 0/0.
- **Decision type:** PREFERENCE-LADEN scoped D-006 successor (form: D-102). Does not re-decide
  any D-006 numeral. Does not mark QUALIFIED.
- **Subject:** this entry; successor distribution-core-leftover-join.v10 `<sha256>` re-measures
  OBL-2 remainder (a).
- **Decision:** For the D-006 numerals "25 / 80 / 40 / 50 / 60 / 100 MB" (CGHS v4 `59f47a61…`
  d006UnitStanding.numerals), MB means [1e6 | 2^20] bytes for DR-G01, DR-G02, and DR-G04.
  G02 installed-tree accounting is [<owner-supplied rule over: logical file lengths, allocated
  blocks, metadata/xattrs, links, deduplicated inventory nodes>]. D-102's GiB definition for RAM
  matching is unchanged. Size comparison at G01/G02/G04 becomes scorable once fixtures exist;
  execution remains condition 4. Does not SATISFY DR-101 (OD-101-1, OD-101-2, Class A remain).
  DR-115 stays SATISFIED (D-089). Does not edit file 08. Does not authorize
  `docs/v2/implementation/`.
- **Readiness effect:** Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 unchanged.
  Condition 5 last.
- **Reversibility:** One supersession line + revert of C-D29x (D-006 overturn form).
- **Commit:** C-D29x.
```

---

## Cross-item facts the owner should hold at once

1. **None of C5–C9 changes Condition 2 by itself.** Each decision closes one or more `leftoverDesign: true` obligations on a join; every affected row (DR-121, DR-107, DR-103, DR-101) also carries an unauthored-fixture obligation (packet D) and an unopened D-056 gate 1 (Class A recording, same form as B1–B3). DR-115 is already `SATISFIED`. Condition 2 stays "5 of 32" after any combination of C5–C9 answers.
2. **The "after Condition 5" reservation is record-backed only for DR-120 and DR-125** (§0). For DR-107/DR-121 the record says "a later implementation successor" / "reserved for the later blueprint" without naming Condition 5; a post-Condition-5 disposition must be recorded to exist.
3. **D-056 gate 2 and deferred design.** Gate 2's text excludes "missing design, or still-UNDECIDED numbers" from a splittable remainder. Whether an obligation deferred by explicit owner disposition (Options B above) still counts as "missing design" is not answered by any byte; the closest precedents are DR-G05's "caps deferred by explicit disposition (D-006)" (a gate cell, not a row eligibility ruling) and the D-002/D-010 row-level deferral limb (D-056: "Deferral limb of condition 2 (D-002 / D-010), not this amendment."). A reviewer under D-000 may accept or reject that reading; expect the question at Stage B.
4. **Ordering dependencies inside this packet.** C9 (unit) gates C8's G01–G05 scoring but not C8's decisions. C7 OD-1 numbers gate any oversized-input fixture in packet D. C8 OD-101-2 overlaps with packet C1 (DR-112 ceremony) at the boundary quoted in C8. C8 OD-101-1 gates DR-126's TCB inventory identity only indirectly (v16 ID-DEP-K2 routes L-TCB identity to "DR-126 / G22"; not re-measured here).

---

## Citations relied on (path + heading/field/line; sha256 for artifacts)

- `docs/v2/architecture/08-decision-and-readiness-register.md` (`e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`): `## How to use the register` (status vocabulary, lines 12–29); rows at lines 283 (DR-101), 284 (DR-102, "Rust substrate" phrase), 285 (DR-103), 289 (DR-107), 297 (DR-115), 300 (DR-118), 302 (DR-120), 303 (DR-121); gate rows 337 (DR-G01), 338 (DR-G02), 341 (DR-G05), 351 (DR-G15), 352 (DR-G16), 354 (DR-G18); `## Blueprint-readiness decision` conditions 2 and 5 (lines 370–395); condition-2 snapshot row (line 415).
- `docs/coop/COORDINATOR-DECISIONS.md` (277 `## D-` headings at HEAD `4abb961`): `## D-000 — Delegation protocol adopted` clauses 1, 2, 5; `## D-001 — Definition of "completed" for the V2 design` ("Condition 2 — all 29 rows classified" paragraph, lines 247–254; "Condition 5" paragraph, line 287); `## D-006 — DR-115: numeric size/startup/memory thresholds` (Decision type, Proposed thresholds 1–6, Falsifiability note); `## D-013 — DR-103: the accepted manifest/index/lock design contract` (Alternatives (b), quoting D-006 turn-2 NOTE-03's closed-vocabulary sentence); `## D-056 — Condition-2 SATISFIED versus qualification remainder`; `## D-089 — Record DR-115 SATISFIED under D-056 Class B`; `## D-102 — D-006 fleet-class successor plus G03/G04 named identifiers` (Decision type); `## D-104` (schemas.v11 recording, heading only); `## D-106 — Record component-manifest-fixture-corpus.v6 …` (Decision: "Locks remain deferred to DR-111"); `## D-107 — Record lifecycle-generation-contract.v2 …` (Decision); `## D-108 — Record component-packaging-contract.v14 …` (Decision: "Adapter implementations remain reserved"); `## D-110 — Record component-sdk-contract.v4 …` (Decision: "Exact SDK APIs/frameworks remain reserved"); `## D-114 — Record distribution-core-inventory-contract.v16 …`; `## D-124 — Record monorepo-ci-contract.v16 …`; `## D-132 — User Route C grant: complete the architecture` (user words items 9, 10); `## D-133 — D-056 successor: SATISFIED eligibility is a property`; `## D-160 — Record distribution-core-leftover-join.v3 …` (Decision naming OD-101-1/2); `## D-161 — Record component-manifest-leftover-join.v2 …` (Decision naming OD-1/OD-2); `## D-231` and `## D-232` (Decision paragraphs, "26214400" / "83886080" refusals, tree-accounting); `## D-275 — Record lifecycle leftover-join.v4 …`; `## D-277 — Record monorepo leftover-join.v4 …`; `## D-282 — Record component-manifest leftover-join.v9 …`; `## D-287 — Record distribution-core leftover-join.v9 …`.
- `docs/coop/artifacts/coordinator-decisions.D-056.turn2.draft.md` (`dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82`): `## Eligibility (narrow)` gates 1–5; `## Ineligible today` table; Decision clauses 1, 4, 5.
- `docs/coop/artifacts/monorepo-leftover-join.v4.json` (`03d4478c3ce6ea843f8a4ee3ea1dcc6d8c06bd661f71970fe836ce107b611481`): `summary.leftoverDesign`, `obligations[OBL-CI-ENCODING-RESERVED]`, `obligations[OBL-G16-FX-AUTHORING]`, `obligations[OBL-WINDOWS]`, `reservedForBlueprintVerbatim`, `proposedLaterWork`, `file08StatusToken`, `liveGateOwners`.
- `docs/coop/artifacts/monorepo-ci-contract.v16.json` (`67ca501660a2ba515ce37adc799c5418e4ffd156308189662245e5a5e45a2ddb`): `reservedForBlueprint`, `selector.ownershipRecord.standing`, `selector.ownershipRecord.unitIdentity`, `selector.authority`, `honestyRepairsFromV1[1]` (CODEX-V1-B2).
- `docs/coop/artifacts/lifecycle-leftover-join.v4.json` (`bcc76ee3d99c88c258496dcc5591682d4ad655e06049b802a383ba03d3f1ddfb`): `summary.leftoverDesign`, `obligations[OBL-ENCODING-RESERVED]`, `obligations[OBL-G18-FX-AUTHORING]`, `proposedLaterWork`, `file08StatusToken`, `liveGateOwners`.
- `docs/coop/artifacts/lifecycle-generation-contract.v2.json` (`a5f9d6a35f83d64687cdd2a00ec3106251ae407e54a5538727c086dd8f9ab77b`): `mechanismReservation` (`file04Verbatim`, `reserved`, `failureRule`), `crashSafety.rules`, `crashSafety.doesNotChoose`.
- `docs/coop/artifacts/component-manifest-leftover-join.v9.json` (`e71dca64c78a8feea9e72df5ae846eb2843be50fb10d01d54d5b65714ed1d2c4`): `summary.leftoverDesign`, `obligations[OBL-OD-1]`, `obligations[OBL-OD-2]`, `obligations[OBL-UNICODE-NORM]`, `obligations[OBL-WINDOWS-PATH]`, `obligations[OBL-ENVELOPE-MISMATCH]`, `authoredFixtureAudit`, `proposedLaterWork[4]`, `proposedLaterWork[6]`.
- `docs/coop/artifacts/component-manifest-schemas.v11.json` (`1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005`): `namedOpenDecisions[OD-1]` (decision, standing, candidateOwners, consequence); `namedOpenDecisions[OD-2]` (decision, standing, candidateOwners, consequence, registerEchoAtApplication, corpusAdvance); `whatThisDoesNotDo[2]` signing-ceremony sentence; `lockSchema.purpose` "NO lock is producible until DR-111 closes".
- `docs/coop/artifacts/distribution-core-leftover-join.v9.json` (`e6b235d3330a03e62acede6770919a413791c958a3e791eca5f677e822100bc7`): `registerRowNote`, `basedOn.occupancyG01V9`/`occupancyG02V4` roles, `obligations[OBL-2]`, `obligations[OBL-D1]`, `obligations[OBL-D2]`, `summary`, `liveGateOwners`, `recordedInputs` (CGHS v4 pin).
- `docs/coop/artifacts/distribution-core-inventory-contract.v16.json` (`429b8c7a9cd5c8f2b495337c055ccbd262e796ba1cc42efb173779c72018fb5b`): `namedOpenDecisions[OD-101-1]`, `namedOpenDecisions[OD-101-2]`, `signingRolesNote`, `recordedInputs.governingSources[1].role` (D-056 eligibility sentence), `whatThisDoesNotDo[0]`, `identityDependencies` ID-DEP-K1/K2, obligation rows OBL-D1/OBL-D2 (lines 53–67).
- `docs/coop/artifacts/core-gate-harness-specifications.v4.json` (`59f47a612f5f7b9ee073caec063a0dd336ca427a40a4aef2f08a174a44284b1b`; `status` "CANDIDATE-NOT-APPLIED", `reviewStatus` "AWAITING-INDEPENDENT-REVIEW", `binds` "NOTHING"; not recorded in any COORD entry; cited via the dclj v9 `recordedInputs` digest pin only): `d006UnitStanding` (numerals, byteMeaning, g02InstalledTreeAccounting, comparisonRule), `whatThisCloses` (leftoverDesignRemainingOnDR101, obl2Standing), `proposedLaterWork[0]`, line 194 G04 unit note.
- `docs/coop/artifacts/harness.DR-G01.core-download.v9.json` (`f28b0d97723550c8690eec2a6ac7803efba93fd797f266600b038b14e269277b`): `basedOn.d002.role`, `basedOn.d006.role`, EV-2 and EV-5 `exactByteIntent`/`passProperty`, `proposedLaterWork`.
- `docs/coop/artifacts/harness.DR-G02.core-installed.v4.json` (`1bc247f779fa980ecde7d7a244effa6116f02a79be4a0ee74e0cedb168ccf360`): `basedOn.d006.role`, EV-3 `exactByteIntent`/`passProperty`, `doesNot` (unit, accounting), `proposedLaterWork`.
- `docs/coop/artifacts/harness.DR-G02.core-installed.v3.review-independent.claude2.json`: Claude reviewer sentence characterising 83886080 as "80 MiB in bytes" (line 132).
- `docs/coop/artifacts/core-gate-harness-specifications.v2.review-independent.codex.json`: Codex reviewer sentence "Those constants are 25×2^20 and 80×2^20."
- `docs/coop/artifacts/packaging-leftover-join.v4.json` (`03251cc80cc774c12335ad038eedbb38ce73431623306f11fa1e75e40db61d07`): `obligations[OBL-ADAPTER-IMPL].reason` ("owner after condition 5"; "and does not mint Rust-as-core."), `proposedLaterWork` ("only after condition 5"); packaging-leftover-join.v1/v2/v3 `obligations[OBL-ADAPTER-IMPL].reason` (byte-identical to v4) and `proposedLaterWork` ("after condition 5", differently worded).
- `docs/coop/artifacts/sdk-leftover-join.v6.json` (`e91d6e926830833d563bb89f3693d65328173af6f0d42275ad5339ef73880341`): `proposedLaterWork` ("after condition 5"); sdk-leftover-join.v1–v5 `proposedLaterWork` (identical sentence).
- `HANDOFF.D-000-orchestrator-live.txt`: line 25 (DR-107 do-not-flatten), `## Do not invent / do not SATISFY` (lines 79–85).
- `STATUS.2026-08-26.md` §3.C (line 60) and `DECISIONS-NEEDED.md` §C items C5–C9 — cited only as the orchestrator's own framing, not as record.

## Open questions not resolvable from bytes

1. Whether an obligation deferred by explicit owner disposition (C5/C6/C7-A4/C8-B/C9-C) counts as "missing design, or still-UNDECIDED numbers" under D-056 gate 2, or as a lawful deferral that lets gate 2 hold. No COORD entry or artifact rules on a sub-row deferral; the only deferral limb D-056 names is the D-002/D-010 row-level limb.
2. For OD-1 assigned to DR-115: whether the caps require an MF-6 note on the (already `SATISFIED`) DR-115 row or only a D-006 successor cited from the schemas/occupancies. The record shows both mechanisms in use (D-089 MF-6 for the label; D-102 successor without label change) and does not say which applies to added thresholds.
3. Whether the D-102 GiB definition for RAM matching (`GiB = bytes/1024³`, D-102 turn-2 draft line 178) constrains the D-006 MB unit choice for consistency. CGHS v4 (a candidate) treats the two as separate domains; no recorded entry requires or forbids a common base.
4. Whether OD-101-1 is route C (preference) or rule-governed: D-001 lists DR-101 as rule-governed; v16's OD-101-1 owner sentence says "A later Route-C or rule-governed successor". The record does not resolve the disjunction.
5. Whether OD-101-2 should be decided jointly with DR-112 OD-112-1..4 (packet C1). v16 says DR-112 is "adjacent, not owner"; nothing forbids or requires a joint act.
6. The stale reference in the DR-103 cell to "DR-115's `DECIDED-V1-NOT-INTEGRATED` annotation" (DR-115 is now `SATISFIED`): whether the owner wants that reconciled at the next DR-103 MF-6 (component-manifest-leftover-join.v9 `proposedLaterWork[0]` already anticipates an MF-6 rewriting that cell).
