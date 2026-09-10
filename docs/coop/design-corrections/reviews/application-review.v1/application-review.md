# Independent application / per-row review — OpenSIP D-372 proposed application

**Verdict: CHANGES_REQUIRED**

**Reviewer:** actual Claude, fresh independent application/per-row reviewer. I authored none of the
subject bytes. No agents were used. No repository, candidate or staged byte was modified; nothing was
committed or pushed; no product implementation was performed or authorized.

**Model continuation (explicit):** this review was started under Claude Fable 5.1 in session
`68ddc51b-5362-4417-a2ca-7a502c8a25d3` and terminated without any verdict by an API 429 Fable usage
limit. That evidence is retained verbatim and unmodified at
`application-review.v1/response.json` (SHA-256 `e0ef83cb2f54af2e106b0c09fb91dbe111b0e3d6af6d6274a4955e4f947fac4d`;
`"api_error_status": 429`, `"terminal_reason": "api_error"`, `"result": "You've reached your Fable
limit."`). The prior run produced **no verdict, no acceptance and no finding set**; nothing in it is
relied upon here and no prior-model agreement is inferred. This review was completed under
**Claude Opus 5** (`claude-opus-5`) resuming the same session per
`application-review.v1/process.opus-resume.v1.json`. Every conclusion below is this session's own,
re-derived from the frozen bytes.

**Standing of this review:** substantive per-row and documentation-correctness review of proposed
FUTURE effective content, conditional on external prerequisites that have not occurred. This is
**not** final application authority. A narrow final exact-evidence/application-binding review must
follow actual independent design acceptance of candidate v3 and the fresh blind consumer B review.

---

## 1. Custody and hash verification

Verified before and after review; nothing drifted.

| Subject | SHA-256 | Result |
|---|---|---|
| Application manifest `application-subject.v1.json` | `9260c1dedbc8de3151e5265983716a180df27f769226de2c49aeac593254e842` | matches required hash, before and after |
| Staged files (16 entries) | per manifest | 16/16 byte- and length-exact, 0 mismatches, before and after |
| Parent design manifest `candidate-subject.v3.json` | `e3365d6e64cb5b0260ec7261af5c3e554504c9ab9515456f680aeb01b31b76fd` | matches the value recorded in the application manifest |
| Parent candidate snapshot | 1317 files | 1317/1317 verified; 0 mismatches; 0 files on disk outside the manifest; 0 manifest entries missing |
| `application-validation-plan.v1.md` | `c5dcb5797513bd484e140f321f587cdf45447f40c0b06db088415bc40fc42a21` | read as a separate procedural proposal, not part of the frozen staged content |

Before-image provenance of the 14 documentation edits: all 14 `beforeSha256` values equal the current
repository working tree. Five (`START-HERE.md`, `catalog/current-design.md`, files 08, 10, 12, 13 —
six paths in total) are also present in the frozen candidate at those exact hashes; the remaining
eight are absent from the candidate and equal both the working tree and `HEAD`, i.e. unchanged
inherited files. That is consistent and lawful.

Product contract pins named by the row map were verified in both the candidate and the repository:
`security-and-lifecycle.md` `cd0d6e2dfda35e48df3c14db5941b47c6b7bbaa8f9fbc2c0efb9fdcbc801f4e7`;
`native-evidence.md` `e1fef3092aa1c00b9272f5a6d6a46ee7c79f5af200fc838f3554bb681c956dc7`;
`admission-and-qualification.md` `7c28fbae2566c84016c1775f8b8676701ee8596804b6b16339b5bc71a14583ca`;
`workflows-and-surfaces.md` `3ae351fc41592513997eb1e59af33c3ccbdd92d7f088260e854231f61de48a1e`;
`identity-and-evidence.md` `1252e866a95bdf54c0fc2f1dd600798bc379703c9d9807bcb8a818bb27a735e5`.
The inherited account `docs/coop/completion/architecture-application.v1.json`
`15b3932adaf1c37f43a3b12e0af66fedbddc10cdd396c64105ac170c6d4bd7f3` matches in the repository; it is
**not** inside candidate v3, so a reviewer confined to the frozen candidate cannot verify it there.

**Positive finding.** All 17 `compatibleInheritedAccount` selectors were resolved against the real
file and are correct: `/rows/0..16` map in order to DR-101, 103, 105, 107, 111, 112, 114, 118, 120,
121, 122, 124, 125, 126, 127, 131, 133. No invented selector was found. Every contract section
selector used by the row map (`S2`–`S15`, native `§1`–`§12`, admission `§1`–`§4`, identity `§2`–`§5`,
workflow `§1`–`§12`) resolves to a real heading in the pinned bytes. Every one of DR-G01..G32 is named
by at least one row.

---

## 2. Overall verdict and the reasons for it

