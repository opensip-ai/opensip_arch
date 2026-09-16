Done. Source25 pristine, v4 immutable, all writes confined to v5 `scratch/`.

## Root's four findings

**1. Carrier migration cannot borrow the logical protocol.** Accepted; the v4 dispatch was wrong. C13 reproduces your counterexample on frozen bytes and asserts the shapes: the intent is a closed **11**-member record, the journal a closed **20**-member record, **neither has a carrier field**. My v4 phrase also conflated an intent with a journal. Withdrawn in both the dispatch JSON and `carrier-format.v3.md`.

New `carrier-migration.v1.md` traces authorization to an existing owner rather than inventing one: `store-gc` — `owner: security`, `authorizationClass: exclusive-lease`, and decisively **`writesTrackedIntent: false`**, which is exactly why it doesn't drag in S9.2. Locks are your S7 fence + non-blocking `EXCLUSIVE`, busy = skip-and-retain; reporting is the existing `store-status` `migration-state` field. No new command, operation, enum or authorization class.

Three atomic acts (TERMINAL → objects → format row), with the **format row as commit point and detection keyed on that row** — that single change is what makes prefix `{A,B}` recoverable rather than merely idempotent. Commit uncertainty on A resolves from the **frozen TERMINAL body's own `operationRef`**, adding no field anywhere. "Table already exists" is explicitly not the mechanism.

**2. AttemptCustodyV1 — and a flaw C14 found in my own draft.** The settlement matrix is normative with exactly one negative cell (`settled` + `refused` + both rows absent). Then C14 showed my `undetermined` outcome was **unresolvable**: the row is immutable, so nothing could ever settle it — your exact objection. Removed. `durability-undetermined` is the D9 *response*; the row stays `admitted`, which *is* the honest unknown; the sweep is the reconciliation. Two outcomes only, because those are the only two provable.

**3. Sweep specified** (§4): same `store-gc` owner, fence + `EXCLUSIVE` as the custody that makes proof possible, one coherent snapshot, writes only `committed`/`refused`, nothing when busy/unreadable/one-sided/already-settled, no authority reuse, GC-only cleanup.

**4. Three claims withdrawn.** DDL now `CHECK (chain_law = 1)`. The "only consistent reading / both operands TEXT" claim was **false** — `seq` is INTEGER — so the encoding is prospective and claims nothing more. The signing-key-requires-networking argument is **withdrawn as unsupported**.

## Your dispositions applied

Items 1/2/5/6 are now selected limits with the chain-head contradiction disposed in S1/S6 (old bytes preserved; no limit listed as both gap and non-gap). Item 4 **settled by execution**: C12 proves `domainDetail` is optional, so `LEDGER.CORRUPT` + `faultCause ledger-corrupt` with **no detail** is schema-valid — nothing minted, `MIGRATION.CORRUPT` not misused. Item 8 selected as law, and C12 additionally demonstrates **`policy-failed`(1) and `indeterminate`(3) survive publication** and that `success` can carry neither an `errorCode` nor `reasonCodes`, so **no lawful reset exists**. Item 9 kept as labelled policy. Item 10 is yours; F32's route and F38–F49 preserved and asserted.

## Two things to weigh

**C11 A8 found that one of my own rules is only policy.** Treating *receipt present but attempt `admitted`* as a contradiction isn't needed for safety — the receipt is the authority. So alongside the second-tail clause, **two** rules are conservative policy, not correctness; both are labelled in the document and you may drop either. I also mis-constructed three drifts as "safe" before getting them right, and fixed them rather than counting them as detections.

**A new gap I did not chase:** `common.schema.json` carries `RunId: run2` while `evaluator3/common.schema.json` carries `run3`. I validated against evaluator3 and asserted the split as the retained-predecessor pattern — but if the non-evaluator3 document is still a live projection owner anywhere, my projections wouldn't validate there.

Executed: C12 39/39, C13 41/41, C14 51/51, C6 78,653 schedules 0 violations, C7 132/0, C4b 74/74, C10 84/84, C11 17/19. `REPORT.md` §5 lists 6 remaining actual gaps, §6 unperformed qualification (still no real processes, no Rust, all 16 added cases `not-executed`), §7 selected limits. No self-acceptance.
