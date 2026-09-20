# Bounded critique — incomplete WIP215 revision 8 (closure of my r7 M-1, M-2, N-1)

Reviewer: Claude. Date 2026-09-19. **Assistance on an incomplete owner; no approval, no protocol acceptance, no root edit, commit or push.** The pending 222 R-2 reconciliation is deliberately not discussed here. Known 222/creator/schema/model-integration omissions are not re-listed.

## 1. Identity and what I ran
- `subject.tar.xz` SHA-256 `8dfbd516802f69cdf62573b760e86a02c83a8c8652146903cb23a4f95d2e017d`, 122,700 bytes, 240 members — equals the request; every member hashed from the tar before extraction; 0 non-regular/unsafe/extra; end pass `re-verified`.
- `beforeimages-r8/OWNER.md` is byte-equal to the r7 `OWNER.md` I reviewed; both schemas byte-equal to r7. The only OWNER change is the missing-`T` ABORT sentence group in D (sentence-level diff).
- Model: my re-run is byte-equal to `ordinary-batch-model-r5.json` (6272; 4096/1024; 18684 states, 862658 edges, 5460 closed). `coordination-corpus-r1/baseline.py` equals the model; `claude-corpus-source.py` is byte-equal to my r7 probe script.
- **Corpus, run independently** (`claude-out/probes/run_corpus.py`, `io/corpus-results.json`): 31 named variants, 29 distinct sources, **31 rejected, 0 survive**, baseline passes; source hashes equal the owner's `report.json`.
- **Disclosure.** My runner globbed `*.py` and therefore also executed `root-corpus-source.py`, which is the owner's *generator*, not a variant. Its first statement is `O.mkdir()` on an existing directory; it raised `FileExistsError` before any read or write, so nothing outside my review directory was touched. I excluded it from the counts above. I should have filtered by the report's case names, not by extension.

## 2. Closure
| r7 | r8 | Status |
|---|---|---|
| M-1 lost/missing assertions | acceptance **decision** asserted against a literal T1 rule (`wrong acceptance decision`), clock write asserted on both refusal kinds, full ordered event trace from an independent oracle, 16-row literal ABORT priority table with per-member results and events, mixed `EXPIRED/TRUSTED` BEGIN seeds with exact selected set, corpus retained and re-run | **closed.** All seven of my r7 survivors (`d`, `f`, `f2`, `j`, `j2`, `n5`, `n6`) are now rejected |
| M-2 COMMIT absent | `commit(world, member_pass)`: interrupted batch cannot commit; success clears binding and staging and advances the head exactly once; any failing member refuses **all** with unchanged state and one refused event each; seven new BEGIN/COMMIT variants rejected | **closed for coordination**, with one wrong expected value — **P-1** |
| N-1 S4 in pre-genesis ABORT | no S4 decision or clock write when time-dependent causes are **known** absent (P0/P1: no accepted-document times, every recovering member never-established, no outside accepted root); records that evaluation was not required; unreadable evidence stays unavailable; existing S4 safeguards otherwise | **closed.** The "known absent vs unreadable" split is exactly the needed condition |
Root's note is right and I agree with not asserting "no TRUSTED after ABORT" globally: an interrupted member later healed by a same-head ordinary import is an ordinary `TRUSTED` role that ABORT must leave alone. The model asserts the correct, narrower property (`aborted[i] != 'TRUSTED'` for members that were `RECOVERY`, plus exact table results).

## 3. New findings

### P-1 (Medium) — the COMMIT oracle asserts the opposite of OWNER C for non-batch roles
OWNER C (unchanged since r5): on recovery COMMIT "Other roles do not gain trust. Preserve REVOKED. **Any other role with previously established non-revoked standing becomes UNBOOTSTRAPPED with private reset cause ROOT_CHANGED**"; C.1 adds that newly applicable OLD revocations for non-batch roles are dispatched *before* those resets.
Model: `commit` returns, and `check_batch_sequences` asserts exactly, `states == ('TRUSTED' if i in binding else state)`. Probe (`io/commit-sibling-probe.json`): seed `('EXPIRED','TRUSTED')` → BEGIN binds role 0 → COMMIT → `('TRUSTED','TRUSTED')`, head +1. The non-batch sibling keeps `TRUSTED` standing, accepted under the *replaced* root, across an authorized root replacement. The limits string lists only "typed-absence resets" as out of scope, so this is not a declared exclusion — it is an exact-equality oracle encoding a rule the prose forbids, and with mixed BEGIN seeds it is now exercised on every such path.
**[P] bounded correction:** expected COMMIT after-state per role = `TRUSTED` if in binding; `REVOKED` if `REVOKED`; `UNBOOTSTRAPPED` (with a `RESET/ROOT_CHANGED` record in the trace) if established and non-revoked; unchanged if never-established. Add the variant "commit leaves non-batch TRUSTED sibling TRUSTED" to the retained corpus. (A batch whose interrupted member was later healed cannot commit, so that case does not interact.)

### P-2 (Low) — the explored world never contains a non-`UNBOOTSTRAPPED` abort result
The 16-row priority table is checked through `abort()` directly (good), but the transition actually taken in the exploration is `batch_abort`, which always supplies all-false causes, so every post-ABORT world has its former members at `UNBOOTSTRAPPED`. Post-ABORT worlds with `EXPIRED`/`STALE-REVOCATION`/`QUORUM-LOST`/`REVOKED` results — from which a *restart* BEGIN and head-advance should be exercised by `check_barrier` — are never enqueued. Cheap to close: enqueue the `aborted` worlds from the table loop (with binding/staging cleared) as possibilities.

### P-3 (Low) — refused-BEGIN audience when a batch is already begun or nothing is staged
`begin_decision` emits no events for "batch barrier or no staging" and events for every role when nothing is applicable. The no-staging case matches 222 r3 (no authenticated scope ⇒ pre-dispatch). The **barrier** case is not stated anywhere in OWNER: is a second BEGIN during a begun batch a pre-dispatch refusal (model) or a dispatched `RECOVERY-BEGIN-REFUSED` to the signed-scope roles (v14's fallback from `ST-RECOVERY`)? Either is lawful; write one sentence so the model's choice is a rule rather than an accident.

### P-4 (Low) — seventeen corpus rejections are bare `AssertionError`
All 31 are rejected, but 17 (including all seven new BEGIN/COMMIT variants and the ABORT ones) fail on unlabelled asserts, so the corpus records *that* a variant died, not *which invariant* killed it. A variant killed by an unrelated assertion would be indistinguishable. Add messages to the batch/ABORT/COMMIT assertions and store the expected message per corpus case, as the r3 publication model already does for its three.

## 4. Independent check of the stated claims
Decisions, clock and full event traces asserted — true, against literal state lists and tables rather than the implementation's `ENTRY`. Exact per-member ABORT priority — true (`ABORT_EXPECTED`, bits revoked/quorum/expired/stale; members get rotated rows, which is adequate since `abort` is per-member independent). Mixed BEGIN — true, including the all-`TRUSTED` refusal with a refused event per role. COMMIT accepted/refused coordination, binding/staging clear, one head advance — true, subject to P-1. Counts reproduce exactly. "31 names / 29 distinct" — reproduced.

## 5. Limits
Prose plus one conditional model; I executed the model, the corpus and one small probe importing the unmodified model. N-1's closure is prose-only (the model has no S4), which is appropriate to the model's declared scope. Nothing here approves r8.