The proposed content is, in substance, a serious and largely well-built full-product design account.
Its contracts are detailed, its exclusions are honest, and its refusal to claim measurement or
confinement is consistent. I nevertheless return **CHANGES_REQUIRED**, because the promised final
application procedure **cannot lawfully apply these exact bytes** even after design and blind
acceptance, and because five of the twenty-eight rows do not have an individually defensible grade
on the evidence named for them.

### MUST findings

**M-1 — Two load-bearing evidence artifacts do not exist and are created by no edit.**
Ten of the fourteen staged documents cite `docs/coop/design-corrections/application.v1.json` as *the*
record that "pins the exact subjects and evidence", and the staged register cites
`docs/coop/design-corrections/readiness-row-map.v1.json` for "exact successor hashes/selectors,
compatible inherited accounts, required release gates and independent grades". Neither file exists in
the repository, in candidate v3, or in the staged set. `documentation-proposal.json` contains exactly
14 edits, all `.md`; no edit creates either file. Independently verified by resolving every link in
the staged markdown: 260 links resolve, and the only missing-file failures are these two paths (11
occurrences). The entire evidentiary weight of the new readiness account is delegated to bytes nobody
has reviewed and no act creates.

**M-2 — The staged register and the staged row map contradict each other; the frozen bytes cannot both be applied.**
The register's condition-2 cell states the 28 rows "have independently accepted full-product design
dispositions in the per-row application map below". The map itself declares
`"standing": "PROPOSED per-row application map; no grade or acceptance yet"` and records
`"independentGrade": "PENDING-APPLICATION-REVIEW"` for **all 28 rows** (verified programmatically).
The same contradiction recurs in condition 1: the register says "reviewed prospective dispositions"
for the 30 evaluation residuals, while `evaluation-residual-dispositions.proposed.json` carries
`"reviewStatus": "PENDING"` on all 30 and declares it "does not close DR-011-R12 before independent
review/application". The row map must change before it can be applied, which means the manifest's
frozen bytes are not the applicable bytes.

**M-3 — Condition 3 is asserted MET without exact evidence and by re-labelling five untouched rows.**
The cell claims MET "through the retained fresh actual-Claude review of mixed final bytes, Codex
technical review/assent, blind consumer B and independent application review under DR-201–205". It
cites no path and no hash. None of those four reviews has occurred. DR-201..205 are untouched by the
staged edit and still carry their 2026-08-13 acceptances against their original subjects and digests.
The pre-staged text was correct that "D-369's accepted reviews remain evidence for their original
subjects"; the replacement reads five historical acceptances as covering a scope they never reviewed.

**M-4 — Condition 4 cites no artifact, and the artifact it depends on is applied by no edit.**
The cell asserts "all32 DR-G01–32 mappings name current contracts, owners, harness scope and
acceptance requirements". That content lives in
`docs/coop/design-corrections/qualification-gates.proposed.json` (32 items verified, each with
`currentContract`, `owner`, `harness`, `qualified:false`, `demonstrated:false`). The staged register
links to it nowhere, and no edit applies it to a path.

