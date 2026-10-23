# M3-C r9: the law record of item 2, the snapshot ledger's caps

**Lead law record r9, round 2, 2026-10-16. Proposed; it needs Codex review.** Round 1 drew REQUIRED-FINDINGS (`reviews/codex-m3c-r9-r1/REVIEW.md`). This record is the gate C1a plan r6 names for C1a4 (`c1a/PLAN-r6.md`:9, RF-1). Until it is accepted, C1a1 to C1a3 stay preparatory: there is no `snapshot_profile` and no production snapshot-ledger claim (PLAN-r6:9).

**The lead's decision (round 2).** The caps are **2^21 objects, 2^24 edges and 2^33 bytes**, conditional on C1a4 landing two classification remedies, (a) and (b′) (§5, §6):
- **(a):** a `.opensip` name is classified once, reusing the anchor scan's classification.
- **(b′):** the shared rule compares member prefixes without allocating, so no member charge remains.

As built today, the rule gives 2^24, 2^24 and 2^36 (§1.2).

## r2 changes

| Finding | Change |
| --- | --- |
| **RF-1**: discovery's depth bounded the snapshot row charge | Discovery's MAX_LISTED_DEPTH is gone from the derivation (§1). Rows are bounded only by the snapshot's own rules:<br>• LogicalPath allows at most 4,096 scalars and 585 `target` segments;<br>• the 4 MiB descriptor bounds the rows' frames jointly.<br>The row term is D × the largest charge per frame byte over every row shape, each at its dearest branch, `target` classification objects included. Codex's counterexample is a model-only regression case (§1.4). No snapshot depth limit is imposed. |
| **RF-2**: D15 member roots were omitted | **As built:** the member terms are bounded by M3-B's limits: 64 members of at most 256 segments each (§2). This is the `memberBounded` variant.<br>**Adopted:** under (b′) no member charge remains (§1.5).<br>**Census:** each entry and workspace is priced with the members `discovery_census.d15_terms` admits. There are none: no T2 tree can hold a `.git`. Workspaces are also priced as if every mount were a member (§4).<br>**`.opensip`:** the double classification is charged as built. Under (a) it goes. |
| **RF-3**: an oversized no-boundary superset was excluded | Pricing and eligibility are separate (§4, §8). Over-item-5 is decided on a lower bound of the admitted extent's rows: discovery's own boundary derivation, less every marker and every row below a directory deeper than MAX_UNIT_DEPTH. All five exclusions are proven that way. |
| **NBO-1**: pin the sealing input | `term_a_r2.py` and `option3_r2.py` refuse any sealing source but the pin. The pin is C1a3 r2's (Codex C1A3-R1-RF-1): **16,400 bytes, SHA-256 `7ad4593b5bc9632cce677e978ce1a385b8d0dbb7303bc391a5ad47fad5be71a0`**, with a byte copy in `evidence/c1a3-snapshot_seal.rs`.<br>Its charged `work.` lines are identical to those of the round-1 candidate (15,993 bytes, `bf009872…8289`), and every number is unchanged.<br>r9 does not accept C1a3. If C1a3's review changes a charged site, the derivation must be redone. |
| **NBO-2**: the completed ledger's margin | The subtotal includes sealing and the leftover capture's path copy. Every census margin is on the full ledger: walk + session + sealing + leftover (§4). |
| **NBO-3**: feasible examples; the cheapest row | Every row is charged at the session's dearer branch (a new blob), used conservatively. Round 1's 100,000-row finding was infeasible (at most 42,362 rows fit the descriptor), and it is replaced (§1.3). The refusal example uses a feasible row count (§5). |
| **Lead decision** | (a)+(b′), with the caps 2^21, 2^24, 2^33 conditional on C1a4 (§5).<br>C1a4's code, model and vector obligations are in §6.<br>The blind receipt goes stale, and a reviewed refresh follows (§6).<br>A discovery undercharge is a finding for M3-B (§7).<br>The alternatives are recorded in §5. |

