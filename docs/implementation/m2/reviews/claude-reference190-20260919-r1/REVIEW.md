# Independent review — frozen `binding-regressions-reference-checkpoint-190`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: exactly the frozen 190 reference bytes — the follow-ups to my 188 T-1, W-1, W-2, W-3 and N-1. Recovery, model, schema and SQL are claimed unchanged; I verified that rather than assumed it. The 191 custody-chain draft is outside this review and was not inspected. No host, product or cumulative approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `9a43fe0adecc1fc926b8460067d7e048b03ec8a8a1f1bf2c3397a9dc6c5f97d4`, 2,112,912 B = request = `archive-pin.json` |
| Members | 1,382, all regular/safe, verified from the tar before extraction; re-verified at end |
| Candidate pins | 1,299/1,299; none unpinned; declared change list equals computed |
| Parent | equals **my own verified 188 extraction**; 10 changed, 0 added/removed: five manifests, `ledger-mutation-immutability.v1.md`, `security-lifecycle-report.v1.json`, `store-transition-protocol.v1.md`, `store_transition_checks.py`, the build plan |
| "Algorithms unchanged" | 90 of 91 Python files byte-identical; the lifecycle model, selector, observer, phase composition, schemas and carrier SQL are all among the 1,289 unchanged pins. Independent confirmation: my 188 `sweep`, `binding` and `phasec` probes re-run on the 190 tree produce output **byte-identical** to my 188 runs (4,320 states, 0 disagreements; the wrong-id limitation unchanged at 12; every binding fault stops before Phase C) |

## 2. Owner checks re-run

Reference order, `-I -B`, fresh outputs: **all seven lanes exit 0**; integration 1,691 checks / 0 failed (my run). Focused modules alone through the loader: 1,265 checks, 0 failed.

## 3. Closure of my 188 findings

### T-1 — **closed**, verified by re-applying my two survivors (`probes/mutation.{py,json,log}`)
| Mutant | 188 | 190 |
|---|---|---|
| binding required for same-store too | survived | **KILLED** — `same-store read attribution input: activeTransitionBinding` (a context that raises on any attribution read) |
| `journalRef` accepted for any revision of the same journal | survived | **KILLED** — `footprint186.stale-revision.*` |

The new tests are well built: same-store uses an explicit expected table over all six states for `core-update` (same schema), `core-repair` and `core-rollback` (same schema), with no binding, no execution id and no observation in the context; stale-revision uses a **healthy** footprint, so an unavailable-observation shortcut cannot hide acceptance (the exact trap my own 188 probe fell into).

### W-1 — **closed.** `store-transition-protocol.v1.md` "Correction190": journal identity includes state; journal and binding are published as one atomic, durably confirmed carrier revision on **every** state change; separate durable writes are forbidden; a torn pair stops every executor, terminal cleanup included; no reference retry guesses or repairs it; the single-record format and its crash qualification are "prerequisites, not an optimisation". That is the consequence I asked to have stated, stated without softening.

### W-2 — **closed, and done honestly** (`probes/w2_w3.py` → `io/w2_w3.txt`)
The pinned report differs from 188's in exactly: `status` → `HISTORICAL-OUTPUT-NOT-CURRENT-QUALIFICATION`; `standing` rewritten to say the 464-case output is retained from the pre-186 run and that `sourcePinsValid`/`passed`/counts describe that run only; two new top-level members; and 16 leaves = `historical: true` + `qualificationScope` on the eight `migration-recover` entries. **0 leaves removed, no result value altered, case count still 464.** The recorded `historicalSourceReportSha256` (`c7a8723b…113b`) equals the SHA-256 I computed of the 188 pinned file. It labels; it does not pretend to have been regenerated.

### W-3 — **closed**, checked mechanically against the product
For all six tables, the law's tuples == the uniqueness constraints SQLite reports for my verified 187 product DDL == the disjuncts actually written in each product `*_no_replace` guard; `commit_associations` has three; every key column is `NOT NULL`. The law also states the coverage distinction correctly: only the attempt DDL is reference-instantiated; the other five guards rest on the product 187 review.

### N-1 — **closed.** The build plan records the 187 (seven) / 188 + 189 (eight) interval, forbids mixing, denies on-read migration and requires formal selection to join the reviewed pair.

## 4. Remaining test-strength note

### T-1′ (low) — one stale revision per state is tested, not every other revision
The stale-revision regression binds each state's journal to the `LEASED` revision (and `LEASED` to `PREPARING`). A finer mutant — *accept a stale reference only when it names the `PREPARED` revision or later* — **survives all 1,265 checks**. A second finer mutant (accept only the immediately preceding state, the realistic torn-write shape) is killed, but only by the `PREPARING` case where "preceding" happens to be `LEASED`; the same fault restricted to `COMMITTED`/`DONE` journals **also survives all 1,265 checks** (run, `probes/mutation2.{py,log}` — I first wrote this sentence as a prediction and then executed it). Production is correct (exact equality), so this is coverage, not a defect. The complete version is cheap: all ordered pairs of distinct states (30 per changed-store family) → `Unavailable`.

## 5. Owner-prose consistency

I read the four changed documents against each other and against 188's protocol: the atomicity sentence agrees with 188's "one coherent carrier revision" and adds no public journal member ("does not silently add a field"); the ledger law's new table agrees with its existing general sentence; the build-plan note agrees with the 189 README; the report's new standing agrees with the checker's `historical` labels. No contradiction found.

## 6. Limits

A follow-up checkpoint: text, one test module and a relabelled report. Nothing here qualifies a host's single-record publication, which W-1 now makes load-bearing. W-3's comparison is against my verified 187 product tree (storage crate unchanged in 189). I did not rebuild the owner's two mutants.

## 7. Verdict (bounded)

**All five 188 follow-ups are closed in these bytes: both surviving mutants now die on well-constructed tests, the atomicity consequence is stated plainly, the stale report is labelled without altering a single historical result, the six key-tuple sets match the product mechanically, and the compatibility interval is recorded. Recovery behaviour is unchanged (my three 188 probes are byte-identical). One low test-strength residual: stale-revision coverage is one revision per state rather than all pairs.** No host, product or cumulative approval.
