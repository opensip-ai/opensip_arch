# C2b-1a funding derivation r4: the closure, native-frame and nested-record admission terms, their funded census with its explicit measured boundary, and the complete price premises (R3 escalated author, 2026-10-29)

Capability route: R3-FRONTIER
Codex: gpt-6-astra / high
Claude: claude-fable-5-1 / high
Claude long-horizon lead: claude-fable-5-1 / high
longHorizonLead: false; one bounded derivation and its review rounds, handed back to the C2b-1a author.
Escalate when: a term needs a change to accepted charge law (M1a) or a cap, or the Fable pass fails on the same term
after a complete R3 review round.
Escalation route: R4-EXCEPTIONAL, only with an explicit coordinator exceptional authorization under OD-AUTO-1. A law
or cap change goes to the coordinator.
Independent review: Codex gpt-6-astra / high (R3-FRONTIER), the same reviewer session in Herdr w16:p1, a different
vendor from the Claude author.
De-escalate when: the combined derivation is accepted. The C2b-1a author (R2-DEEP) folds it into its plan.
Exceptional authorization: none; max/xhigh prohibited.

**Author derivation r4, 2026-10-29. Proposed; it needs Codex review.** Author: Claude Fable 5.1 high
(R3-FRONTIER, Herdr w17:p1), escalated from the Opus 5.5 author under PLAN.md's escalation line after `REVIEW-r2.md`
left round-1 RF-1 open (`CONTINUATION-r3.md`; LEAD-LOG.md; route preflight `ROUTE-OK R3-FRONTIER claude
claude-fable-5-1/high`). Documents and scripts only; no product, architecture or control edit. Plan: `PLAN.md` here
(coordinator ruling LD-Q-5), continued by `CONTINUATION-r3.md`. It answers C2b-1a plan review r2 RF-1 and RF-2
(`../plan/REVIEW-r2.md`) and fills the FUNDING-R3 slots of `../plan/PLAN-r3.md` LD-C2B1-8.
**Round 4 answers `REVIEW-r3.md`** (REQUIRED-FINDINGS: for this subject RF-1, NBO-1 and NBO-2; for the companion RF-2),
under coordinator ruling LD-Q-12 (round 4 at R3-FRONTIER by this author). Round 3 answered `REVIEW-r2.md`. r1, r2 and
r3 are kept unchanged as `FUNDING-DERIVATION-r1.md`, `-r2.md` and `-r3.md`, with their scripts and evidence under
`scripts/r1/`, `evidence/r1/`, `scripts/r2/`, `evidence/r2/`, `scripts/r3/` and `evidence/r3/`.

**Companion subject (coordinator ruling LD-Q-6).** The C2b-1a author's non-admission slot derivation
(`../evidence/SLOT-DERIVATION-r4.md`, sha256 `c6924ed3c26b6754351bbc8420a25fa9bf64f94c9bf0b4dc4048fce64fb723bd`; T-WALK-ROOT/CTX/UNI,
T-OWNER-CTX/UNI, T-REFUSE-CTX/UNI, COPY-R377/U187/R400) is reviewed with this one under one verdict. That author
writes it; this author owns the combined derivation and checks that it uses §2–§3.7's primitives unchanged, counts
nothing that §6 counts, and keeps §9's partition (§12). Its §4 is the one occurrence matrix of both calls; §6 here is
that matrix's funding column.

## r4 changes