**M-5 — Release-gate routing omits the two gates that are exactly the newly-closed rows' own obligations.**
`DR-G06 OFFLINE-CLOSURE` ("Supported authoritative product installs/runs with no network and mandatory
storage") is named only by DR-103, DR-104, DR-114 and DR-123 — not by **DR-106**, whose obligation is
signed offline analysis closure and mandatory verified storage. `DR-G11 STORAGE-CUSTODY`
("Authoritative closure cannot succeed without verified durable storage") is named only by DR-120 and
DR-121 — not by **DR-106, DR-109, DR-113 or DR-124**, the storage/custody rows. G06 and G11 are the
two gates the register records as `HARD-BLOCKED — BLOCKED by DR-002–008`, i.e. precisely the
obligations whose design closure is now being claimed for the first time. Each affected row's
remaining-measurement list therefore understates what that row still owes.

**M-6 — Five rows do not have an individually defensible grade (detail in §3): DR-106, DR-109, DR-117, DR-122, DR-130.**

**M-7 — The applying act itself is not recorded and is not in the edit set.**
Every document in the set attributes the application to "D-372". `COORDINATOR-DECISIONS.md` contains
zero occurrences of D-372 (D-371 appears twice, with a full entry, as do D-367..D-370).
`COORDINATOR-DECISIONS.md` is not among the 14 edits. `D-372-corrections.proposed.md` in the candidate
is explicitly "PROPOSED. No adoption or readiness change is made by this file." The current design
account would therefore become effective by reference to a decision that has no recorded home in the
register where every other decision lives.

### SHOULD findings

**S-1 — Six "retain" rows carry no inherited pin.** Eleven of 28 rows have no
`compatibleInheritedAccount`. Five of those (DR-106, 109, 110, 113, 130) were never SATISFIED, so
there is nothing to inherit. But six (**DR-102, DR-104, DR-115, DR-117, DR-119, DR-123**) hold preview
SATISFIED grades resting on named inherited contracts or decisions, and their dispositions begin
"Retain…" while naming nothing to retain from. Concretely: DR-102 retains "byte-opaque common control
framing" from `control-protocol-contract.v2.json` `c50a79fe…` (verified present, unpinned here);
DR-117 from `preview-product-boundary-successor.v10.json` `8f34c92e…`; DR-115 from D-006's numerics;
DR-104 from D-012; DR-119 from D-008; DR-123 from D-009. The instruction to inspect actual required
selectors where a row preserves them cannot be discharged for these six.

**S-2 — Superseded permission truth table cited.** `native-evidence.md` §5.2 copies enforcement values
from "the pinned `permission-truth-tables.v7.json`" (`afc2d6aa…`). DR-105's accepted inherited head is
`permission-truth-tables.v9.json` (`05d55964…`). The two files differ (occurrences of `ENFORCED`: 82 vs
84), though `DISCLOSURE-ONLY` (114) and `ENFORCED-BY-CONSTRUCTION` (10) counts are identical, so the
four copied values are probably unchanged. The final review must confirm the four values in v9 and
re-pin to the accepted head rather than a superseded version.

**S-3 — A generated file is hand-edited without its generator.** `docs/catalog/current-design.md`
states it is "Generated from `document-classification.v1.json`". The staged edit hand-adds two
`REFERENCED` entries. `document-classification.v1.json` and `document-inventory.v1.json` are not in
the edit set, so the next regeneration silently drops both lines. (Both added link targets do
resolve.)

**S-4 — Three gate rows are left asserting a blocking cause the same document now says is dispositioned.**
The staged register does not touch the release-gate registry. `DR-G06` and `DR-G11` still read
"BLOCKED by DR-002–008 … HARD-BLOCKED" and `DR-G10` still reads "HARD-BLOCKED pending selector
refresh", while the new section says DR-002–011 now carry reviewed dispositions and the gates file
supplies G10's selector successor (TS major 2 / Rust major 3). Either reconcile the cells or state
explicitly that gate-row cells retain historical standing.

**S-5 — The dated snapshot block is not cross-referenced.** "Historical preview position — measured
snapshot, 2026-09-05" still reports condition 2 as "23 of 23" and condition 1 as "MET for
architecture-preview scope only", directly beneath a new table asserting a different condition set. The
block's own rule ("rows are authoritative … if this block and a row disagree, the row wins") saves it,
but a forward pointer to the new section should be added.

**S-6 — `START-HERE.md` drops the topic-chapter path.** The five-minute path no longer links files 01,
02, 03, 04 or 13. They remain reachable from the architecture README. This is coherent with making the
contracts the current account, but a human reader loses the prose walk-through the file advertises as
"the architecture in ordinary prose".

### Advisory

**A-1 — Pre-existing anchor defect, explicitly not attributed to this application.** DR-117's source
cell links `02-distribution-and-components.md#product-boundary`; the real heading is "Current V1
product boundary and required successors" (anchor
`current-v1-product-boundary-and-required-successors`). The broken anchor occurs twice in the
before-image and twice in the after-image, so it is inherited, not introduced. It should be fixed, but
it is not this act's defect.

**A-2 — Untracked link targets.** `docs/coop/design-corrections/` and `docs/v2/contracts/` are
untracked. Under D-372's recorded delivery ("reviewed working-tree design update; commit and push are
not part of this task") this is consistent, but a reader with only the committed tree gets broken
links from the current head documents.

---

## 3. Individual disposition for every one of the 28 condition-2 rows

Grades below are **design-contract grades conditional on the external prerequisites in §6**. None is a
measurement or qualification claim; `productQualified:false` is correct and preserved on all 28.

