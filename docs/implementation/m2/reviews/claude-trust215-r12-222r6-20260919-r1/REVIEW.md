# Bounded review — frozen incomplete 215 r12 + 222 r6 prose (closure of my T-1 and U-1..U-3)

Reviewer: Claude. Date 2026-09-19. **Scoped to T-1/U-1..U-3; not protocol approval; no root/product edit, commit or push.** The creator (224) reconciliation is deliberately not discussed.

## 1. Identity and what I ran
| Subject | SHA-256 | bytes | members |
|---|---|---|---|
| `trust-owner-wip-215-r12` | `40ffcb7c0682e74bcbf1042fc000094a31ff3a9623f3f50bc504301a82c33ff0` | 161,952 | 996 |
| `trust-capsule-wip-222-r6` | `5b6df2a585caa2dba302354183f83821e309623e06b1c5eb1333dd9d22c41d5c` | 127,388 | 165 |
Both equal the request; every `subject.json` member of both rehashed from the tar before extraction; 0 non-regular/unsafe/extra; end pass `re-verified` for both.
- Continuity: 215 `beforeimages-r12/OWNER.md` = my r11; 222 `beforeimages-r6/*.md` = my r5; **222's three models are byte-equal to r5** (inherited, not re-run, as stated). All changed sentences read (215 C.2 and C.4; 222 RoleRecord paragraph, reset-slot sentence, S-2 idempotence sentence).
- Re-runs: main model = `ordinary-batch-model-r8.json` (6272; 4096/1024; 80; 1 protected sequence; 26258 states, 1075413 edges, 12987 closed); reset model = `standing-reset-model-r3.json` (42 exact, **4** refusals). Baselines equal their models. **Report-named cases only** (guarded runner): coordination corpus r6 **46 named / 44 distinct, 46 rejected, 46/46 exact labels**; reset mutants r2 **6/6 rejected, 6/6 exact labels**; both baselines pass; all source hashes match the reports. No generator or historical script executed.

## 2. Closure
| Finding | r12 / r6 | Status |
|---|---|---|
| **T-1** REVOKED discharged by interruption | 215 C.2: for a `RECOVERY` member whose exact bound BEGIN source was `REVOKED`, v14's below-threshold guard is FALSE ("REVOKED also holds"): accepted stay in `RECOVERY`, batch stays live; COMMIT still needs prospective quorum; ABORT includes the admitted active revocation as first still-true cause ⇒ `REVOKED`; a newly applicable OLD hit still takes the named REVOKE exit; "only a fully authorized recovery COMMIT discharges the pre-BEGIN revocation"; unavailable evidence never becomes a false input. 222 mirrors it and says it "must be enforced by current-context producers, not inferred from a RECOVERY token alone". Model: `BatchWorld.begin_sources` recorded by `begin`, cleared by COMMIT/termination/ABORT; `Role.recovery_revoked`; rule inside `ordinary()` and inside `abort()`; scripted `check_revoked_ceremony` asserts all five exits; a `REVOKED` seed in the mixed profile; restart from ABORT-result `REVOKED` worlds is protected because `begin` records sources from the current states | **closed.** Every exit from `RECOVERY` now preserves the restriction: COMMIT (authorized), ABORT, private termination (r11), observation (r12), REVOKE |
| **U-1** reset needs active evidence as well as BEGIN source | reset model gains the missing-evidence refusal (4 refusals); variant rejected by label | **closed** |
| **U-2** REVOKED takes no reset vs evidenced reset from U | stated as intentional in 215 C.4 and in 222 | **closed** |
| **U-3** idempotence scope | 222: applies mainly to the same prepared operation; "retries cannot rely on idempotence to conserve capacity" | **closed** |

## 3. Independent variants (T-1 scope)
Six of my own (`claude-out/probes/model_mutants_r12.py`, `io/model-mutants-r12.json`): 5 rejected, 1 survives.
- `x3` begin does not record sources, `x6` abort ignores the BEGIN source → rejected by **`protected ABORT restores revocation`** (semantic).
- `x1` exploration passes an *unprotected* role for a revoked-source member, `x2` harness still generates the QUORUM-LOST interruption for it, `x4` termination keeps stale sources → rejected, but **only by `retained exploration coverage`** (the pinned counts). See V-1.
- `x5` the protected flag survives leaving `RECOVERY` → survives; it is an **equivalent** variant (the flag is read only when state is `RECOVERY`), not a gap.

## 4. Observations (Low; no blocking finding)
- **V-1 — the exploration has no path invariant for the restriction.** `x1` re-opens exactly the T-1 path inside the exploration (a same-head import that forgets the producer input), and what kills it is a changed state count, not a statement of the rule. Counts catch *any* drift, which is their job, but they do not say what went wrong and would be "fixed" by re-pinning. **[P]:** in the transition loop assert, for every member with `begin_sources[i]=='REVOKED'`, that the next state is in {`RECOVERY`,`REVOKED`} unless the action was an accepted COMMIT — label it (e.g. `pre-BEGIN revocation discharged only by COMMIT`) and point `x1`/`x2` at it in the corpus.
- **V-2 — `recovery_revoked` defaults to `False`.** The comment says "Missing evidence is not represented as False; producer must refuse first", yet a caller that simply omits the argument gets the unprotected behaviour silently — the very failure r12's prose forbids ("unavailable evidence never becomes a false revoked-also-holds input"). The reset model already refuses on missing evidence. **[P]:** make it `bool|None = None` and have `ordinary()` raise for a `RECOVERY` role with `None`; the 6272 cells pass an explicit `False`.
- **V-3 — one assertion label no longer describes its condition.** The post-ABORT assertion now expects `REVOKED` for revoked-source members but keeps the label "…`stopped.states[i] == 'UNBOOTSTRAPPED'`…". With per-case expected labels in the corpus, a stale label is a small but real hazard for the next reader; rename it.
- The six established-role profiles still seed only `EXPIRED`/`TRUSTED`; revoked-source members enter them through ABORT-result restarts and, directly, only through the two-role mixed profile. That is stated in the README/limits and is adequate for this scope.

## 5. Limits
Prose plus conditional models with admitted boolean inputs; I executed the 215 main and reset models, their 52 report-named cases and six variants, all inside my review directory; the 222 models are unchanged from r5 and were not re-run. No crypto, S4, format or native behaviour is modelled or reviewed. Nothing here approves 215 or 222.

## 6. Result
**T-1 and U-1..U-3 are closed. No new finding; three Low observations (V-1..V-3) on how the model states and guards the new rule.**