**What it amends.** M3-C r8 item 2, "Ledger" (`PROPOSAL.md`:249-259):
- the object cap (:250);
- the edge cap (:251);
- the byte cap's derivation (:252-257).

Exhaustion is still `WORK.BUDGET_EXHAUSTED`, never truncation (:259). B2-b's census margin test still extends to all three caps (:259). C1-T27 holds at the final caps (:298).

**The evidence** is in `c1a-r9/evidence/`. Every number is computed by:
- the charge model `tools/security/snapshot_ledger_model.py`;
- the discovery models `tools/security/discovery_census.py` and `discovery_member_model.py`.

The inputs are product main `e937dac`, whose every input file is identical to the C1a4 worktree base `a9a84a6`, and the pinned C1a3 sealing source.

| File | Contents |
| --- | --- |
| `term_a_r2.py`, `.output.json` | The bounded subtotal as built (both variants), the regression case, the cap-bounded reference terms, and a sensitivity |
| `option3_r2.py`, `.output.json`, `option3-r2.md` | The subtotal under each remedy combination, including the adopted (a)+(b′), and the vectors each would change |
| `c1a3-snapshot_seal.rs` | The pinned sealing source (C1a3 r2) |
| `snapshot_ledger_census.py` | The round-2 census tool (a byte copy of the C1a4 candidate's `tools/security/snapshot_ledger_census.py`) |
| `census-r2.json`, `census-r2.log` | The census against four cap sets. Ids and counts only |
| `term_a.py`, `.output.json` | Round 1's term (a), kept as history. Q1's script reads it |
| `term_a_discovery_bound.py`, `.output.json` | Q1 (§3), unchanged |
| `captures_term.py`, `.output.json` | Q2 (§3), unchanged |
| `r1/` | Round 1's census tool and outputs, as history |

## 1. The bounded subtotal (RF-1, RF-2)

### 1.1 The method

- **The row path.** A row path is a LogicalPath: at most 4,096 scalars and 255 per segment (identity `descriptors.rs`), each scalar at most four UTF-8 bytes. A `target` segment takes 6 scalars plus a separator, so a path holds at most **585**. Discovery's depth plays no part.
- **The descriptor.** Each row's canonical frame `{"bytes":N,"path":"P","sha256":"H"}`, plus its separator, is at least 98 bytes plus the path's UTF-8 bytes: one size digit, and escaping only lengthens it. All frames together fit D = 4 MiB − 374 (the empty-inventory envelope) + 1 = **4,193,931** bytes.
- **The bound.** For any set of rows, Σc = Σframe × (c/frame) ≤ D × max(c/frame), so the row term per component is D × the largest charge per frame byte. 100,000 minimal frames exceed D, so the row-count bound never binds, and the script asserts this.
- **A row's charge**, at its dearest branch:
  - listing: its visit, its converted copies, its observation and its slot;
  - the `.opensip` anchor question, which as built classifies the row a second time when the name is `.opensip` and the path is not an anchor;
  - its classification: `target` copies, member lists, and object records;
  - its open and sample, and a marker's capture;
  - the session's dearer branch;
  - the read envelope's per-row share: 4 attempts and 1 write.
- **The affine form.** For a fixed `target` count and leaf class, a row's charge is affine in its path bytes L, its segments S and its leaf's bytes. The coefficients come from the model's own code, by differences on concrete paths, and are checked on further paths with four-byte scalars. The bound uses S ≤ (L+1)/2 and leaf ≤ min(L, 1,020), then maximizes over L's range for every `target` count (0 to 585) and every leaf class: plain, `target`, `.opensip`, and the four markers.
- **Members, as built.**
  - `zeroMember` is a tree that admits no D15 member.
  - `memberBounded` takes 64 members of 256 segments each. `classify_cost` then adds 64 objects and 64 × 256 × 16 bytes to every classification (`snapshot_walk.rs`:51-66, charged at :224 and :328).

### 1.2 The subtotal as built

| Term | zeroMember: objects | edges | bytes | memberBounded: objects | edges | bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Rows (D × dearest per frame byte) | 1,189,981 | 5,824,905 | 5,036,420,140 | 5,824,905 | 5,824,905 | 21,182,419,333 |
| Reads: payload share at 8 GiB (2·T/64 KiB attempts, T/64 KiB writes) | 0 | 393,216 | 0 | 0 | 393,216 | 0 |
| Session once | 4 | 136 | 135,940 | 4 | 136 | 135,940 |
| Sealing (C1a3, pinned) | 11 | 68 | 8,390,463 | 11 | 68 | 8,390,463 |
| Root | 6 | 139 | 12,100 | 6 | 139 | 12,100 |
| Leftover capture: one path copy | 1 | 0 | 16,512 | 1 | 0 | 16,512 |
| **Subtotal** | **1,190,003** | **6,218,464** | **5,044,975,155** | **5,824,927** | **6,218,464** | **21,190,974,348** |

**The dearest row shapes:**
- **zeroMember, objects and bytes:** a `.opensip` row under 584 `target` segments (a 4,096-byte path): 0.284 objects and 1,200.9 bytes per frame byte. That row is classified twice, and each classification copies its path once per `target`.
- **memberBounded, objects and bytes:** `x/.opensip`: 1.389 objects and 5,050.7 bytes per frame byte. Each classification recharges the 64 member lists (about 270 KB), so the shortest row is the dearest.
- **Edges, both variants:** `Cargo.toml` at the root: 1.389 per frame byte.

### 1.3 The findings, corrected

- **r8's caps fail item 5 on rows alone.** The descriptor-bounded row term alone is at least 776,654 objects and 5,824,905 edges under every remedy (§1.5), and the edges are over r8's 2^21. Round 1's argument (100,000 rows at 18 objects each) was infeasible: at most 42,362 rows fit the descriptor. Its conclusion stands on the corrected bound.
- **The edge bound falls.** Rows are bounded by the descriptor rather than by 100,000, so the edge subtotal is 6.2 million, not round 1's 15.4 million.
- **Round 1's row bound was unsound.** Codex's counterexample exceeds it (§1.4); this round's bound covers it.

### 1.4 The regression case (Codex's counterexample, model only)

The tree: 580 nested `target` directories, no Cargo marker, and 1,000 empty leaves `n000` to `n999`, each row path 4,064 scalars long. It is priced by the model's own walk and session.

| | Objects | Edges | Bytes |
| --- | ---: | ---: | ---: |
| The descriptor (census recipe): 4,162,373 bytes, within item 5 | | | |
| The leaves' classification alone (Codex's figure) | 584,000 | 0 | 2,453,360,000 |
| The rows' part (the tree less the bare chain) | 598,000 | 15,000 | 2,464,997,670 |
| The 580-directory chain (refusal-regime work) | 177,200 | 83,215 | 494,265,412 |
| The whole ledger, with sealing and leftover | 775,212 | 98,283 | 2,967,670,057 |

