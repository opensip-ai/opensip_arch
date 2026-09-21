# Independent review — native current-event local trace 325

**Standing:** bounded native-Rust review of frozen `native-event-trace-checkpoint-325`. Private unselected `bind_trace` for **current D0 with unknown predecessor**: listed-event shells, per-role local adjacency, no invented before, no 215 effect grant, no current/census/child 235. Installed product remains `fa72e50`. 324 REVIEW+ADDENDUM were read and are **unchanged**. 323 is parent product only.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Review-local copies. Frozen fixture/mutant directories were not overwritten. r1 97-case and r2 compile/rename logs are historical; **final is r3**.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **9568856 B, 1252 members, SHA256 `9f099e13a83715fd7a6cafa4650abc2e451491602be6941d644be021b911642d`**, `allMembersRehashed: true`, **473** product pins. Extract rehashed **1252/1252**. Parent 323 live tar SHA `5ba84833…421f` (13517936 / 2037 / 471). Source 324 archive **639 members** SHA `b7c3a83e…270d` live-equal; subject `source324/` file count **639**. Packet `review324/REVIEW.md` / `ADDENDUM.md` byte-identical to live (`9990fb78…b0c0` / `08685351…7694`).

Product vs 323: **470** unchanged, **1** changed (`trust.rs` **only** `include!("trust/current_event_trace.rs")`), **2** added (`current_event_trace.rs` SHA256 `cd4da31a…28fa` 18837 B; `event-trace325.ndjson` SHA256 `36f2d598…818b` 1000416 B). `lib.rs` has **no** public export. Unchanged 235/265 `bind_events` remains the known-before owner (this module does not call it).

---

## Scope vs 324 addendum

| 324 addendum | 325 |
|---|---|
| Not `bind_events`; no six-role synthetic before | `current` starts empty; `invent-projected-before` first-fails |
| Skip owned `ordered-role-before`; keep `literal-role-event` | First change: literals only; later: `current.get(role)` vs before |
| Do not load first `previous` target | `unknown-external-previous` **1** events read (listed only) |
| `previous is null` iff initial; rev>1 null refuses | `initial-event-origin`: `(prev is None)==(revision==1)` on first listed event |
| Touched last after == projection.roles[role]; not all-roles tautology | `touched-role-projection`; empty current map, not seeded from projection |
| BeginBatch / abort-same-descriptor / reset-exact-effect | Kept; mutants false-accept if dropped |
| Distinct standing; no `pendingAuthenticatedRoleEffects` | `partial-local-trace-only`, `claimedRoleChanges`, `touchedRoles` |
| Forbidden on child/restore/continuity 235 | Not wired there; 235 unchanged |
| Operation / optional outcome separate | Not loaded; `separate-outcome-owner-*` can pass **this** helper only |
| Empty D: no 279 invented before | Empty list skips origin/279; `eventHead` store-only |

---

## Initial-origin challenge (222 + continuity forward)

The guard is **`(first previous is null) == (descriptor.revision == 1)`**, plus `event-chain` (`null ⇒ sequence==1`, else `sequence == previous.sequence+1`) and `previous-event-store` (same `storeInstanceId`). It does **not** load that first previous EventRef.

**Correct reading vs 222.** Revision 1 with `previousCapsule`/`nativeBefore` null is 222’s initial store: ordinary **creation** and **continuity forward** (new-store first capsule, `TargetAbsence` path). Both have first event `previous is null` and sequence 1. Continuity **ancestor** is revision `target+1` with a real previous EventRef (target-before `eventHead`), not loaded here. Using **`revision==1`** therefore covers forward-initial **without** requiring `action==creation`.

**Rejected misreadings.**

1. **Creation-action only** would refuse a lawful continuity-forward rev-1 first event (`kind: continuity`, `previous: null`). The code does not do that.
2. **`sequence==1` without revision** would **accept** synthetic later-revision seq-1/null rows that 274 `bind_events(before_head=None)` accepted. 325 **refuses** those (`inherited-original-0`, `first-null-previous-sequence-one`, `inherited-null-kind-continuity`) with `initial-event-origin`. That is the intended split, not a rubber stamp of 274.
3. **Rev-1 with an external previous** is refused (`initial-revision-cannot-have-external-previous`). That matches 222 initial-store first event, not a carried prior-store head on revision 1.

`ignore-initial-event-origin` false-accepts `inherited-original-0`. Positives `first-null-initial-revision` / `initial-creation-local-trace` (rev 1, null previous) and `continuity-local-trace-with-prior-event` / `unknown-external-previous` (rev 2, EventRef previous, **not loaded**) exercise both sides.

This helper still does **not** check `revision==1` iff `previousCapsule is null`; that pairing remains the 227/current-capsule join owner.

---

## Primary oracle and live cargo

Independent replay of frozen ndjson through extract-local `event_trace_reference325.py` with `budget.guard` (same as the generator): **101/101**, **0** mismatches, **42** first / **39** second positives. `old-evaluation-absent` and `old-evaluation-malformed-present` both accept with **1** listed-event read (non-vacuous for this helper; 324’s 19 restore probes remain **not** claimed T-bearing). `load-old-evaluation` wrongly refuses `old-evaluation-absent` (`Budget(Capture)`).

**Executed** review-local product, `cargo clean -p opensip-security` then:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-security` | **258 passed / 0 failed / 2 ignored**; `Compiling opensip-security` |
| Workspace Clippy `--all-targets -D warnings` | exit 0 (Clippy-r2 equivalent) |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **16** includes | exit 0 |

Corrections preserved: r2 `conditionEvidence` literal restore (no verdict change); mutation-r2 rustfmt match-text only; clock/continuity positives given real prior locators so origin cannot vacate T-invariance. No predicate relaxation.

**Thirteen compiled controls plus baseline** replayed into `grok-out/io/mutation-check-live-r3` (frozen r3 not overwritten). Live `report.json` SHA256 **`60acc21b…9419`**, **byte-identical** to frozen r3. All **14** compiled; no compile-fail kills.

---

## Findings

This is a valid **current-D0 local trace** as specified in 324’s addendum, including the initial-origin reading as **store revision 1**, not creation-only and not seq-1-only. It is **not** CurrentRecoveryImage, 279 empty-event proof, 235 known-before replay, operation/outcome admission, or child census. `claimedRoleChanges` are local claims. Full ordinary/continuity/restore still use unchanged 235 with an owned before.

**Actionable defects in this freeze:** none that make `bind_trace` self-contradictory with the disclosed 235 patch, 324 addendum constraints, or 222 initial-store/forward vs ancestor previous law on the 101 cases.

---

## Remaining (do not count closed)

Creation marker / same-store operation shell / optional outcome **composition**; child census T-invariance and full 235; 326 T-bearing restore fixtures; physical fence/custody; 321 constructors; TCB/history/full T/writers; M2–M6.

---

## Verdicts

- [x] **325 as frozen current-D0 local trace:** archive verified; 324 addendum constraints implemented; initial-origin is revision-1 (creation **and** continuity-forward), rejecting synthetic later-rev seq1/null; 101/101 reference; live 258/2 ignored; Clippy/fmt16; 13 compiled controls + baseline frozen-equal.
- [ ] **Not** current standing, 235, 279, child census, 326 restore-T work, or product installation.