| Row | My independent design disposition | Basis and residue |
|---|---|---|
| DR-101 | ACCEPT-DESIGN-CONDITIONAL | Security S2/S8/S9, native §1/§3/§5, admission §2/§3 all resolve and carry signed closure, TCB and packaging law. Inherited `/rows/0` correct. Gates G01–G05/G07/G22 match the source cell. |
| DR-102 | ACCEPT-DESIGN-CONDITIONAL, with S-1 | Native §9 supplies major-2/3 negotiation, frames, 22-phase state machine and EOF/fault law; workflows §1/§8 supply host framing. "Retain byte-opaque framing" is unanchored: no pin to `control-protocol-contract.v2` `c50a79fe…`. |
| DR-103 | ACCEPT-DESIGN-CONDITIONAL | Admission §1/§1.1 exact typed admission, security S2/S3/S9.1 signed metadata, workflows §8/§9 registry. Inherited `/rows/1` correct. |
| DR-104 | ACCEPT-DESIGN-CONDITIONAL, with S-1 | Identity §2/§3 (namespace, alias, collision refusal, discriminator law) and workflows §8's closed 45-command registry are substantive. No pin to D-012. |
| DR-105 | ACCEPT-DESIGN-CONDITIONAL, with S-2 | Security S3/S6/S7/S8/S10/S10.1/S10.2 is the strongest security material in the set: revocation linearization under one append lock, postimage-checked rollback, bounded cancellation, explicit no-confinement. Inherited `/rows/2` correct. Truth-table version defect at S-2. |
| **DR-106** | **CHANGES_REQUIRED** | Obligation is "signed offline analysis closure contents and mandatory verified storage mechanics". Cited selectors (identity §3/§4/§5, security S11, native §3/§5, workflows §2) cover custody, retention and sealed dependency inputs but **no section carrying the signed offline closure inventory** — that material is in admission §2/§3 and security S9.1, neither cited. Gates omit **G06 and G11**, the two gates for exactly this claim. Row was `OPEN / inherits hard blockers`; this is a first-time closure and needs the strongest, not the weakest, selector set. |
| DR-107 | ACCEPT-DESIGN-CONDITIONAL | Security S6/S7/S9/S9.2/S15 give five-level lock order, three lease modes, all-or-nothing namespace acquisition, and a crash-recovery table keyed to journal state. Inherited `/rows/3` correct. G18/G19/G21 match. |
| **DR-109** | **CHANGES_REQUIRED** | Identity §4/§5 and security S3.1/S7 do support one-writer commit, custody, recovery and typed failure. But the host-storage-mechanics row omits **G11 STORAGE-CUSTODY**, whose claim ("authoritative closure cannot succeed without verified durable storage") is this row's obligation restated. Row previously inherited hard blockers; no inherited pin. |
| DR-110 | ACCEPT-DESIGN-CONDITIONAL, with S-1 | Security S4/S4.5/S5/S9/S11/S14/S15 cover signed core update/repair/rollback, TR-REPAIR role, air-gap/removable-media import, expiry and revocation-aware rollback with a 30-day window. G07/G08/G18/G22 correct. |
| DR-111 | ACCEPT-DESIGN-CONDITIONAL | Identity §3/§5, native §9, security S9, workflows §2/§3/§4 give per-surface windows, retained runnable prior detector and a six-pivot typed attribution chain. Inherited `/rows/4` correct. |
| DR-112 | ACCEPT-DESIGN-CONDITIONAL | Security S4/S4.5/S5/S6/S9.1/S11. S4.5's install-bound single-use recovery epoch, with recovery authority disjoint from root keys and exact counter preservation, is a genuine advance over the source cell. Inherited `/rows/5` correct. |
| DR-113 | ACCEPT-DESIGN-CONDITIONAL, **subject to M-5** | Identity §4/§5 and workflows §2/§4/§8/§9 cover replay, verification, regeneration, purge, availability-versus-assurance and the retained executable window. Must add **G11**. |
| DR-114 | ACCEPT-DESIGN-CONDITIONAL | Security S3/S11/S14 and workflows §8/§9 keep doctor report-only with `writes: []`, defects at exit 0, and CI gating on the typed outcome rather than the exit code. Inherited `/rows/6` correct. |
| DR-115 | ACCEPT-DESIGN-CONDITIONAL, with S-1 | Admission §2/§3 supply gate-computed counts, 3 warmups + 7 measured runs, 1.20×/1.25× checked wide-integer limits and no readable PASS flag. D-006's numerics are retained only by reference through the unlinked gates file. |
| **DR-117** | **CHANGES_REQUIRED** | The obligation is count-pinned at **seven** enumerated items by D-011, and "any change to that enumeration re-opens this row". File 02 enumerates them: (1) marketplace/catalog governance, (2) external lifecycle parity/discovery, (3) contribution roles beyond narrow/data-only, (4) untrusted native/WASM admission, (5) imperative contributions/probes/hooks/root commands, (6) network-granted analysis and egress defaults, (7) replacement of the G3 substrate. Measured across all five contracts: `marketplace` 0, `third-party` 0, `TUI` 0, `rustc_driver` 0, `sidecar` 0, `core-only` 0 occurrences. Items 3, 4 and 5 are well covered (security S10, native §5.5, workflows §5/§7/§8); items **1, 2, 6 and 7 are not demonstrably covered by the cited selectors**. `admission-and-qualification.md §1.1` is cited but is the zero-config configuration section and addresses no boundary item. The actual exclusion list lives in file 10's scope table, which the row map does not cite, and there is no pin to the accepted `preview-product-boundary-successor.v10` `8f34c92e…`. |
| DR-118 | ACCEPT-DESIGN-CONDITIONAL | Best-supported row in the set. Native §1–§9 give 60 matrix cells, closed language modes, closed limitation ids L-JS1..L-CL1, and an explicit no-silent-fallback law. Inherited `/rows/7` correct. |
| DR-119 | ACCEPT-DESIGN-CONDITIONAL, with S-1 | Native §1/§2/§3/§5/§9 and security S8/S9.1 give sealed toolchain closures, `ToolClosureV1` with no PATH lookup, and typed refusal when a bundled linker is absent. No pin to D-008's universal rule. |
| DR-120 | ACCEPT-DESIGN-CONDITIONAL | Admission §2/§3, native §1/§3/§5/§9, security S8/S9.1. Inherited `/rows/8` correct. Correctly one of only two rows naming G11. |
| DR-121 | ACCEPT-DESIGN-CONDITIONAL | Admission §2/§3 report custody, independently bound producer reports and per-lane qualification. Inherited `/rows/9` correct. |
| **DR-122** | **CHANGES_REQUIRED** | The disposition asserts "SARIF re-enters for declared finding-producing commands", and `qualification-gates.proposed.json` marks G17 "REACTIVATED for full product". But D-077 is a recorded owner decision dropping SARIF; the register's own DR-122 cell says the authoritative projection "remains G17 **on re-entry**", i.e. re-entry is an act that must be performed. No such act exists: D-372's decision list does not name SARIF reactivation, and the staged register leaves the G17 row reading "dropped / inapplicable (D-077 SARIF drop; D-086). not required-now." verbatim. The applied bytes would simultaneously advertise and disclaim SARIF. (The underlying design is sound — the inventory declares SARIF for exactly `default`, `analyze`, `audit`, `repair-verify` with explicit `parityFields` — it is the authorising act and the register cell that are missing.) |
| DR-123 | ACCEPT-DESIGN-CONDITIONAL | Verified directly: `command-inventory.v1.json` carries exactly **45** commands and **43** goldens, matching the disposition's "All45 commands". Workflows §1/§8/§9 supply the closed envelope major 2, renderer parity fields, and the required-output failure path. |
| DR-124 | ACCEPT-DESIGN-CONDITIONAL, **subject to M-5** | Identity §2–§5 and security S3.1/S7/S9 separate authoritative evidence, analysis-affecting inputs, rebuildable cache and operational metadata with distinct custody. Inherited `/rows/11` correct. Must add **G11**. |
| DR-125 | ACCEPT-DESIGN-CONDITIONAL | Workflows §1/§8/§9, security S6/S7/S10, native §9 keep components free of rendering and final authority. Inherited `/rows/12` correct. |
| DR-126 | ACCEPT-DESIGN-CONDITIONAL | Security S8 defines four machine platform ids with display aliases refused as ids; I confirmed the same four ids are used by native §1.1 and the workflow test-execution schema, and that the gates file's `platformFamilies` matches. Inherited `/rows/13` correct. |
| DR-127 | ACCEPT-DESIGN-CONDITIONAL | Native §9's frame/EOF/fault rules and security S6/S7/S9 transitions support anti-lockstep and control precedence. Inherited `/rows/14` correct. |
| **DR-130** | **CHANGES_REQUIRED** | Required evidence is an independently reviewed transition statement satisfying file 05 §Migration constraints **as written** — the six-member "No migration silently…" enumeration, the five-item preserve list and the five distinctions (6/5/5, all three counts confirmed present in file 05). Measured across all five contracts: `prototype` 0, `opensip-cli` 0, `existing user` 0, `V1 user` 0, `coexistence` 0, `upgrade continuity` 0, `a62509d6` 0 occurrences. The cited selectors (security S9/S14/S15, identity §5, workflows §8/§12) describe **the product's own stage-1→stage-2 state-schema bridge and installation transitions**, not the V1-prototype users' local state. The disposition's phrase "Prototype stays alongside, never silently imported/promoted" is not carried by any named successor. The row's own register cell records that slice 1 claims no upgrade continuity, and the pre-staged text is explicit that "prior delivery-stage deferral no longer supplies design closure". |
| DR-131 | ACCEPT-DESIGN-CONDITIONAL | Identity §3/§4/§5 (pure evaluator, seal binding Plan/proof/verdict), native §4, workflows §1/§5/§8/§9. Preview unstable identities are correctly left historical and non-promotable. Inherited `/rows/15` correct. Shares the DR-122 SARIF/D-077 residue. |
| DR-133 | ACCEPT-DESIGN-CONDITIONAL | Native §4/§9 and identity §4 keep providers to facts and Coverage with host-owned admission; the finding-masquerade and Coverage-domain-mutation refusals are explicit. Inherited `/rows/16` correct. |

