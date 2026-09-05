# Design delta DRAFT — Gortex borrow triage (register-wide)

> **DRAFT. NOT ADOPTED. BINDS NOTHING. CHANGES NO STATUS.**
>
> This file is a proposal written under
> [`IMPLEMENTATION-FREEZE.md`](../IMPLEMENTATION-FREEZE.md) §10. It has not been
> taken up, has not been reviewed, and is **not reviewable authority** until the
> architecture freeze is signed *and* this file has had independent review
> recorded against its exact bytes. It amends no law, no binding artifact, no
> claim status, no product disposition, and no seal. It applies no edit to any
> other file in this tree.
>
> `CD-RT-5` remains `BLOCKED_ON_PHASE_1A`. The §11 signature block remains
> `[NOT FROZEN]` with every field `[UNSET]`. Every §7.1 parked recipe remains
> parked and open.
>
> **If you are reading this file alone, out of its directory:** nothing in it is
> in force. If any sentence here conflicts with the live authority set — binding
> artifacts and the claim register, then accepted product scope and dispositions,
> then the signed freeze and implementer blueprint, then narrative architecture —
> **this file loses.**

**Drafted:** 2026-08-04 · **Subject:** the borrow rows of
[`GORTEX-BORROW-REGISTER.md`](../GORTEX-BORROW-REGISTER.md), triaged against the
live corpus · **Proposes:** nothing.

---

## 0. What this is, and what it is not

### 0.1 It proposes no change, and that is the finding

**This document proposes zero borrows, zero normative text, zero artifact edits,
and zero checker changes.** It is filed under §10's location and written to §10's
seven-item shape so a reviewer can read it beside its sibling draft — but a
document that proposes no change **triggers no §10 obligation and is not a delta
in §10's operative sense.** §10 requires a delta for *"a change to a binding
artifact, v1 scope/product disposition, non-negotiable law, process authority, or
dependency direction."* There is no such change here. If this file is adopted,
adopting it is a no-op.

That is stated first and plainly because the alternative framing — a document
that reads as a change while changing nothing — is the **paper seal** failure
this corpus names repeatedly, and a triage record is only honest if it refuses
that costume outright.

The finding is: **every accepted Gortex borrow and every explicit non-borrow is
already covered by the live corpus.** Nine of nine accepted rows are redundant as
proposals. Six of six non-borrows are already guarded by non-negotiable law. The
value of writing that down is not that it changes anything; it is that it
**bounds the residue**, so a later lane does not reopen Gortex and re-propose
`GX-06` or `GX-08` as though they were new.

### 0.2 Relationship to the sibling draft — companion, not competitor

[`gortex-graph-lanes.delta-draft.v1.md`](gortex-graph-lanes.delta-draft.v1.md),
SHA-256 `4c11eae011aeda4a6f69d2b833259b1758985f87768e1dd3e24b0213b0a8f52d`,
already holds the only live Gortex-derived proposals in this tree: `D-1` (an
identity-exclusion clause), `D-2` (a citation repair), `D-3` (an instrument
question, deliberately unadjudicated).

**That draft is adequate for its subject and this file does not revise, restate,
or compete with it.** It already performed the refusal that matters — it found
the accelerator/producer distinction to be *already law* and narrowed itself
accordingly instead of shipping a restatement. Its subject is the graph lane.
This file's subject is the register as a whole. Where they meet, **v1 governs and
this file defers.** No proposal here duplicates `D-1`, `D-2`, or `D-3`, and none
contradicts
[`IMPLEMENTER-BLUEPRINT.md`](../IMPLEMENTER-BLUEPRINT.md) §5.A, which already
assigns owners and conditional gates to `GX-01`–`GX-08`.

### 0.3 The evidence ceiling — read this before the tables

**Every claim in this corpus about what Gortex *does* is UNVERIFIED at source,
including every claim in this file.**

This lane cannot fetch the network and cannot read
`zzet/gortex@4d2f4972…`. The only available description of upstream behaviour is
[`GORTEX-BORROW-REGISTER.md`](../GORTEX-BORROW-REGISTER.md), which declares
itself **"NON-AUTHORITATIVE SOURCE MAP AND IMPLEMENTATION CHECKLIST"** and whose
rows are already *adapted to OpenSIP* rather than transcribed. So the register
does not report what Gortex does; it reports what an earlier reader concluded
OpenSIP should take from it.

