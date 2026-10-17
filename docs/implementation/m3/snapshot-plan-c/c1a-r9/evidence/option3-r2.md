# M3-C r9 round 2, addendum: option 3 quantified

**Status:** the question as put to the lead. **Decided since:** (a)+(b′), the non-allocating member comparison, with caps 2^21, 2^24 and 2^33 conditional on C1a4. RECORD-r9.md §1.5 and §5 to §7 hold the decision, (b′)'s obligations and the M3-B finding; `option3_r2.py` now models (b′) too. No product file is edited.

**Source:** `option3_r2.py`, with its output in `option3_r2.output.json`.
- Each remedy is modelled as a subclass of `SnapshotModel`, and `term_a_r2.py`'s row bound is re-run under it.
- The 2× rule uses the larger of each subtotal and the round-2 census maxima. Every remedy only removes charges, so those maxima remain upper bounds.
- The script asserts that its baseline equals `term_a_r2.output.json`, and that the unmodified model still reproduces all 35 accepted snapshot walk vectors.

**The remedies:**
- **(a)** A non-anchor `.opensip` name is classified once: the walk loop reuses the anchor question's result.
- **(b)** The admitted members' segment lists are charged once per walk, not on every classification.
- **(c)** The per-`target` Cargo-root prefix copies are not made.

## The numbers

| Combination | Variant | Objects | Edges | Bytes | Caps (objects, edges, bytes) |
| --- | --- | ---: | ---: | ---: | --- |
| none (record §5) | memberBounded | 5,824,927 | 6,218,464 | 21,190,974,348 | 2^24, 2^24, 2^36 |
| | zeroMember | 1,190,003 | 6,218,464 | 5,044,975,155 | 2^22, 2^24, 2^34 |
| (a) | memberBounded | 3,473,784 | 6,218,464 | 11,632,183,052 | 2^23, 2^24, 2^35 |
| | zeroMember | 776,676 | 6,218,464 | 2,538,872,386 | 2^21, 2^24, 2^33 |
| **(a)+(b)** | **memberBounded** | **776,740** | **6,218,464** | **2,539,142,722** | **2^21, 2^24, 2^33** |
| | zeroMember | 776,676 | 6,218,464 | 2,538,872,386 | 2^21, 2^24, 2^33 |
| (a)+(b)+(c) | memberBounded | 776,740 | 6,218,464 | 571,472,261 | 2^21, 2^24, 2^31 |
| | zeroMember | 776,676 | 6,218,464 | 571,201,925 | 2^21, 2^24, 2^31 |

**What the remedies leave:**
- Under (b), the once-per-walk member charge is 64 objects and 270,336 bytes (64 × 256 × 16 + 64 × 128).
- With (a) and (b), the dearest byte row is a plain leaf under 585 `target` segments (603.3 per frame byte). Members no longer matter.
- With (c) as well, the dearest row is `Cargo.toml` at the root for every component.
- Edges are unchanged throughout: classification charges no edges.
- With (b) alone, the bytes would still be at least the zeroMember baseline (5.04 GB, 2^34). So **(a)+(b) is the smallest combination** that brings member-bounded bytes to 2^33 or below.
- At 2^21, 2^24 and 2^33, the census's smallest margins are about 3,960, 11,274 and 39,040 per mille (`poly-large-rspack`; 2^21 / 529,529 objects).

## The code changes for (a)+(b), in C1a4 on top of C1a3 r2

The lines cited are main `e937dac`'s; C1a3 r2 edits `snapshot_walk.rs`, so they will move.

**(a) Reuse the anchor question's classification** (`crates/security/src/snapshot_walk.rs`).
- **`custody_state_anchor`** (:317-330) keeps its charge, `classify_cost(path, members)` at :328. It returns the classification, `Option<PrunedAnchor>`, instead of a bool, and the caller tests for `OpensipCustodyState`.
- **`enter`** (:338 on): the anchor loop (:364-371) records the classification of a `.opensip` path that is not an anchor in a new `Level` field, `opensip: Option<(usize, Option<PrunedAnchor>)>`. A listing holds at most one `.opensip`, so an anchor removal and a recorded index never occur together.
- **The walk loop** (:224-227): at the recorded index, it skips both `classify_cost` and `rule::classify_path` and uses the recorded result.
- **Why the reuse is exact:**
  - The only difference in `known` between the anchor scan and the loop is this directory's own Cargo push (:407-411), which `enter` makes after the scan.
  - `classify_path` tests a Cargo prefix only in front of a `target` segment. Every such prefix of `x/.opensip` is a strict ancestor of `x`.
  - `member_roots` is fixed.