**Summary:** 23 of 28 rows carry an individually defensible design-contract grade conditional on the
prerequisites; 5 do not (DR-106, DR-109, DR-117, DR-122, DR-130); 2 further rows (DR-113, DR-124)
require the G11 correction. No row is accepted because a reference test passed or because the author
claimed ACCEPT — the reference suites were treated as design evidence only, exactly as the units
themselves state.

**Scope exclusions.** DR-108, DR-116, DR-128 and DR-129 are correctly recorded as D-371's bounded
selection (credentials, third-party publisher/ecosystem, untrusted contributions, TUI) and **not** as
new scope cuts made to obtain completion. The staged register's sentence "No product capability was
moved out of the design to obtain completion" is supported: the excluded set is identical to the
pre-staged D-371 text, and the 28-row affected set is unchanged.

---

## 4. DR-201 through DR-205 — individual dispositions

All five are condition-3 owners. Each retains its 2026-08-13 `ACCEPTED` standing for its original
subject and digests; none has been re-reviewed against the corrected full-product bytes; none is
touched by the staged edit.

| Row | Disposition |
|---|---|
| DR-201 (semantic correctness) | **RETAINED-HISTORICAL — NOT RE-REVIEWED FOR THIS SCOPE.** Accepted at frozen digest `40ab9a3e…`, verdict `bc1413b3…`. The new identity/evidence and D9 material is a different subject; the acceptance does not extend to it. |
| DR-202 (delivery/operations) | **RETAINED-HISTORICAL — NOT RE-REVIEWED FOR THIS SCOPE.** Turn-2 verdict `4d25da30…`. Its F3/F4 remain routed to DR-111/DR-112, whose successors this act changes; the routing must be re-checked, not inherited. |
| DR-203 (prototype lessons) | **RETAINED-HISTORICAL — NOT RE-REVIEWED; DIRECTLY IMPLICATED BY M-6/DR-130.** Verdict `aae33421…` verified the external prototype pin at commit `a62509d6…`. The full-product transition contract for those prototype users is the gap found at DR-130. |
| DR-204 (V1/coop invariant coverage) | **RETAINED-HISTORICAL — NOT RE-REVIEWED FOR THIS SCOPE.** Verdict `0934ffbe…`. Its central precedent — that a coordinator-composed discharge is unlawful for a grade requiring independent review — is the precedent M-2 and M-3 apply here. |
| DR-205 (small-core/components) | **RETAINED-HISTORICAL — NOT RE-REVIEWED FOR THIS SCOPE.** Verdict `6dc92b43…`, taken against file 02 `1811c682…` and file 10 `5378cdba…`; this act changes file 10, so the subject has moved. |

