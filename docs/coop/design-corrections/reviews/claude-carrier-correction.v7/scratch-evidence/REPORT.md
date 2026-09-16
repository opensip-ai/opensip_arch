# Carrier correction, pass v7 — bounded consistency correction

**Standing: NOT-SELF-ACCEPTED.** This is a bounded design/reference correction written in this
runtime scratch only. Nothing here is accepted, qualified, implementation-ready or authorized for
application. Source25, every previous runtime and the live repository were read-only throughout.
Root assesses, merges with the separately authored PS01 and PS04 work, and obtains fresh
independent review on the merged frozen successor.

**The v6 control results do not cover these bytes, and are not reused.** The v6 attempt-custody
schema shipped with a duplicate `admitted` key, and every v6 check over it passed, because
`json.load` is last-wins: the parser silently discarded one of the two values before any assertion
ran. Every JSON admission in this pass goes through `object_pairs_hook` duplicate-key rejection,
and C17 asserts that the **v6 bytes are rejected** by it, so the check is demonstrated able to fail
rather than merely observed to pass.

---

## 1. The six corrections

### 1.1 `attempt-custody.schema.v1.json` — duplicate key, overclaimed durability, scope, joins

- The duplicate `admitted` key is gone. The two colliding values are merged into one coupling key.
- `tracedExistingOwners` no longer claims the identity §2 reservation already makes every attempt
  record durable. It is split into `whatExistingLawGives` (a **pre-use uniqueness** rule, all
  request modes), `whatExistingLawDoesNotGive` (*"does NOT establish durable permanent storage… a
  uniqueness check before use can be satisfied without retaining a durable per-attempt row after
  the request ends. Treating the reservation sentence as proof of durable persistence was the v6
  error and is withdrawn"*), `whatThisRecordAdds` (a **separate, scoped** durable private record),
  and `excludedModes`. The v6 claim that "no second record is added" is withdrawn: a second record
  **is** added, scoped to durable-authoritative commit-capable attempts.
- Recovery §5 is scoped the same way. Read-only requests and `--ephemeral` acquire **no** row.
- The phase description now says a stopped cleanup-only session may **not** write it, and
  `laws[0]` names the two writers that may: the guarded commit facade while its session is live,
  and the authorized settlement sweep under the install fence plus EXCLUSIVE.
- `joins.toReceipt` is **MANDATORY** on `runId`, `commitSequence` and `inventoryDigest` — taken
  from the receipt, never from caller-supplied request fields. The "where the caller supplies them"
  wording is removed.

### 1.2 `carrier-dispatch.v3.json` — row-last detection

`openDispatch.order` was table-existence detection while `migration.detectionIsKeyedOnTheFormatRow`
said otherwise. The order is now an explicit eight-step, row-last algorithm:

| step | condition | result |
|---|---|---|
| 1 | observe object **names** in `sqlite_master` | no table contents read |
| 2 | none of the seven present | go to step 6, reading no v3 table |
| 3 | some but not all seven | `MIGRATION.CORRUPT` |
| 4 | all seven names, any stored definition differs | `MIGRATION.CORRUPT` |
| 5 | all seven names and all definitions valid | read `carrier_format`: row → 3, absent → incomplete footprint |
| 6 | `grant_journal` + `gj_seq_contiguous` | 2 |
| 7 | `grant_journal` | 1 |
| 8 | no journal table | fresh install: create carrierFormat 3 directly |

Step 4 exists because **a malformed stub can carry all seven names** with wrong definitions, so
name presence alone is not enough to justify reading the row. Step 8 states the fresh-format-3
empty-install path without reading absent tables (`freshInstallPath.readsAbsentTables: false`).

C18 executes this selected algorithm — not a paraphrase — over: the fresh empty install, fresh
after acts B and C, inherited 2, inherited 1, lawful prefixes A / AB / ABC, a lone stub, six of
seven, all-seven-names-all-invalid, and all-seven-names-one-altered. It asserts `contentReads == 0`
for every corrupt, inherited and fresh case and `== 1` only when the object set is complete and
valid. 20 checks, 0 failed.

C2's legacy five-case dispatch table is labelled as the superseded v5/v6 evidence it is; the
selected algorithm is the one in the dispatch document and the one C18 exercises.

### 1.3 Proposed fault cases — six corrections, IDs and F32 preserved

F47 (no installation transition intent or journal is written), F48 (carrierFormat-**aware** versus
format-**unaware**, not a blanket typed refusal), F50 (one explicit transaction; commit or barrier
uncertainty **stops** the attempt, no stale retry), F52 (receipt-present-while-`admitted` is the
**lawful pre-settle interval**, not a contradiction), F38 (an actual aborted action distinguished
from an observer standing before any sweep, consistent with F36), F40 (two senses of terminal: D9
terminality for retry purposes is not durable settled custody).

IDs F38–F53 are unchanged, F32's root fix is preserved byte-identically, and **all sixteen added
cases are `not-executed`.**

### 1.4 Prose scoping

- S9's first paragraph is scoped to format-**aware** cores: such a core supporting only {1, 2}
  refuses; a format-**unaware** core cannot be made to refuse at all.
- S12 gains a fifth row excluding a valid joined receipt present while the attempt row is still
  `admitted` from the busy and custody conditions.
- carrier-format §7's "a second migration aborts because the table already exists" is scoped to
  the historic C2 evidence and explicitly **not** the current recovery law.
- carrier-migration's "unmigrated carrier is fully usable" is scoped: historical **reading** is
  unaffected; current authoritative **writes** are not possible and refuse with the F31 standing.

### 1.5 Recovery v3 steps 3/4 and §5/§6 are complete standalone

No step defers to "unchanged from v2". Step 3 is totalized with the five-observation capture block,
its bounds, the closed witness shape, the requested-sequence-versus-tail/floor checks, the ordering
hazard, the domain-framed SEAL join at *k*, a five-row anchor table and a determinism paragraph.
Step 4, §5 and §6 are stated in full.

New §2.2 covers the previously uncovered case: an AttemptCustody row **missing** while a receipt
and association are present. It yields two separate answers — commitment `committed-historically`,
settlement `custody-unknown-legacy` — and **no negative conclusion**. New §2.3 distinguishes a
logically retained tombstone from physically missing bytes, and states that no receipt is ever
reconstructed, synthesized or forged from a tombstone.

### 1.6 Stable normative paths

`attempt-custody.schema.v1.json` and `carrier-fault-cases.v1.json` now live at
`docs/v2/architecture/`. All references are repo-relative. No stable normative file resolves its
**law** through `scratch/` or `owner-correction.v3`. PS01 is consumed unchanged at
`docs/v2/architecture/store-instance-lineage.v1.json` and PS04 at `report-asset-binding.v1.json`.

---

## 2. What my own new checks found in my own work

Two defects, both fixed, both now carried by a negative control:

1. **A real law-deferral leak.** carrier-migration §6 said the PS-01 lineage allocation "is in
   `owner-correction.v3`" — exactly the dependency finding 6 prohibits, since a repo consumer
   cannot resolve it. It now cites the stable owner path and restates nothing. C19's **N20**
   reintroduces the original sentence and the selected validator rejects it.
2. **A misplaced flag lookup in my own new check.** I asserted `detectionIsKeyedOnTheFormatRow`
   under `openDispatch`; it lives under `migration`. Corrected, and the dispatch and migration
   orders are now cross-checked against each other.

---

## 3. Executed controls, over these bytes

| control | result |
|---|---|
| C1 inherited carrier laws | rc 0 |
| C2 carrierFormat 3 DDL, migration, dispatch probes | rc 0 |
| C4b **selected** validator `check-carrier-v3.py` | **87 passed, 0 failed** |
| C6 concurrency schedules | **78 653 schedules, 0 violations**, all coverage assertions held |
| C7 PS05 gate bits | **132 schedules, 0 violations**, all four states observed |
| C8 incompatibility inventory | rc 0 |
| C9 owner patches | 2 owner + 2 planning files, **both owner before-digests match the frozen manifest**, F32 preserved |
| C10 bounded validator `check-correction-v7.py` | **95 passed, 0 failed** |
| C12 D9 projection | **42 passed, 0 failed** |
| C13 migration prefixes | **50 passed, 0 failed** |
| C14 settlement | **57 passed, 0 failed** |
| C15 root atomicity replay | **7 passed, 0 failed**; v5 act B left `["carrier_format"]`, corrected act B leaves `[]` |
| C16 receipt join | **22 passed, 0 failed** |
| C17 strict JSON + propagation (new) | **73 passed, 0 failed**; v6 bytes **rejected** as `DUPLICATE KEY: admitted` |
| C18 selected dispatch (new) | **20 passed, 0 failed** |
| C19 negative controls (new) | **20 drifts, 20 detected**, 19 clean failures |

C19's one non-clean detection is N1: reintroducing the duplicate key makes the strict loader raise
`ValueError: DUPLICATE KEY: admitted` before the check body runs. That is a correct detection, and
it is reported as a crash rather than as a failed check.

### Selected file digests

| file (repo-relative) | v6 sha256[:16] | v7 sha256[:16] | bytes |
|---|---|---|---|
| `docs/v2/architecture/attempt-custody.schema.v1.json` | `c7e22e9e6baa22fc` *(at v6 flat path)* | `37f1445c573a31be` | 22 865 |
| `docs/v2/architecture/carrier-fault-cases.v1.json` | `475a9233d4312ddd` *(at v6 flat path)* | `d510662ce455b851` | 22 499 |
| `docs/v2/architecture/commit-recovery-readonly.v3.md` | `c60090301401098e` | `a60b048c82db55e6` | 30 791 |
| `docs/coop/design-corrections/security/carrier-dispatch.v3.json` | `00c31e174aaa308f` | `e3ce0d5f6172cead` | 25 077 |
| `docs/coop/design-corrections/security/carrier-format.v3.md` | `e58676b5d947c88e` | `ecbe4362332f67a2` | 35 531 |
| `docs/coop/design-corrections/security/carrier-migration.v1.md` | `dcfdc509359215ca` | `227fb89c7159700f` | 16 731 |
| `docs/coop/design-corrections/security/check-carrier-v3.py` | `464aa4e4cb9fe970` | `137f5cb77eaf9859` | 22 996 |
| `docs/coop/design-corrections/security/carrier-highwater.schema.v1.json` | `1bbfd9135bd9492e` | **unchanged** | 3 366 |
| `docs/coop/design-corrections/security/grant-journal.carrier.v3.sql` | `23902324163196cf` | **unchanged** | 7 019 |

---

## 4. Remaining limitations

Architectural and disclosed:

- The **format-unaware old-core** limitation stands: a core that predates `carrierFormat` cannot be
  made to refuse a migrated carrier, because it has no concept to refuse on. Release ordering is an
  implementation and release obligation, not something this correction can close.
- Confirmation is `confirmed-under-retained-custody` only, and `chain_law = 1` only.
- The two-agreeing-tails clause is a deliberately conservative diagnostic policy.

Limits of what was executed here:

- **Nothing here is a qualification gate.** All sixteen added fault cases F38–F53 are
  `not-executed`.
- The `no-run-directory-for-LAW` scan uses a **lexical** classifier to separate evidence citations
  from law. It caught the real leak in §2 above, but a law deferral phrased as an ordinary evidence
  citation would pass it. It is not an exhaustive proof.
- C18 drives in-memory SQLite through the same helper the DDL uses. It establishes nothing about a
  real file being concurrently mutated by a foreign writer.
- Act B atomicity is established only as in-memory transaction behaviour (C13, C15). Nothing here
  establishes fsync, `F_FULLFSYNC`, OS durability or real crash behaviour.
- C6 interleaves a **model**, not two OS processes. Process isolation and real process control are
  unmodelled; F42 has no feasible model in this runtime.
- The authorized settlement sweep is **specified** and its decision matrix is reference-executed in
  C14. Its execution remains, as qualification.
- No Rust compiles here. No API sketch is type-checked.
- Byte compatibility of the pinned `prev_sha256` encoding with a real carrierFormat 1 or 2 instance
  is unestablished: no such instance and no fixture exists in the reviewed corpus.
- F00–F37, the final sourcepins, the final normativekit and the final integrated checks are
  root-owned and were not edited or assessed here.

Frozen bytes, digests and per-control reports: `scratch/output-manifest.json`. Reproduction:
`scratch/REPRODUCE.md`.