**(b) Member lists once per walk.** The allocation is in the shared rule: `custody_state` (`crates/security/src/custody/discovery_rule.rs`:132-152) collects `base.split('/')` for each member root on every call. So (b) needs a change to the rule.
- **`discovery_rule.rs`:**
  - Add a `MemberPrefixes`, the split lists built once from `member_roots`, and a `classify_path_with(relpath, cargo_roots, &MemberPrefixes)` that `custody_state` uses.
  - `classify_path` keeps its signature: it builds the prefixes and delegates. Its behaviour and every existing caller's charges are unchanged: B2, `discovery_scan.rs`, `workspace_declarations.rs`, `discovery_export.rs` and `host/src/discovery.rs`.
  - This is an M3-B file, pinned whole in the census closure (`discovery_census.py`:76, 18,080 bytes). Editing it needs that owner's reviewed acceptance and a refreshed closure pin.
- **`snapshot_walk.rs`:**
  - `walk_snapshot` (:185-200) builds the prefixes once, after the root's custody and before the root frame (:199). It charges them once with a new `member_lists_cost(members)`: objects = lists; bytes = member segments × 2·`size_of::<usize>()` + lists × `RECORD`.
  - `classify_cost` (:51-66) drops `lists` and `member_segments`.
  - Both classification sites (:224-225 and :328-329) call `classify_path_with`, and `custody_state_anchor` takes the prefixes.
- **An alternative, (b′):** compare each member root to the path's byte prefix in `custody_state`, without allocating. That removes the member charge entirely: 64 objects and 270,336 bytes less than (b), with the same caps. It changes the same rule file.

**The model terms that move** (`tools/security/snapshot_ledger_model.py`):
- `SNAPSHOT_ANCHORS`:
  - the `CLASSIFY` pattern (:81-92) loses the member fold;
  - new anchors pin `member_lists_cost`, its one charge site in `walk_snapshot`, and the loop's reuse of the recorded `.opensip` classification;
  - `ANCHOR_CLASSIFY` (:93-95) stays, matched against `custody_state_anchor`'s new return form.
- `SnapshotModel`:
  - `classify` (:238-247) drops `lists` and `member_segments`;
  - `custody_anchor` (:249-255) records a classified non-anchor `.opensip`;
  - `walk` (:281 on) charges the member lists once at its start and skips the recorded name's second classification. This is exactly `option3_r2.py`'s `Remedied`.
- `SNAPSHOT_FILES` re-pins `snapshot_walk.rs` whole. With (b), `discovery_census.py`'s `CLOSURE` re-pins `discovery_rule.rs`.

**The regenerated vectors** (`option3_r2.output.json`, `vectorsChanged`):
- **`snapshot_ledger_vectors.json`:** under (a)+(b), only `opensip-anchors-root-and-member` changes its predicted charge: −11 objects, 0 edges, −1,582 bytes. Under (a) alone that case moves −5 objects and −718 bytes. The other 34 cases are unchanged, and the file's pins change.
- **`snapshot_session_vectors.json`:** unchanged; the session charges nothing for classification.
- **Discovery's walk, census and composition vectors:** unchanged in their predicted charges; only the closure pin moves with (b).
- **If (c) were added,** three more snapshot cases would change: `pruned-anchors-all-four` and `markers-pruned-boundary-and-link` (−1 object, −134 bytes each), and `target-without-cargo-is-ordinary` (−3 objects, −419 bytes). The bytes cap would fall to 2^31.

## An observation outside r9, for M3-B

Discovery's own `classify_cost` (`crates/security/src/custody/discovery_walk.rs`:99-110) charges no member term. Yet the walk calls `rule::classify_path(…, self.members)` (:1037, :1074), whose `custody_state` allocates one segment list per member root on every call. Unless those lists are charged elsewhere, which I have not checked, discovery's charge misses up to 64 lists per classification. (b′) would remove the allocation for both walks.
