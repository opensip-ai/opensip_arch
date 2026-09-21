# Independent review — corrected initial-root owner 397

Reviewer: Claude Opus 5 (1M context), `claude-opus-5[1m]`. Capacity available; substantive review
performed. Bounded owner/reference review, document and model only.

**Top verdict: NEEDS-CHANGES.**

**All nine of my 392 findings — B-1, B-2, B-3 and N-1…N-6 — are closed**, and closed well: several
corrections go past what I asked for. Every citation the corrections introduce, I re-derived from the
selected sources rather than accepting it.

NEEDS-CHANGES is for **two blocking defects inside the newly written §5**, both in the doctor
diagnostic that B-1(c) asked for. Root asked me to critique that diagnostic specifically and not to
grant blanket approval because the 390 findings closed; this is that critique. Two smaller findings
follow, including a fifth model gap beyond the four §10 declares.

---

## 1. Verification

### Pins and members

| Artefact | Declared | Observed | Match |
|---|---|---|---|
| `…/trials/initial-root-binding-proposal-397/subject.tar.xz` | 34 256 B, `f089c050a0d8e09d9f5c647c8bfabeec432386f4d3e3bd495af3a378f041f7bc` | identical | ✓ |
| `…/trials/initial-root-binding-proposal-397/subject.json` | 5 547 B, `4fc15f6d960c6a3a658239a6b162ea87901f3aae3066b2b90a6c4925cdf7bb8c` | identical | ✓ |

Both pins verified **before** extraction; extraction went only into this review directory.
**36 / 36 members** verified byte-for-byte and by sha256: 0 missing, 0 extra, 0 mismatched, 0 unsafe
(no symlink, hard link, absolute path, `..` component, non-regular member).

### Source anchors — 34 of 35 live-match, and the one that does not is the expected one

All **13 product anchors match at `cd5af4d`**. Exactly one anchor does not match live:

| Anchor | Declared (= `cd5af4d`) | Live now |
|---|---|---|
| `crates/platform/src/filesystem.rs` | 73 907 B, `9a02dcbb3f2343cab623dba9258fb68d1803938395f557867043c2c0defc82cd` | 81 671 B, `87636b866277a93811b93e38337d753666ba339246774ec153e49bdf4a5f029a` |

**Both provenances, reported honestly.** Root integrated runtime32 at product `ef3b1b51c`
(2026-09-21T15:36:08-07:00) while this review was running. The declared anchor is the **historical**
`cd5af4d` value and still resolves there exactly, so no 397 pin is stale and none should be edited.
The live divergence is precisely the source395 delta I accepted in the runtime32 review — and I
confirmed the integrated bytes are **byte-identical to the candidate I accepted** (`filesystem.rs`
`87636b86…`, `lib.rs` `8cbed576…` both equal my staged tree). From that review the delta is additive
documentation plus one test rename, with `confirm_directory_with` byte-identical, so **no anchored
behaviour moved**; only added documentation and a test name did.

### Evidence provenance inside the archive

The 392 artefacts the README says are "copied byte-for-byte" are — checked against my own retained 392
copies, not against the manifest: `preinstallation_model.py`, `check_preinstallation.py`,
`publication_model.py`, `check_publication.py`, `check_digest_compatibility.py`, `lineage_probe.rs`,
`run_lineage_probe.py` and all four frozen result JSONs are **byte-identical**.

### Replay

| Check | Result | Frozen output reproduced |
|---|---|---|
| `check_surfaces.py` (**new** in 397) | **PASS 32 cases** | `surface-checks.json` identical |
| `check_preinstallation.py` (historical 392) | PASS 54 | identical |
| `check_publication.py` (historical 392) | PASS 36 | identical |
| `check_digest_compatibility.py` (historical 392) | PASS 7 vectors / 9 refusals | identical |

The author ran the new surface checks under Python **3.14.6** (`/opt/homebrew/opt/python@3.14/…`); I
ran them under the system `python3`. Identical output, so the result is not interpreter-dependent. The
digest script needs `jsonschema` and was run under
`/tmp/opensip-implementation/source-audit364-env/bin/python` (3.12.13, jsonschema 4.25.1) — the same
disclosed substitution as in 390 and 392. The seven lineage checks are carried 390 evidence and were
**not** rerun; my own 390 rebuild remains the record. I make no fresh-native or composed-creator claim.

---

## 2. Closure of the 392 findings

Checked against the new bytes and against the selected sources they cite.

### B-1 — read-only surfaces — **CLOSED**, all three parts