- The case has no `.opensip` and no member, so (a)+(b′) leaves it unchanged.
- Its rows' part is within the row term as built and also under (a)+(b′): 776,654 objects, 5,824,905 edges and 2,530,317,371 bytes.
- The whole case fits 2^21, 2^24 and 2^33. Round 1's row bound was 2,318,979,168 bytes, below it.

### 1.5 Under the adopted remedies, (a)+(b′)

`option3_r2.py` models each remedy as a subclass of `SnapshotModel` and re-runs §1.1's bound under it. It asserts that its baseline equals `term_a_r2.output.json` and that the unmodified model still reproduces all 35 accepted snapshot walk vectors.

| Combination | memberBounded (objects / edges / bytes) | Caps | zeroMember | Caps |
| --- | --- | --- | --- | --- |
| As built | 5,824,927 / 6,218,464 / 21,190,974,348 | 2^24, 2^24, 2^36 | 1,190,003 / 6,218,464 / 5,044,975,155 | 2^22, 2^24, 2^34 |
| (a) | 3,473,784 / 6,218,464 / 11,632,183,052 | 2^23, 2^24, 2^35 | 776,676 / 6,218,464 / 2,538,872,386 | 2^21, 2^24, 2^33 |
| (a)+(b): lists charged once per walk | 776,740 / 6,218,464 / 2,539,142,722 | 2^21, 2^24, 2^33 | 776,676 / 6,218,464 / 2,538,872,386 | 2^21, 2^24, 2^33 |
| **(a)+(b′), adopted** | **776,676 / 6,218,464 / 2,538,872,386** | **2^21, 2^24, 2^33** | 776,676 / 6,218,464 / 2,538,872,386 | 2^21, 2^24, 2^33 |
| (a)+(b)+(c): no per-`target` copies | 776,740 / 6,218,464 / 571,472,261 | 2^21, 2^24, 2^31 | 776,676 / 6,218,464 / 571,201,925 | 2^21, 2^24, 2^31 |

