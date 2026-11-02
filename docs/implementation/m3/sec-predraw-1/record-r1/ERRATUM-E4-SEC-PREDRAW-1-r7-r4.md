# ERRATUM E-4 r4 to SEC-PREDRAW-1 r7 (§1.8, §4.3, §5.2): three control forms

**Author:** claude-sec-predraw-1 (w35:p1), Claude Opus 5.5 / high, R3-FRONTIER, long-horizon lead.

**Authority:** LD-Q-244 (`coordinator/msg-ldq244.txt`, `923d8dfe…`), option A for item 1, and LD-Q-247 (`coordinator/msg-ldq247.txt`, `be384246…`), on REVIEW-E4's alternative, and LD-Q-247-B (`coordinator/msg-ldq247b.txt`, `b2a3c2f5…`) and LD-Q-250 (`coordinator/msg-ldq250.txt`, `327516a8…`), on REVIEW-E4r2's. **Scope: text only, on three controls, scored per item.** It extends §4.3's fixture list by one item. No constant, order, row or bound changes, and `forbid(unsafe_code)` is untouched.

E-4 is a standalone erratum to the adopted record `SUCCESSOR-SEC-PREDRAW-1-r7.md` (`f8bbd0fb…`), read with E-1, E-2 and E-3. **Their bytes are not edited.** If adopted, E-4 controls on the three items below.

**Pins:** product `b7c2070f6ad5c08b742e30b2a21f19a77d1f3bda` (TESTFIX-1); the SP branch at `a5b27d8490aa20df1045d1d4946bf5be0b5257c8`; architecture `5f328f32`. **The evidence runs predate that rebase:** 34 of 34 commits are identical patches (`sp7h-v1/range-diff.txt`), and main's change is one line in `crates/host/tests/commit_matrix_tests.rs`.

## Item 1. The counting allocator (r7:529-530, :1066, :1135-1136; RF-1's completion gate)

**The defect.** r7 requires counting-allocator observations of P-1, but it names no place they can run. `opensip-security` has `#![forbid(unsafe_code)]` in `lib.rs` and `unsafe_code = "forbid"` in its manifest. A global allocator needs `unsafe`, so it cannot live in that crate or any of its test targets. From outside, only §4.3's fixture is reachable, and it counts a whole acquisition, not P-1, up to five components.

**The form.**
- **The probe:** `crates/security/tests/p1_alloc_probe/`, a package with its own `[workspace]`, never published, holding the global allocator in a test binary.
- **Its lock:** `Cargo.lock`, seeded from the workspace's. Mechanically checked: 51 packages, and only the probe itself is absent from the root lock by name, version, checksum and source (`sp7g-controls-v1/lock-seed.txt`).
- **Who runs it:** not the lane. It is run for evidence, like `fixture_release_probe`. The freeze must record a run at the frozen head.
- **The one new fixture item, added to r7:877's list:**
  ```rust
  pub fn project_counted(components: usize, revoke_last: bool, around: impl FnOnce(&mut dyn FnMut()))
      -> (Result<usize, &'static str>, (usize, usize, usize));
  ```