- **(a)** §5 replaces my objectionable conditional with a determination: *"Selected §5.6 categorically
  forbids durability primitives on metadata-only commands and doctor. `doctor`, `trust doctor` and
  `store status` remain report-only for installation durability; S7's fence-only permission is not the
  blocker."* That is exactly the finding, with the right citation and the right diagnosis of which
  conjunct blocks.
- **(b)** The fork I described is resolved by defining a third option I had not: an explicit
  **observation-only binding** path. SHARED-READ surfaces may run §7's registry/endpoint/node/binding
  observations under the fence, then take their normal S7 read lease — with no barrier, initialization,
  metadata repair, clock/high-water write, no serialized form, and no conversion into a write
  capability. Queries stay usable: *"root durability not tested is NOT itself
  `queryResponse.context.availability` unavailability"*, and `query-latest-empty` /
  `query-completeness-unmet` keep their selected behaviour. Good resolution.
- **(c)** Reported through doctor's existing `defects` channel with a fixed code, no new parity field.
  The mechanism is right; **two consequences of how it is specified are not** — see C-1 and C-2.

I verified the SHARED-READ list against selected S7 line 671. It matches exactly — `query`,
`recommend`, `baseline show`, `policy show|test`, `candidates`, `inspect`, `review brief`,
`repair preview`, `agent serve` reads, `doctor` project checks — plus `repair recover` inspection,
which selected S7 legitimately supplies from the EXCLUSIVE row's parenthetical. One entry has no
referent: see C-3.

Every exit code and class §5 and §6 cite is correct against the selected goldens: request-rejected = 2,
indeterminate = 3, operational-failed = 4, success = 0; `doctor-report-not-producible` is exit 4 and
`query-completeness-unmet` is exit 3.

### B-2 — first-creation backup custody — **CLOSED**

The new "First-creation storage choice" block states the consequence I said was missing, and states it
more completely than I asked: `--allow-backup-custody` required **before any ancestor/stage effect**;
CI refusal `REQUEST.PRECONDITION_FAILED` / `storage.backup-choice-required`, exit 2; `--ephemeral` is a
separate no-creator route and *"not a creator permit or an automatic fallback"*; *"There can be no
already-admitted installation storage-policy record before I exists"*; *"The fixed account root has no
'choose another admitted root' remedy here"*; `UNKNOWN` keeps its selected mandatory disclosure. §1a
step 5 now orders the decision before ancestor effects. The one thing with no evidence behind it is
that ordering — see C-4.

### B-3 — absent I for a non-eligible invocation — **CLOSED**

§6 gains the row I asked for and goes further: request-rejected, exit 2,
`REQUEST.PRECONDITION_FAILED`, new domain detail `INSTALLATION.NOT_INITIALIZED`, explicitly covering
`import`, `baseline-upgrade`, `repair-apply`, `test-run`, `native-prepare` *"despite
`firstSourceWrite:true`"*, plus `repair-verify` and any read request requiring the installation; no
implicit ephemeral fallback, no automatic analysis; a stated remedy; and separate handling for
report-only diagnostics and for commands that do not require I.

### N-1 … N-6 — all **CLOSED**

| Finding | Correction | Verified |
|---|---|---|
| N-1 citation | now "registry-v2 owner.md, opening delegation paragraph and 'Registry snapshot and first-use observations'" | both anchors resolve; the delegation is at line 9 and line 33 |
| N-2 rule not list | states `authority == "authoritative-default"`, reconciled with S7 APPEND-WRITE and identity §5; excludes `repair-verify` structurally; *"`firstSourceWrite` alone is NOT the discriminator"* | re-derived: `authority == authoritative-default` is exactly `{default, analyze, fit, audit, repair-verify}`; `firstSourceWrite` is a **ten**-command set |
| N-3 label | *"requiring the actual storage-root identity in that disclosure is NEW content beyond identity §5's retention-origin/durable-unbounded disclosure"* | identity §5 requires posture and origin only ✓ |
| N-4 boundary set | §2: *"explicitly EXTENDS §5.6's operation-boundary set"* with H, each fixed/staged directory and parent, the I-parent barrier and §5's reconfirmation; *"Only an admitted creating or writing operation pays these new boundaries"* | ✓ and it ties the extension to cost scoping, which is what made it matter |
| N-5 obligations | §9 now names *"a distinct pre-installation platform evidence producer that does NOT borrow an existing installation fence"* and *"qualification of the pre-existing account-home durable-reachability premise"* | ✓ both items, as asked |
| N-6 model gaps | new **§10** lists all four verbatim and says they are "explicitly UNIMPLEMENTED coverage" | ✓ |