Two consequences, and the second is the load-bearing one:

1. The "what Gortex does" column below is marked **UNVERIFIED** throughout. It
   paraphrases the register, nothing more. No sentence in this file should be
   read as a statement about upstream code.
2. **Therefore this triage can only ever ask one question honestly:** *is the
   adapted idea, as the register states it, already covered by the live corpus?*
   It cannot ask whether the register captured Gortex correctly, whether a
   better idea was missed, or whether an upstream mechanism differs materially
   from its paraphrase. **A reviewer must not read a "redundant" verdict below as
   evidence that Gortex has nothing further to offer.** It is evidence only that
   *the register's own rows* are covered.

This ceiling is also an argument against adopting anything new here: a borrow
cannot responsibly be admitted into a corpus with this one's evidentiary
standards on the strength of a self-declared non-authoritative secondhand
summary of bytes nobody in this lane can open.

### 0.4 Citations are content anchors, not line numbers — with cause

Every citation below names a **document, a section, and verbatim text**. No line
numbers are used. This is not stylistic.

`IMPLEMENTATION-FREEZE.md` was **modified during the drafting of this file**
(law 8 moved from line 1034 to line 1049 between two reads roughly ten minutes
apart; mtime `2026-08-03 23:20:29`). Other lanes hold that file and the blueprint
concurrently. Line-number citations into those documents are therefore
**structurally unreliable in this corpus**, not merely fragile.

The corpus already binds the durable alternative. Freeze §6 law 2 carries the
note *"The first two sentences of this law are a verbatim content anchor of
`check-retention-custody-v23/v24.py`. Do not reword them — see the note on
content anchors at the end of §2."* Content anchoring is an existing OpenSIP
mechanism; this file uses it, and borrows nothing to do so.

---

## 1. Reason and new evidence — §10 item 1

### 1.1 Triage of the nine accepted borrows

Columns are the six questions this triage is required to answer. **"Gortex idea"
is UNVERIFIED throughout (§0.3).** "Sits beneath" names the contract the borrow
would sit *under*, never beside and never above.

| Row | Gortex idea, as the register states it (UNVERIFIED) | Where the live corpus already covers it | Sits beneath | v1? | Verdict |
|---|---|---|---|---|---|
| `GX-01` | Separate exact accelerators from semantic graph producers | Freeze §6 **law 8**, verbatim: *"an **exact accelerator** is project-scoped, rebuildable, optional, and must be parity-equivalent to canonical traversal. Any graph computation whose algorithm/version/parameters/inputs can change an edge, finding, ordering, omission, or Coverage is a **semantic producer**, not a cache."* Also freeze §8 litmus; blueprint §2.1 rule 6; blueprint §5.A; arch 04 classification table; arch 11 `GX-01` | law 8 | already bound | **REDUNDANT — dropped** |
| `GX-02` | Immutable index generations `building → complete → active → stale → collectible` | Blueprint §2.1 rule 3, verbatim: *"An exact generation follows `building -> complete -> active -> stale -> collectible`. Every required component is digest/count/schema/kind/version/parameter checked before one atomic active-pointer transition. Queries pin one generation; partial or cross-generation answers are unrepresentable."* Gates at blueprint §7.4; lifecycle prose at arch 06 | blueprint §2.1 / §7.4 | not required — v1 completes with no derived index (blueprint §2.1: *"An implementation can complete the first vertical slice with no derived index"*) | **REDUNDANT — dropped** |
| `GX-03` | One typed bounded `QueryService` feeding CLI now, MCP/HTTP later; adapters never read physical tables | Freeze §6 **law 16**, verbatim: *"No renderer, agent surface, or report performs policy or reads physical storage tables directly."* Plus blueprint §2.1 rule 7, verbatim: *"The v1 CLI and later transports are adapters over this same service."* Plus blueprint §4 forbidden edges; arch 08 | law 16 | CLI adapter yes; MCP/HTTP later scope, already so stated | **REDUNDANT — dropped** |
| `GX-04` | Scope every generation beneath canonical `ProjectId`; dense IDs generation-local | Freeze §6 **law 8**, verbatim: *"Each canonical ProjectId owns `projects/<ProjectId>/ledger.sqlite` and its own physical CAS; cross-project physical deduplication is forbidden."* Plus blueprint §2.1 rule 8, verbatim: *"Dense graph IDs are local to one generation and never become FactId, subject identity, or cross-project authority."* Plus arch 06 | law 8 | yes, already bound | **REDUNDANT — dropped** |
| `GX-05` | Sharding, CSR, O(1) side indexes, precomputed bounded reach | Blueprint §2.1 rule 2 (these stay private cache work) and §8.4, verbatim: *"`GX-05` and `GX-09` are implementation-selection measurements, not Phase-4 seal gates."* Plus blueprint §5.A: *"measured candidates. No architecture or performance claim before comparison with the reference path"* | blueprint §8.4 | **no — Phase 5**, correctly | **REDUNDANT — dropped** |
| `GX-06` | Compact versioned lossless agent projection | Register disposition `POST-V1-PARKED`; blueprint §5.A: *"Parked until product scope change; compact bytes never become evidence identity"*; arch 11 | arch 08 + product scope | **no — post-v1**, correctly parked | **REDUNDANT — dropped** |
| `GX-07` | Session-scoped editor/speculative overlays | Register disposition `POST-V1-PARKED`; blueprint §5.A: *"Parked ephemeral overlay view; promotion recaptures a Snapshot and uses ordinary admission"* | arch 08 + product scope | **no — post-v1**, correctly parked | **REDUNDANT — dropped** |
| `GX-08` | Resident provider pools, lazy startup, idle reaping, watcher debouncing | Register disposition `POST-V1-PARKED`; blueprint §5.A: *"Parked behind R-1 measurement and product scope change"* | R-1 park + product scope | **no — post-v1**, correctly parked | **REDUNDANT — dropped** |
| `GX-09` | Retained graph/query instrumentation | Blueprint §8.4 measurement table; blueprint §5.A acceptance entry *"§8.4 retained benchmark report"* | blueprint §8.4 | **no — Phase 5**, correctly | **REDUNDANT — dropped** |