**Consequence:** condition 3 cannot read as MET by naming these five rows. It needs either explicit
re-reviews, or a cell that states plainly that DR-201..205 retain their historical scope while named
new reviews (with paths and hashes) supply this scope.

---

## 5. The five conditions

| Condition | Proposed | My disposition |
|---|---|---|
| 1 — inherited semantics | MET | **CONDITIONALLY SUPPORTABLE, NOT AS WRITTEN.** Counts verified exactly: DR-001..011 = 11, DR-011 residuals R01..R16 = 16, evaluation subresiduals 19 RES + 7 IR-NB + 4 measured escapes = **30**. Each has an individual written disposition; no aggregate score substitutes. But every one of the 30 carries `reviewStatus: PENDING`, and R10 is closed by asserting a blind consumer B that has not run. The **DR-003 timing disposition is correctly framed** — it changes only the pre-blueprint demonstration timing, keeps DR-G09/G18/G19/G21/G22 and DR-012 mandatory, and explicitly claims no demonstrated OS enforcement, persistence or V10. That is the right treatment and I affirm it. |
| 2 — affected product rows | MET | **NOT MET AS WRITTEN.** 23 of 28 rows are individually defensible; DR-106, DR-109, DR-117, DR-122 and DR-130 are not; DR-113 and DR-124 need the G11 correction. The cell also asserts independent acceptance that the cited map denies (M-2). Correctly *not* a count-based blanket grade — each row does carry its own disposition text — but five of those dispositions are not supported by the evidence named for them. |
| 3 — integrated independent review | MET | **NOT MET.** See §4 and M-3. No exact evidence; none of the four named reviews has occurred; five historical rows re-labelled. |
| 4 — qualification ownership and contracts | MET at design level | **SUPPORTABLE IN SUBSTANCE, DEFECTIVE IN FORM.** I verified all 32 gate mappings exist with owner, harness, current contract, `qualified:false`, `demonstrated:false`, `implementationHarnessAuthored:false`, and that no document claims QUALIFIED or DEMONSTRATED. But the cell links no artifact (M-4), no edit applies the gates file, per-row routing drops G06/G11 (M-5), and three gate rows still assert stale blocking causes (S-4). |
| 5 — implementation authorization | NOT MET | **CORRECT AND AFFIRMED. MUST REMAIN NOT MET.** Verified consistently across the staged register, `START-HERE.md`, file 12 and the architecture README. No staged byte authorizes implementation, commit, push, publication or release qualification. |

