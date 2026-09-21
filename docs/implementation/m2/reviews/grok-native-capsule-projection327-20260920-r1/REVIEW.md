# Independent review — native local capsule projection 327

**Standing:** bounded native-Rust review of frozen `native-capsule-projection-checkpoint-327`. Private unselected `capsule_projection` / `LocalCapsuleProjection` for **already-materialized C+D only**: common 279 C/D shape, raw descriptor pin, predecessor locator, store/revision, afterProjection, phase/heads/history/counters, roles/ceremony, retained accepted times, mandatory eventHead, nonempty final event. **No** before image, effects, capture, custody, or current authority. Full `capsule_consistency` keeps prior C/D/optional-before **shape order** and **all** empty-event before-dependent guards, and still returns `CapsuleBound` with the actual before. This checkpoint also replays the exact frozen **326** 24-fixture corpus against **unchanged** native `restore_proof`. Installed product remains `fa72e50`. 324 REVIEW+ADDENDUM, 325 REVIEW, and 326 REVIEW were read and are **unchanged**.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Review-local copies. Frozen fixture/mutant directories were not overwritten. r1 `drop-local-failure-latch` compile-fail is historical harness noise, **not** a kill; **final compiled set is combined r1+r2**.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Independent rehash of the live trial tar and of all **1182** extract members matched the pin.

Frozen archive: **9623572 B, 1182 members, SHA256 `cc6aa4731c7942845e4e2a28430bc072083ed77e4a07980b81eb7ce061ac51a8`**, `allMembersRehashed: true`, **475** product pins. Parent 325 live tar SHA `9f099e13…642d` (9568856 / 1252 / 473). Source 326 pin `c64ccac1…741e` (2864748 / 650) live-equal; packet copies of the 24 fixtures/report/generator/README match after the 650-member rehash. Source 324 archive **639 members** SHA `b7c3a83e…270d` live-equal; extract `source324/` file count **639**. Packet `review324/REVIEW.md` / `ADDENDUM.md` byte-identical to live (`9990fb78…b0c0` / `08685351…7694`). 325 REVIEW `e9ff6ae4…aabe` and 326 REVIEW `e8e746c0…f178` unchanged.

Product vs 325: **472** unchanged, **1** changed (`trust.rs` SHA256 `ae19f71c…6789`, 613526 B; 325 was `b87415c4…4981`, 605697 B), **2** added (`capsule-projection327.ndjson` SHA256 `26442226…eea8`; `retained-scope326.ndjson` SHA256 `9bce0ef2…ff4b9`, byte-identical to source326 `fixtures.ndjson`). `current_event_trace.rs` and `lib.rs` are **unchanged**. `lib.rs` has **no** public export of `LocalCapsuleProjection` / `capsule_projection`. `original-capsule-consistency.rs` is **byte-identical** to the 325 `capsule_consistency` body (8338 B). Native `restore_proof` body is **byte-identical** to 325 and contains **no** `timeEvidence` load.

---

## Local projection vs full known-before owner

`check_capsule_projection` holds the common C/D predicates. `capsule_projection` wraps it in `budget.scope`, returns `LocalCapsuleProjection { capsule, descriptor }` clones, charges **(0, 0, 0)**, and latches failures. It has **no** before field, no store callback, and no effect/capture/custody/current standing.

Full `capsule_consistency` still:

1. shapes C, D, then optional before (same input-shape order as 325);
2. re-runs the common helper (validation, not a second physical capture);
3. if `events` is empty, runs **all six** empty-event before guards:

| Guard | Literal |
|---|---|
| missing before | `empty-event publication needs exact before image` |
| store + next revision + predecessor hash | `empty-event predecessor binding` |
| eventHead unchanged | `empty-event publication preserves event head` |
| roles / staged / batch / sourceFence | `empty-event publication has no hidden role or ceremony effect` |
| both phases retained | `empty-event head update stays retained` |
| T locator + F/L/anchor/serial/challenge | `empty-event publication cannot hide a clock write` |

4. returns `CapsuleBound` with `before: before.cloned()`.

The sole production caller remains `capsule_clock` → `capsule_consistency`. No full consumer was redirected to the partial type. Empty D on the **local** helper does not require before; empty D on the **full** owner still does (`original-30`, events `[]`, `before is None`, retained phase).

Python `admit_local_projection` is an explicit prefix of unchanged 227: `reference-projection.patch` deletes only the empty-event `else` branch. Regenerating `capsule-projection327.ndjson` from `capsule279.ndjson` through that helper is **SHA-equal** to the frozen file.

**649 / 155** local vs **unchanged native full 649 / 116**. The **39** changed verdicts are the scope exclusions, not silent weakenings of the full owner:

- **24** `shape-before`: native full shapes Optional before even when events are nonempty; local has no before parameter. Original 227 Python also does not shape an unused before (independent replay **140** Python-full positives = 116 + these 24). That 227/279 split predates 327.
- **15** empty-event family: `original-30`…`original-42` (13) plus `empty-hidden-batch` / `empty-hidden-staged`. Local accepts; full still refuses with the six literals above.