**Nine of nine dropped as already covered.**

### 1.2 Triage of the six explicit non-borrows

Each is already forbidden by non-negotiable law, so none needs a delta to stay
forbidden. Recorded so a later lane cannot reintroduce one as a "new" borrow.

| Row | Rejected Gortex-shaped choice (UNVERIFIED) | Already guarded by | Verdict |
|---|---|---|---|
| `GX-N01` | Global provenance / fact-quality / fallback rank | Freeze §6 **law 3**, verbatim: *"C-1 is predicate-relative. There is no global fact or layer ordering."* Mechanically: `artifacts/fact-plane.v1.json` `$.c1Boundary.forbiddenGlobalFields = ["quality", "tier", "degraded", "rank"]` | **already forbidden** |
| `GX-N02` | System/`PATH`-selected provider authority | Freeze §6 laws 9–11 (bundled, signed, pinned, Plan-bound providers) | **already forbidden** |
| `GX-N03` | Silent substitution on unavailable provider/relation/index | Freeze §6 **law 4**, verbatim: *"Every required predicate receives exact Coverage; unmet requiredness cannot become pass or a false no-match."* Reinforced by law 3's *"no silent syntax substitution"* elaboration | **already forbidden** |
| `GX-N04` | Live daemon / overlay / cache state as evidence authority | Freeze §6 **law 8**, verbatim: *"Warm/provider state is acceleration only … Neither cache absence nor cache corruption may become a false empty or clean result."* | **already forbidden** |
| `GX-N05` | VCS commit alone as snapshot identity | Freeze §6 law 6 (separate identities, separate custody); `SNAPSHOT-ID-V1` host-owned | **already forbidden** |
| `GX-N06` | Model-generated ranking on the analysis path | Freeze §6 **law 1**, verbatim: *"Core analysis is deterministic, local-first, fully useful offline, and makes no language-model calls."* | **already forbidden** |

**Six of six already guarded.**

### 1.3 What genuinely remains — and it is not a borrow

After the triage, the residue is **not a capability Gortex supplies**. It is a
set of defects in how the corpus *records* borrows it has already adopted. All
three are already on the table in the sibling draft:

| Residue | Nature | Already proposed as |
|---|---|---|
| The identity-exclusion half of law 8 sits only in narrative architecture, while the recipes it constrains are §7.1 parks | recording-tier defect | v1 draft `D-1` |
| `GX-05`/`GX-09` cite a plan section that does not carry the cited content | citation defect | v1 draft `D-2` |
| The accelerator/producer distinction has no instrument | conformance defect | v1 draft `D-3` |

**This file proposes no fourth item and no variant of these three.** Its
contribution is the negative result: the residue is exactly this, and the
register contains nothing further.

### 1.4 New evidence — the `D-2` `C-b` cost is understated by roughly fivefold

The v1 draft prices its `D-2` option `C-b` (restore Phase-5 content into
`ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md`) at *"seven retained checkers."* That
count is correct for **checkers** and materially understates the blast radius.

Measured 2026-08-04 by searching `artifacts/` for
`47df412dba5d62a823ca7c008c382c489b8a10c797fd8656f3d4dd5d6c342e2e`:

```
37 files record the plan's SHA-256
   7  retained checkers          check-retention-custody-v16.py … -v22.py
  12  binding contract artifacts retention-tiers.v16 … v24.json, v10-disposition.v1.json,
                                 consumer-b-implementer-litmus.v2.json,
                                 phase1a-a-prime-successor.response.v3.json
  18  review artifacts           independent reviews / re-reviews / adjudications
```

Two precisions that matter and that cut in opposite directions:

- **The 7 checkers would genuinely fail.** In `check-retention-custody-v22.py`
  the digest sits in a hash-verified closure map keyed `ARCHITECTURE_PLAN`,
  recomputed against disk. Editing the plan breaks all seven, and §7.2 forbids
  the in-place repair: *"A change to reviewed bytes requires a version bump and a
  new verdict; it may never be made in place."*
- **`check-retention-custody-v24.py` would *not* fail, and that is worse, not
  better.** The head retention contract `retention-tiers.v24.json` records the
  plan digest at `$.recordedInputs.citedNotGated[1].sha256`. The v24 checker
  validates that row's *shape and path* but never recomputes its `sha256`
  against disk. So an edit to the plan would leave the head retention contract
  carrying a **stale digest under a green checker** — silent drift of exactly
  the class §7.2 exists to prevent, and it would not be reported by any of the
  five checkers required green today.

Set against freeze §7.6 — *"88 pinned by >=1 non-measurement file, 5 unpinned"* —
the plan is not a document that can be repaired; it is a fixed point. **This
strengthens the v1 draft's existing recommendation of `C-a` (repoint the
citation) and this file recommends no different option.** It only prices the
alternative honestly.

### 1.5 New evidence — the v1 draft's line anchors have drifted

Recorded as a maintenance observation about a sibling draft. **This file proposes
no edit to it** (§2).

The v1 draft cites the freeze and blueprint by line number. Both documents have
since grown. Verified 2026-08-04:

| Quotation | v1 draft cites | Actually at |
|---|---|---|
| law 3 | `:796` | 999 |
| law 8 | `:846-855` | 1049 |
| law 16 | `:874-875` | 1077 |
| §8 litmus | `:1452-1453` | 1748 |
| blueprint §2.1 rule 6 | `:792-795` | 818 |
| blueprint §7.4 header | `:1552-1555` | 1593 |

The right-hand column was measured at `IMPLEMENTATION-FREEZE.md` mtime
`2026-08-03 23:20:29` and **is expected to be wrong by the time it is read** —
that is the point of the observation, not a flaw in it.

**Every quoted string still matches its source verbatim** — the draft's substance
is intact and every quotation remains locatable by content search. The defect is
navigational, not evidentiary.

It is also **recurring rather than one-off**: the freeze moved again *during the
drafting of this file* (§0.4). Renumbering would be a band-aid that decays within
the hour. The systemic repair is to re-anchor those citations on verbatim
content, per the corpus's own §2 content-anchor mechanism — and that is properly
a deliberate `v2` authored by whoever owns that draft, under §7.2.1's
frozen-subject rule, not a drive-by edit by this lane.

---

## 2. Affected claims, artifacts, modules, fixtures, product behavior — §10 item 2

**Nothing, in every category, by construction.**

- **Claims.** No claim changes status. `C-1`, `C-2`, `V10`, `G19`, `R-1`, `D9`,
  `P-4` untouched. `CD-RT-5` remains `BLOCKED_ON_PHASE_1A`.
  `claim-register.v1.json` needs no edit.