---

## 6. Unresolved external prerequisites — none of which I can supply

1. **Actual independent design review of frozen candidate v3** (`e3365d6e…`). Has not occurred. The two
   retained reviews (post-reset v1 and v2) are both `CHANGES_REQUIRED` and are addressed to
   *earlier* frozen subjects (`e7403b70…`, `5bd9cde1…`); neither accepts v3's bytes.
2. **Fresh blind consumer B (DR-011-R10).** Has not been launched. `NEXT-REVIEW.md` states plainly:
   "No blind consumer has yet run." Condition 1 depends on it.
3. **Recorded D-372 act** in `COORDINATOR-DECISIONS.md` (M-7).
4. **`application.v1.json` and `readiness-row-map.v1.json`** as reviewable bytes at their cited paths
   (M-1), plus an act that applies `qualification-gates.proposed.json` (M-4).
5. **A corrected row map** carrying real independent grades rather than `PENDING-APPLICATION-REVIEW`
   (M-2), which necessarily changes its hash and therefore this application subject.
6. **A final exact-evidence/application-binding review** of the corrected set. I am not that review,
   and I cannot supply prerequisites 1 or 2.

---

## 7. Assessment of `application-validation-plan.v1.md` (separate procedural proposal)

Read at SHA-256 `c5dcb579…`. It is not part of the frozen staged content and I assess it only as a
proposal. **Its central factual claim is correct and I independently verified it.**

**Verified correct.** Exactly two current reference-input pins intersect the 14 documentation edits,
and they are in `native/source-pins.v2.json` (66 pins total):

| Pin | Document | Pinned / before | After application | `consumedFor` |
|---|---|---|---|---|
| `/pins/60` | `docs/v2/architecture/03-configuration-and-security.md` | `b97d70eea9e84c66b05b67c569fad4feddda6a7d37b9d23df6770d8895c44e03` | `2e50e8945d3d43b54b098f92d87f5a017d60c8f91a173d20f33f77083e5a2d9a` | "preserved confinement honesty and execution default" |
| `/pins/61` | `docs/v2/architecture/10-mvp-and-future-scope.md` | `27b3e353f6217cc6fc1f2ce2fb685f5f8eb646105dc3fc49dffb28bc35218f21` | `d98627d2b7c7260c9c370f499a71546d1a8737ab76b4c2ae494d9821211cbd74` | "one product design: native language depth, platforms, exclusions" |

Both pinned values match the candidate before-image exactly; both change under the staged edits. The
foundation, security and workflow pin manifests have **zero** intersection with the 14 edits, as
claimed. The plan's statement that the native model does not interpret either document as an input
record is also correct: `native-evidence-report.v2.json` mentions neither filename. And the delta is
not cosmetic — `check_native_evidence.v2.py` states "The checker refuses to run cases if any pin
differs" and `verify_pins()` emits a `sha256 mismatch` fault, so **applying the 14 edits without the
pin successor breaks the native reference suite**. The plan is right to require the successor, right
to keep the original manifest and report immutable in the accepted archive, right to forbid changing
the old checker or its manifest, and right that a normative change requires a new freeze, fresh
independent review and a fresh blind consumer.

**Gaps the plan must close before it can serve as the final procedure.**

- It does not require `application.v1.json`, `readiness-row-map.v1.json` or the applied gate map to be
  in the final subject, yet the staged documents make them load-bearing (M-1, M-4).
- It does not mention recording D-372 in `COORDINATOR-DECISIONS.md` (M-7).
- It predicts the outcome — "regenerated `native-evidence-report.v2.json` with100 passing cases" —
  before running it. It should require the regenerated report's **actual** result to be recorded,
  whatever it is. Predicting a pass is the same class of defect the corpus repeatedly rejects.
- It does not name the two exact before/after hashes; they are supplied above and should be pinned
  verbatim in the final subject.
- It does not address the generated-catalog drift (S-3), which its "check current documentation
  links/inventory hashes" step would surface only if the classification input is included.
- Its "account for every old-checker failure newly caused by reviewed current-document annotations"
  step is the right instinct and should explicitly enumerate the pre-existing root README custody
  divergence, which D-370/D-371 already record as not attributable to this work.

With those additions the procedure is sound in shape: an application-only pin/report delta over
byte-identical product contracts, recorded as a prospective change and never as a repin of a frozen
acceptance.

---

## 8. Documentation review — does the staged set make one bounded product design the current account?