**What the item does and exposes (LD-Q-244's conditions):**
- **Real P-1:** it runs `project` over the inventory a real retaining report read returned, on a real signed catalog of `components`, through signing, receipt and acceptance.
- **No custody value, in or out.** It takes numbers and a callback whose only argument is `&mut dyn FnMut()`. It returns the held count or a refusal's name, and the ledger's three numbers. The hold is dropped inside it. No hold, view, inventory, session, evidence constructor or receipt crosses it.
- **Nothing to skip P-1 with:** it yields no `DurablePreDraw`, `ReadPreDraw`, `PreDrawEvidence` or view.
- **It adds no new public type name.**

**The results** (`sp7f-controls-v2`, real signed chains, P-1's one call counted on its own thread):

| Path | Heap allocations | Charged objects | r7's bound |
|---|---|---|---|
| success, n = 1 | 5 | 5 | at most 10 |
| success, n = 2, 5, 20 | 7 | 7 | at most 10 (C-NC-20 at n = 20) |
| revocation refusal, n = 2 | 3 | 3 | at most 5 |
| cap refusal, n = 21 | 0 | 0 | 0 (C-NC-21) |

Allocations **equal** charged objects on each path measured, which is stronger than r7's upper bounds, and this is RF-1's completion gate. It is an accounting observation: it does not establish each allocation's purpose or the order of its funding, nor absence of I/O (REVIEW-E4). Mutations, each killed by a test failure: the RF-1 namespace copy, the mark before the cap, the mark's charge removed, and an unfunded allocation.

**Parity (A-RF-4 at X8/X9 parity, r7:898 onward). Please score whether it still holds.** My claim is that it does, because the new item sits inside the same module:

| Fence | How it covers `project_counted` | Evidence |
|---|---|---|
| 1. The module `cfg` | the item is inside `pre_draw_fixture`, under the same joint predicate | source |
| 2. The release guard | unchanged; the isolated release probe still fails with the guard's exact text, in security only | `exclusion.json` |
| 3. Plain-host unnameability | the module's witness, E0432 in dev, `--release`, `--profile harness`, and a **new case** naming this item (`security_pre_draw_fixture_project_counted_unnameable.rs`) | `exclusion.json`, `host.log` |
| 4. The manifest pin | unchanged: the item adds no feature or dependency to any root manifest | `admission_tests` |
| 5. The effective-graph check | passes | `exclusion.json` |

**Where the larger surface differs, stated plainly:**
- `pre_draw_fixture` previously offered site creation and two acquisitions. This adds a third kind of entry, a callback run during the fixture. It carries no custody value.
- The probe crate enables `scenario-fixtures` in its own workspace. **The checker's root inventory does not see it**, because it comes from `cargo metadata` on the root. That is true of `fixture_release_probe` too, and it falls in CP-TEST-FEATURE-EXCLUSION-1's `--manifest-path` class (r7:933, "carried, not claimed").

**Where this is weaker than r7's text.** r7:529-530 says C-NC-21's counting allocator runs "on both the durable path and the read `Some` path". This runs `project` on its own ledger, in neither wrapper. So the allocator half is P-1's allocations alone, and not those of `gate_step` or `charged_step`, whose rechecks charge objects of their own. The wrappers' zero-charge half is E-3's ledger observation, on both paths. **So the claim is exact for P-1, and no allocator count is claimed for either wrapper.**

## Item 2. C-A1d (r7:490-492)

r7 says TR-COMPONENT below threshold, and an authority namespace other than the publisher, each "refuses `Authority` with `PayloadNotAdmissible("inventory")`".

**What the real chain does** (committed controls, `sp7g-controls-v1`):

| Case | Where it refuses | Row |
|---|---|---|
| TR-COMPONENT `Unbootstrapped`, `Expired`, `StaleRevocation`, `QuorumLost`, `Revoked` (fenced and report) | **the read**, before P-1 | `ComponentContinuation("component:<state>")` |
| publisher other than the signing namespace | **the read** (`Scope(Inventory(Namespace))`), before P-1 | `PayloadNotAdmissible("inventory")`, r7's row |
| a component's own envelope below quorum, the role whole (`ScopeError::ComponentQuorum`; `sp7i-controls-v1`) | **the read** | `PayloadNotAdmissible("component")` |
| **a component's own envelope below quorum, with the role's other keys revoked (the witness; `sp7i-controls-v1`)** | **P-1**, the read having admitted it | **`Authority`, `PayloadNotAdmissible("inventory")`: r7's row** |

So the publisher clause's row matches r7's, from an earlier owner, and **the below-threshold clause holds exactly as r7 words it, on the witness's path.** The other below-threshold states refuse earlier on other rows.

**Is P-1's own refusal reachable? As LD-Q-244, LD-Q-247-B and LD-Q-250 ask, plainly:**

**P-1's authority check is a LIVE security guard.** On real signed documents, through the real read and real P-1, in fenced and report reads alike (`sp7_c_a1d_a_below_quorum_manifest_passes_the_read_and_p1_refuses_it`):

| TR-COMPONENT's manifest | Revocation list | Read | P-1 |
|---|---|---|---|
| signed by 14, 15 (quorum 2) | none | admits: 1 component, 1 authority | holds 1 |
| signed by 14 only | none | **refuses:** `PayloadNotAdmissible("component")` | not entered |
| signed by 14 only | 15 and 16 revoked | **admits: 1 component, 0 authorities** | **refuses: `Authority`, the mark its sole charge** |

The first two rows are controls: the store is sound, and the read enforces quorum while the role is whole.

**The capsule limit, stated plainly.** The witness's store is **hand-built**, by a test-only generator knob (`Spec.constructed_component`), and its capsule's `Trusted` is constructed. **No real store can reach it at these pins:** real acceptance over this payload refuses with `PayloadNotAdmissible("component")` and writes nothing, and no built producer can record `QuorumLost` (`sec-harden-1/ASSESSMENT-r1.md` a.1, executed by that unit; X4B r6 items 2, 4, 9). So this shows what the read does **given** a capsule that says `Trusted`, and not a history a real store can have. **P-1 stays a live guard for that state.** SEC-HARDEN-1 owns the read-side question (SEC-X4T-QUORUM-1), and E-4 does not answer it.

**The case analysis** (R3 confirms the split is exhaustive). `authorities_len() != n` needs `n > 0` and an admitted read with too few authorities. `prepare_scoped` pushes one authority per component when `remaining()[1]` is true, or refuses, so the read must have `remaining()[1]` false. `standing_of` runs over the capsule's bound states and refuses unless TR-COMPONENT is `Trusted`. For a bound `Trusted` role, `plan` leaves `remaining()[1]` false in exactly three cases:

| Case | Status | Basis |
|---|---|---|
| inactive in this root | **blocked:** `closure_components` re-verifies each component; the inactive role is `RoleUnavailable`; the read refuses on `PayloadNotAdmissible("inventory")` | source; REVIEW-E4's trace. Planning and standing are pinned by `sp7_c_a1d_a_trusted_inactive_…` |
| `below_threshold` | **reaches P-1, given such a capsule.** r2's claim that a verified component has met its threshold was **false**: `verify_envelope` rejects only an empty signer set, and `admit_revocation` has no listed key to name | **executed:** the witness above |
| `old_subject_hit` | **input disabled today:** the only non-test `ScopeContext` passes `old_hits: [false; 6]` (`current_trust_admission.rs:744`). If it is wired, this is a second path to the same check | source |

**The other branches:**

| P-1 branch | Status for an inventory a real read creates | Its control |
|---|---|---|
| authority's path or namespace mismatch (step 4) | no admitted-read witness found: authority construction preserves order and path, and the read's `Namespace` check supplies publisher agreement. **Reachability unknown beyond that; not called dead.** | `p1_refuses_…_misnamed`; removing the branch is killed by it |
| `next_part` yields none; `pair` yields none | not found reachable, given step 1's equality, the n-element walk, and the read's own pairs. **As far as shown; not called dead.** | none: they handle `Option`s and fail closed |

**The branch stays,** as LD-Q-247 ruled. It is the guard on the witness's path, and it is in r7's adopted order.

**The named controls:**
- **The witness,** above. With step 1 removed, it fails, because later work is charged; the refusal's row alone would not have shown this, since step 4 refuses on the same row.
- **`sp7_c_a1d_p1s_authority_premise_refuses_before_any_later_work`** pins step 1 over a constructed loss: `Authority` with the mark as the sole charge, and ahead of step R though a release is revoked too.

**What this finds outside this unit.** That revoking more of a role's keys turns a read's refusal into an admission is a finding about trust admission, not about P-1. The coordinator has placed it in SEC-HARDEN-1 (LD-Q-250). **E-4 changes neither `prepare_scoped` nor `old_hits`,** and SEC-PREDRAW-1 does not wait on it.

**The form.** C-A1d is executed as: the table's rows on real signed documents; P-1's `Authority` refusal through the witness, and over a constructed authority loss (`p1_refuses_an_authority_that_is_missing_or_misnamed`, and the named control above); and the planning and standing unit control.

**Stronger:** the real-chain rows, which r7 did not require, and the named controls, which pin step 1 itself. **Weaker, exactly:** the witness's store is hand-built, and no real store can reach it at these pins, so r7's clause is observed through the real read and real P-1, but **not from any real acceptance history**. The inactive and old-hit rows rest on source reading, not an executed signed chain.

## Item 3. C-A1c (r7:488-489)

r7 requires a source census, and that "the fixture store's access counter is unchanged across P-1". No such counter exists, and `project` takes no store handle.

**The form.** The census stands, as the enumerated-body regression check. In place of the counter: **with the whole installation dropped, home, trust store and signed trees, and the home asserted gone, P-1 still holds all five components** (`sp7_c_a1c_…`).

**What it shows, precisely.** A successful projection of this fixture does not need a successful read of any removed installation path. This is an observation of success with those paths gone, not a count of attempts.

**Stronger:** it holds for any read of those paths that P-1's result would depend on, by any route, where a counter sees only what passes through it.

**Weaker, exactly:** ignored read attempts are not observed, including attempts using an existing buffer, or an additional properly charged buffer that stays within the bounds. A counter covering the attempted path would see such an attempt. Item 1's allocator equality is an accounting observation, not an I/O observation, and does not close this. The enumerated lexical census is supplementary, and it does not prove a transitive no-read property. LD-Q-244 allows an explicitly weaker replacement; this is one, in that respect.

## What does not change

Every constant; P-1's order and routes; E-1, E-2 and E-3; `forbid(unsafe_code)`. C-NC-20/21's ledger forms stand as E-3 states them.

## Disclosures

- **Inventory rows:** the probe and the new case are in LD-Q-203's classification (`planned-files-v7`, 0 of 45 rows touch a shared artifact). Their inventory rows are owed through the binding successor (LD-Q-217), marked as fixtures.
- **Removed:** `RetainedInventory`'s `tr_component` field and accessor, which I added at SP-2 and nothing called.
- **Added:** a test-only knob in `trust/accepted_store_fixture.rs`, `Spec.constructed_component` (`planned-files-v8`, 0 of 46). Default stores are unaffected: the unfiltered security lib is 1394/0/7 at `a5b27d8`.
- **Evidence runs** are bounded: part F's full gate ran before the rebase and the later test-only commits. The security lib ran unfiltered at this head. The other head checks run at the next batch.

## Changes from r1 (`2871ceaa…`, REVIEW-E4 `c9b916e4…`)

- **Item 1:** the text is unchanged except for one sentence bounding what equality shows. R3 scored it ADOPTABLE, with A-RF-4 parity HOLDS.
- **E4-RF-1:** r1's claim that a `Trusted`, inactive role reaches P-1, with P-1 as "the only guard", was **false**. Replaced by the complete case analysis and the plain statement LD-Q-247 requires. The named control is new.
- **E4-RF-2:** r1's "rules out any read that allocates a buffer" and "allocates nothing" are withdrawn, for R3's boundary. The two source comments R3 flagged are corrected (`sp7h-v1`).
- **Rebased** onto `b7c2070`; see the pins.

## Changes from r2 (`c309a941…`, REVIEW-E4r2 `f5420dd5…`)

- **E4R2-RF-1:** r2's "dead by construction for real reads TODAY" and "none can today" are **withdrawn** (LD-Q-247-B). Its below-threshold row assumed a verified component had met its threshold, which was false. R3's counterexample is now an executed witness. Item 2 says the guard is live and states the capsule limit.
- **Reachability of the other branches** is stated as far as shown, never as "dead".
- **Items 1 and 3:** unchanged, as already scored ADOPTABLE.

## Changes from r3 (`56964d2e…`)

- **One correction (coordinator `msg-witness-correction.txt`, `af5861b1…`):** r3 said real acceptance over this payload records the role as lost. **That was my inference, and it is wrong:** it refuses and writes nothing, per SEC-HARDEN-1's executed experiment. The capsule limit and the "weaker" clause are restated. Nothing else changes.
- **Two source comments repeat r3's wording,** in `Spec.constructed_component` and the witness control. They are corrected in the next commit on the branch. The pinned head still carries them.
