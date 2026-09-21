# Independent review — candidate S4 time-input record 309

**Standing:** bounded native-Rust review of frozen `native-time-input-checkpoint-309`. Private `prepare` **assembles** the existing full-125 `S4EvaluationInputV1` candidate from a borrowed 308 `CurrentOrdinaryProposal`. It does **not** admit old T/history/root/closure dependencies, persist, reserve capacity, produce a complete proof/receipt, or publish. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Prior 298–308 reports were not edited (308 fully read and left archived). This freeze does not add P0/P1 core-anchor wire data (assistance 310 is separate).

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/host/mutant directories were not overwritten. No workspace rerun. No load/suspend/VM/proof-prep/namespace qualification.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **9021492 B, 951 members, SHA256 `0f78bc97147af21567173761195e057e0b4ff05f48ebce6386f118bfdff4e7ba`**. Standing: private unselected309 candidate S4 time-input record; no proof admission/durability or publication qualification. Extract rehashed **951/951**. Product-inputs **463/463**. Nested 308 pin `ac8d73b9…6c25` (live tar match). `kernel201.py` `df45c9c5…2299`; `shape_join_model227.py` `781061b6…cdf2`. Whole `trust_time.rs` **byte-identical** to 308 (`b76c829f…1dc4f`). `clock_observation.rs` and `captured_capsule_clock.rs` byte-identical to 308. `lib.rs` unchanged; **no** public export. Product vs 308: **463** files, **459** unchanged. Changed: `trust.rs` `d513ccac…5721` (private `include!("trust/proposed_time_input.rs")`), `ordinary_targets.rs` `0ec5c40b…3a3d` (`closure_raw` / retained `time_evidence` accessors plus TEST-ONLY host hook). Added: `trust/proposed_time_input.rs` `fe9a39af…3565`, `time-invocations309.ndjson` (29 rows, 4 valid, SHA256 `58f2403b…a5ce`). `trust-before.rs` and `ordinary-targets-before.rs` equal 308.

---

## What the assembler does

`prepare(&CurrentOrdinaryProposal, invocation)` borrows the whole 308 proposal (image + 301 input + OS sample). Branch is existing 301 `proof_retention`:

- **NoWrite:** `Plan::NoWrite`. **Does not inspect** `invocation`.
- **Keep:** `Plan::Keep` of `inputs().time_evidence()` — the exact original T NodeRef on retained phase. **Does not inspect** `invocation`.
- **NewRequired:** builds closed `{inputSchema:1, kind:s4-evaluation, invocation, store, beforeImage, beforeClock, observation, source:{kind:ordinary, closure}}` from the **owned** capsule NodeRef / store / complete `capsule.clock`, the **exact** S4 recording document, and a NodeRef of `closure_raw()` (already-owned authenticated metadata-closure bytes). Canonicalize, `Record::parse(S4EvaluationInputV1, raw, 131072)`, own raw Record + SHA/length NodeRef. `ProposedInput` **borrows** the proposal (`ptr::eq` in the host hook).

Those eight members are exactly the 125 `S4EvaluationInputV1` required set (`additionalProperties: false`). `beforeImage`/`beforeClock` come from the same captured capsule (join by construction, not an independent re-read). Invocation is the only supplied new value; closed `InvocationBinding` shape is **not** live execution identity. Typed reader extracts dependency edges; this producer does not walk or authenticate them.

**NoWrite/Keep unused-binding behavior:** an irrelevant malformed argument cannot replace an already-evaluated no-write/Keep or force a new proof. That is private candidate-API behavior. A future host must still admit the actual invocation on its own. `reject-unused-invocation` (pre-match `Null` refuse) is caught as a Rust failure because Keep/NoWrite would then fail the `prepared.is_ok()` assertion.

S4/S4.5 arithmetic is unchanged. No equal-L provenance rewrite. No filesystem write. Keep still needs original provenance admission before operational publication.