- **Binding artifacts.** None edited, none proposed, no digest changes.
- **Documents.** None edited. Specifically **not** edited:
  `IMPLEMENTATION-FREEZE.md`, `IMPLEMENTER-BLUEPRINT.md`,
  `claim-register.v1.json`, anything under `artifacts/`, and
  `ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md` — which remains at
  `47df412dba5d62a823ca7c008c382c489b8a10c797fd8656f3d4dd5d6c342e2e`,
  re-confirmed after this file was written (§7).
- **Sibling draft.** `gortex-graph-lanes.delta-draft.v1.md` is **not modified**;
  its bytes remain at `4c11eae0…`. §1.5 observes; it does not act.
- **Modules and dependency edges.** No crate boundary moves. No forbidden edge
  is added, removed, or weakened.
- **Fixtures.** None added, retired, or altered.
- **Product behavior.** None. §4.1's required set does not grow; §4.2's
  exclusions stand. No v1 capability is added, enabled, or flagged.

---

## 3. Old and new normative text — §10 item 3

**None. No normative text is proposed, in any document.**

This section is deliberately empty rather than omitted. An empty item 3 is the
structural signature of a document that is not a change, and it is the single
clearest way to make this file impossible to mistake for something adopted.

The only live Gortex-derived normative proposal in this tree is the v1 draft's
`D-1`, in that file, unmodified by this one.

---

## 4. Checker and mutation changes — §10 item 4

**None.** No checker is added, edited, retired, or re-pinned. No mutation suite
changes. No artifact digest moves.

Verified after writing (§7): the five checkers required green — `check-claims`,
`check-product-dispositions`, `check-c2-v9`, `check-retention-custody-v24`,
`check-d9-v1.14` — all exit `0`. `check-package-coherence` exits `1` with
`pathsMissing 0`; its finding count moved from 1 to 3 during this session because
a **concurrent lane** edited `artifacts/claim-register.v1.json`. Neither new
finding is attributable to this file, and §7 sets out both the mtime evidence and
the structural reason a file under `deltas/` cannot produce a `PC-2` finding.

This file cannot affect `PC-1` dead-link detection in either direction:
`check-package-coherence.py` scans markdown links in `IMPLEMENTATION-FREEZE.md`
and `IMPLEMENTER-BLUEPRINT.md` only, and this file is linked from neither. Its
own links were nonetheless resolved on disk by hand.

---

## 5. Independent review and adjudication — §10 item 5

**OPEN. No review of this file exists and none is claimed. The author is not
independent of it.**

What a reviewer should try to falsify, in descending order of consequence:

1. **The completeness of §1.1 and §1.2.** The claim is that *all fifteen*
   register rows are covered. One uncovered row falsifies the central finding.
   The quickest attack is `GX-02`'s generation lifecycle and `GX-05`'s
   candidates: confirm blueprint §2.1 rule 3 and §8.4 genuinely bind them rather
   than merely mentioning them.
2. **Whether this file is itself a paper seal.** It defends itself in §0.1 by
   proposing nothing. A reviewer who finds any sentence that *functions* as a
   change — a coverage verdict that would be cited later as authority, a
   disposition that reads as adjudicated — should reject it. **The right outcome
   for this file may be to note the finding and discard the document.**
3. **The §1.4 measurement.** 37 files, the 7/12/18 split, and the claim that
   `check-retention-custody-v24.py` validates `citedNotGated` shape without
   recomputing its digest are all mechanically re-derivable. Re-derive them.
4. **The §0.3 evidence ceiling.** If a reviewer *can* read upstream, every
   UNVERIFIED marking becomes checkable, and any register row that misdescribes
   Gortex would invalidate that row's triage — though not, note, the coverage
   citation on the OpenSIP side.

Under §7.2.1 the reviewed subject must be frozen before dispatch. If this file is
dispatched, its SHA-256 at dispatch must be recorded, and any later edit requires
a `v2` and a new verdict.

---

## 6. Compatibility and migration impact — §10 item 6

**None, in every dimension.** No product behavior changes; no implementation
exists to migrate — freeze §11 reads `[NOT FROZEN]` and carries no permission to
start Phase-5 implementation; no stored data changes shape; no identity, recipe,
or park is closed, narrowed, or reinterpreted.