- Under (a)+(b′), members change nothing, so the two variants are equal.
- The dearest byte row is then a plain leaf under 585 `target` segments, at 603.3 bytes per frame byte. The dearest object and edge row is `Cargo.toml` at the root.

## 2. Member roots (RF-2)

- **The owner's limits.** M3-B bounds the admitted D15 members:
  - at most 64: `MAX_MEMBERS` (`workspace_declarations.rs`:30), refused at :875 and :1024 (`config-discovery-b/PROPOSAL.md`:147, :829);
  - each candidate at most 256 segments: `MAX_DEPTH` (:32), refused at :678.

  Both are read through the census's anchors. As built, they bound the member terms (§1.2). Under (b′) there are none (§1.5). Either way, no member term is left to the refusal regime.
- **The census path.**
  - `discovery_census.d15_terms` admits no member for any of the 44 lead-readable trees or workspaces.
  - This holds whatever the carriers say: a candidate passes `candidate_failure` only with a `.git` directory at it, and `verified_tree` refuses any `.git` component in a T2 tree.
  - Priced as if every mount were an admitted member, the five workspaces reach at most 1,163,168 objects, 1,732,207 edges and 357,679,988 bytes (`mr-ts-very-large-smithy-sdk`, which is over item 5). Every measured workspace passes 2^21, 2^24 and 2^33 that way too.

## 3. Q1 (discovery bound) and Q2 (pre-walk captures): unchanged

- **Q1.** The refutation stands. Discovery never lists below its depth bound, while the snapshot charges each entry there (a link: 8, 2, 20,107 against 0, 0, 0).
  - The factors k and term (a′) in `term_a_discovery_bound.output.json` are round-1 figures. They are sampled within the depth bound, with no member, so they are not universal maxima (Codex).
  - Nothing in r9 relies on them.
- **Q2.** B2's and C2's pre-walk captures are discovery-ledger work (`PROPOSAL.md`:206; PLAN-r6:119).
  - On the snapshot ledger, a reached capture adds nothing beyond its row.
  - A leftover adds one path copy (1, 0, 16,512), inside the subtotal.
  - The M3-B exposure stands as round 1 recorded it, for M3-B's next record: about 23.7 million objects if J1 routes B2's reads through the session. So does C2's open read-count bound.

## 4. The census (RF-2, RF-3, NBO-2)

**Coverage:** 44 lead-readable trees: 39 repository entries and 5 workspaces. Held-out entries are never opened.

**Pricing** is conservative:
- it uses the as-built charges, which each remedy only lowers;
- no boundary is applied;
- every blob is new;
- every capture is at its dearer branch;
- the members are the admitted ones (none);
- margins are on the full ledger: walk + session + sealing + leftover. The sealing and leftover terms come from `term_a_r2.output.json`: 12 objects, 68 edges, 8,406,975 bytes.

**Eligibility** is separate (§8): no tree has an admitted boundary or a directory past discovery's depth bound.