**Largely yes, and this is the strongest part of the proposal.** The reading path in `START-HERE.md`
now runs scope → contracts → register → source map. The architecture README changes "Wider
authoritative architecture (future scope)" to "Authoritative architecture (current product design)".
File 13 states that the Fallow "future" labels preserve the original D-370 act and are "not a
competing current design or a reason to omit a selected capability" — which is the correct disposal of
the future-scope reading. File 10 leads with the contracts as the complete selected design and keeps
stages for implementation only. File 12 flips the completion goal and immediately re-states that
condition 5 is NOT MET. Eight inherited chapters receive a uniform current-applicability banner that
routes the reader through the source map while preserving their historical labels and frozen evidence.

The source map does reconcile the old prose the instruction names: old commands (`08-surfaces`,
`MAP-VS-CONTROL`, the preview command set), platforms (SEALED Windows and the Rust V1 spine, with
Windows explicitly not selected), identity (`IMPLEMENTATION-FREEZE` §7.1's "unproduced
capabilityManifestId" corrected against applied DELIVERY v4) and retention (defaultless prose against
the binding CD-RT-5 durable-unbounded default). The central register remains the sole readiness
checklist; no second checklist is created, no duplicate row ids appear, and the historical preview
grades keep their old standing while current annotations explain applicability prospectively. Keeping
the `.proposed` filenames is acceptable in principle — an external act applying their exact content is
not a second design — **but only if such an act exists**, which is precisely what M-1 and M-7 find
missing.

Against that, the documentation review returns the defects already recorded: two cited evidence files
that do not exist, an unlinked gate map, an unrecorded applying decision, a hand-edited generated
catalog, three stale gate cells, and a stale dated snapshot block.

---

## 9. Retained executable checks

All checks below are read-only and were run by this reviewer against the frozen bytes. No mirror tests
were written.

- Manifest and staged-hash verification, before and after review (16/16, twice).
- Parent manifest hash check plus full 1317-file candidate verification, including both directions of
  the set difference between manifest and disk.
- Before-image provenance of all 14 edits against candidate, working tree and `HEAD`.
- Resolution of all 17 `compatibleInheritedAccount` JSON-pointer selectors against the real inherited
  file.
- Existence check of every contract section selector used by the row map, against headings extracted
  from the pinned contract bytes.
- Full markdown link-and-anchor resolution over the staged set (260 resolved; 12 failures, of which 11
  are M-1's two missing files and 1 is the pre-existing anchor at A-1).
- Gate-coverage analysis: union of all 28 rows' `releaseGates` against DR-G01..G32, plus reverse
  lookup for G06, G10, G11 and G17.
- Row-map invariants: 28 rows, ids equal to `condition2AffectedSet`, single `proposedDesignGrade`
  value, single `independentGrade` value, `productQualified` false on all.
- Residual counts: 11 inherited rows, 16 DR-011 residuals, 30 evaluation subresiduals with their
  `reviewStatus` values.
- Source-pin intersection across all four unit pin manifests against the 14 edited paths, with exact
  before/after digests for the two hits and inspection of the checker's pin-refusal behaviour.
- Enumeration counts for DR-130 (6/5/5 in file 05) and DR-117 (seven items in file 02), plus term
  coverage measurement for both across all five contracts.
- Command-inventory count (45 commands, 43 goldens) and SARIF applicability set.
- Permission truth table v7 versus v9 differential.

---

## 10. Conclusion

**CHANGES_REQUIRED.** The design content is substantially better than the register's previous state and
most of it is defensible: 23 of 28 rows, the DR-003 timing disposition, the scope exclusions, condition
5, and the documentation restructuring into one bounded current account. But the frozen bytes cannot
lawfully be applied as they stand. Two cited evidence files do not exist and no edit creates them; the
register and the row map contradict each other on whether independent acceptance has happened; the
applying decision is unrecorded; condition 3 is asserted by re-labelling five untouched historical
rows; condition 4 links no artifact; the two hardest gates are routed away from the rows they belong
to; and five rows carry grades their named evidence does not support.

Correcting these changes the row map and therefore this application subject, so a fresh application
subject and a fresh application review will be required. That review must still follow, not precede,
the two external prerequisites I cannot supply: actual independent design acceptance of candidate v3,
and the fresh blind consumer B review.

**Paths.**

- This review: `/tmp/opensip-design-corrections/application-review.v1/application-review.md` and
  `application-review.json`
- Frozen application manifest: `/tmp/opensip-design-corrections/application-review.v1/application-subject.v1.json` (`9260c1de…`)
- Staged subject: `/tmp/opensip-design-corrections/application-stage.v2`
- Parent design candidate: `/tmp/opensip-design-corrections/candidate-subject.v3` (manifest `e3365d6e…`)
- Prior Fable 429 evidence, unmodified: `/tmp/opensip-design-corrections/application-review.v1/response.json`
- Register diff retained from the interrupted run: `/tmp/opensip-design-corrections/application-review.v1/scratch-register.diff`
- Procedural proposal assessed: `/tmp/opensip-design-corrections/application-validation-plan.v1.md` (`c5dcb579…`)