`FactViewId`, cache and regeneration key recipes, `RunId`, sealed-Run manifest
identity, `EvidenceDigest`, finding fingerprints, `subjectScopeCommitment`,
`capabilityManifestId`, and `policyOutcome.derivationDigest` all remain exactly
as parked. Nothing here may be read as closing any of them.

---

## 7. New freeze version, payload manifest, snapshot reference — §10 item 7

**CANNOT BE FILLED, AND IS NOT INVENTED HERE.**

`IMPLEMENTATION-FREEZE.md` §11 reads, live at 2026-08-04: `Disposition: [NOT
FROZEN]`, `Freeze version: [UNSET]`, `Payload hash: [UNSET]`, `Snapshot/tag:
[UNSET]`. §9.2 is likewise `[UNSET]` throughout. There is no version to
increment. Writing plausible values here would be a fabricated field of the class
freeze §4.4 exists to record.

One consequence a reviewer should note rather than have restated as a field:
§9.2's manifest covers the complete `docs/coop/` snapshot, so **this file is
inside that payload** and its mere existence moves the payload hash before
anything is adopted. That is correct behavior, not a defect.

### Verification record

Executed 2026-08-04 from `docs/coop/`, `python3 -I -B`:

```text
check-claims.py                  exit 0
check-product-dispositions.py    exit 0
check-c2-v9.py                   exit 0
check-retention-custody-v24.py   exit 0
check-d9-v1.14.py                exit 0
check-package-coherence.py       exit 1 — FINDINGS: 3
    PC-7-PINNED-ARTIFACT-IS-REJECTED  artifacts/rust-provider-protocol.v2.json
    PC-2-DIGEST-DRIFT (FREEZE)        artifacts/claim-register.v1.json
    PC-2-DIGEST-DRIFT (BLUEPRINT)     artifacts/claim-register.v1.json
    pathsReferenced 49 · pathsMissing 0
```

**The pre-write baseline was `FINDINGS: 1` (`PC-7` only). Two findings appeared
while this file was being written, and neither is attributable to it.** Stated
precisely rather than smoothed over, because an unexplained finding count is the
kind of thing this corpus is built to refuse:

- Both new findings are `PC-2-DIGEST-DRIFT` on `artifacts/claim-register.v1.json`
  — its live bytes no longer match the digest recorded for it in either the
  freeze or the blueprint (`recorded a83fac4df620… actual 1a16f7510a9a…`).
- The cause is a **concurrent lane**, evidenced by mtime: `claim-register.v1.json`
  moved `1785812696 → 1785824555`, `IMPLEMENTER-BLUEPRINT.md` moved
  `1785823854 → 1785824622`, and `IMPLEMENTATION-FREEZE.md` moved
  `1785824323 → 1785824429`, all during this drafting session and none by this
  lane. This file wrote nothing outside `deltas/`.
- It is also **structurally impossible** for this file to produce a `PC-2`
  finding: `PC-2` iterates only the artifact/digest pairs recorded in the freeze
  §3 ledger and blueprint §1.1 table. This file appears in neither, is linked
  from neither, and records no digest of anything.
- `pathsMissing` remains `0`. This file introduced **no dead link**; `PC-1` scans
  markdown links in the freeze and blueprint only, and this file is referenced by
  neither. Its own links were resolved on disk by hand regardless.

The `PC-2` drift is another lane's to reconcile and is recorded here only so this
file's verification record is not read as claiming a cleaner tree than exists.

```text
47df412dba5d62a823ca7c008c382c489b8a10c797fd8656f3d4dd5d6c342e2e  ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md
4c11eae011aeda4a6f69d2b833259b1758985f87768e1dd3e24b0213b0a8f52d  deltas/gortex-graph-lanes.delta-draft.v1.md
```

both unchanged after this file was written.

**Files modified by this draft:** none. **Files created:** this one, under
`deltas/`. Confirmed by mtime comparison across the whole of `docs/coop/`.

**Sources this triage is entitled to rely on:** `GORTEX-BORROW-REGISTER.md`
(non-authoritative, §0.3), the sibling draft, and the live corpus. **The network
was not fetched and the upstream Gortex repository was not read.** Every
statement about upstream behaviour is marked UNVERIFIED and is a paraphrase of
the register, not an observation of code.