**Over item 5:** 5, each proven on the admitted extent (§8).

**Measured:** 39. The full-ledger maxima are all `poly-large-rspack`: **529,529 objects, 1,488,056 edges and 220,027,344 bytes**. That is Codex's NBO-2 figure plus the leftover copy.

**At the adopted caps** (2^21, 2^24, 2^33), every measured entry passes 2×. The smallest margins are **3,960, 11,274 and 39,040 per mille**, all on `poly-large-rspack`.

**Against r8's caps,** `js-large-webpack` and `poly-large-rspack` fail, as in round 1.

**Other cap sets** (smallest margins, per mille, all `poly-large-rspack`):

| Cap set | Objects | Edges | Bytes |
| --- | ---: | ---: | ---: |
| As built, memberBounded (2^24, 2^24, 2^36) | 31,683 | 11,274 | 312,322 |
| As built, zeroMember (2^22, 2^24, 2^34) | 7,920 | 11,274 | 78,080 |
| r9 round 1 (2^22, 2^25, 2^33) | 7,920 | 22,549 | 39,040 |

## 5. The caps (lead decision)

**The rule** (r5, PLAN-r6:9): each cap is the smallest power of two at least twice the larger of the sound subtotal and the census maximum, per component. Under (a)+(b′):

| | Subtotal (both variants) | Census maximum | ×2 of the larger | **Cap** |
| --- | ---: | ---: | ---: | ---: |
| Objects | 776,676 | 529,529 | 1,553,352 | **2^21** (2,097,152) |
| Edges | 6,218,464 | 1,488,056 | 12,436,928 | **2^24** (16,777,216) |
| Bytes | 2,538,872,386 | 220,027,344 | 5,077,744,772 | **2^33** (8,589,934,592) |

**Decided: 2^21 objects, 2^24 edges and 2^33 bytes, conditional on C1a4 landing (a) and (b′)** as §6 states them, reviewed, with the model and vectors regenerated.

**If C1a4 lands something else,** these caps do not hold. C1a4 then returns to this law, and the caps are re-derived over what it built.

**The guarantee at these caps.**
- Every tree within item 5 fits, with any D15 members within M3-B's limits, provided its work that is not a row (below) stays within the margin left over the subtotal. That margin is 1,320,476 objects, 10,558,752 edges and 6,051,062,206 bytes.
- Every measured lead-readable tree fits, with the margins in §4.

**The typed-refusal regime.** Work bounded by no item-5 or owner limit:
- directories entered (their frames, listings, captures and Cargo keys);
- listed names that are not rows (excluded, pruned, links, special files, directory names, root and member `.opensip` anchors), with their classifications;
- link and special-file path copies;
- C2's layout reads (outside r9).

As built, at r8's caps and the LogicalPath envelopes, these sum to 2,230,987 objects, 2,150,865 edges and 33,526,606,033 bytes (`capBoundedReference`, for reference). Beyond the margin they refuse `WORK.BUDGET_EXHAUSTED`, typed and never truncated (:259).

**A feasible refusal example.** Take the regression case's 1,000 rows (descriptor 4,162,373 bytes) plus 263,000 links. Each link is charged at least 8 objects: 2 for its converted copies, 1 for its observation, 4 for its classification and 1 for its path copy. That is at least 2,104,000 objects, over 2^21, so the tree refuses.

**This departs from RF-2's cap-bounded terms** (PLAN-r6:10), explicitly, as round 1 proposed. Codex judged this a reasonable law choice, provided the departure stays explicit.

**Alternatives considered and recorded:**

