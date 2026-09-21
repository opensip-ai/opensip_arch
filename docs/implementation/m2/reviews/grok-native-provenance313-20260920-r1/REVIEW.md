# Independent review — native successor codecs and retained-P2 V2 producer 313

**Standing:** bounded native-Rust review of frozen `native-provenance-checkpoint-313`. Private unselected integration of independently reviewed 312 into frozen 311: 127-definition schema admission, 136-site typed extraction, and a retained-**P2** producer that emits `S4EvaluationInputV2`. It does **not** implement the 312 embedded-root resolver, original-authority authentication, 314 scoped admitter, or a publisher. Installed product remains `fa72e50`. Keys are **TEST ONLY**. 314 REVIEW and ADDENDUM were not edited. Native 313 is separate from 314.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/host/mutant directories were not overwritten. No workspace rerun. No load/suspend/VM/proof-prep/namespace qualification.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **9483840 B, 1008 members, SHA256 `355396bd32b40c177bb34c8b7cb81ae65e0496f74751d28cd8551b389b10ee39`**. Standing: private unselected313 successor127 codecs/V2 retained-P2 input producer; no proof admission/durability or publication qualification. Extract rehashed **1008/1008**. Product-inputs **463/463**. Nested 311 pin `5c8d692e…b87d` and 312 pin `f04b5b42…6e5b` (live tar match). `kernel201.py` `df45c9c5…2299`. Successor schema `a0431300…7928` **byte-identical** to frozen 312. `S4EvaluationInputV1` def **byte-identical** to frozen 125. Original `trust_record_reference.py` `00ad3a34…e6df` unchanged. Whole `trust_time.rs` / `clock_observation.rs` / `captured_capsule_clock.rs` / `ordinary_targets.rs` / `lib.rs` **byte-identical** to 311. `ordinary_targets.rs` still uses the **TIME311** telemetry prefix; recorded documents are schema 2. `lib.rs` has **no** public export.

Product vs 311: **463** files, **452** unchanged, **11** deltas: `trust.rs`, `trust/proposed_time_input.rs`, `trust_record_reader_tests.rs`, `trust_record_shape_nodes.rs`, `trust_record_shape_tests.rs`, `trust_record_visit_nodes.rs`, and five reader/record fixtures. `proposed-time-input-before.rs` equals 311 `proposed_time_input.rs`.

Preserved unchanged: 311 REVIEW `02e8228a…d1f1`; 312 REVIEW `4b91fece…71ff`; 314 REVIEW `d54342fd…daca` (17022 B); 314 ADDENDUM `02a3a0bc…c8ee` (11149 B).

Generated: **127** `$defs`, **555** fragments, **25** regexes, **942** schema visitors, **393** edge visitors, **136** typed sites, **29** root kinds. Clock-event `evaluation` / s4 `timeEvidence.proof` target the `S4EvaluationInput` union. V2 `authority` is NodeRef / records / `RootAdmissionNodeV1`. Aggregate + V2 are graph roots.

---

## What the producer does

`prepare` still branches on 301 `proof_retention`. **NoWrite** does not inspect invocation. **Keep** and **NewRequired** both construct a closed V2 record: `inputSchema: 2`, `kind: s4-evaluation`, **required** `authority` copied from the **owned** captured capsule `heads.root.admission` (no caller authority argument), plus the 311 eight members (invocation, store, beforeImage, beforeClock, observation, ordinary `closure` NodeRef of `closure_raw()`). Canonicalize, `Record::parse(S4EvaluationInputV2, raw, 131072)`. `evaluation()` is always that fresh node. `time_evidence()` is exact old T on Keep and the new NodeRef on NewRequired.

This path already requires retained-P2 captured ordinary input (`heads` present). It does **not** construct P0/P1 authority or run the 312 embedded-byte resolver. The authority field is a **locator**, not admitted historical CoreAnchor/complete-chain proof (314). Closed `InvocationBinding` is not live execution identity.

---

## Reproduction

**Executed:** `cargo clean -p opensip-security` then **253 passed / 0 failed / 2 ignored** with `Compiling opensip-security` (`Finished` 10.45s; tests 12.04s). Ignored: 305 host observation pilot and this actual-host composition. Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **eleven** include files.

**Host (TIME311 prefix, schema-2 documents):** 8 samples × 29 bindings = **232** decisions. Independent 201/265 `clock_decision` plus 312 `S4EvaluationInputV2` / source-exact SHA/length assembly (`authority == capsule.heads.root.admission`).

- Historical replay of frozen `host-r1`: **8/8** (1 NewRequired / 2 Keep / 5 NoWrite); **12** evaluations (**4** new-T, **8** kept-T), **75** invalid-binding, **145** NoWrite; all 12 writes `inputSchema=2`. Frozen stdout SHA256 `c30372fa…711c` unchanged.
- Live `grok-out/io/host-live/`: **8/8** and the same 232/12/4/8/75/145 split this wall. Frozen `host-r1` not overwritten. 302 1 s remains unqualified.