| finding | change | where |
| --- | --- | --- |
| **REVIEW-r3 RF-1** (the r3 binary search executed `x < kb` and then `x > kb` per iteration while counting one comparison; the same in `Store.lookup`) | Every search iteration is now **one explicit three-way byte comparison** (`compare_keys`, what `Ord::cmp` on `[u8]` and a Rust `binary_search_by` iteration execute): both operands are read up to the first differing byte or the length tie-break, and the iteration is counted as one comparison with exactly the bytes it read. No relational operator on key strings runs inside the boundary, and an **independent observer** (`ObservedBytes`, the reviewer's method) checks that: with every static key wrapped, the observed relational operations are 0 for below-first-key, equal-first-key, equal-last-key, above-last-key and undeclared-middle lookups on the context root slot (K = 9) and its `honoredOptions` slot (K = 18), with comparisons ≤ bitlen(K) and bytes within the member charge; the store search is checked the same way (present, below every digest, above every digest). r3's defect is reproduced as the `two-sided` mutation and is caught by the observer (8 observed operations against 4 counted). | §8; `compare_keys`, `slot_lookup`, `Store.lookup`, `observe_keys` in `scripts/admission_model.py`; `lookup_controls` in `scripts/vectors.py`; §7.1; F6 |
| **REVIEW-r3 NBO-1** (the synthetic digest was computed inside the boundary before the store lookup) | The retained digest is **supplied to the census from outside the boundary**: the fixture builds it when it builds the store, and `Record` receives it as `key`, as the pinned fetch receives an already supplied digest (`closure.rs`:85-95). Nothing is encoded or hashed between the record's census and its charged lookup. A **retained-lookup exhaustion probe** is added on each frame and record: with the budget set to the work charged before the lookup, the census refuses at the lookup with no store comparison run. | §8; `Record`, `digest_key`; `scripts/exhaustion.py`; §7.1; F6, F11 |
| **REVIEW-r3 NBO-2** (§8's wording on when the aggregate census charge is debited) | §8 now says: the published aggregate per record is the **sum of the debits made during the single census**, element by element; it is not available beforehand and is not charged beforehand. It is additional to the admission and owner prices. | §8 |
| companion **REVIEW-r3 RF-2** (DFS `state` on refusing graphs) | Answered by the C2b-1a author in `SLOT-DERIVATION-r4.md`: the DFS terms are re-derived over every discovered key, missing edge targets included (K ≤ 1 + E, pops ≤ 2 + 2E, 2K state inserts, key lengths over L\_key = max(\|entry\|, \|e\|max); U:482-490 searches K; U:469 formatted over L\_key), with the missing-target fan-out control S10. §12 records this author's check and restates the whole-call coverage claim as the review asks. | §12 |

r4 changes no term's price, no §6 row or occurrence count, and no premise file (`scripts/compare_r2.py`: all 35
admitting terms equal to r2 on allocation side, pass side and total; every cross-check output byte-identical to r3's
and r2's). The census's counted bytes fall slightly (a three-way comparison reads only to the first differing byte);
its charges are unchanged.

## r3 changes

| finding | change | where |
| --- | --- | --- |
| **RF-1** (the r2 reference did work before its element charge, and its counters did not measure the stated algorithm) | **The measured boundary is explicit** (LD-F-8; §8). *Outside it*, built before the census and never counted: the accounted value representation, which is what Rust's `Value` supplies in O(1) (`String::len`, `Vec::len`, `BTreeMap::len`; object members in UTF-8 byte order, `canonical.rs`:143-148, :549-550); the static price table (each slot with its **sorted declared-key list** and per-key member table, RESOLVE, DISPATCH, literal statistics, ORDER\_PARSE, the `ordered` arms, ROW\_CLONE); and C2b-1a's retained map. *Inside it*: every element is **charged before its work** from those O(1) sizes; a string is then scanned once, the scan counting **per scalar inside its loop** with no second pass; a member key is scanned once after its charge and looked up by an **explicit binary search** over the sorted static keys, each comparison counted with the bytes it examines; every loop counts in its body. Counted ≤ charged holds **per element** and in total. **Exhaustion tests** (`scripts/exhaustion.py`): with the budget set to the work charged before a chosen element, the census refuses at exactly that element with no scan and no visit of it begun; chosen elements include the first element, a string node and a member key after earlier elements have consumed budget, and the last of each kind, on five record kinds (42 probes). The `scan-first` mutation (r2's defect), `linear-lookup` and `unique-extra` are caught. Every term's price is **unchanged** from r2 (`scripts/compare_r2.py`: equal allocation side, pass side and total on all 35 admitting terms). | LD-F-8; §8 (rewritten); `scripts/admission_model.py` (`AV`, `Slot`, `Inv`, `scan`, `slot_lookup`, `Census`, `Store`); `scripts/exhaustion.py`; §7.1; F6 (rewritten) |
| **RF-6** (whole-call sums not disjoint; joint with the companion) | §6 is stated as the **admission-only, fully additive funding column** of the companion's occurrence matrix (`SLOT-DERIVATION-r3.md` §4). Its notes are marked non-additive. §12 cites the companion's term names and ledger rows instead of re-listing operations, and states both whole calls as that matrix's column sums. | §6; §12 |
| **NBO-1** (the depth gate was off by one for an empty final container) | The gate is the encoder's: **a container at container depth 32 refuses** (`canonical.rs`:536), whatever it holds; a scalar inside the 32nd nested container is priced. Six boundary vectors (F10). | LD-F-7 (amended); `census`; §7.1; F10 |
| **NBO-2** (T-SNAPSHOT's equation) | owned(74), the refusal-path `MissingObject(key.into())` string of the 74-byte `snapshot2:` key, is added to T-SNAPSHOT's equation, as OBJECT carries it. | §5.1 |
| companion **RF-3**, applied to these terms (its "all BLOB occurrences") | Every BLOB here (FRAME `:1450`, RECORD `:1119` and `:1120`, W-REC) hashes the **actual retained length β(d)**, obtained by a funded, counted census lookup into C2b-1a's retained map. Gate **F11** refuses `PriceUnavailable` when β(d) is not the value's own encoding length (F for a frame, L for a record), because PARSE and UNFRAME are derived over that encoding. An absent digest is priced at the full term (the fetch refuses `MissingBlob` after its search, which BLOB covers). | LD-F-9; §3.7; §4.4; §4.5; §7.1; F11 |

r3 changes no term's price, no §6 row or occurrence count, and no premise file. Every cross-check output is
byte-identical to r2's (`evidence/*-r3.stdout`). The census's own charge rises by one edge per string value node (its
scan is now a counted element) and by one retained-length lookup per frame or record.

## r2 changes (kept for the record)

| finding | change | where |
| --- | --- | --- |
| **RF-1** (the price pass's own charge was asserted) | The price is computed by **one fused, post-order census per record**. It visits each value once, keeps O(1) state per frame and allocates nothing. Every subtree statistic is computed once and passed to the parent. The census is **charged element by element (C1), before each element's work, from sizes available in O(1) at that moment**: node, member, item. The bound is the census's own step count, so no unfunded census supplies N. The reference model counts the steps its loops actually execute and holds counted ≤ charged on every record. A mutation adding an unpriced traversal is caught. | LD-F-6; §8 (rewritten); `scripts/admission_model.py` `census`; F6 (rewritten) |
| **RF-2** (the price was undefined on malformed values) | **Every rule is a total function of per-node statistics.** A price exists for every JSON value of container depth ≤ 32. A deeper value refuses `PriceUnavailable`: the canonical encoder could not have produced it (`canonical.rs`:6, :536). ORDER\_VERIFY's key is bounded by the item's walk bytes, and the field lookups are priced on any item kind. Every `ordered` arm is priced. §3.2's argument now states the defined cost of the artificial tail. Eleven malformed-shape vectors carry their expected verdicts. | §3.2; §3.6; §4.2; §7.1; F8, F10 |
| **NBO-1** (the long-path vector refused) | Distinct, strictly increasing 4,096-scalar paths are used for the admitting case. r1's 26-distinct construction is kept as a named refusal vector. Every vector carries its expected verdict, which F8 asserts. | §5.2; §7.1 |
| **NBO-2** (allocation/pass split) | Every price is published as (allocations, passes), as C9's `AdmissionPrice`. The meter's parse price is held whole on the allocation side, `btree_insert` is split as C9 splits it, and `digest_cost` sits on the pass side. F8 holds storage to the allocation side. | §3.7; §7.1; F8 |
| **NBO-3** (F4's order checks) | F4 also checks the sorted, non-overlapping ranges of `CASED` and `CASE_IGNORABLE`. It is described as checking the price-relevant populations and extrema; F1's hash catches every byte. | §10 |
| self-found | OBJECT adds the refusal-path `MissingObject(key.into())` string (`closure.rs`:103-106). | §4.3 |
| LD-Q-6 | The companion slot derivation is reviewed with this one. | §12 |

r2 changes no §6 row or occurrence count and no premise file. Against r1 it raises each term's total by bounds
only. `scripts/compare_r1.py` checks r2 ≥ r1 componentwise on every term of every admitting scenario, comparing
r1's recursive model with r2's census.

**Subject pin.** Product main `98159381648b0ddad022f1c7fffe678ce0e27208`. It contains C2a-3 (integrated) and the
reviews' product pin `e97f0bd`. Every source line below is at this commit, and every script reads its premises
through `git show 9815938:<path>`, never a working tree.

Evidence prefixes: `P/` = the product at the pin; `M/` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25/`.
Unprefixed paths are relative to this directory.

## 0. The answer in brief

- **RF-1.** There is one generic schema-admission term, **ADMIT(E, x)**. It is derived once, line by line, from
  `P/crates/identity/src/schema.rs`, and instantiated for each selected entry *E* by that entry's own evaluation tree
  τ\_E. τ\_E is generated from the pinned registered schema document. Around ADMIT sit the wrappers each call path
  actually runs:
  - FROM\_JSON (identity `from_json`), used by OBJECT;
  - FRAME (`frame_candidate`);
  - RECORD (`inspect_current_record`).

  These give the per-schema terms:

  | slot (PLAN-r3) | term | entry *E* |
  | --- | --- | --- |
  | T-SNAPSHOT | OBJECT(snapshot) with **C9's `descriptor_admission_cost` as published** | identity-v3 `/$defs/snapshot` |
  | T-CLOSURE | OBJECT(closure) = FROM\_JSON over `$defs/closure` | identity-v3 `/$defs/closure` |
  | T-FRAME-CTX | FRAME | native-v2 `/$defs/TypeScriptNativeContextV2` |
  | T-FRAME-UNI | FRAME | native-v2 `/$defs/TypeScriptUniverseV2ResolvedInputs` |
  | T-REC-GRAPH | RECORD (+ the callers' re-reads, W-REC) | native-v2 `/$defs/TypeScriptConfigGraphV1` |
  | T-REC-LAYOUT | RECORD (+ W-REC) | native-v2 `/$defs/ResolvedNodeModulesLayoutV1` |

  - C9's published price is kept only for the snapshot, where its premises hold (§5.1).
  - Every other term is priced over its own schema, ordering and hash domain, from the exact value C2b-1a passes.
  - Closure rows with long or escaped paths are priced exactly: decoded lengths drive evaluation and matchers, and
    canonical lengths drive parse, encode and hash (§5.2).
- **The price pass (r2, r3).** One funded, allocation-free census per record computes every term from per-node
  statistics. Its measured boundary is explicit (§8): it is charged element by element under C1, before each
  element's work, from sizes the value representation supplies in O(1), and it counts its own work where that work
  runs. Its rules are total on every value with at most 32 nested containers (§3.2). Every price is split into
  allocations and passes (§3.7).
- **The admission composition** of the two whole calls is counted from source (§6). Mint runs:
  - T-SNAPSHOT 1;
  - T-FRAME-CTX 2;
  - T-CLOSURE 2 per closure;
  - T-REC-LAYOUT 1.

  Bind runs:
  - T-SNAPSHOT 2;
  - T-FRAME-UNI 2;
  - T-FRAME-CTX 4;
  - T-CLOSURE 3 per closure;
  - T-REC-GRAPH 2;
  - T-REC-LAYOUT 2.

  The context owner's deep clones of both closure descriptors are added (1 per closure at mint, 2 at bind).
- **RF-2.** The complete premise list, `PRICE_PREMISES` (§10), covers:
  - 25 files with their blob SHA-256, including the generated `unicode_case_tables.rs`, the reused host, security and
    platform helpers, both schema sources, `rust-toolchain.toml` and `Cargo.lock`;
  - the std premises, incorporated by exact reference to their existing M1a controls.

  Each premise names the control that invalidates it. Four new derivation controls go beyond the blob pins: the
  schema-table, pattern-table, case-table drift and multiplicity controls (§11).
- **T/L/N: none** (§9). No term is a charge of the selected snapshot operation, so successor-law item 1 assigns them
  no family. *T*sound, *L*max, *N* and the caps are unchanged.

## 1. Lead decisions (this unit)

- **LD-F-1. Scope.** This derivation covers the R2-RF-1 admission terms, their call multiplicities in both calls, and
  the complete premise list for every file the priced calls reach. The non-admission operations in the T-WALK,
  T-OWNER-CTX, T-OWNER-UNI and T-REFUSE slots stay with the C2b-1a author's reachable-operation inventory
  (`../plan/PLAN-r2.md` LD-C2B1-8). The reviewer accepted that inventory's structure at plan level
  (`../plan/REVIEW-r2.md` Q4); RF-1 was confined to the admission prices. §12 lists the operations in those slots
  that this derivation found and the inventory lacks, and gives the primitives (CLONE, the fold constants) they need.
  The premise list (§10) covers all slots, because it must cover every file the whole call reaches. **r2:**
  coordinator ruling LD-Q-6 makes the author's slot derivation a companion subject of this review, checked as §12
  states.
- **LD-F-2. One generic evaluation term, mechanically instantiated, instead of a C9-style hand table per schema.**
  - C9 counts lookups by hand for one fixed structure (`M/c2b-m1/C9-DERIVATION-r1.md`:84-96).
  - The five schemas here are different: 107 evaluation-tree invocations for the context alone, with `oneOf`
    nullable branches, five order kinds and variable arrays (§3.8).
  - A hand table per schema would be a large new surface for transcription error. Instead, one per-invocation cost
    is derived from `evaluate`, and τ\_E is generated from the registered document and pinned by a control that
    regenerates it.
  - The generic term is cross-checked against both published precedents on the same records (§7.2). It is within
    1–2.3% of C9 on every component of six snapshot descriptors. It is the higher in edges and walk bytes, and C9 is
    looser where it bounds by means or a 20-byte query. Against C2b-0's layout admission price, generic edges run
    10–13% lower, an amount accounted for by C2b-0's fixed 64/128-edge allowances.
- **LD-F-3. The price is computed from the exact values C2b-1a passes.** C2b-1a builds the context, universe, graph
  and layout records itself, and it holds the admitted closure descriptors and the sealed snapshot descriptor. Its
  shape census is a walk over those values (r2's `RetentionShape`, made exact). The price pass is funded first
  (§8).
- **LD-F-4. A conservative envelope where exact metering is impractical (M1a C1; successor law M1a "conservative
  bounded envelopes are acceptable").** Evaluation is priced as if every `oneOf` rule ran and no early
  `return Ok(false)` were taken. The actual evaluation is a sub-multiset of that, operation by operation (§3.2).
  Search, growth and comparison bounds are the accepted primitives (§2).
- **LD-F-5. T-SNAPSHOT keeps C9 as published.** Its premises hold here: the same `from_json` over the same canonical
  sealed descriptor. Only its new wrapper is added: the object-map search, the re-encode, the identifier comparison
  and the role scan. The generic term over the snapshot is computed and published as reference only (§7.2).
- **LD-F-6 (r2, RF-1). One funded census per record.** Every admission term is computed from a single post-order
  walk of each priced record (§8):
  - each value is visited once, and its statistics (§3.2) are returned to its parent;
  - O(1) state is kept per frame, and nothing is allocated;
  - the evaluation table is static.

  The census is charged element by element before each element's work (M1a C1, "if its extent is known only
  element by element"), and its charge is its own step count. A record's census runs once, and every occurrence of
  its term (§6) reuses the result.
- **LD-F-7 (r2, RF-2). Total rules over statistics, not a narrowed theorem.** Every rule is a total function of the
  statistics of a node and of its direct children. The price is therefore defined for any JSON value the census
  accepts, which is any value with at most 32 nested containers: a container at container depth 32 refuses, exactly
  as the encoder does (`canonical.rs`:536; r3, NBO-1), and a scalar inside the 32nd container is priced. A malformed
  record is priced, not refused before pricing. The one `PriceUnavailable` gate on shape is that container gate; r3
  adds the retained-length gate F11 (LD-F-9). The static gates, all fixed by the table and checked by F2, are:
  - a keyword outside §3.2;
  - a Rust or syntax domain;
  - C9's structure for T-SNAPSHOT.
- **LD-F-8 (r3, REVIEW-r2 RF-1). The measured boundary is explicit, and the reference measures the algorithm it
  claims.** The census is specified against the value representation C2b-1a already holds (Rust's `Value`, LD-F-3),
  whose lengths are O(1) and whose object members are ordered; against a static price table that holds, per slot,
  its sorted declared keys and its per-key member tables; and against C2b-1a's retained map. Those three are
  outside the boundary. Inside it, every element is charged before its work from those O(1) sizes, and every loop
  counts in its body: the string scan per scalar, the declared-key binary search per comparison, the store search
  per comparison. Counted ≤ charged is held per element and in total, and the exhaustion tests of §8 are the F6
  reference. No count is taken from an unfunded pass: N, B, L, the scan results and the lookup results are outputs
  of charged elements.
- **LD-F-9 (r3; companion RF-3). Every BLOB hashes the actual retained length.** BLOB(d) is search(|blobs|, 32) +
  digest\_cost(β(d)), with β(d) the length of the buffer actually retained under d, obtained by a charged census
  lookup (§8). These terms' PARSE and UNFRAME are derived over the value's own canonical encoding, so the census
  requires β(d) to equal that encoding's length (F for a frame, L for a record) and otherwise refuses
  `PriceUnavailable` before any term work (F11). C2b-1a builds its retained store from the same values it prices, so
  the gate is a fail-closed check of that construction, not a narrowing of the priced inputs. An absent digest is
  priced at the full term: the fetch refuses `MissingBlob` after its search (`closure.rs`:85-96), which BLOB covers.

## 2. Reused primitives and their premises

Each is used exactly as published. A source line is given for each; `PRICE_PREMISES` (§10) pins each file.

| name | definition | source | premise / existing control |
| --- | --- | --- | --- |
| C1 pass | {0, k, b}: k elements, b bytes examined | `M/c2b-m1/M1A-PRICING.md` C1 | convention |
| owned(b) | {1, 0, b + 128} | `P/crates/security/src/snapshot_source.rs`:616-618 → `custody/discovery_walk.rs`:87-95 | RECORD = 128 |
| search(m, q) | k = min(m, 11·bitlen(m)) comparisons, 2k(q + 1) bytes | `P/crates/host/src/snapshot_admission.rs`:160-166, `node_modules_layout.rs`:246-249, :332-334 | P2/P3: `search_comparison_bound_covers_node_and_population_growth`, `tree_search_bound_covers_many_long_common_prefix_keys` (`node_modules_layout_tests.rs`:1764, :1778) |
| digest\_cost(n) (C2) | {1, 1, n + 32 + 128} | `P/crates/host/src/snapshot.rs`:82-87 | sha2-const-stable 0.1.0 (`Cargo.lock`) |
| btree\_insert(m, key, entry) (L2) | height 1 + bitlen(m); h + 1 nodes, 12h + 1 edges, node, search and move bytes | `snapshot.rs`:89-130 | P2/P3 |
| growth(n, size) (P1) | 2 + log2 n events, 3·max(min, 2n)·size + events·128 bytes | `snapshot_admission.rs`:170-184 | `the_growth_bound_covers_its_sequences` (`snapshot_admission_tests.rs`:192-211); the toolchain rule in `metered_parse.rs`:196 |
| formatted(n) | owned(2n) + growth(n, 1) | `snapshot_admission.rs`:208-212 | `format!` estimate ≤ 2× its pieces (C9) |
| meter prices (C4) | entry {0, 1, 16L}; value {0, 1, 0}; string; search; insert; array | `P/crates/identity/src/canonical.rs`:139-258 | `the_metered_parse_is_parse_and_its_charges_bound_its_allocations` and `the_toolchains_growth_rule_is_the_one_the_meter_prices` (`P/crates/host/tests/metered_parse.rs`:142, :196; the latter also holds `parse_prices::array`) |
| C9 | `descriptor_admission_cost(DescriptorShape)` | `snapshot_admission.rs`:564-582 | its own controls (`snapshot_admission_tests.rs`, `tests/admission_allocations.rs`) |
| sizes | String 24, JsonValue 32, &str 16, Vec<u8> 24; leaf 16 + 11·56 = 632, +96 internal | `canonical.rs`:143-148 | `node_modules_layout_tests.rs`:1893-1896 |

Five of these are private functions of `snapshot_admission.rs`: `search`, `growth`, `growths`, `formatted` and
`descriptor_admission_cost`. C2b-1a makes them `pub(crate)` unchanged, which is a host-local, pin-only change. A
copy would be a second definition that the premise pin could not hold.

## 3. The generic schema-admission term ADMIT(E, x)

### 3.1 The whole admission

`SchemaHandle::admit_json(raw, budget)` (`P/crates/identity/src/schema_registry.rs`:716-726) calls
`Program::admit_json(entry, raw, budget)` (`P/crates/identity/src/schema.rs`:451-469). For the canonical encoding
`raw` of a value *x*, with *L* = |raw|:

**ADMIT(E, x) = MEMBERSHIP(|entry|) + PARSE(x, L) + WALK(x) + RESOLVE(entry, "") + EVAL(τ\_E root, x)**

- **MEMBERSHIP(ℓ)** (`:457`, `entries.contains`): k = 11·bitlen(population bound) comparisons, with bytes k·2(ℓ + 1).
  The population bound is `registry_entry_population_bound` = 1,879,078, so k = 231. This is C9's `membership`.
- **PARSE(x, L)** (`:460`, `parse_json` → `parse_with(raw, Unmetered)`, `canonical.rs`:98-131). It is the C4 meter's
  own prices over x's actual structure:
  - entry(L);
  - value() per value;
  - for each object, in encoding order, each key's string(|k|), search(i, |k|) and insert(i, |k|);
  - string(|s|) per string value (decoded bytes);
  - array(n) per array.

  This is C9's `parse` generalized from snapshot rows to any value. The unmetered parse is the same core, so the
  metered prices bound it (C4).
- **WALK(x)** (`:461-462`, `Meter::value`, `:29-50`): {0, N(x), B(x)}, where:
  - N is the number of values;
  - B is the bytes of every key and string, plus 16 per integer and 1 per literal.

  The integer and literal terms make one measure also bound an equality's read of one operand. B is at least C9's
  `walk` bytes.
- **RESOLVE(entry, "")** (`:463`; §3.4).
- **EVAL** (`:464`; §3.2–3.6).

### 3.2 EVAL and the over-approximation

EVAL(t, v) is defined recursively, exactly as `evaluate` (`schema.rs`:501-712) recurses, with two changes:

1. **Every `oneOf` rule is evaluated.** The source already does this (`:555-573`; only `anyOf` breaks). The `not`
   rule is evaluated too (`:574-578`).
2. **No early `return Ok(false)` is taken.** Each keyword's work is charged, and so is every child invocation the
   source *could* make on that value: `$ref` target, `oneOf` rules, `not`, `properties[k]` or `additionalProperties`
   per key, `items` per item.

*Claim.* For a value v and schema t, the source's actual invocations and operations are a sub-multiset of EVAL's.

*Proof sketch.*
- Which child invocation runs on which value is a function of t and v alone:
  - the key decides `properties[k]` against `additionalProperties`, and the latter is reached only when unmatched
    (`:701-703`);
  - the index decides `items`;
  - nothing else is consulted.
- The kind arm (`:591-710`) is chosen by the actual kind of v in both.
- Every source exit before the end of an invocation (`return Ok(false)`, `?` on `Err`) omits operations and never
  adds one.
- A loop that breaks early does fewer iterations than EVAL charges (`enum` at `:536-537`, `required` at `:667-668`).

So the charged work is at least the actual work, invocation by invocation, **provided every charged step has a
defined, non-negative cost on every value**. The steps that run after the source would already have stopped are
the artificial tail. **r2 (RF-2) makes every rule total.**
- **Each rule's inputs are the statistics of the value and of its direct children.** The census computes them for
  every node: kind, N, B (walk bytes), I (integers), L (canonical length), and for a string its decoded bytes n,
  parts S and scalars. A container also carries its length, and an object the (n, S) of a string `path` member.
- **Each rule is total over every kind.**
  - A keyword's kind arm is chosen by the value's kind.
  - A `required`, `properties` or order-field lookup on a non-object is priced as a search over 0 keys. The source
    exits there.
  - ORDER\_VERIFY's key is bounded by the item's walk bytes (§3.6). A missing or non-string field is a source exit,
    costed as its lookup.
  - ORDERED prices every arm of `ordered` (§4.2).
  - UNIQUE and ENC use the item's statistics whatever its kind.

So the tail has a defined finite cost. The price of a refusing record is at least its actual refusal work, by the
same sub-multiset argument. `evidence/VECTORS-r4.json` prices eleven ordinary malformed records (§7.1); each carries
the evaluator verdict F8 asserts. These vectors include the three REVIEW-r1 counterexamples:
- `tree = [null]`;
- a row `path` of 7;
- a graph node without `path`.

This makes the price total on the values C2b-1a can pass. It does not claim those malformed values can enter
through C2b-1a's typed inputs.

The keywords that never occur in any of the six entries are `allOf`, `anyOf`, `if`, `then`, `else`, `contains`,
`prefixItems`, `patternProperties` and `propertyNames` (§3.8). EVAL treats each of them as **outside the derivation**,
so the price refuses `PriceUnavailable` if one appears. The schema-table control F2 (§11) fails if the pinned
document adds one.

### 3.3 One invocation's own cost

For an object schema t with *m* = |t| keywords, the query bound for keyword lookups is 20 bytes (the longest
keyword, `additionalProperties`, as C9's QUERY). Write S = search(m, 20).

| step (schema.rs) | cost |
| --- | --- |
| :509-512 depth check and visit | {0, 1, 0} (a boolean schema stops here, :513-515) |
| the nine fixed lookups `$ref`, `const`, `enum`, `type`, `allOf`, `anyOf`, `oneOf`, `not`, `if` (:517, :523, :530, :544, :555-556, :574, :579) | 9·S |
| `$ref` (:517-522) | RESOLVE(ref, owner) + EVAL(target, v) |
| `const` c (:523-529) | WALK(v) + WALK(c) + EQ(v, c), EQ = {0, N(v)+N(c), B(v)+B(c)} |
| `enum` (:530-543) | per candidate c: WALK(v) + WALK(c) + EQ(v, c) |
| `type` (:544-554) | {0, 1, 16} per type name (each comparison ≤ 7 bytes per operand; C9) |
| `oneOf` (:555-573) | per rule {0, 1, 0} + EVAL(rule, v) |
| `not` (:574-578) | EVAL(rule, v) |
| integer (:592-594) | 2·S (`minimum`, `maximum`) |
| string (:595-607) | {0, 1, \|v\|} for `chars().count()`, 3·S (`minLength`, `maxLength`, `pattern`), and DISPATCH + MATCH when `pattern` is present (§3.5) |
| array (:608-659) | 6·S (`minItems`, `maxItems`, `prefixItems`, `contains`, `uniqueItems`, `x-opensip-order`); per item {0, 1, 0} + S (`o.get("items")` inside the loop, :615) + EVAL(items, item); UNIQUE when `uniqueItems` is true; ORDER when `x-opensip-order` is present (§3.6) |
| object (:660-708) | 5·S (`minProperties`, `maxProperties`, `required`, `properties`, `patternProperties`); per required key r: {0, 1, 0} + search(\|v\|, \|r\|); per data key k: {0, 1, 0} + S (`propertyNames`) + search(\|properties\|, \|k\|) when `properties` exists, then EVAL(properties[k], v[k]) when declared, otherwise S (`additionalProperties`, only on an unmatched key) + EVAL(additionalProperties, v[k]) |

Data-map searches use the actual key length rather than C9's 20, since the data keys (for example
`resolutionCompletenessImplied`, 29) can exceed 20.

These counts are C9's, generalized. C9 quotes "an integer: two; a string: three; an array: six, plus one per item;
an object: five, one per key, one more per unmatched key" (`M/c2b-m1/C9-DERIVATION-r1.md`:79-82).

**Allocations inside evaluation** come from four places only:
- RESOLVE's pointer-part key strings;
- UNIQUE's canonical keys and set nodes;
- ORDER's parsed annotation and its per-item tuple or canonical keys;
- and, outside this derivation, `propertyNames`'s key clone (`:678`).

`Ok(Some(value))` moves the parsed value; the meter allocates nothing.

### 3.4 RESOLVE(ref, owner) (`schema.rs`:267-298)

| step | cost |
| --- | --- |
| `split_once('#')` | {0, 1, \|ref\|} |
| `documents.get_key_value(id)` (`id` = the owner when empty) | search(52, \|id\|) |
| fragment `starts_with('/')`, `contains('%')` | {0, 2, 2·\|ref\|} (C9) |
| per pointer part: its decode loop, its key `String`'s pushes, its member search | {0, 1, \|part\|} + meter `string(\|part\|)` + search(members, \|part\|) |

For `#/$defs/Name`, the parts are `$defs` (the owner document's root keys: identity-v3 7, native-v2 10) and `Name`
(its `$defs`: identity-v3 54, native-v2 115). The documents count is 52 (`SOURCE_PINS`). This is C9's `resolve`, with
the native document's populations.

### 3.5 Pattern dispatch and matchers (`schema.rs`:237-265; `schema_patterns.rs`:265-305, :456-521)

**DISPATCH(owner, p)** has three parts:

1. **The owner equalities.** Four equalities, each reserving both complete operands: |owner| + 31, 49, 37, 34. This
   is C9's `dispatch`. It is conservative for the native owner, which matches on the second.
2. **The owner's selection.**
   - **identity-v3 (legacy, `matches`):** the `TABLE` find through the matched row i: {0, i + 1, Σ\_{j≤i}(|p| + |TABLE\_j|)}.
   - **native-v2 (`matches_native_owner`):**
     - the `FORMS.contains` scan through row f: {0, f + 1, Σ\_{j≤f}(|p| + |FORMS\_j|)};
     - the two `allows_empty` comparisons;
     - for a non-empty form, the dot-pattern and security comparisons, then the legacy `TABLE` find.
3. **The rows the six entries reach**, parsed from the pinned file (`evidence/schema-facts-r4.stdout`):

| pattern | owner | matcher | FORMS row | TABLE row | DISPATCH |
| --- | --- | --- | --- | --- | --- |
| `^[0-9a-f]{64}(?![\s\S])` | identity-v3 | Hex("", 64) | — | 22 | {0, 27, 2,247} |
| LogicalPath `^[^/\\\u0000]{1,255}(/…)*` | identity-v3 | Segments255 | — | 26 | {0, 31, 3,326} |
| `(^\|/)\.\.?(/\|$)` (LogicalPath's `not`) | identity-v3 | DotSegment | — | 1 | {0, 6, 336} |
| `^prj1-[0-9a-f]{64}` (snapshot only) | identity-v3 | Hex("prj1-", 64) | — | 50 | {0, 55, 4,164} |
| `^[0-9a-f]{64}(?![\s\S])` | native-v2 | Hex("", 64) | 11 | 22 | {0, 43, 3,588} |
| `^closure2:[0-9a-f]{64}` | native-v2 | Hex("closure2:", 64) | 18 | 36 | {0, 64, 5,461} |
| `^sha256:[0-9a-f]{64}` | native-v2 | Hex("sha256:", 64) | 24 | 65 | {0, 99, 7,697} |
| CanonicalPath `^(?!/)(?![\s\S]*(^\|/)\.\.?(/\|$))[^\u0000\\]+` | native-v2 | NegativePath (native form) | 2 | — | {0, 9, 848} |

The identity rows equal C9's `TableRow` pins (#22, #26, #1, #50). The native rows equal C2b-0's layout derivation:
"digest FORMS prefix12, …, inherited TABLE prefix23; path FORMS prefix3" (`P/crates/host/src/node_modules_layout.rs`:340-342).

**MATCH(kind, s)**, where n = |s| in bytes and S = the number of `/`-separated parts. No matcher allocates
(`schema_patterns.rs`:2).

| matcher | source | cost |
| --- | --- | --- |
| Segments255 | :277 | {0, 2 + 2S, 3n}: the exclusion scan, the split, a bounded scalar count per part |
| DotSegment | :315-337 | {0, 1 + S, n + 6S + 2} |
| NegativePath (native) | :497-503 | {0, 2 + S, 2n + 6S + 2}: emptiness, `starts_with`, `contains`, the split, ≤ 6 bytes per part test |
| Hex(prefix, 64) | :274, :309-311 | {0, 2, 2·\|prefix\| + 64} |

### 3.6 `uniqueItems` and `x-opensip-order`

- **UNIQUE(items)** (`schema.rs`:634-644): per item, WALK(item) + ENC(item) + btree\_insert(n, |C(item)|, 24), at the
  array's full population n. ENC is the item's `canonical_bytes`, with its allocations (§3.7). This is C9's
  `uniqueItems` term, generalized.
- **ORDER(ann, v)** (`schema.rs`:645-658) is WALK(v) + WALK(ann) + ORDER\_PARSE(ann) + ORDER\_VERIFY(ann, items).
  - **ORDER\_PARSE** (`descriptors.rs`:191-232):
    - a string annotation: 11 arm comparisons of at most 16 bytes, {0, 11, 11·2·17};
    - a named field order (`path`, `ruleId`, `waiverId`, `predicate`): owned(24·f) for its Vec and owned(|name|)
      per field String;
    - `{"by": [...]}`: the length check, search(1, 2) for `by`, owned(24·f), and per field btree\_insert(i, |f|, 8)
      for the seen set plus owned(|f|).
  - **ORDER\_VERIFY** (`descriptors.rs`:243-314):
    - `sequence`: {0, 1, 0}.
    - `utf8`: per item {0, 1, 0}, then one comparison with the previous key of B(prev) + B(cur) + 2 bytes.
    - Fields(f): per item the tuple Vec, which is owned(64) for f ≤ 4 (first push allocates 4 slots,
      SpecFromIterNested, as C9) and P1 beyond. Per field: search(k, |f|) + {0, 1, 0}, with k the item's key count
      (0 for a non-object, where the source exits at `:257-264`). Then the tuple comparison over
      (B(prev) + f) + (B(cur) + f) + 2 bytes.
    - **The key's bytes are bounded by the item's walk bytes plus one per field (r2, RF-2).** Each ordered field's
      string is among the item's strings, so Σ\_f(|item\_f| + 1) ≤ B(item) + f. The bound is defined for every item
      shape, including a missing or non-string field.
    - `canonical-set`/`canonical-order`: per item ENC(item) and the byte comparison.
    - numeric kinds: {0, 1, 16} per item.
  - **The annotations reached:**

    | entry | annotations |
    | --- | --- |
    | closure | `"path"` |
    | context | `"sequence"`, `"utf8"`, `{"by":["component"]}` |
    | universe | `"sequence"` |
    | graph | `"sequence"`, `{"by":["path"]}` |
    | layout | `{"by":["installPath"]}` |

### 3.7 The encoding, hash, identifier and clone primitives

**The split (r2, NBO-2).** Every price is a pair (allocations, passes), as C9's `AdmissionPrice`
(`snapshot_admission.rs`:115-125, :564-581):
- **the allocation side:** owned, growth and formatted; the meter's parse prices, held whole as C9 holds them
  (:571-576); `btree_insert`'s new nodes and their bytes; CLONE's owned parts;
- **the pass side:** C1 passes, `search`, `digest_cost` (as C9's `hash`), `btree_insert`'s 12h + 1 edges and its
  search and move bytes, and CLONE's copy pass.

F8 holds measured allocations and allocated bytes to the allocation side only. The ledger charges the sum.

| primitive | source | cost |
| --- | --- | --- |
| ENC(x), `canonical_bytes` | `canonical.rs`:477-562 | growth(L, 1) + I(x)·growth(20, 1) + {0, N(x), 2L}: the output Vec under P1 to its length, one decimal temporary per integer, one pass visiting each value and reading/writing each output byte (C9's `hash` encode) |
| HASH(d, x), `hash_canonical_value` | `digests.rs`:64-66 → `frame` :52-62 | {0, 1, \|d\|} + ENC(x) + growth(F, 1) + {0, 1, F + L} + digest\_cost(F), with F = 19 + \|d\| + 1 + 8 + L (C9 §6) |
| IDENT(prefix) | `descriptors.rs`:601, `digests.rs`:43-49 | owned(64) + formatted(\|prefix\| + 65) + {0, 32, 96} + {0, 1, 2(\|prefix\| + 65)} (C9's `identifier`, its prefix generalized) |
| CLONE(x), derived `JsonValue::clone` | — | each string owned(\|s\|); each non-empty array owned(32n); each non-empty map one leaf owned(632) when it holds ≤ 11 keys (the only shape such a map has), otherwise ≤ one node per key, each owned(728); each key owned(\|k\|); plus {0, N, B} |
| BLOB(d), `RetainedInputs::blob` | `closure.rs`:85-96 | search(\|blobs\|, 32) + digest\_cost(β(d)), with **β(d) the actual retained length** under digest d, obtained by the census's charged lookup (§8; LD-F-9). F11 requires β(d) = F for a frame and L for a record; the vectors' stores hold exactly that. |
| CANONICAL\_RECORD(x) | `closure.rs`:55-61 | PARSE(x, L) + ENC(x) + {0, 1, 2L} |

### 3.8 The evaluation tables

τ\_E is generated by `scripts/admission_model.py` (`tau_size`) from the registered document at the pin. Two of its
measures matter:
- **its invocations**: the size of the "every rule" expansion;
- **the multiplicity μ\_E**: the most invocations any one value receives (per key, each invocation contributes its
  own `properties[k]` or `additionalProperties`).

| entry | τ invocations | slots | μ | keyword map max | features |
| --- | --- | --- | --- | --- | --- |
| identity-v3 `/$defs/closure` | 17 | 14 | 3 | 6 | 2 `$ref`; `not`; `const`; `enum`; 1 `uniqueItems` |
| identity-v3 `/$defs/snapshot` | 18 | 13 | 3 | 6 | 4 `$ref`; `not`; `const`; 1 `uniqueItems` |
| native-v2 `/$defs/TypeScriptNativeContextV2` | 107 | 73 | 4 | 7 | 12 `$ref`; 5 `oneOf`; 8 `const`; 6 `enum`; 9 `uniqueItems` |
| native-v2 `/$defs/TypeScriptUniverseV2ResolvedInputs` | 38 | 33 | 4 | 6 | 1 `$ref`; 2 `oneOf`; 13 `const`; 4 `enum`; 2 `uniqueItems` |
| native-v2 `/$defs/TypeScriptConfigGraphV1` | 18 | 12 | 4 | 6 | 2 `$ref`; 1 `oneOf`; 1 `uniqueItems` |
| native-v2 `/$defs/ResolvedNodeModulesLayoutV1` | 14 | 11 | 2 | 6 | 2 `$ref`; 1 `uniqueItems` |

Every `$ref` reached is local to its own document: no external document is evaluated. None of the keywords outside
the derivation (§3.2) occurs.

## 4. The call-path wrappers

### 4.1 Lookups

**LOOKUP(id, sel)** is `RegisteredSchemas::schema` (`schema_registry.rs`:674-694):
- the codec guard {0, 1, 2(|id| + 1)};
- the `SOURCE_PINS` position scan {0, 52, 52·2(|id| + 1)};
- `format!("{id}#{sel}")`: formatted(e) + {0, 1, e}, with e = |id| + 1 + |sel|;
- MEMBERSHIP(e) for `has_entry`;
- `selector.to_string()`: owned(|sel|) + {0, 1, |sel|}.

This is C9's `lookup` minus `admit_json`'s membership, which ADMIT carries.

**ALIAS(document)** is `current_record_schema`'s alias find (`schema_registry.rs`:601-612): the 15 rows of the table,
each equality reserving both operands. Its cost is {0, 15, Σ(|document| + |alias\_j|)}.

### 4.2 FROM\_JSON(domain, x)

`IdentityCandidate::from_json` (`P/crates/identity/src/descriptors.rs`:586-607):

FROM\_JSON = formatted(|sel|) + {0, 1, |sel|} + LOOKUP(identity-v3, sel) + ADMIT(E, x) + ORDERED(x, "") + HASH(domain, x) + IDENT(prefix)

Here sel = `/$defs/<domain>`, and the prefixes are `closure2` and `snapshot2`.

**ORDERED** (`descriptors.rs`:654-711) is {0, 1, 0} per call, plus:
- **per object key:** the `path`/`logicalPath` tests {0, 2, 2|k| + 15}. When the key is `path` or `logicalPath` and
  its value is a string, PATHCHECK(s) = {0, 1 + S, 2|s| + 12S} (`path`, :621-623; C9's `paths`). Then the recursion.
- **per array:** the arm match {0, 11, 11·2·17}.
  - For `tree`, `sourceInventory` and `blobs`: per element search(|item|, 4) + {0, 1, 0} + PATHCHECK(path). Then
    `named_order("path")`: owned(4) for the temporary `V::String`, + ORDER\_PARSE + ORDER\_VERIFY.
  - For any other name, `canonical-set`: owned(13) + ORDER\_PARSE + ORDER\_VERIFY with ENC per item.
  - **r2 (RF-2) prices every arm, because a malformed closure can carry any key.** These arms are reached only after
    the admission refuses, which the over-approximation ignores:
    - `allowedScopes` (`sequence`);
    - `requires` (`numeric`);
    - `owner-source-set`: the temporary `{"by": ["ownerKey"]}` map, which is owned(632) + owned(2) + owned(32) +
      owned(8), then ORDER\_PARSE;
    - `stages` (`ordinal`): verified twice (:685, :703), plus per stage two field searches and a pass over its
      values for the `requires` loop, {0, N, 32N};
    - `predicateProofs` (`predicate`);
    - `ruleResults` (`ruleId`).
  - The recursion into each element follows.

### 4.3 OBJECT(key, domain, x)

`RetainedInputs::object` (`closure.rs`:125-162) → `candidate` (:97-124):

OBJECT = search(|objects|, |key|) + owned(|key|) + ENC(x) + FROM\_JSON(domain, x) + {0, 1, 2|key|} + {0, 9, Σ(|owner\_j| + |domain|)}

- owned(|key|) (r2) is the refusal path's `Error::MissingObject(key.into())` (:103-106): the one allocating error
  on these paths. Every other error here is `Copy` or `&'static`.

- The second-to-last term is the identifier comparison.
- The last term is the scan of the 9 `CANDIDATE_CLOSURE_ROLES` rows. No row names `closure` or `snapshot`, so no
  nested candidate runs.
- The capture is `None`, because C2b-1a builds `RetainedInputs::new`.

### 4.4 FRAME(domain, set, x)

`RetainedInputs::frame_candidate` (`closure.rs`:1444-1495), with F = 19 + |d| + 1 + 8 + L:

| line | operation | cost |
| --- | --- | --- |
| :1450 | the blob fetch and rehash | BLOB(d), with β(d) = F (F11) |
| :1451-1454 | the frame prefix | {0, 1, 38} |
| :1455-1459 | the domain cut | {0, 1, \|d\| + 1} |
| :1460-1465 | UTF-8 and ASCII checks | {0, 2, 2\|d\|} |
| :1466-1468 | the identity document | search(52, 34) |
| :1469 | `x-opensip-digest-domains`, `domainSets` | search(7, 24) + search(\|dd\|, 10) |
| :1470-1472 | the set and the domain row | search(3, \|set\|) + search(\|set rows\|, \|d\|) |
| :1473 | **the registry row's deep clone** | CLONE(row) |
| :1474 | `parse_hash_preimage` (`digests.rs` `unframe`, :88-106) | UNFRAME = {0, 1, \|d\|} + {0, 1, 38} + {0, 1, 2(\|d\| + 1)} + {0, 1, 16} + PARSE(x, L) + ENC(x) + {0, 1, 2L} |
| :1475 | `canonical_bytes` | ENC(x) |
| :1476-1478 | `document`, `selector` | 2·search(\|row\|, 8) |
| :1479-1481 | the schema handle | ALIAS(`native/native-evidence.schemas.v2.json`) + LOOKUP(native-v2, sel) |
| :1482 | the admission | ADMIT(E, x) |
| :1483-1485 | the identity rehash and comparison | HASH(d, x) + {0, 1, 64} |
| :1488-1494 | `domain.into()` | owned(\|d\|) |

So one FRAME parses the descriptor twice, encodes it three times and hashes F bytes twice.

### 4.5 RECORD(selector, x)

`inspect_current_record` (`closure.rs`:621-655) → `Walker::foreign_record` (:1107-1144), for a document that does not
start with `foundation/`:

| line | operation | cost |
| --- | --- | --- |
| :1114, and `self.blob`'s own (:733) | two spends | {0, 2, 0} |
| :1115 | the key's two strings | owned(\|document\|) + owned(\|selector\|) |
| :1119 | `self.blob` (its fetch and `checked.blobs.insert`, :732-737) | BLOB(d), with β(d) = L (F11), + btree\_insert(0, 32, 32) |
| :1120 | `self.inputs.blob` again | BLOB(d) |
| :1121 | `canonical_record` | CANONICAL\_RECORD(x) |
| :1122-1126 | the alias and lookup | ALIAS + LOOKUP(native-v2, pointer) |
| :1128 | the admission | ADMIT(E, x) |
| :1129 | `foreign.insert` | btree\_insert(0, 32 + \|document\| + \|selector\|, 80) |

No walk follows (:1130-1142). Both callers re-read the record after the inspection (W-REC):
- retention: `self.inputs.blob(d).and_then(canonical_record)` (`native_retention.rs`:316-320);
- the universe owner's `nested_record`: `inputs.blob` before the inspection and `canonical_record` after it
  (`native_universe.rs`:320-339).

**W-REC = BLOB(d) + CANONICAL\_RECORD(x)**, with β(d) = L. One retained nested-record admission therefore rehashes the record four
times (with retention's own `self.blob` at :303) and parses it three times.

## 5. The per-schema terms

All formulas are §3–4 with the entry substituted. Each term's vector values are in §7 and `evidence/VECTORS-r4.json`.

### 5.1 T-SNAPSHOT: C9 as published, where its premises apply

**T-SNAPSHOT = search(|objects|, 74) + owned(74) + ENC(snapshot) + C9(shape) + {0, 1, 148} + {0, 9, Σ(|owner\_j| + 8)}**

- **Premises.** C9 prices `IdentityCandidate::from_json(registry, Snapshot, raw, ..)`, where raw is the canonical
  encoding of a descriptor of the snapshot's fixed structure (`snapshot_admission.rs`:101-113;
  `M/c2b-m1/C9-DERIVATION-r1.md`:28-39):
  - six top keys;
  - rows of `{bytes, path, sha256}`;
  - `projectId` and three digests.
- **Here.** `RetainedInputs::object` passes `canonical_bytes(&input.descriptor)` (`closure.rs`:108). C2b-1a supplies
  the descriptor of its `SealedSnapshot` (`snapshot_seal.rs`:167-176). Those are the same bytes C9 priced, so its
  premises apply.
- **The shape** (`top`, `rows`, `paths`, `segments`, `encoded_rows`, `length`) is computed by C2b-1a's census from that
  descriptor. A descriptor that is not of this structure refuses `PriceUnavailable` (control F7).
- **The new wrapper terms** are the object-map search, the refusal-path key string owned(74) for
  `MissingObject(key.into())` of the 74-byte `snapshot2:<hex>` key (`closure.rs`:103-106; r3, NBO-2, as OBJECT
  carries it in §4.3), the re-encode, the identifier comparison and the role-row scan. C9 does not include them,
  because the seal calls `from_json` directly.

### 5.2 T-CLOSURE: identity-v3 `$defs/closure`

**T-CLOSURE = OBJECT(`closure2:<hex>`, closure, x)**

FROM\_JSON over `/$defs/closure` (14 bytes), domain `closure`, prefix `closure2`. The schema and its operations:
- **The top object.** 7 required keys and 7 properties, `additionalProperties: false`:
  - `schemaVersion` `const` 2;
  - `kind` `type` + an 8-entry `enum`;
  - `manifestDigest` Hex64 (legacy row 22);
  - `semanticVersion` and `platform`, length-bounded strings;
  - `protocolMajor`, an integer in [0, u64::MAX];
  - `tree`.
- **`tree`.** `maxItems` 100,000; `items` `$ref #/$defs/Blob`; `uniqueItems`; `x-opensip-order` `path`.
- **Per row**, the same Blob and LogicalPath schemas as the snapshot's inventory: Segments255, its `not` DotSegment,
  Hex64. The snapshot's `sourceInventory` reference and inventory-schema lookups are absent.
- **`ordered`.** The `tree` arm: the per-row path checks, `named_order("path")` and verify.
- **The hash domain** is `closure`; F = 19 + 7 + 1 + 8 + L.

**Long and escaped paths.** The evaluation and matchers read decoded bytes. Parse entry, encode, hash and the
`uniqueItems` keys read canonical bytes. An escaped scalar (a control character below U+0020, `"`, a tab) decodes to
1 byte and encodes to 2 or 6. The term uses both lengths exactly, from the value:
- string(|decoded|) in PARSE;
- |C(row)| in UNIQUE;
- L in HASH.

The vectors include:
- 200 rows of **distinct, strictly increasing** 4,096-scalar paths (r2, NBO-1): a 3-digit-led first segment of 255
  scalars, 14 more of 255, then one of 254 and one of 1. These rows admit. r1's construction, with 26 distinct
  paths, refuses at `x-opensip-order` and is kept as a named refusal vector (§7.1);
- 300 rows mixing a control character, `"`, a 2-, a 3- and a 4-byte scalar, a tab and U+001F;
- 2,000 short rows.

The closure descriptor is bounded by the canonical 4 MiB limit (`canonical.rs`:5, :489-491): a larger re-encode
refuses `ByteLimit` before `from_json`. That bound is what limits the term's size.

### 5.3 T-FRAME-CTX and T-FRAME-UNI: native frames

- **T-FRAME-CTX = FRAME(`native.context.typescript.v2`, `native-context`, context)**, against
  `/$defs/TypeScriptNativeContextV2`. Its evaluation covers:
  - the closed top object (9 keys);
  - `toolchain`: `standardLibraryComponentDigests` with `uniqueItems` and `by: component`; `libSelection` `utf8`;
  - `toolClosure`: ClosureId2, legacy row 36;
  - `configProjection` and `honoredOptions` (18 keys): `types` `oneOf` [array, null], `baseUrl` `oneOf`, `paths`
    rows, `rootDirs`, `customConditions`, `jsx` `oneOf`;
  - `nodeModulesLayoutDigest` `oneOf` [DigestHex, null];
  - `lockfileIdentity` `oneOf` [object, null].

  Its registry row clone is the context row (`identity-v3.schema.json` `domainSets.native-context`).
- **T-FRAME-UNI = FRAME(`native.semantic-universe.typescript.v2`, `native-semantic-universe`, universe)**, against
  `/$defs/TypeScriptUniverseV2ResolvedInputs`. Its evaluation covers:
  - 18 required keys;
  - 13 `const`s;
  - `programRootFiles` and `jsRootFiles`: each item a CanonicalPath (native form 2), up to 100,000, with
    `uniqueItems` and `sequence`;
  - `nativeContextId` sha256-text (row 65);
  - `tsconfigGraphHash` Hex64.

  Its registry row clone is the universe row, which carries the large `languageVersionBinding` text. That is why
  CLONE is priced over the row's actual values rather than as a constant.

### 5.4 T-REC-GRAPH and T-REC-LAYOUT: nested records

- **T-REC-GRAPH = RECORD(`#/$defs/TypeScriptConfigGraphV1`, graph).** The evaluation covers:
  - `entryConfigPath` `oneOf` [CanonicalPath, null];
  - `nodes` (≤ 1,024): `uniqueItems`, `by: path`, and per node a 4-key object with an `extendsResolved` sequence of
    CanonicalPaths.
- **T-REC-LAYOUT = RECORD(`#/$defs/ResolvedNodeModulesLayoutV1`, layout).** The evaluation covers `entries`
  (≤ 100,000): `uniqueItems`, `by: installPath`, and per row a 5-key object with two CanonicalPaths, two
  length-bounded strings and a DigestHex.

C2b-0's layout admission price (`node_modules_layout.rs`:292-520) prices the same `admit_json` over
`push_record`'s bytes. It is not reused here. Its premise is C2b-0's own encoder, and RECORD's inspection includes
two blob fetches, a canonical record and the alias, which that price does not cover. It serves as the second
cross-check (§7.2).

## 6. The admission composition of the two calls

Mint calls `inspect_native_retention(ctx, Context, snapshot2, ·)`. Bind calls
`inspect_native_retention(u, SemanticUniverse, snapshot2, ·)` with the universe bound. Counted from
`P/crates/evaluator/src/native_retention.rs`, `native_context.rs` and `native_universe.rs`.

**This table is the admission-only funding column of the companion's occurrence matrix** (`SLOT-DERIVATION-r3.md`
§4; r3, RF-6). Every row is additive: it names source sites that no companion term prices (the companion's ledger
marks each of them "funding"), and its two columns are the multiplicities of those sites in one call. The notes
after the table are non-additive. A whole call is the companion's §4 column sum, which adds this column once (§12).

| term | mint | bind | source of each occurrence |
| --- | --- | --- | --- |
| T-SNAPSHOT | 1 | 2 | retention `:93-99`; universe owner `native_universe.rs`:179-181 |
| T-FRAME-CTX | 2 | 4 | retention `frame` `:276-279` (bind: via `contextField`, `:359-369`); context owner `native_context.rs`:373-375, run from retention `:372-379`; bind adds the universe owner's `frame_candidate` (`native_universe.rs`:170-172) and its context owner run (`:176-177`) |
| T-CLOSURE, per closure | 2 | 3 | retention `closure` `:249-252` (once per walk; its `closures` set dedupes only the blob loop, `:256-259`); context owner `closure` (`native_context.rs`:195), once per owner run |
| CLONE(closure descriptor), per closure (T-OWNER-CTX) | 1 | 2 | `native_context.rs`:222, per owner run |
| T-FRAME-UNI | 0 | 2 | retention `frame` `:276-279`; universe owner `native_universe.rs`:151-153 |
| T-REC-GRAPH + W-REC | 0 | 2 | retention `nestedRecords` `:288-322`; universe owner `nested_record(.., "configGraph")` `:190`, `:297-340` |
| T-REC-LAYOUT + W-REC (when the context names a layout) | 1 | 2 | retention, via the context frame's `nestedRecords` `:288-322`; universe owner `nested_record(.., "nodeModulesLayout")` `:238` |

Notes (non-additive):
- **Not admissions.** Retention's `self.blob(d)` before each nested record (`:303`), the member and manifest blob
  fetches (`:260-266`) and the layout's `blobJoins` (`:321`, per entry) are blob fetches. They stay in the companion's
  T-WALK rows, priced BLOB(d) each at the actual retained length (LD-F-9; companion RF-3).
- **Rows absent from the TypeScript registry.** The universe row has no `snapshotJoins`, `blobJoins` or
  `closureJoins`. Both rows' `nestedIdentities` are empty (`identity-v3.schema.json` `domainSets`), so those loops
  admit nothing.
- **A null layout** (`nodeModulesLayoutDigest` null) skips its RECORD in retention (`:296-301`) and in
  `nested_record` (`native_universe.rs`:316-318).
- **Other domains** (Rust or syntax contexts and universes) are unreachable through C2b-1a's typed inputs. The price
  refuses them as outside the derivation.

## 7. Vectors and cross-checks

### 7.1 The terms on sample, stress and malformed records

The values come from `scripts/vectors.py` and are written to `evidence/VECTORS-r4.json`, sha256
`fd64aaa10f7287b8b37385c70ac022c3a4e663d332ceecbbb3a6df6b6555cdf7`. That file carries:
- every record and its expected verdict;
- every term's allocations, passes and total;
- the census's counted and charged work, its element count, its scans, its key and store comparisons and the
  retained length it looked up;
- both compositions and the census charge summed over the priced records;
- the depth-gate, retained-length-gate and lookup-control records and the mutation self-tests.

F5 holds the Rust price to it; F8 asserts each verdict. The `census` column is {edges; bytes}, counted ≤ charged, held
per element and in total (§8); `comparisons` are the three-way key comparisons executed (slot + store). **Every
allocation side, pass side and total below equals r2's** (`scripts/compare_r2.py`, `evidence/compare-r2-r4.stdout`);
only the census columns changed since r2.

| scenario (admits) | term | N | L | census elements | comparisons | census counted ≤ charged | allocations | passes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| typical | T-CLOSURE toolchain, 161 rows | 652 | 20,318 | 1,304 | 822 + 0 | 7,662; 40,092 ≤ 8,478; 51,484 | 14,704; 35,128; 4,992,971 | 1; 126,900; 9,466,632 |
| typical | T-CLOSURE stdlib, 91 rows | 372 | 11,661 | 744 | 472 + 0 | 4,372; 23,058 ≤ 4,838; 29,690 | 8,295; 20,130; 2,812,401 | 1; 70,728; 5,104,371 |
| typical | T-FRAME-CTX | 337 | 12,033 | 675 | 420 + 7 | 3,803; 25,804 ≤ 4,486; 43,366 | 10,234; 29,232; 3,952,309 | 2; 71,121; 5,480,277 |
| typical | T-FRAME-UNI (50 roots) | 69 | 2,039 | 139 | 72 + 8 | 607; 4,348 ≤ 842; 13,734 | 2,031; 4,990; 888,459 | 2; 11,164; 786,221 |
| typical | T-REC-GRAPH (2 nodes) | 15 | 408 | 31 | 23 + 2 | 167; 994 ≤ 291; 8,064 | 402; 1,468; 166,883 | 2; 3,283; 238,893 |
| typical | T-REC-LAYOUT (120 rows) | 723 | 28,111 | 1,447 | 1,332 + 9 | 8,442; 66,654 ≤ 9,855; 114,706 | 22,892; 91,900; 10,880,064 | 2; 126,652; 11,033,879 |
| closure-long-paths | T-CLOSURE, 200 distinct 4,096-scalar paths | 808 | 839,600 | 1,616 | 1,017 + 0 | 9,495; 1,678,500 ≤ 10,506; 1,692,544 | 21,016; 46,276; 45,423,405 | 1; 171,295; 195,050,443 |
| closure-escaped-paths | T-CLOSURE, 300 escaped rows | 1,208 | 40,100 | 2,416 | 1,517 + 0 | 14,195; 71,900 ≤ 15,706; 92,744 | 27,805; 65,165; 9,514,245 | 1; 237,395; 19,070,547 |
| closure-2000-rows | T-CLOSURE, 2,000 rows | 8,008 | 236,200 | 16,016 | 10,017 + 0 | 94,095; 464,500 ≤ 104,106; 600,944 | 186,213; 428,673; 63,360,669 | 1; 1,623,295; 132,119,559 |
| large-universe | T-FRAME-UNI (20,000 roots) | 20,019 | 580,589 | 40,039 | 73 + 9 | 140,258; 1,041,752 ≤ 180,392; 1,051,134 | 700,784; 404,043; 237,701,707 | 2; 5,462,914; 440,000,621 |
| large-universe | T-REC-GRAPH (500 nodes) | 3,003 | 91,044 | 6,007 | 4,013 + 8 | 31,049; 198,214 ≤ 37,641; 320,808 | 81,114; 279,374; 32,539,911 | 2; 571,669; 46,456,199 |
| large-universe | T-REC-LAYOUT (5,000 rows) | 30,003 | 1,170,031 | 60,007 | 55,011 + 8 | 350,041; 2,770,168 ≤ 405,135; 4,506,706 | 980,110; 3,820,238; 467,852,000 | 2; 5,591,132; 624,342,039 |

The composed admissions (totals), excluding T-SNAPSHOT, and the census charge summed over the priced records (each
record once, §8):

| scenario | mint | bind | census charged, Σ records {edges; bytes} |
| --- | --- | --- | --- |
| typical | 99,589; 971,694; 91,185,491 | 181,359; 1,733,938; 164,328,123 | 28,790; 261,044 |
| closure-2000-rows | 424,776; 4,526,111; 431,497,156 | 660,224; 6,952,832; 663,930,828 | 115,508; 711,504 |
| large-universe | 1,408,179; 11,970,124; 1,372,792,979 | 4,414,271; 37,390,950; 4,266,425,983 | 640,970; 6,003,188 |

T-SNAPSHOT adds C9 at the snapshot's shape, plus its wrapper (§5.1), once at mint and twice at bind.

**Malformed records (r2, RF-2).** Each is priced, with census counted ≤ charged. Each verdict is by construction
from the cited lines; none was executed here, and F8 executes each one.

| record | entry | census counted ≤ charged | total | expected verdict |
| --- | --- | --- | --- | --- |
| closure tree [null] | closure | 103; 500 ≤ 115; 944 | 192; 2,151; 164,993 | refuse: items type (schema.rs:544-553, :613-620) |
| closure row path = 7 | closure | 1,034; 5,672 ≤ 1,145; 7,476 | 1,956; 21,092; 1,732,407 | refuse: Blob path type (schema.rs:544-553) |
| closure duplicate rows | closure | 189; 900 ≤ 210; 1,480 | 338; 3,748; 279,652 | refuse: uniqueItems (schema.rs:634-644) |
| closure 200 long paths, 26 distinct (r1 vector) | closure | 9,495; 1,678,500 ≤ 10,506; 1,692,544 | 21,017; 217,571; 240,325,648 | refuse: x-opensip-order NonIncreasing (descriptors.rs:301-308) |
| closure extra key | closure | 1,069; 5,716 ≤ 1,185; 7,576 | 1,978; 21,411; 1,756,753 | refuse: additionalProperties false (schema.rs:701-704) |
| closure is an array | closure | 588; 4,708 ≤ 678; 5,584 | 1,301; 6,185; 670,491 | refuse: type object (schema.rs:544-553) |
| graph node without path | TypeScriptConfigGraphV1 | 275; 1,642 ≤ 326; 2,682 | 682; 7,617; 638,339 | refuse: required (schema.rs:664-669) |
| graph node kind outside enum | TypeScriptConfigGraphV1 | 288; 1,716 ≤ 341; 2,784 | 717; 8,028; 669,879 | refuse: enum (schema.rs:530-543) |
| layout installPath null | ResolvedNodeModulesLayoutV1 | 1,431; 11,128 ≤ 1,654; 18,134 | 3,836; 37,024; 3,528,125 | refuse: CanonicalPath type (schema.rs:544-553) |
| universe root with dot segment | TypeScriptUniverseV2ResolvedInputs | 255; 1,690 ≤ 301; 4,624 | 738; 7,011; 734,882 | refuse: CanonicalPath pattern (schema_patterns.rs:497-503) |
| context libSelection not an array | TypeScriptNativeContextV2 | 3,773; 25,568 ≤ 4,358; 36,674 | 10,188; 99,925; 9,401,925 | refuse: type array (schema.rs:544-553) |

**The depth gate (r3, NBO-1; F10).** The gate is the encoder's (`canonical.rs`:536): a container at container depth
32 refuses, whatever it holds; 32 nested containers are priced, and so is a scalar inside the 32nd.

| record | result | detail |
| --- | --- | --- |
| 32 nested arrays, innermost [] | price | 32 nodes; census 105; 0 ≤ 138; 0 |
| 33 nested arrays, innermost [] | PriceUnavailable | refused at the 33rd container's dispatch |
| 32 nested arrays, innermost {} | price | 32 nodes; census 105; 0 ≤ 138; 0 |
| 33 nested arrays, innermost {} | PriceUnavailable | refused at the 33rd container's dispatch |
| 32 nested arrays around a scalar | price | 33 nodes; census 108; 0 ≤ 142; 0 |
| 33 nested arrays around a scalar | PriceUnavailable | refused at the 33rd container's dispatch |

**The lookup controls (r4, REVIEW-r3 RF-1).** Every static key is wrapped in a byte string that counts relational
operations applied to it (the reviewer's observation method); the search must run none (all comparisons are the
counted byte reads of `compare_keys`), execute ≤ bitlen(K) comparisons and read ≤ the member charge's lookup
allowance 2(bitlen(K) + 1)(|k| + 1) bytes. The store is checked against its charge 2k·33. The last row is r3's
defect as the `two-sided` mutation.

| slot | K | key | comparisons ≤ bitlen(K) | bytes ≤ allowance | observed relational ops | result |
| --- | --- | --- | --- | --- | --- | --- |
| context root | 9 | `!` | 4 ≤ 4 | 8 ≤ 20 | 0 | OK |
| context root | 9 | `configProjection` | 4 ≤ 4 | 40 ≤ 170 | 0 | OK |
| context root | 9 | `toolchain` | 3 ≤ 4 | 32 ≤ 100 | 0 | OK |
| context root | 9 | `~` | 3 ≤ 4 | 6 ≤ 20 | 0 | OK |
| context root | 9 | `nodeModulesLayoutDigest0` | 4 ≤ 4 | 54 ≤ 250 | 0 | OK |
| honoredOptions | 18 | `!` | 5 ≤ 5 | 10 ≤ 24 | 0 | OK |
| honoredOptions | 18 | `allowJs` | 5 ≤ 5 | 34 ≤ 96 | 0 | OK |
| honoredOptions | 18 | `types` | 4 ≤ 5 | 20 ≤ 72 | 0 | OK |
| honoredOptions | 18 | `~` | 4 ≤ 5 | 8 ≤ 24 | 0 | OK |
| honoredOptions | 18 | `moduleResolution0` | 5 ≤ 5 | 42 ≤ 216 | 0 | OK |
| store | 400 | `a present digest` | 2 ≤ 9 | 68 ≤ 6,534 | — | OK |
| store | 400 | `below every digest` | 9 ≤ 9 | 18 ≤ 6,534 | — | OK |
| store | 400 | `above every digest` | 8 ≤ 9 | 18 ≤ 6,534 | — | OK |
| context root | 9 | `! (two-sided mutation)` | 4 ≤ 4 | 16 ≤ 20 | 8 | caught: observed relational operations exceed the counted comparisons |

**The retained-length gate (r3; F11).** The census looks β(d) up in the scenario's store (a charged, counted search,
the digest supplied from outside the boundary) and requires the value's own encoding length.

| record | result | detail |
| --- | --- | --- |
| graph record retained at 1 MiB | PriceUnavailable | retained length 1048576 is not the value's own encoding length 408 (F11) |
| universe frame retained one byte short | PriceUnavailable | retained length 2104 is not the value's own encoding length 2105 (F11) |
| graph record absent from the store | price | the full term; the fetch refuses MissingBlob after its search |

**The census mutations** (each must be caught):

| mutation | result |
| --- | --- |
| `unique-extra`: an unpriced extra traversal per UNIQUE item | caught: (('item', 8), (0, 7, 0), (0, 5, 0)) |
| `linear-lookup`: the declared-key lookup as a linear scan | caught: (('key', 12), (0, 14, 26), (0, 13, 54)) |
| `scan-first`: a string scanned before its charge (r2's defect) | caught by the per-element check: (('item', 4), (0, 4, 52), (0, 5, 0)); caught by the exhaustion probe: a scan began before the refused element (scans 100 -> 101) |
| `two-sided`: two relational operations per search iteration, one counted (r3's defect) | caught by the observer: 8 observed relational operations against 4 counted comparisons (table above) |

The caught tuples are (element, counted, charged): the first element whose counted work exceeded its charge.

**The exhaustion control** (`scripts/exhaustion.py`, `evidence/exhaustion-r4.stdout`, `.json`): 46 probes over
toolchain closure (1,304 elements, 326 strings, 490 keys, 822 key comparisons), context frame (675 elements, 212 strings, 233 keys, 420 key comparisons), universe frame (139 elements, 56 strings, 18 keys, 72 key comparisons), graph record (31 elements, 8 strings, 11 keys, 23 key comparisons), layout record (1,447 elements, 600 strings, 602 keys, 1,332 key comparisons). Every probe refused at exactly the chosen element, with no scan and no visit of it begun, and the
retained-lookup probes refused before any store comparison; the whole budget completes each census. The chosen
elements are the first element (budget zero), the 2nd, 40th and last string node, the 2nd, 30th and last member key,
the last item, the last element and the retained-length lookup of each record.

**Disclosed magnitude.** This is unchanged from r1. A closure near the 4 MiB descriptor bound (≈ 38,000 rows) costs
about 19 times the 2,000-row closure term per admission, and bind admits each closure three times. This derivation
claims no fit.

### 7.2 Cross-checks (consistency, not proof)

- **C9.** `scripts/c9_crosscheck.py`, run on r4, still reproduces C9's four published vectors exactly. On the six
  snapshot descriptors, whose 200 long paths are now distinct, generic/C9 is objects 0.977–1.0, edges 1.003–1.004 and
  bytes 0.992–1.0 (`evidence/c9-crosscheck-r4.stdout`). The explanations are r1's.
- **C2b-0's layout price.** Generic/C2b-0 is objects 1.41–1.51, edges 0.87–0.96 and bytes 0.96–1.08
  (`evidence/layout-crosscheck-r4.stdout`). The explanations are r1's.
- **r1 against r2** (kept): `scripts/r2/compare_r1.py` runs r1's recursive model (`scripts/r1/`) and r2's census on
  every admitting scenario's six terms; r2 ≥ r1 componentwise on all 35 (`evidence/r2/compare-r1-r2.stdout`). The
  excess comes from the bound changes only: ORDER's key bound, OBJECT's refusal string and the registry row's clone
  pass.
- **r2 against r3 and r4.** `scripts/compare_r2.py` runs r2's census (`scripts/r2/`) and the current one on the same
  records. Every term's allocation side, pass side and total are **equal** on all 35 (`evidence/compare-r2-r4.stdout`;
  r3's run is `evidence/r3/compare-r2-r3.stdout`). r3 and r4 moved the charges and the counting, not the prices:
  these are two implementations of one derivation agreeing exactly.
- **Every other r2 output is reproduced byte for byte** by the r4 model: `c9-crosscheck`, `layout-crosscheck`,
  `schema-facts`, `tables` and `case-table-premise` (`evidence/*-r4.*` against `evidence/r3/*-r3.*` and
  `evidence/r2/*-r2.*`).

## 8. Funding the price pass (r2, REVIEW-r1 RF-1; r3, REVIEW-r2 RF-1; M1a C1)

**The measured boundary (LD-F-8).** The price pass is the census below and nothing else. What lies outside it is
built before the census and is never counted; what lies inside is charged before it runs and counted where it runs.
The reference (`scripts/admission_model.py`) is organized by that boundary, and the Rust census mirrors it.

**Outside the boundary** (built before the census; not census work):
- **The accounted value representation.** The census reads the value through Rust's `Value`
  (`canonical.rs`:143-148): `String::len`, `Vec::len` and `BTreeMap::len` are O(1), and an object's members iterate
  in UTF-8 byte order (`:549-550`: "Rust String ordering is lexical UTF-8 byte ordering"). C2b-1a holds every priced
  value in that form before pricing (LD-F-3): it built the context, universe, graph and layout records, and it holds
  the admitted closure descriptors and the sealed snapshot descriptor. The reference's `AV` is exactly that
  representation: a string's byte length, a container's length, and an object's members sorted by key bytes with
  each key's byte length. Building `AV` stands in for a value C2b-1a already has; the census only reads it.
- **The static price table** (F2). One `Slot` per schema position, holding: its invocations' static entries (`Inv`:
  the keyword count m and query search S, the nine fixed lookups, RESOLVE of its `$ref`, DISPATCH of its pattern and
  the matcher kind, the literal statistics of its `const` and `enum`, ORDER\_PARSE of its annotation, its required
  keys' byte lengths, its `properties` population, `additionalProperties` and `uniqueItems`); its **sorted
  declared-key list**; for every declared key and for an undeclared key, the child slot and the per-invocation
  member table (which invocations declare the key); and its items slot. The table is prebuilt to the census's
  maximum depth from the pinned documents. The `ordered` arm table (per member name) and ROW\_CLONE are static too.
- **C2b-1a's retained blob map**: digest → the actual retained length β(d) (LD-F-9).

**Inside the boundary** (`census`, `scan`, `slot_lookup`, `Store.lookup`):
- each element is **charged before its work**, from sizes available in O(1) at that moment (the table below); a
  budget that the charge would exceed refuses the element before any of its work (`Exhausted`);
- a string value is scanned **once, after its charge**; the scan is one counted element and counts **per scalar
  inside its loop** (each scalar's bytes, read once to decode and once to classify the escape class and the `/`
  separator), so there is no second pass and no `count('/')`;
- a member key is scanned once, after its charge, then looked up by an **explicit binary search** over the slot's
  sorted declared keys. **Each iteration is one three-way byte comparison** (`compare_keys`; r4, REVIEW-r3 RF-1), as
  `Ord::cmp` on `[u8]` and a Rust `binary_search_by(|k| k.as_bytes().cmp(key))` iteration execute it: both operands
  are read up to the first differing byte, or to the shorter length plus the length tie-break, and the iteration is
  counted as one comparison with exactly the bytes it read (≤ 2(min(|a|, |b|) + 1)). No relational operator on key
  strings runs inside the boundary; the observer control (`observe_keys`, every static key wrapped in a byte string
  that counts relational operations) shows 0 such operations on every probe (§7.1). At most bitlen(K) iterations,
  under the charged L = bitlen(K) + 1 comparisons of 2(|k| + 1) bytes. An undeclared key falls to the slot's
  `additionalProperties` child;
- the per-invocation, per-member, per-item, per-UNIQUE and per-ORDER loops count in their bodies. An invocation's
  own cost (§3.3) is a closed form of its static entry and the node's statistics, computed in time bounded by the
  entry's size (a constant of the table), and counts as one step;
- the retained-length lookup is one counted element and a counted binary search over the store, after its charge,
  each iteration one three-way comparison of two 32-byte digests. The digest itself is **supplied from outside the
  boundary** (r4, REVIEW-r3 NBO-1): C2b-1a holds it (the pinned fetch receives an already supplied digest,
  `closure.rs`:85-95), and the reference's fixture builds it when it builds the store and passes it to `Record` as
  `key`. Nothing is encoded or hashed between the record's census and the lookup.

**The algorithm.** One post-order walk per priced record r:
- **the records:** the two closures, the context, the universe, the graph, the layout and the snapshot (the snapshot
  only for C9's shape and its wrapper);
- **at each node:** it descends with the node's static slot, which is the list of evaluation-table invocations at
  that position (§3.8); a container at container depth 32 refuses `PriceUnavailable` at its own dispatch step, as the
  encoder refuses it (`canonical.rs`:536; NBO-1);
- **after its children:** it computes the node's statistics from theirs, and each invocation's own cost (§3.3) from
  the node's statistics and its direct children's;
- **what it accumulates:** the parse, `ordered` and clone contributions.

Each child's statistics are folded into the parent as the child returns: running sums; UNIQUE's per-item term at
the array's known length; ORDER's previous key, one integer. So each frame holds O(1) state. The table is static and
nothing is heap-allocated; F8 holds that to zero. Each record's census runs once, and §6's multiplicities reuse its
result.

**Its charge, element by element (C1: "If its extent is known only element by element, each element is charged
before its own work").** Each element is charged from sizes available in O(1) at that moment:
- **a node's kind and, for a string, its byte length**, from the representation (`String::len`);
- **the slot's invocation count** m and declared-key count K, from the static table;
- **a member key's byte length**, from the representation;
- **the store's population** |blobs|.

| element | charged before its work | the counted steps it pays for |
| --- | --- | --- |
| a node | {0, 2 + m + [string], 2n} (n = a string's byte length, else 0; [string] = 1 for a string, else 0) | dispatch, including the depth gate; for a string, its one scan: 1 element and 2 bytes per byte; m invocation costs; statistics finalization |
| an object member | {0, 1 + L + m + 3 + 1, 2\|k\| + 2L(\|k\| + 1)}, with L = bitlen(K) + 1 and \|k\| the key's byte length | the key's scan (1 element, 2 bytes per byte); the binary search (≤ bitlen(K) three-way comparisons, each reading ≤ 2(\|k\| + 1) bytes); m member costs; its parse, clone and `ordered` contributions; the child's accumulation |
| an array item | {0, 3m + 2, 0} | per invocation ≤ 3 item terms (`items` lookup, UNIQUE, ORDER); the `ordered` contribution; the child's accumulation |
| the retained length (r3) | {0, 1 + k, 2k·33}, with k = min(\|blobs\|, 11·bitlen(\|blobs\|)) | one element; the binary search over the store (≤ bitlen(\|blobs\|) three-way comparisons, each reading ≤ 33 bytes of both operands) |
| a record | {0, 8, 0} | the term assembly |

**The reference counts where the work runs**, and it holds counted ≤ charged **per element** and in total
(`Census.check`): each charge opens an element, and every step counted until that element closes, its children's
elements excluded, is attributed to it. Slack in one element therefore cannot hide an excess in another; the
`linear-lookup` mutation is caught at the first member whose linear scan exceeds its charge, and the `scan-first`
mutation (r2's defect) is caught because the pre-charge scan lands on the enclosing element, and the `two-sided`
mutation (r3's defect: two relational operations per iteration, one counted) is caught by the observer. §7.1 shows
the totals and the caught tuples. No count is taken from an unfunded pass: N, B, L, the scan results and the lookup results are
outputs of charged elements, never inputs to the charge.

**Exhaustion (the F6 reference, `scripts/exhaustion.py`).** For each record kind the census runs once with a trace
of every element's charge, then reruns with the budget set to exactly the work charged before a chosen element, so
every earlier element fits and the chosen one does not. It asserts that the census refuses at exactly that element,
that no scan of it began (scans started unchanged) and that no visit of it began (nodes visited unchanged). The chosen
elements are the first element (budget zero: exhaustion before the first visit), a string value node and a member
key after earlier elements have consumed budget (the 2nd, 40th and last of each), the last item, the last element
and, for each frame and record, **the retained-length lookup** (r4: refused at the lookup, with no store comparison
run). On the toolchain closure, the context and universe frames and the graph and layout records, all 46 probes
hold, and the whole budget completes each census (§7.1; `evidence/exhaustion-r4.stdout`). Under `scan-first` the probe
at a string element sees a scan that began before the refusal, so the defect REVIEW-r2 found is what this control
catches.

**The census charge in the whole call (r4, REVIEW-r3 NBO-2).** The census is debited element by element, during
the single census, by the C1 protocol above; the aggregate per record that §7.1's `charged` column publishes is the
**sum of those debits**, which contains scan-derived counts and is neither available nor charged beforehand. It is
additional to the admission and owner prices; §7.1 gives the sums per scenario. The census runs once per record,
never per occurrence.

**Static tables, computed offline and pinned by F2, are not census work:** RESOLVE per reference; DISPATCH per
pattern; literal statistics per `const`, `enum` and annotation; ORDER\_PARSE per annotation; the slots' sorted keys,
children and member tables; the `ordered` arm table; ROW\_CLONE per registry row.

## 9. *T*/*L*/*N* under successor-law item 1

Successor-law item 1 assigns "every charge of the selected operation" to *T*, *L* or *N*
(`opensip_arch/docs/implementation/m3/snapshot-plan-c/c2b/law-revision-r4/PLAN.md`:35-50). These terms are charged
on the pre-Plan resolved-inputs scope that C4a supplies (PLAN-r3 LD-C2B1-8), after the seal. **None of them is a
charge of the selected operation, so none takes a family.** *T*sound, *L*max, *N* and the caps are unchanged. This
agrees with REVIEW-r1's answer to Q1.

T-SNAPSHOT reuses C9's *function*. The snapshot ledger's *T* charge at the seal is a separate execution on another
scope and is untouched.

If C4a were ever to charge these calls on the snapshot ledger, they would need an assignment, which is a law question
for the coordinator. C2b-1a's control 23 and its composition precondition exclude that.

**Pricing under M1a C1.** Every pass above is {0, k, b} over its elements and examined bytes. The other conventions
apply as follows:
- allocations are owned/P1/L2;
- SHA is C2;
- parses are C4;
- encodes and frames follow C9's discipline;
- no constant stands for variable work (C6).

## 10. `PRICE_PREMISES` (RF-2)

**Rule.** Control P1/F1 pins every file below by blob SHA-256 at `9815938`. A change to any of them fails F1, and the
affected terms must be re-derived; F1 is updated only with that re-derivation. Existing enforced closures that hold
some of the same bytes are listed in the last column. They are complementary, not substitutes: re-pinning one of
them does not re-derive this price.

| file | bytes | sha256 | premise | invalidating controls |
| --- | --- | --- | --- | --- |
| `crates/evaluator/src/native_retention.rs` | 16,456 | `362dafad8aa63f05704544045a5258ed199a01fd5c7a15649813c9524abce9b8` | composition counts (§6), T-WALK | F1, F5 |
| `crates/evaluator/src/native_context.rs` | 15,809 | `c16fe03d2693bf376ca90fabcbf115f986efd6df6e33724f3a074ade3c2e8a2e` | context-owner admissions and clones | F1, F5 |
| `crates/evaluator/src/native_universe.rs` | 33,043 | `ddf30b44dc12367765ec81df2e840203cf882f2e72646e19b5b28f03b0b26254` | universe-owner admissions, `nested_record` | F1, F5; snapshot-ledger `LAYOUT_FILES` (`tools/security/snapshot_ledger_model.py`:132) |
| `crates/evaluator/src/unicode_case.rs` | 2,757 | `c04c71a0e7cda370e87f44fb599f743e60fee565330e9f8b333f1d858523d0ab` | the fold's passes (§12) | F1, F4 |
| `crates/evaluator/src/generated/unicode_case_tables.rs` | 49,680 | `6012d5ee0506a70947418e2ec828506a062e3f23be1b0090432a668d47e13e0a` | VERSION (15,0,0); \|LOWER\| 1,433, \|CASED\| 157, \|CASE\_IGNORABLE\| 437; ≤ 4 output bytes per scalar; expansion ≤ 3/2 (U+0130) | F1, **F4 (drift)** |
| `crates/evaluator/src/native-context-registry.json` | 9,783 | `8601618ad47b9a2d37af916b4db42aa1e108ea78c4071898c9bfbeef72d38611` | parsed by `graph()` (`native_universe.rs`:418) at each universe-owner run | F1 |
| `crates/evaluator/src/lib.rs` | 4,505 | `bed8e6d1c52c624ce805af8289f299a214ff31e8bd0f53f3b036d8c05f03efb3` | the owners named by retention's imports | F1 |
| `crates/identity/src/closure.rs` | 62,207 | `7412df224a155f5409c766a8f1fcf72f142a907c7461195928b4d6b0d2c02efb` | OBJECT, BLOB, FRAME, RECORD, CANONICAL\_RECORD | F1, F5, F8; identity `dependency-policy.json` `localSources` |
| `crates/identity/src/descriptors.rs` | 27,429 | `0477db5b64f63902fb07af5b02d4a7f39d752fbbb1a9165725c64e3c1d3e5e12` | FROM\_JSON, ORDERED, ArrayOrder | F1, F5, F9; dependency-policy |
| `crates/identity/src/schema.rs` | 26,088 | `9ef186d91d6f4686e79fdf247d2ce75f2168744bfa408406b13990ccd6f1328b` | ADMIT, EVAL, RESOLVE, dispatch owners | F1, F2, F5; dependency-policy |
| `crates/identity/src/schema_registry.rs` | 29,593 | `9e1f0e60edc086d9c5f85dc4a6f74c4d8c872b14714fe3349fbe89a4baaa8827` | LOOKUP, ALIAS (15 rows; native row 9), SOURCE\_PINS (52; population bound 1,879,078), schema-source pins | F1, F2; dependency-policy |
| `crates/identity/src/schema_patterns.rs` | 25,372 | `fa9b5431e13277a17009eaac5aea0c78e29a277ecafbbe3b9ea5be4d01fe472c` | FORMS (26) and TABLE (72) rows, matchers, no allocation | F1, **F3**; dependency-policy |
| `crates/identity/src/canonical.rs` | 20,515 | `a5565692f7081afe25c7ec597340fa2ac553a9419a0fe52407286fea91aba506` | meter prices, parse core, encoder, MAX\_BYTES | F1; dependency-policy; snapshot-ledger `METERED_*` anchors (`snapshot_ledger_model.py`:169-176) |
| `crates/identity/src/digests.rs` | 5,643 | `8de86abcdf1f2ffd1e5880efc26f18e3d45306e11d55889ab44af6354d786422` | HASH, UNFRAME, hex | F1; dependency-policy; `DIGEST_IMPLEMENTATION` anchor (:165) |
| `crates/identity/src/lib.rs` | 3,968 | `7434550fa8df0ccdf3592e6aa554b5dbe8544fc3c5fc5a167cd65660ae735dca` | the re-exported names (`canonical_bytes`, `parse_json`, …) | F1; dependency-policy |
| `schemas/sources/identity-v3.schema.json` | 201,224 | `aa7cb4744ae20bc4fa2ce82e734e59a7d53e2eb23e0b57a843b70558fb0a2ebd` | `$defs/closure`, `$defs/snapshot`, `domainSets` rows (cloned), root 7 / `$defs` 54 | F1, **F2**; `SOURCE_PINS` (runtime refusal on drift) |
| `schemas/sources/native-v2.schema.json` | 295,104 | `7179d52e3b7ce7400a3ab24badcae5b4242acab7c1cb4523032adf4c706d3132` | the four native entries, root 10 / `$defs` 115 | F1, **F2**; `SOURCE_PINS` |
| `crates/host/src/snapshot_admission.rs` | 22,448 | `59febe43c4d2dca3129560deecaee9c7d491629aa25be2c0a569ac1b02799bb5` | C9, search, growth, growths, formatted | F1, F7; C9's own controls |
| `crates/host/src/snapshot.rs` | 33,734 | `e281f3b6ee18dab7a8b8a7235fcde79131c3b1033fe3c9cc2656d5a105d88731` | digest\_cost (C2), btree\_height, btree\_insert (L2), growth\_cost | F1 |
| `crates/host/src/node_modules_layout.rs` | 56,678 | `660a46add48aa423533a7eaa8f2cad03471ad59fc002852dccd6380b7c127310` | tree\_search\_comparisons, map\_search\_comparisons, registry\_entry\_population\_bound | F1 |
| `crates/security/src/snapshot_source.rs` | 32,817 | `1a56f038004a747fd6bf5c42cb8e1f2a3b1246df430e1825f0ec9382fbddbd18` | `owned_record` | F1 |
| `crates/security/src/custody/discovery_walk.rs` | 51,204 | `4dbd3d1e3e34684548116ae7adf08e6ba58e3ff813c0423e5b5b45b6c38493e6` | `owned`, RECORD = 128 | F1; discovery census closure |
| `crates/platform/src/work_ledger.rs` | 48,098 | `7b4b304057f21960d24d7a6c0570747445656b72041f9c537458cb7dadcf474e` | `Cost` (WorkCost) and its charge semantics | F1 |
| `rust-toolchain.toml` | 86 | `7d21c66a15f41bad66b82ed06a289f5dc8a6e3751951d2696bbf20ce296f2b0f` | 1.95.0: the std premises below | F1; M1a std controls |
| `Cargo.lock` | 13,836 | `75331035faaed0969b098d5f8b92e36614d6856871e72db19e65f32215461414` | `sha2-const-stable` 0.1.0 (checksum `5f179d4e…`): allocation-free, linear SHA-256 (C2) | F1; identity `dependency-policy.json` `dependencies` |

**The std premises (1.95.0), by exact reference to their existing controls:**
- **P1 growth:** `the_growth_bound_covers_its_sequences` and `the_toolchains_growth_rule_is_the_one_the_meter_prices`.
- **P2/P3 B-tree search:** `search_comparison_bound_covers_node_and_population_growth` and
  `tree_search_bound_covers_many_long_common_prefix_keys` (`node_modules_layout_tests.rs`:1764, :1778), which count
  actual comparisons. No existing control holds `btree_insert`'s node and move side; F8 checks its allocations on
  this derivation's paths, and its moves stay source-derived (L2).
- **Sizes:** `node_modules_layout_tests.rs`:1893-1896.
- **`meter_prices::array`:** `tests/metered_parse.rs`.
- **The remaining allocation premises:** the `format!` capacity estimate, `SpecFromIterNested`'s four slots,
  `BTreeMap::clone`'s node mirroring and exact-capacity `String`/`Vec` clones. These are checked on this derivation's
  own call paths by the counting-allocator control F8, in C9's form.

**The generated table's drift control F4.** F4 checks the table's **price-relevant populations and extrema**
(r2, NBO-3). It parses `generated/unicode_case_tables.rs`, recomputes the following, and asserts that each equals the
constant the fold price uses:
- VERSION;
- the three table populations;
- the order each search requires:
  - `LOWER` strictly increasing by code, for `binary_search_by_key` (`unicode_case.rs`:43);
  - `CASED` and `CASE_IGNORABLE` as sorted, well-formed, non-overlapping ranges, for `partition_point` (:11-15);
- the maximum output bytes per input scalar;
- the maximum ratio of output to input bytes.

F4 fails on any change that alters an expansion or a search population, even if VERSION is unchanged. That is the
case REVIEW-r2 RF-2 names. A change to one mapping that leaves those extrema unchanged is caught by F1's whole-file
hash, not by F4. F1 and F4 together close the drift gap. `scripts/case_table_premise.py` is the reference
(`evidence/case-table-premise-r4.json`).

## 11. Controls and mutations C2b-1a must carry

| control | what it checks |
| --- | --- |
| **F1** `PRICE_PREMISES` | Every §10 file's blob SHA-256 at its recorded value (= PLAN-r3 P1). |
| **F2** schema tables | For each of the six entries, it regenerates the price module's evaluation table (keyword-map sizes, `$ref` targets and pointer parts, `const`/`enum` literals, required keys, property keys, `additionalProperties`, `items`, `oneOf`, `not`, pattern, `uniqueItems`, order annotation) from `include_bytes!` of the schema source, with its SHA-256 checked against `SOURCE_PINS`. It requires equality. It also checks the root and `$defs` populations (7/54, 10/115), the 52 documents, the population bound, the 15 aliases and the native alias row, and that no keyword outside §3.2 occurs. This is C9's `the_price_reads_the_registered_identity_v3_shape`, generalized. |
| **F3** pattern rows | It parses `schema_patterns.rs` and checks: the FORMS and TABLE row index and cumulative bytes for each §3.5 pattern; the four owner literals in `pattern_matches`, in order; the two `allows_empty` literals; and the matcher kind of each row. |
| **F4** case table | As §10 (drift). |
| **F5** formula vectors | The Rust price equals `scripts/admission_model.py` on every term's allocation side, pass side and total, and on both compositions, over `evidence/VECTORS-r4.json`'s admitting and malformed records (= PLAN-r3 P4). |
| **F6** the price pass (r2, RF-1; r3, REVIEW-r2 RF-1) | C2b-1a's census is its own code, so it can be instrumented. Under a test seam it does what `scripts/admission_model.py` and `scripts/exhaustion.py` do. **(a) Counting:** it counts its executed steps and examined bytes **per element** (each charge opens an element) and asserts counted ≤ charged per element and in total on every vector, admitting and malformed (§8); its string scan counts inside its loop; its declared-key lookup is a binary search over the slot's sorted static keys whose comparisons are counted; its store lookup likewise. **(b) Exhaustion:** with the budget set to the work charged before a chosen element, the census refuses at exactly that element, with no scan of it begun and no visit of it begun; the chosen elements are the first (budget zero: before the first visit), a string value node and a member key after earlier elements have consumed budget, and the last of each kind, on each record kind; the whole budget completes the census. **(c)** the census allocates nothing (counting allocator: zero allocations between the census's start and end). **(d)** invocations ≤ μ\_E·N, and μ\_E equals §3.8. **(e)** the mutations `scan-first`, `linear-lookup`, `two-sided` and `unique-extra` are caught. **(f) The searches (r4):** each iteration of the declared-key search and of the retained-map search is one three-way comparison counted with the bytes it read; an observer that counts relational operations on the wrapped keys sees none; below-first-key, equal-first-key, equal-last-key, above-last-key and undeclared lookups stay within ≤ bitlen(K) comparisons and the member charge; the retained digest is supplied from outside the census and a retained-lookup exhaustion probe refuses before any store comparison. |
| **F7** C9 premise | The census refuses `PriceUnavailable` for a snapshot descriptor without C9's structure: an extra top key, a 4-key row, a non-string path. On the sealed fixture, T-SNAPSHOT equals the wrapper plus `descriptor_admission_cost` at the census shape. |
| **F8** allocations and verdicts | A counting-allocator integration binary, in C9's form, runs `RetainedInputs::object` (closure, snapshot), `frame_candidate` (context, universe) and `inspect_current_record` (graph, layout) on each vector's records, and the two whole calls on the fixtures. For each run it does two things. It **asserts the record's expected verdict** (§7.1), so an early refusal cannot silently satisfy the bound (NBO-1). It holds the run's allocations and allocated bytes to ≤ the term's **allocation side** (NBO-2). The cases are the distinct long-path, escaped and 2,000-row closures, the layout at 5,000 rows, the universe at 20,000 roots, and the eleven malformed records. |
| **F9** order arms | The `ArrayOrder::parse` arms and the `ordered` arms, by reference to C9's pin. The F2 table adds the annotations reached, and §4.2's arm prices (r2). |
| **F10** totality (r2, RF-2; r3, NBO-1) | The price is defined, and F5-equal, on every malformed vector. The depth gate is the encoder's: 32 nested containers, empty or not, with or without a scalar inside the 32nd, are priced; a 33rd refuses `PriceUnavailable` at that container's dispatch step, with no allocation and no evaluator entry (§7.1's six boundary vectors). |
| **F11** retained length (r3; companion RF-3) | For each frame and record the census looks β(d) up in C2b-1a's retained map (a charged, counted search) and requires β(d) = F (a frame) or L (a record); otherwise it refuses `PriceUnavailable` before any term work and before the evaluator. Vectors: a graph record retained at 1 MiB, a universe frame retained one byte short, and an absent graph digest (priced at the full term). |

| mutation | caught by |
| --- | --- |
| price a closure with `descriptor_admission_cost` (the r2 error) | F5 |
| drop ORDERED from T-CLOSURE | F5 |
| drop FRAME's UNFRAME parse or its registry-row CLONE | F5 (and F8 for the clone) |
| drop RECORD's second BLOB | F5 |
| count T-FRAME-CTX three times at bind | F5 (composition vector) |
| change a keyword-map size in the table | F2 |
| change a FORMS or TABLE index | F3 |
| change a case-table constant | F4 |
| edit `unicode_case_tables.rs` without re-deriving | F1, F4 |
| evaluate one `oneOf` rule only | F5, F6 |
| add an unpriced traversal or a heap allocation to the census | F6 (counted > charged; non-zero census allocations) |
| fund the census from a precomputed N, B or L | F6 (exhaustion before the first visit) |
| price ORDER\_VERIFY from the field's own length without the item's kind check | F10 (the malformed vectors) |
| compare F8 storage against the total instead of the allocation side | F8 (the allocation side is published separately) |
| scan a string before its charge (the r2 reference's defect) | F6 (the exhaustion probe sees a begun scan; the per-element check fails) |
| look a member key up by a linear scan, or record the lookup's allowance without doing the search | F6 (per-element counted > charged; the comparisons are counted inside the search) |
| execute two relational operations per search iteration and count one (r3's reference defect) | F6 (f): the observer counts relational operations on the wrapped keys |
| compute or re-derive the retained digest inside the census | F6 (f): the retained-lookup exhaustion probe; the census receives the digest |
| sort or encode an object's keys inside the census | F6 (counted work with no element charge) and F8 (an allocation) |
| retain a buffer of another length under a frame's or record's digest | F11 |
| accept a 33rd nested container, or refuse a scalar inside the 32nd | F10 |

## 12. The companion slots (coordinator ruling LD-Q-6)

**The companion subject.** It is `../evidence/SLOT-DERIVATION-r4.md`, sha256
`c6924ed3c26b6754351bbc8420a25fa9bf64f94c9bf0b4dc4048fce64fb723bd`, with its ledger checker
`../evidence/scripts/slot_ledger_check.py` (sha256 `dabfbcd5bd654605794768b56073861291a3dac528643137f7ddb53e249fe204`; controls S1 and S6) and
`s1_check.py` (sha256 `7a983aec68f5b6a815ff65222564ad243abd380fcdcf2cd45a8b6c07f7f9a10d`). The C2b-1a author wrote it against r2, revised it for
REVIEW-r2 RF-2 to RF-5 (its own findings) and RF-6 (joint) as r3 (sha256 `377b7c4e…`, kept), and revised it
for REVIEW-r3 RF-2 as r4. It is a line-by-line ledger of the three evaluator files at the pin: this author reran
`slot_ledger_check.py` on r4 from the product checkout at `9815938`: **93 rows, 10 helper rows, 0 S1 misses, 0 double
claims, 0 uncovered lines**. Its terms are T-WALK-ROOT, T-WALK-CTX, T-WALK-UNI, T-OWNER-CTX, T-OWNER-UNI,
T-REFUSE-CTX, T-REFUSE-UNI and the three copies COPY-R377, COPY-U187 and COPY-R400.

**r4 (REVIEW-r3 RF-2), checked by this author.** Only the U:459-481, U:482-490 and U:469 rows and §5 changed (diff of
r3 against r4). The DFS row is re-derived from the push rules at the pin: U:438-442 reports a missing edge target
and continues; U:476-478 pushes every edge target; U:474, :475 and :463 insert, push and re-insert each newly
discovered key whether or not it is a node. So the discovered keys are the entry plus the pushed edge targets,
K ≤ 1 + E (G bounds them in neither direction: unreachable nodes never enter `state`, and missing targets are not
nodes); pops ≤ 2 + 2E (1 + E key pushes plus K done markers); 2K state inserts; key lengths over
L\_key = max(|entry|, |e|max), since a missing target can be longer than every node path; U:482-490's lookups
search K; U:469's cycle fault is formatted over L\_key. The new control S10 (one entry node, 64 distinct missing
targets) expects K = 65, 130 inserts, 130 pops and 64 edge pushes, which is the reviewer's own transcription. This
author agrees with the bound and its derivation.

**This author's checks of it, as LD-Q-6 requires:**
- **The primitives are used unchanged.** Its §0.1 uses §2 and §3.7 as published: `pass`, `owned`, `search`,
  `digest_cost`, `btree_insert`, `growth`, `formatted`, `CLONE`, `PARSE`, `FOLD` (the F4 constants), and EQ over
  both operands; `field(o, k)` is `search(K_o, |k|)`; its split is r2's §0.2, which is §3.7's split. Its BLOB(d)
  is search(|blobs|, 32) + digest\_cost(β(d)) with β(d) the actual retained length, the rule this r3 adopts for its
  own BLOBs (LD-F-9), and its §0.3 funds β(d)'s lookup exactly as §8's retained-length element does.
- **Nothing is counted twice against §6.** By construction no companion term contains an owner call, an admission,
  W-REC or a copy (its r3 changes, RF-6). Its ledger marks every §6 site "funding": R:93-99 (T-SNAPSHOT), the
  `object` call inside R:247-268 (T-CLOSURE), R:276-279 (T-FRAME), R:304-315 and :316-320 (RECORD and W-REC),
  C:195 (T-CLOSURE), C:222-223 (CLONE), C:373-375 (T-FRAME-CTX), U:151-153 (T-FRAME-UNI), U:170-172
  (T-FRAME-CTX), U:179-181 (T-SNAPSHOT), and U:190/U:238 with `nested_record`'s :320, :325-336 and :337-339
  (RECORD and W-REC); OBJECT's `MissingObject` string is funding's (§4.3, §5.1). Its own nested-record rows cover
  only what W-REC does not: retention's pre-inspection `self.blob` at R:303 and `nested_record`'s filter, `path`,
  `format!` and `sha256_text` at U:297-319. The closure manifest and member blob fetches (R:260-266) and the
  layout's `blobJoins` (R:321) are its T-WALK rows and are not in §6.
- **The partition is kept.** Its §0.5 assigns no family, as §9 does.
- **The census is funded.** Its §0.3 derives every population from this census's node, member and item steps, or
  states an extra element-by-element charge (the lib-name scalar counts, the 5-byte `.d.ts` test, the basename scan,
  the running maxima, and β(d)'s lookup, which is §8's retained-length element). Its §0.5 keeps the prefix rule and
  prices the allocating exits.

**The whole calls (RF-6).** The companion's §4 is the single occurrence matrix of both calls, with terms disjoint by
construction, and §6 here is its funding column. So:
- **mint** = T-WALK-ROOT + T-WALK-CTX + T-OWNER-CTX + T-REFUSE-CTX + COPY-R377 + §6's mint column
  (T-SNAPSHOT 1, T-FRAME-CTX 2, T-CLOSURE 2 per closure, CLONE 1 per closure, T-REC-LAYOUT + W-REC 1 when the context
  names a layout);
- **bind** = T-WALK-ROOT + T-WALK-CTX + T-WALK-UNI + 2·T-OWNER-CTX + 2·T-REFUSE-CTX + T-OWNER-UNI + T-REFUSE-UNI +
  COPY-R377 + COPY-U187 + COPY-R400 + §6's bind column (T-SNAPSHOT 2, T-FRAME-UNI 2, T-FRAME-CTX 4, T-CLOSURE 3 per
  closure, CLONE 2 per closure, T-REC-GRAPH + W-REC 2, T-REC-LAYOUT + W-REC 2);
- plus each priced record's census charge once (§8).

Checked against the source: the context owner runs at R:372-379 once per `frame(context)` (mint 1; bind 1, via
`contextField` at R:359-369) and at U:176-177 (bind 1), which is §6's T-FRAME-CTX 2/4 and the matrix's T-OWNER-CTX 1/2;
the universe owner runs at R:380-400 (bind 1); the copies are R:377 (one per context-owner run from retention: mint 1,
bind 1), R:400 (bind 1) and U:187 (bind 1). Every row of the matrix is additive, and no site is in two rows (S6).

**What the coverage claim is, and is not (r4, as REVIEW-r3 asks).** S1 and S6 establish that every reachable line of
the three evaluator files lies in exactly one ledger row and that each row's range contains its named construct;
they are syntactic coverage, and they do not by themselves establish any row's multiplicity or cost bound. Each row's
bound is a derivation from the cited lines that the R3 review checks row by row; REVIEW-r3 RF-2 found one such bound
wrong (the DFS population) and r4 re-derives it. So the whole-call claim is: the companion's matrix and §6 together
assign every reachable site to exactly one additive row, and every row's bound is a source derivation under R3 review,
with S7 to S10 as its executable controls; it is not a claim that range coverage proves the bounds.

**Operations this derivation found in r1, now carried by the companion** (cited by its rows, not re-listed here):
- the context owner's deep clone of each closure descriptor: §6's CLONE row; its C:222-223 row marks it funding's;
- `graph()`'s parse of the embedded `native-context-registry.json` (9,783 bytes, pinned by F1), once per
  universe-owner run: its U:417-423 row (PARSE);
- the universe owner's copy of the context owner's refusals into its set: its COPY-U187;
- retention's deep clone of each inventory row and the universe owner's borrowed map: its R:100-103 and U:182-185
  rows;
- `frame`'s and `closure`'s set insertions and the `closure2-suffix` `format!`: its R:284-287, R:247-268 and
  R:349-358 rows;
- the fold (`unicode_case.rs`:23-53) with the F4 constants: its FOLD primitive, used at C:97-100, C:111-115 and
  C:157-161 (its S3);
- the T-REFUSE strings, bounded by the record fields each `format!` names: its §3, by ownership path, over its §0.3
  populations.

## 13. Not claimed

- No *T*/*L*/*N* assignment, cap or fit claim for the resolved-inputs scope (§9).
- No change to accepted charge law. Every convention is used as published.
- No instrumented measurement of examinations. Visits and examinations are bounded by the source derivation, and F8
  measures allocations only.
- No pricing of Rust or syntax domains, or of keywords outside §3.2. Each refuses `PriceUnavailable`.
- No claim about the companion's slot terms beyond §12's checks; the companion is its author's derivation under this joint review.
- No claim that the Rust census exists yet: F6, F10 and F11 are the controls C2b-1a must carry, with `scripts/admission_model.py` and `scripts/exhaustion.py` as their reference.
- No claim that S1/S6 coverage proves a bound (§12); bounds are derivations under this review.
- No product edit. The scripts read the product only through `git show` at the pin.

## Evidence

| file | sha256 |
| --- | --- |
| `scripts/admission_model.py` (r4: one three-way comparison per iteration; the digest supplied) | `51e3ce853f6fdf40fc3b4dcdad25b4e391571b20b2d9f5f555d727903ea2c200` |
| `scripts/vectors.py` (r4: lookup controls) | `fc93ae9cc506f9acbb846bf55cffeed095837a2f8292705b5f42a0d1f46d0ff2` |
| `scripts/exhaustion.py` (r4: the retained-lookup probe) | `eed82234df7711e3e5a7b8cb9147175998292fbc8bb4ceb36e3bb0fe7931ade1` |
| `scripts/compare_r2.py` (r3) | `ec2b506c4031e73d028cbb00f6898d0748a6625dd21d69414c39da2bea49ffa7` |
| `scripts/c9_crosscheck.py` | `c70d506a3400fdb810c704d52ed34a0998d8c68063ddd16acf9d19586d92b366` |
| `scripts/layout_crosscheck.py` | `7c35885e0e4c70aca06417c6b5855172e63194027c40bc1e9ac618f73d23cda9` |
| `scripts/case_table_premise.py` | `4e68756357dc411a0289d502d04fc72375a9b261df3984cf5dfd496034d23777` |
| `scripts/schema_facts.py` | `1c210d0b91e9d8f68192fb2ee47ba9333b1b97bbe9823014f17b0484bd78757c` |
| `evidence/VECTORS-r4.json` | `fd64aaa10f7287b8b37385c70ac022c3a4e663d332ceecbbb3a6df6b6555cdf7` |
| `evidence/vectors-r4.stdout` | `3b39c0cc4a3f05edd168b9649639976592a0a01622af8d2c652b3663e3661f55` |
| `evidence/exhaustion-r4.json` | `b196140930f7c17fef54e69778071b034f0ee63626f145c6557803d3cef67de8` |
| `evidence/exhaustion-r4.stdout` | `bae8324794c47ddb36b293261d16b68e8c84fbc685d63fb75b908975355fec0f` |
| `evidence/compare-r2-r4.stdout` | `eb6abf46f8c2e51ba8b39e1a7e74c1b134663ab3223a26f31119dcff0032013a` |
| `evidence/c9-crosscheck-r4.stdout` | `f93295d93e70d7cc69b8255aeb68ba20b0880bb20d5a33d34eccefde7fc95772` |
| `evidence/layout-crosscheck-r4.stdout` | `9ab1cf460dbe04f8a33cdd797e2ca6b56c29bba45951d9b089a1fef59b85b427` |
| `evidence/case-table-premise-r4.json` | `bb677c17ffcc2f2a98fdc8463429de45a6a2ab281a926ec6c1c7983aa406ec41` |
| `evidence/schema-facts-r4.stdout` | `654a279cc22ac9a5b449d38b9e421e434473cf53ee4d89207dae0fb64c90bf42` |
| `evidence/tables-r4.stdout` | `29ec0a5b837fa0f2b477320b4154e65798f3e2513e5fb36de0d4831a226d5446` |

Reproduce with `python3 -I -B scripts/<name>.py /Users/sb/code/opensip-ai/opensip` (`exhaustion.py` and `compare_r2.py`
import `vectors.py`). r1's, r2's and r3's scripts and evidence are under `scripts/r1/`, `evidence/r1/`, `scripts/r2/`,
`evidence/r2/`, `scripts/r3/` and `evidence/r3/`, unchanged, at the hashes their derivations name.
`scripts/c9_crosscheck.py`, `layout_crosscheck.py`, `case_table_premise.py` and `schema_facts.py` are r2's, unchanged,
rerun on the r4 model.