| Alternative | Caps | Why not taken |
| --- | --- | --- |
| As built, member-bounded | 2^24, 2^24, 2^36 | 64 GiB of charged bytes meets the objection that rejected 2^37: a hostile tree could exhaust memory before the ledger refuses (Codex notes that charged storage is not peak RSS). It also keeps the double classification and the per-classification member lists, which are avoidable work |
| As built, with member classification beyond the census in the refusal regime | 2^22, 2^24, 2^34 | It leaves bounded member work to the refusal regime, and still gives 16 GiB |
| (a)+(b): member lists built once and charged once per walk | 2^21, 2^24, 2^33 | It needs a new rule entry and a walk-wide structure. (b′) gives the same caps with no member charge at all, and it also corrects discovery's undercharge (§7) |
| (a)+(b)+(c): no per-`target` prefix copies | 2^21, 2^24, 2^31 | Not needed for 2^33. It changes three more vectors and the per-`target` cost basis, which discovery's `classify_cost` shares. It can be a later remedy |
| 2^37 and term (a); (a′); r8's caps; the census alone; a non-power-of-two cap | — | As round 1 records: memory exposure; unsound (§3); they fail item 5 (§1.3) and two entries (§4); nothing beyond the corpus tied to item 5; tuning to the corpus |

## 6. C1a4's code obligations, model terms and vectors

C1a4 lands these on top of C1a3 r2, which edits `snapshot_walk.rs` and must integrate first. The lines below are main `e937dac`'s, so they will move. The model of each obligation is `option3_r2.py`'s `Remedied` class (`a` and `p`).

**(a) The anchor scan's classification, reused** (`crates/security/src/snapshot_walk.rs`).
- **`custody_state_anchor`** (:319-331) keeps its one charge, `classify_cost(path, members)`. It returns the classification, `Option<PrunedAnchor>`, instead of a bool, and the caller tests for `OpensipCustodyState`.
- **`enter`** (:338 on): the anchor loop (:364-371) records the classification of a `.opensip` path that is not an anchor in a new `Level` field, `opensip: Option<(usize, Option<PrunedAnchor>)>`. A listing holds at most one `.opensip`, so an anchor removal and a recorded index never occur together.
- **The walk loop** (:224-227): at the recorded index, it neither charges `classify_cost` nor calls `rule::classify_path`, and it uses the recorded result.
- **Why the reuse is exact:**
  - The only difference in `known` between the anchor scan and the loop is the directory's own Cargo push (:407-411), which `enter` makes after the scan.
  - `classify_path` tests a Cargo prefix only in front of a `target` segment. Every such prefix of `x/.opensip` is a strict ancestor of `x`.
  - The member roots are fixed.

**(b′) Member prefixes compared without allocating** (`crates/security/src/custody/discovery_rule.rs`).
- **`custody_state`** (:132-152) stops collecting `base.split('/')` for each member root. For a non-empty base, it tests the path's byte prefix: `relpath` begins with `base` followed by `/`, and the next segment is `.opensip`. It takes k, the base's segment count, from a non-allocating count. The result is the same `PrunedAnchor`.
- **The rule's behaviour is unchanged.** `classify_path`'s signature and results stay, for every caller: the snapshot walk, `discovery_walk.rs`, `discovery_scan.rs`, `workspace_declarations.rs`, `discovery_export.rs` and `host/src/discovery.rs`. The Python reference rule is unaffected.
- **`snapshot_walk.rs` `classify_cost`** (:51-66) drops `lists` and `member_segments`, and keeps the segment list, the per-`target` prefixes, the three anchors and their records. Its doc comment (:44-50) drops the member clause.
- **`discovery_rule.rs` is M3-B's file.** The change needs that owner's reviewed acceptance in C1a4's review.

**The model terms** (`tools/security/snapshot_ledger_model.py`).
- `SNAPSHOT_ANCHORS`:
  - `CLASSIFY` (:81-92) loses the member fold;
  - `ANCHOR_CLASSIFY` (:93-95) is re-matched against `custody_state_anchor`'s new return;
  - a new anchor pins the walk loop's reuse of the recorded `.opensip` classification.
- `SnapshotModel`:
  - `classify` (:238-247) drops `lists` and `member_segments`;
  - `custody_anchor` (:249-255) records a classified `.opensip` that is not an anchor;
  - `walk` (:281 on) skips that name's second classification.