This is **not** CurrentRecoveryImage and **not** permission to implement a child 235/279 check from `LocalCapsuleProjection` alone.

---

## Native 326 restore replay (T not loaded)

Exact 24 frozen 326 fixtures against **unedited** `restore_proof`. Native counts **(24, 6)**. Independent classification:

| Class | N | Labels |
|---|---|---|
| T-absence / malformed-present positives | 6 | `{empty,clock,longer}-retained-chain-{absent,malformed-present}` |
| missing required non-time | 15 | observed / proven / first-child / direct-terminal / operation × 3 graphs; `operation-capture-cap` |
| non-DIRECT terminal | 3 | `*-non-direct-terminal`; `witness-is-recovery-operation` |

Probe-report targets are nonempty (`55…55`; clock/longer also `aa…aa`). **0** of those hashes appear in expected physical reads. Probe-report SHA `1014f844…70ea` matches frozen 326. The **3** extra 326 before-mismatch source probes (`empty-retained-chain-wrong-before` → 279 `empty-event predecessor binding`; two `*-wrong-before-head` → 235 `event-chain`) are **not** in the native 24.

`force-old-time-target-into-restore` injects `Budget.load` of retained `timeEvidence` after the observed image is in hand. First failure: `empty-retained-chain-absent` → `Budget(Capture)` — the declared T locator is **not** in the store, so a real load would have to capture it. Baseline accepts that case with 0 T reads. Native restore therefore does **not** follow old T. No nested-T coverage is claimed.

---

## Primary oracle and live cargo

Independent replay of frozen local ndjson through extract-local `capsule_projection_reference327.py`: **649/649**, **0** mismatches, **155** positives. Full native 279 fixture `valid` flag remains **116**.

**Executed** review-local product, `cargo clean -p opensip-security` then:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-security` | **260 passed / 0 failed / 2 ignored**; `Compiling opensip-security`; 12.58s |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **16** includes | exit 0 |

---

## Mutants

Eight compiled controls plus baseline replayed into `grok-out/io/mutation-check-live` (frozen `mutation-check-r1` / `mutation-latch-correction-r2` not overwritten). Frozen r1 `drop-local-failure-latch` **compile-failed** (`expected function, found Result<LocalCapsuleProjection, _>` from an overbroad `})` replace that also invoked the inner `Ok`). That is **not** a kill (SHA256 `dcf0e965…0a2a`). Isolated r2 restricts the replace to the last closure terminator of `capsule_projection` only; it **compiled** and panics `original-1 latch` (SHA256 `fc5adcb7…2a37`). Product was **not** edited. Live compiled-control source SHA/exit match frozen `mutation-combined-report.json`.

| Control | First failure |
|---|---|
| `discard-descriptor-byte-pin` | false-accept `original-2` |
| `discard-common-role-ceremony` | false-accept `original-23` |
| `discard-common-retained-history` | false-accept `original-11` |
| `discard-common-final-event` | false-accept `final-event` |
| `skip-full-empty-before-guards` | false-accept `original-30` (`empty-event publication needs exact before image`) |
| `drop-full-empty-clock-equality` | false-accept `original-42` (`empty-event publication cannot hide a clock write`) |
| `drop-local-failure-latch` r2 | panic `original-1 latch` |
| `force-old-time-target-into-restore` | wrong-refusal `empty-retained-chain-absent` `Budget(Capture)` |
| baseline | 260 passed / 2 ignored |

`skip-full-empty-before-guards` and `drop-full-empty-clock-equality` are the evidence that the full owner still requires exact before and T-locator equality. They would be silent if 327 had moved empty-event law onto the partial type.

---

## Findings

The factoring is faithful to the disclosed 325 body plus a **distinct** partial type: local owns C/D after Budget drop; full still owns empty-event predecessor law and still feeds `capsule_clock`. Partial must not be read as a known-before `CapsuleBound`. Old T is declared on the 326 graphs and is **not** loaded by native restore.

**Actionable defects in this freeze:** none that make `capsule_projection` self-contradictory with preserved full 279 empty-event guards, unchanged `restore_proof`, or the enumerated 39 local/full verdict splits on the 649+24 cases.

Not claimed: CurrentRecoveryImage, child census from local projection, original-T admission, nested-T restore, 325 trace composition, or product installation.

---

## Remaining (do not count closed)

P2 calendar; descriptor operation; current 325 local trace; optional outcomes; live qualified current/census/custody/fence/capacity; TCB/history/original T; writers; M2–M6.

---

## Verdicts

- [x] **327 as frozen local C/D projection plus 326 native restore replay:** archive verified; 324/325/326 reports preserved; full empty-event before guards intact; local type has no before; 649/155 local reference SHA-equal; native full 649/116; 24/6 restore with 0 T reads; live 260/2 ignored; Clippy/fmt16; 8 compiled controls + baseline (r1 latch compile-fail not counted).
- [ ] **Not** current standing, known-before 279/235 child owner, original-T validity, nested-T restore, or product installation.