N-2's correction adds something I did not ask for and should have: *"A future inventory change must
reconcile this owner and supply the new command's prerequisites before extending creator eligibility; a
new enum value or a recipe cannot silently widen this closed set."* That closes the divergence risk the
enumeration created.

---

## 3. The critique root asked for: doctor's always-unchecked diagnostic

### C-1 (blocking) — `defects-found` becomes permanently true, defeating the selected CI contract

§5 specifies: emit `INSTALLATION.DURABILITY_NOT_CHECKED` through `defects` whenever a complete I is
observed, *"even if another invocation historically confirmed I"*, and **"set `defects-found` true"**.

Probe S1: across every healthy world the model admits, doctor returns exactly
`Result(kind='report', exit=0, detail='INSTALLATION.DURABILITY_NOT_CHECKED')`. There is no
configuration of a healthy installation in which it does not fire. `defects-found` is therefore
**constant true** for every successful doctor run, forever, by design.

The selected golden `doctor-defects-found` (class success, exit 0) carries this remedy text:

> **"CI must inspect `doctor.defectsFound`; exit 0 means the report was produced"**

Selected law directs CI at that boolean as *the* actionable signal, because exit 0 deliberately does
not discriminate. 397 makes the boolean uninformative: a corrupt closure, an expiring trust root and a
perfectly healthy installation all report `defects-found: true`. Any pipeline following the selected
remedy breaks permanently on first upgrade.

There is a second, principled problem underneath. §5 tells consumers *"Consumers must not treat this
fixed code as a proved durability failure"* — an instruction to disregard an entry in the defects list.
A `defects` channel describes the **subject's** state; this entry describes the **observer's**
permissions, which are fixed by selected §5.6 and identical on every run. A constant property of the
tool is not a defect of the installation.

*Required:* keep the diagnostic — it is honest and worth reporting — but do not let it set
`defects-found`. Either state that `defects-found` counts only actionable defects and that this
informational code is excluded, or give it a severity/kind within `defects` that the selected golden's
CI contract can filter on. If neither is possible without touching a parity field, say so explicitly,
because §9 currently forbids that.

### C-2 (blocking) — two of the three named diagnostic surfaces have no channel for the text

§5 ends: *"Other diagnostic surfaces use their existing report channels with the same fixed explanatory
text."* Checked against the selected inventory:

| Surface | Parity fields | Has a defects/report channel for this? |
|---|---|---|
| `doctor` | `report-produced, outcome, defects-found, defects, offline-window, termination-class` | yes |
| `trust-doctor` | `report-produced, outcome, **floors**, offline-window, termination-class` | **no `defects`** |
| `store-status` | `migration-state, lease-mode, termination-class` | **no report channel at all** |

The instruction is unimplementable for `trust doctor` and `store status` without adding a parity field —
which §9 of this same draft forbids ("without changing the selected envelope or parity fields"). That
is an internal contradiction, and probe S4 shows the model cannot detect it: `Mode` has a single
`DOCTOR` member, so the three surfaces are indistinguishable in the only evidence the unit carries.

*Required:* either name only `doctor` as carrying this diagnostic and say the other two simply do not
report it, or identify the exact existing field on each surface that carries it, or record the parity
addition as a named reconciliation item alongside the two new domain details in §9.

### C-3 (non-blocking) — `recover(ExecutionId)` has no referent

§5's SHARED-READ list contains `recover(ExecutionId)`. No such command exists: `command-inventory.v3`
has `repair-recover` (`opensip repair recover REQUEST-ID`), `trust-recovery-challenge` and
`trust-recovery-import`, and S7's SHARED-READ row names none of them. `ExecutionId` is a workflow
identity (`exec1_` + 32 hex, identity §2), not a command parameter here. The list separately and
correctly names "`repair recover` inspection", so this appears to be a duplicate that drifted.

This is the same class of defect as N-1, inside the section written to correct N-1's siblings, and
probe S3 shows why the model cannot catch it: the surface model has four coarse modes and no command
granularity, so the SHARED-READ list is entirely unmodelled. Since §9 requires formal reconciliation of
this text, an unresolvable name will surface there.

### C-4 (non-blocking) — a fifth model gap, not declared in §10

§10 declares four gaps, correctly and in my own terms. There is a fifth, and it is about the B-2
correction specifically.

`initial_storage_choice` is a **free function**, not a `Session` step (probe S5). No check composes it
with `parents()` or stage allocation, and the preinstallation model — copied unchanged from 392 — has
no backup concept at all (`'backup'` does not appear in its source). So the *decision* is well modelled
across `BACKED_UP`/`UNKNOWN`/`NOT_BACKED_UP` × acknowledged × ephemeral × disclosure, but the
**ordering** — §1a step 5's "before any ancestor/stage effect", which is the load-bearing half of B-2 —
has no evidence anywhere in the unit.