- `SNAPSHOT_FILES` re-pins `snapshot_walk.rs` whole. `SNAPSHOT_OBJECTS` and `SNAPSHOT_EDGES` (:131-133) become 2^21 and 2^24, and C1a4 adds the byte cap 2^33 and the `snapshot_profile`.

**The regenerated vectors** (`option3_r2.output.json`, `vectorsChanged`):
- **`snapshot_ledger_vectors.json`:** only `opensip-anchors-root-and-member` changes its predicted charge, by −12 objects, 0 edges and −1,726 bytes. The other 34 cases are unchanged, and the file's pins change.
- **`snapshot_session_vectors.json`:** unchanged.
- **Discovery's walk, census and composition vectors:** unchanged in their predicted charges, since discovery's `classify_cost` is untouched.

**The census closure, and the blind receipt.**
- `discovery_rule.rs` is a census-closure file, pinned whole in `discovery_census.py`'s `CLOSURE` (:76, 18,080 bytes). `receipt_bindings` (:1086-1095) binds the closure and the tool's own pin into the held-out receipt `crates/security/src/custody/discovery_census_held_out.json`, which now holds.
- So C1a4 refreshes the `CLOSURE` row, which changes `discovery_census.py` itself, and **the blind receipt becomes stale**.
- **A reviewed blind refresh follows,** under the owner's held-out protocol (`owner-decisions/2026-10-16/HELD-OUT-T2-MARGIN.md`) and B2-b4c's reviewed blind mode: the request is reviewed before the run, and the receipt after it.
- C1a4's own blind snapshot validation (PLAN-r6:11, RF-3) is separate and still runs once, against the frozen caps.

## 7. A finding for M3-B's owner: discovery undercharges member classification

- **What discovery's walk charges.** It classifies at three sites, each charging only `classify_cost(&rel)`:
  - `crates/security/src/custody/discovery_walk.rs`:943-945, through `rule::classify_entry`, which calls `classify_path` (`discovery_rule.rs`:506-519);
  - :1036-1037;
  - :1073-1074.

  `classify_cost` (:99-110) takes no members. It charges the segment list, one prefix per `target` and the anchor.
- **What the rule allocates.** Each call passes `self.members` (the admitted D15 member roots, set at :1172 from `request.member_roots`). `classify_path` calls `custody_state` (`discovery_rule.rs`:132-152), which collects a `Vec<&str>` for every non-empty member root on every call.
- **Nothing else charges them.** The walk's construction (:1155-1180) charges nothing for members, and no other charge in `discovery_walk.rs` names them. The census model mirrors the omission: `discovery_census.Model.classify` (:525-529) has no member term.
- **The result.** Each classification with m admitted members leaves m allocations uncharged, up to 64 lists totalling 256 × 64 segments of 16 bytes. Charged as the snapshot charges them, that is up to 64 objects and 270,336 bytes per classification. Only walks with admitted members are affected; the lead-readable census admits none (§2).
- **(b′) removes the allocation for both walks.** Discovery's `classify_cost` is then exact for it, with no change to discovery's charges, vectors or caps.
- **Recorded here for M3-B's owner; r9 does not amend M3-B.**

## 8. Over item 5 and margin coverage (RF-3)

**An entry is classified over-item-5 only on its admitted extent.** The lower bound of its rows is built in four steps:
1. Start from the boundaries the discovery walk model derives over the same tree: a child directory with VCS evidence or an `opensip.json` that is not a member (`discovery_census.Model.subtree`), recorded by a subclass of the census's own model.
2. Remove every marker, since a MARKER_CUSTODY row excludes only its marker.
3. Remove every row below a directory deeper than MAX_UNIT_DEPTH (`discovery_scan.rs`:22, 256), since a DEPTH row excludes its unit and below.
4. DIRECTORY_CUSTODY rows depend on ownership and modes, not on the tree. The reference installation installs every directory 0755 and every file 0644 with one link, owned by the invoking user (`discovery_census.reference_population`), so it raises none.