**Executed:** `cargo clean -p opensip-security` then **253 passed / 0 failed / 2 ignored** with `Compiling opensip-security`. Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **eleven** include files.

**Host samples (separate from frozen `host-r1`):** 8 actual 308 samples × 29 invocation values = **232** decisions. Independent 201/265 `clock_decision` plus 227 `S4EvaluationInputV1` / source-exact SHA/length assembly.

- Historical replay of frozen `host-r1/observed.ndjson`: **8/8** S4 match (1 NewRequired / 2 Keep / 5 NoWrite); **4** new records, **25** invalid-binding (NewRequired only), **58** Keep, **145** NoWrite. Frozen stdout SHA256 `73a8a349…84c9` unchanged.
- Live `grok-out/io/host-live/`: new samples, **8/8** and the same 232/4/25/58/145 split this wall. Frozen `host-r1` not overwritten. Counts are **this wall**. 302 1 s remains unqualified.

**Nine compiled host controls:**

| Control | Rust | Independent primary | Class |
|---|---|---|---|
| `drop-required-keep` | 101 | not run | Rust fail (Keep→NoWrite) |
| `turn-no-write-into-keep` | 101 | not run | Rust fail (NoWrite→Keep) |
| `reject-unused-invocation` | 101 | not run | Rust fail (malformed used on Keep/NoWrite) |
| `wrong-closure-source` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-before-image` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-before-clock` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-observation` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-store` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-byte-count` | **0** | **rejected** | Rust-success / oracle-reject |

The six field mutants do **not** fail cargo: the host hook serializes whatever NewRequired produced. Independent 125/source-exact comparison rejects them. Live 9/9 core-equal frozen `mutation-check-r1` (`report.json` SHA256 `40c696af…c133`). No compile correction.

---

## Findings

### 1. Branch behavior — hold for this private API

Keep/NoWrite ignoring unused invocation is the stated law and is mutant-covered. It is **not** a host admission of a live request. Future publishers must still validate invocation independently.

### 2. Record fields vs 125/227 — hold

Required members match `S4EvaluationInputV1`. Observation is the exact S4 recording. Closure NodeRef is hashed from owned raw, not a caller-supplied digest. Store/beforeClock/beforeImage are taken from the captured P2 image, not invented.

### 3. Not provenance

NodeRef does not prove durability or authority. No walk of old T, history, root, or closure dependencies. No P0/P1 core-anchor claim.

**Actionable defects in this freeze:** none that make the private candidate assembler self-contradictory.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 309 pins before extract | match |
| Nested 308 / `trust_time` / capture / 307 clock | byte-identical / pin match |
| Live `cargo test -p opensip-security` | **253 passed / 2 ignored** after force rebuild |
| Clippy / fmt / rustfmt 11 includes | pass |
| Frozen host-r1 | 8/8 S4; 232 decisions; 4/25/58/145 |
| Live host-live | 8/8; 232; 4/25/58/145; **separate files** |
| 9 r1 mutants | 3 Rust 101; 6 Rust 0 + primary reject |
| 1 s / publication / P0–P1 core | **not this freeze** |

---

## Remaining (do not count closed)

Old T/history/current-head admission, OLD/R/revocation population, core bootstrap/batch, namespace/custody/fences/census, capacity, final age guard, 222 durability, post-S4 minima/completeness/role effects, writers, source selection, M3–M6, and whether a first P0/P1 time proof has a reachable immutable core anchor (310) remain open. 305 1 s is still unqualified.

---

## Verdicts

- [x] **309 as private candidate assembler:** archive verified; existing 125 record only; Keep/NoWrite ignore unused binding; NewRequired fields from owned 308 proposal; 232 host decisions match 201/265+125; six field mutants distinguished as Rust-success/oracle-reject; 253/2 ignored, Clippy, fmt11.
- [ ] **Not** complete or durable provenance, current-head proof, invocation identity, publication, OS qualification, completeness, grant, or product installation.
