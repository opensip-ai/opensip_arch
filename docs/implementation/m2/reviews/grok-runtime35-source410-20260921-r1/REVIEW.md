# Native runtime35 + endpoint-lineage-410 — source and formal review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Independent Grok source+formal review. Not Claude agreement. Native/Node jobs were **not** rerun; ROOT owns that lane. Prior Claude Opus5 replays are **evidence of those runs**, not this reviewer’s replay and not prior approval (those sessions ended 529/500 without a verdict). Live product was **not** written (`e60ce01`, 35 inventory / 56 contract). Root assent is **not** manufactured.

**subjectManifestSha256** `172da5fa5333f8d36cd905b0695ffff6bbc731bf3ec374b1465fb6c3e6d7f9d8`  
`docs/implementation/m2/native-runtime-selection-v35-subject.json` **2472** B, **12** members, sorted unique, **0** pin mismatches. `passageOverrides`: []. Candidates (11) cover the subject minus the successor. Parents are not members. Candidate-path reuse on the live lock: **0**.

---

## Formal parents (live lock 35 / 56)

| Parent | Bytes | SHA-256 | Class |
| --- | ---: | --- | --- |
| initial-owner406 successor | 43921 | `3a713c5c39a3feca2db3a05924103d49c10f11bef3c32f93d8c286fecd813e54` | selected contract |
| runtime34 successor | 3076 | `373a5d9fc12695115ae175ffdfc83246dc38f36c8b616595c45984a1e1ce7745` | selected contract |
| inventory59 | 280949 | `c2400990cf4f9ec0c6c4e4331e2194313dea272f17ad04c83866a23c9c1cb815` | selected inventory |

Parent order is lexicographic (`initial-root-…` before `native-runtime-…` before `repository-file-inventory.v59.json`). All three match accepted lock pins.

Inventory59 **stored** row 104 (`crates/host/src/installation_lineage.rs`) still describes per-node store markers. Selected 406 successor already overrides `/files/104/description` to endpoint-only retained ancestry. This unit adds **no** passage override; it implements that effective description.

`stage.py` **5719** B `3a71d80a…b1c4` is byte-identical to selected34/29. Map: **1** write + **590** unchanged non-lock; archive `design-lock.json` excluded. Independent private stage: **610** archive members verified; non-lock source **591**; mapped 1; unchanged non-lock 590; staged lock equals live; live product unchanged; `runtimeAcceptance: false`.

---

## Source410 (one file)

Archive `6e67855c…e370` / **6898704 B / 610 members** (592 product); subject.json **114763** B `16c32949…9774`; **0** member digest mismatches. Live `installation_lineage.rs` **6104** B `e0581cd4…438c` equals map **before**. Frozen 410 file **11756** B `882006f7…60a2` equals map **after** and the staged write. `installation_records.rs`, `installation_selection.rs`, `installation_trust.rs`, and lifecycle `lineage.rs` are byte-equal live. Baseline reconciliation: vs original 407 test head, only `design-lock.json` and `tools/typescript-lanes.json` changed; `nativeSourceChangedSince407Tests: false`. Claude 407-provenance notes rustfmt reflow between carried 407 draft and frozen 410 tokens; that does not change the endpoint law. Fresh Claude replay (below) was on frozen 410 bytes.

**Behavior vs live (per-hop markers) and owner406 §7:**

Production `read_existing` still opens `ProvisionalInstallationRecords` under the original `InstallationReadFence` (selected pair **and** selected-endpoint marker). Start key is parsed from the pair. The walker is still `inspect_supplied_lineage` (identity `store_lineage.rs` 186–219): full triple equality, missing node, misbound, cycle, `max_nodes` limit, nonnegative G as a key field (not monotonic; test uses G=3 then G=9), K 1|2. **Removed:** `ProvisionalStoreMarker::read_existing` on every hop and the `markers: Vec<…>` field. Intermediate ancestry is node files only (`transitions/lineage/S/G/K.node`). Missing immutable nodes remain `Err` (`Ok(None)` still becomes `WalkError::Missing` in the walker; the new tests return Read errors). Reclaimed intermediate **stores** are no longer probed.

Private `read_retained_chain` sequences `recheck` **before** each observe, **after** observe (including failed reads), and **again** after walker Limit/Cycle/Misbound/Read, **before** reporting the walker error. Test `earlier_owner_change_overrides_later_failed_observation`: later node fail + original change → `RetainedChainError::Read`, not Chain. Test `final_recheck_cannot_be_skipped_by_cycle_or_limit_refusal` forces the post-walker recheck. Production `check_all` rechecks records (pair+endpoint marker) around node-capture rechecks; it no longer iterates per-hop markers. `ReadError::Marker` remains on the public enum for source compatibility; endpoint marker failures surface as `Records`. `failed` still latches `recheck`/`selection` errors to `Closed`. No public handle injection; the generic observe/recheck seam is private/`cfg(test)` and does not mint native capabilities.

`ProvisionalInstallationRecords::read_existing` is unchanged: it still captures the pair then the marker for that pair’s S under the same fence, and `records.recheck()` re-visits both (failed second owner still rechecks the first). Lineage no longer duplicates that marker capture per hop. `inspect_supplied_lineage` still refuses `Ok(None)` as `Missing`, self-cycles, and `nodes.len() >= max_nodes`. Pair fields only **locate** the start key; G/K are admitted by the node at that key.

Error precedence: a failed later node read still runs `recheck` on already-held records/captures; if that recheck fails, `RetainedChainError::Read` wins over `Chain`. After Limit/Cycle the same final recheck runs before the walker error is returned. `read_existing` does not construct `Self` unless the chain and a trailing `recheck` succeed; `failed` latches later `recheck`/`selection` errors to `Closed`. Dropping a failed observe’s local `ProvisionalHeldFile` without pushing it is correct: unsuccessful captures are not retained successes.

This matches 406 §7: S from the **physically opened selected endpoint** marker; intermediate ancestry by admitted node keys; missing intermediate node unavailable; reclaimed intermediate store with a retained node is not an error. A node is still not a rollback handle. It does **not** add shared operation budget, registry/core/current authority, creator/P0, or GC execution (owner §9 still lists those as outstanding). Sequential rechecks are not atomic snapshots and do not detect arbitrary ABA.

---

## Prior Claude replay (not this reviewer’s)

`/tmp/opensip-implementation/reviews/claude-opus5-runtime35-source410-20260921-r1/evidence/replay-checks.json` **1871** B `1d06850f…2dfc`, rustc 1.95.0, 368 vendor, own target, Darwin TMPDIR, `RUST_TEST_THREADS=1`, offline. Checks exit 0: `installation_lineage::` **4** passed; `installation_records::` **2** passed; workspace `--all-targets`. Root archived the same bytes as partial-evidence (not a review). This Grok review **did not** rebuild or re-run those tests.

---

Conditional tests compose the private seam with in-memory nodes; they are not native endpoint-custody fixtures and do not replace the Claude host-package replay. `ReadError::Marker` is unused on the production path by design (compat). No new public API, crate edge, or inventory row is added.

---

## requiredFindings

None.

---

## Scope

ACCEPT-DESIGN-UNIT for this one-file endpoint walk plus formal composition onto runtime34 / owner406 / inventory59. Not M2–M6, not creator, not S9.3 writers, not current authority, not shared-budget implementation. Integration still needs root assent and private/live checks.