**Sixteen compiled controls plus baseline** (live 17/17 core-equal frozen `mutation-check-r1`, report SHA256 `2b37c498…126e`):

| Control | Rust | Independent primary | Class |
|---|---|---|---|
| `omit-kept-write-evaluation` | 101 | not run | Rust fail |
| `rewrite-kept-time-evidence` | 101 | not run | Rust fail |
| `keep-old-evidence-for-new-proof` | 101 | not run | Rust fail |
| `omit-required-new-evaluation` | 101 | not run | Rust fail |
| `reject-unused-invocation` | 101 | not run | Rust fail |
| `emit-legacy-version` | 101 | not run | Rust fail (schema 1 parsed as V2) |
| `optional-v2-authority` | 101 | `trust_record_` | Rust fail (shape optional) |
| `wrong-authority-collection` | 101 | `trust_record_` | Rust fail (Objects) |
| `wrong-authority-target-kind` | 101 | `trust_record_` | Rust fail (`StoreMarkerV1`) |
| `wrong-closure-source` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-before-image` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-before-clock` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-observation` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-store` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-byte-count` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-authority-context` | **0** | **rejected** | Rust-success / oracle-reject (capsule ref as authority) |

Matcher uniqueness 1 for all eleven producer replace-targets and both generated visitor/shape targets. No compile correction.

**Fixture corpora (independent counts, not renamed totals):** fragments **38048** inherited + **40** new = **38088** / **555** nodes; inherited validity flags **0** boolean changes vs `before-fixtures`. Records **326 / 219** positive. Extract **415 / 252** positive. Decode+targets **566 / 152** positive. Independent 312 Python `decode_edge` **566/566** match. Independent `extract` on owned roots: records **212/212**; extract **378/414** match, **36** remaining are native `limit=0` `edge-budget` rows (Python successor extract does not latch `edge_limit=0`; native cargo tests do). Full native corpus is the 253-test run, not the Python helper.

---

## Findings

### 1. V2 retained-P2 assembly — hold

Required `authority` is taken from owned `heads.root.admission`. Keep/NewRequired still build a fresh evaluation; NoWrite still ignores unused binding. Clock-event union routing matches 312 registry (136 sites). Legacy V1 shape remains parseable; this producer emits only V2.

### 2. Locator is not admission — hold

`Record::parse(S4EvaluationInputV2)` does not walk CoreAnchor, complete embedded chain, or 314 floor/tEval modes. P0/P1 producer and 312 `embedded_bytes` are absent, as stated.

### 3. Visitor/budget coverage — hold for native; Python helper limit=0 is not this freeze’s codec

Native `trust_record_` tests refuse optional V2 authority, wrong collection, wrong target kind, and `limit=0` edge-budget. Independent Python decode is exact. Do not treat the 312 helper’s `edge_limit=0` acceptance as a native 313 defect.

**Actionable defects in this freeze:** none that make the private V2 P2 assembler or generated 127/136 visitor self-contradictory with frozen 312.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 313 pins before extract | match |
| Nested 311 / 312 live tars / successor schema | SHA match; V1 def identical |
| `trust_time` / capture / OS sample / ordinary_targets | byte-identical to 311 |
| Live `cargo test -p opensip-security` | **253 passed / 2 ignored** after force rebuild |
| Clippy / fmt / rustfmt 11 includes | pass |
| Frozen host-r1 | 8/8 S4; 232; 12/4/8/75/145; schema 2 |
| Live host-live | 8/8; same split; **separate files** |
| 16 r1 mutants + baseline | 9 Rust 101; 7 Rust 0 + primary reject; core-equal frozen |
| Fragments / records / extract / decode | 38088 / 326/219 / 415/252 / 566/152 |
| 314 admitter / P0–P1 / embedded resolver / 222 | **not this freeze** |

---

## Remaining (do not count closed)

P0/P1 producer, 312 embedded-root resolver, 314 scoped AdmitTEval/AdmitFloor (including ADDENDUM continuity/context.time/S4.5-tEval corrections), old T/history admission, OLD/R/revocation, core bootstrap/batch, custody/fence/census/capacity, final age, 222 durability, post-S4 effects, writers, source selection, M3–M6. 305 1 s is still unqualified. Original full125 workflow modules remain unmodified on purpose.

---

## Verdicts

- [x] **313 as private 127-codec + retained-P2 V2 assembler:** archive verified; V1 preserved; V2 authority from owned P2 head admission; Keep/NoWrite as 311; 232 host decisions match 201/265+127; 16 controls distinguished; 253/2 ignored, Clippy, fmt11.
- [ ] **Not** original-authority admission, embedded-chain resolver, 314 admitter, publication, OS qualification, or product installation.