*Required (non-blocking):* add it to §10's list, or compose the choice into the preinstallation
session so that an unacknowledged `BACKED_UP` world provably reaches `parents()` with zero effects.

---

## 4. Reviewer probes

Eight adversarial probes against the frozen 397 surface model — not the author's cases
(`evidence/reviewer-probe-397.txt`, `evidence/reviewer-probe-397.json`).

| Probe | Result |
|---|---|
| **S1** does the doctor diagnostic ever not fire on a healthy installation? | **never** — unconditional by construction. Basis for C-1 |
| **S2** is `defects-found` modelled? | **no** — `'defect'` does not appear in the model; `Result` is `{kind, exit, detail}`. The decision I am challenging has zero coverage |
| **S3** can the model distinguish individual SHARED-READ commands? | **no** — four coarse modes. Basis for C-3's invisibility |
| **S4** are `trust doctor` / `store status` distinguishable? | **no** — single `DOCTOR` member. Basis for C-2's invisibility |
| **S5** is the storage choice ordered before ancestor effects anywhere? | **not composed** — free function, no check pairs it with `parents()`/stage, no backup concept in the preinstallation model. Basis for C-4 |
| **S6** after a read, can a separately admitted write proceed? | yes — reader refused `confirm_for_write`, a fresh WRITE session confirmed and wrote. **Faithful**: the bar is on promoting a read, not on a separate write |
| **S7** can a doctor session reach a barrier by any route? | **no** — gated on `Mode.WRITE`; `barrier_effects` stayed 0. Faithful to selected §5.6 |
| **S8** does acknowledging backup custody authorize creation? | best outcome is `creator-storage-step-only`. **Faithful** — a step, never a permit |

S6, S7 and S8 matter as much as the failures: the read/write split is structurally sound in the model,
and the backup acknowledgement cannot be mistaken for a permit.

---

## 5. Limits

- **Level:** document and model reading, archive/anchor verification, model replay and probing.
- **No native tests run**, as instructed; none needed.
- **Not qualified:** native eligibility producers, actor/custody/profile qualification, exclusive
  directory rename, directory barriers, crash and power-loss behaviour, GC, Linux, release.
- **Not rerun:** the seven supplied-lineage checks (carried 390 evidence; my 390 rebuild is the record).
- **Not re-reviewed:** runtime32/source395 (separate unit, separate ACCEPT), the 391 and 396 native
  work, runtime30, registry-v2, inventory58. Inventory v59 is reviewed separately and neither review
  depends on the other.
- **Unselected references remain unselected:** this owner, S9.3, `store-instance-lineage.v1.json`,
  `host-foundation-completion.v2.md`, 215.
- **Replay caveat:** the four replayed checks run the author's scripts. The independent parts are the
  392→397 diff, the byte-identity of the copied 392 artefacts against my own copies, the
  re-derivation of every new citation from the selected sources, the interpreter cross-check, and
  probes S1–S8.

---

## 6. Context HEADs — as of 2026-09-21T15:42:23-07:00

Stated as of that sample only. Both repositories may advance between the last sample and the last
written word; the byte pins above, not these labels, are the authority.

| Repository | HEAD | Subject | Committed |
|---|---|---|---|
| architecture | `f657f2a40038c3c87d0133ed969147a054e85cc7` | "Select reviewed directory barrier runtime and freeze exclusive publication source" | 2026-09-21T15:40:11-07:00 |
| product | `ef3b1b51cba879151e58220e64975c5c3a7af441` | "Expose retained directory barrier observations with explicit limits" | 2026-09-21T15:36:08-07:00 |

Both trees clean at that instant. The 397 archive and manifest are tracked, and their committed blob
ids equal their worktree blob ids.

---

## 7. Attestation

Read-only against live, frozen, history, product and lock. No architecture, product, frozen, history or
lock byte was edited; **no pin was edited**, including the historical `cd5af4d` code anchor that live
has since moved past. No select script was run. No commits, no pushes. All writing went into this
review directory; extraction went only there.

This grants no root assent, no formal selection, no passage reconciliation, no native writer or current
authority, no S9.3 or 215 adoption, no M2 completion and no release qualification. The owner392 and
owner390 reports, the 392 eligibility audit, and the source393/formal31 and source395/formal32 reports
are untouched and keep their own standing.

Reviewer: Claude Opus 5 (1M context).