The entry is over-item-5 only if this lower bound exceeds 100,000 rows, a 4 MiB descriptor or 8 GiB. Any other entry stays in the margin population at its conservative price.

**The evidence for each exclusion.** Every one has 0 admitted boundaries, 0 directories past the depth bound and 0 members. In the table, "less markers" means the rows the lower bound removed.

| Entry | Admitted rows (less markers) | Lower-bound rows | Lower-bound descriptor | Exceeds |
| --- | ---: | ---: | ---: | --- |
| `rs-very-large-aws-sdk-rust` | 245,250 (483) | 244,767 | 40,190,661 | rows, descriptor |
| `ts-very-large-aws-cdk` | 29,336 (143) | 29,193 | 6,489,994 | descriptor |
| `ts-very-large-aws-sdk-js-v3` | 51,178 (1,071) | 50,107 | 8,262,274 | descriptor |
| `py-very-large-home-assistant` | 28,570 (1) | 28,569 | 4,217,533 | descriptor, by 23,229 bytes |
| `mr-ts-very-large-smithy-sdk` | 53,494 (1,158) | 52,336 | 10,096,694 | descriptor |

**Which entries count.**
- These five cannot seal, and they never count toward the maximum.
- The other 39 are measured on all three components at 2×.
- Held-out entries are covered only by C1a4's one reviewed blind validation run, which measures against frozen caps and chooses nothing (PLAN-r6:11, RF-3).

## 9. What r9 supersedes (Q3)

**Current text, superseded:**
- `snapshot-plan-c/PROPOSAL.md`:250, :251 and :252-257. :259 and :298 stand.
- `c1a/PLAN-r6.md`:97, and :10, :17 and :20-22 as §5 departs from them.

**Product code, which C1a4 changes (§6):**
- `tools/security/snapshot_ledger_model.py`: :131-133, its docstring at :16, and §6's model terms;
- `crates/security/src/snapshot_walk.rs`: (a), and (b′)'s `classify_cost`;
- `crates/security/src/custody/discovery_rule.rs`: (b′);
- `tools/security/discovery_census.py`'s `CLOSURE` row;
- the regenerated vectors.

No snapshot profile exists yet in `crates/platform/src/work_ledger.rs`.

**History, left unchanged:**
- `PROPOSAL-r8.md`:248-249 and :255;
- `c1a/PLAN-r1.md` to `PLAN-r5.md` (round 1's lines);
- the `codex-c1a-plan-r5` and `codex-c1a-plan-r6` requests;
- the archived model copies;
- this record's round 1 (`term_a.py`, `r1/`).

**Not this ledger's:** discovery's caps, which r9 leaves unaffected, in `config-discovery-b/PROPOSAL*.md`, B2-b, `M3-PLAN*.md`, `IMPLEMENTATION-STATUS.md`:183, :226 and :246, and `HELD-OUT-T2-MARGIN.md`:5. §7's finding is for M3-B's owner.

## 10. Questions for the reviewer

- **Q1.** Is §1's row bound sound and complete for item 5?
  - D × the largest charge per frame byte;
  - the affine form in L, S and the leaf, checked against the model;
  - the relaxations S ≤ (L+1)/2 and leaf ≤ min(L, 1,020);
  - every `target` count up to 585.
- **Q2.** Do §1.5 and `option3_r2.py` model (a) and (b′) faithfully? Are §6's obligations complete and exact, including the reuse argument and the vector changes? Are 2^21, 2^24 and 2^33 rightly conditional on C1a4 landing them?
- **Q3.** Is §6's account of the census closure and the blind refresh right?
- **Q4.** Is §7's undercharge real, and does (b′) correct it for discovery with no change to discovery's charges?
- **Q5.** Is §8's lower bound a valid proof of over-item-5 for each of the five, and is the reference installation's lack of directory-custody rows a valid premise?
- **Q6.** Is §5's typed-refusal regime (directories, names that are not rows, copies) correctly bounded away from the subtotal?
