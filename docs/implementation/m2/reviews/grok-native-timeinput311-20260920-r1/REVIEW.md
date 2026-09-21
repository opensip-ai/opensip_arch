# Independent review — private S4 write evaluation 311

**Standing:** bounded native-Rust review of frozen `native-time-input-checkpoint-311`. Private `prepare` now constructs a fresh full-125 `S4EvaluationInputV1` for **every write-bearing** S4 decision, including Keep-old-T. `Plan::NoWrite` still ignores an unused invocation. This is existing 227 TIME-INPUT-JOINS law, not a schema/kernel/public-grant change. It does **not** admit old T/history/root/closure dependencies, persist, reserve capacity, produce a complete proof/receipt, or publish. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Prior 309 and 310 reports were not edited (310 fully read, including ADDENDUM withdrawal of the two §3 joins). Root is authoring a **separate** unselected successor codec 312 with explicit versioning and original evaluation core context; **no** product installation in this freeze.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/host/mutant directories were not overwritten. No workspace rerun. No load/suspend/VM/proof-prep/namespace qualification.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **8953260 B, 957 members, SHA256 `5c8d692ef6bed440fc8ed382e4277396c3ebb59cfc86cd934a706e38a519b87d`**. Standing: private unselected311 fresh S4 evaluation for every clock write; no proof admission/durability or publication qualification. Extract rehashed **957/957**. Product-inputs **463/463**. Nested 309 pin `0f78bc97…e7ba` (live tar match). `kernel201.py` `df45c9c5…2299`; `shape_join_model227.py` `781061b6…cdf2`. Whole `trust_time.rs` **byte-identical** to 309 (`b76c829f…1dc4f`). `clock_observation.rs`, `captured_capsule_clock.rs`, `trust.rs` (`d513ccac…5721`), and `lib.rs` (`28977259…3469`) byte-identical to 309. `lib.rs` has **no** public export; `include!("trust/proposed_time_input.rs")` remains private inside `trust.rs`. Product vs 309: **463** files, **461** unchanged. Changed: `trust/proposed_time_input.rs` `fb54a959…19d3`, `ordinary_targets.rs` `dfc6b339…d857` (TEST-ONLY host hook: `TIME311` prefix and Keep-as-write). `proposed-time-input-before.rs` equals 309 `proposed_time_input.rs`; `ordinary-targets-before.rs` equals 309 `ordinary_targets.rs` (`0ec5c40b…3a3d`). Full-125 copies (`trust-capsule-shapes.v1.json` `1328ba16…4208`, `trust_input_reference.py` `13491b74…4393`, `trust_record_reference.py` `00ad3a34…e6df`) byte-identical to frozen 309. Invocations fixture still `time-invocations309.ndjson` (29 rows, 4 valid, SHA256 `58f2403b…a5ce`).

227 r9 `TIME-INPUT-JOINS.md` is **not** in the 311 extract (`verified-inputs/codec227r9/` holds only `CODECS.md` / `README.md` / `shape_join_model.py`). This review used the independently verified 310 packet copy SHA256 `912110ffd81b0080ed64530ab1290e774ce9261a463852c4229cfa8b91cda2d6`.

Preserved unchanged: 309 REVIEW SHA256 `6a47037d3743ebc03cd36f6c6aeb068fb267154cf957f96863814fc990caeb67`; 310 REVIEW `fb443e047561b5fd08bfaa023fc7c15689ec41680e1ca41265502d76bf305b33`, FOLLOWTHROUGH `1c8c2acee3dbefb80c7a7397d7e02e5d46e08bdf91e7741458bd8fe48b8f456b`, ADDENDUM `6d7c499ddb097939a2f0503f2e2a07e030b9c58084579ea8c3145179f9c845a9`.

---

## What the assembler does

`prepare(&CurrentOrdinaryProposal, invocation)` still borrows the whole 308 proposal. Branch is existing 301 `proof_retention`:

- **NoWrite:** `Plan::NoWrite`. **Does not inspect** `invocation`.
- **Keep and NewRequired:** both construct a closed `{inputSchema:1, kind:s4-evaluation, invocation, store, beforeImage, beforeClock, observation, source:{kind:ordinary, closure}}` from the **owned** capsule NodeRef / store / complete `capsule.clock`, the **exact** S4 recording document, and a NodeRef of `closure_raw()`. Canonicalize, `Record::parse(S4EvaluationInputV1, raw, 131072)`, own raw Record + SHA/length NodeRef. Result is `Plan::Write(WriteInput)`. `ProposedInput` **borrows** the proposal (`ptr::eq` in the host hook).

`WriteInput` private fields: `evaluation: ProposedInput` (always the fresh node) and `retained: Option<&V>` (exact original T NodeRef on Keep, `None` on NewRequired). `evaluation()` always returns that fresh node. `time_evidence()` returns the **exact** original T for Keep and the new evaluation NodeRef for NewRequired. No old-T rewrite. No equal-L provenance substitution.

Host expected-ok is `retention == "NoWrite" || boolean(&b["valid"])`. Keep **must** validate closed-shape `InvocationBinding`. Do **not** repeat the 309 unused-binding claim for Keep. NoWrite alone still ignores an unused invalid binding, preserving the already-evaluated refusal.

Those eight members remain exactly the 125 `S4EvaluationInputV1` required set (`additionalProperties: false`). Closed `InvocationBinding` shape is **not** live execution identity. Typed reader extracts dependency edges; this producer does not walk or authenticate them. Node creation is not original-context admission, durable proof, or permission to publish.

227 TIME-INPUT-JOINS: a durable clock-write’s evaluation must admit a successful non-report-only kernel decision; **new T iff `lastAccepted` is written**; equal/older sources **keep prior T**; BEGIN/COMMIT create a **fresh evaluation input under CURRENT context** even when retained payload bytes are identical. 309 `Plan::Keep` constructed no evaluation record and was incomplete as a publication input producer. 311 is that missing 227 distinction on the existing V1 record.

S4/S4.5 arithmetic is unchanged. No filesystem write. Keep still needs original provenance admission before operational publication.

**Executed:** `cargo clean -p opensip-security` then **253 passed / 0 failed / 2 ignored** with `Compiling opensip-security` (`Finished` 11.00s; tests 12.12s). Ignored: 305 host observation pilot and this 311 actual-host composition. Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **eleven** include files.

**Host samples (separate from frozen `host-r1`):** 8 actual 308 samples × 29 invocation values = **232** decisions. Independent 201/265 `clock_decision` plus 227 `S4EvaluationInputV1` / source-exact SHA/length assembly.

- Historical replay of frozen `host-r1/observed.ndjson`: **8/8** S4 match (1 NewRequired / 2 Keep / 5 NoWrite); **12** evaluation records (**4** new-T, **8** kept-T), **75** invalid-binding, **145** NoWrite. Frozen stdout SHA256 `f2909c93…df14` unchanged.
- Live `grok-out/io/host-live/`: new samples, **8/8** and the same 232/12/4/8/75/145 split this wall. Frozen `host-r1` not overwritten. Counts are **this wall**. 302 1 s remains unqualified.

**Eleven compiled host controls plus baseline:**

| Control | Rust | Independent primary | Class |
|---|---|---|---|
| `omit-kept-write-evaluation` | 101 | not run | Rust fail (Keep→NoWrite) |
| `rewrite-kept-time-evidence` | 101 | not run | Rust fail (Keep T rewritten to new node) |
| `keep-old-evidence-for-new-proof` | 101 | not run | Rust fail (NewRequired T stays old) |
| `omit-required-new-evaluation` | 101 | not run | Rust fail (NewRequired→NoWrite) |
| `reject-unused-invocation` | 101 | not run | Rust fail (Null refused before NoWrite) |
| `wrong-closure-source` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-before-image` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-before-clock` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-observation` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-store` | **0** | **rejected** | Rust-success / oracle-reject |
| `wrong-byte-count` | **0** | **rejected** | Rust-success / oracle-reject |

The six field mutants do **not** fail cargo: the host hook serializes whatever Write produced. Independent 125/source-exact comparison rejects them. Live 12/12 core-equal frozen `mutation-check-r1` (`report.json` SHA256 `e4cedad0ac723d195f52fef2330aa8c860a4f457da2a32d640aca1899c1a8eea`). Nine replace-targets each occur once. No compile correction.

---

## Findings

### 1. Keep now builds an evaluation — hold for this private API

Every write constructs a fresh V1 evaluation and requires a valid binding. Selected `timeEvidence` is the prior T on Keep and the new node on NewRequired. That is 227 publication-input law, not a new schema. It is **not** a host admission of a live request. Future publishers must still validate invocation independently.

### 2. Record fields vs 125/227 — hold

Required members match `S4EvaluationInputV1`. Observation is the exact S4 recording. Closure NodeRef is hashed from owned raw, not a caller-supplied digest. Store/beforeClock/beforeImage are taken from the captured P2 image, not invented.

### 3. Not provenance, not 310, not 312

NodeRef does not prove durability or authority. No walk of old T, history, root, or closure dependencies. 311 does **not** close 310’s P0/P1 CoreAnchor locator gap (ADDENDUM: that gap stands; the two withdrawn §3 joins are not reopened here). 311 does **not** author a successor input schema; 312 is a separate unselected codec proposal.

**Actionable defects in this freeze:** none that make the private write-evaluation assembler self-contradictory.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 311 pins before extract | match |
| Nested 309 / `trust_time` / capture / 307 clock / full125 | byte-identical / pin match |
| 227 TIME-INPUT-JOINS | 310 packet copy `912110ff…a2d6`; absent from 311 extract |
| Live `cargo test -p opensip-security` | **253 passed / 2 ignored** after force rebuild |
| Clippy / fmt / rustfmt 11 includes | pass |
| Frozen host-r1 | 8/8 S4; 232 decisions; 12/4/8/75/145 |
| Live host-live | 8/8; 232; 12/4/8/75/145; **separate files** |
| 11 r1 mutants + baseline | 5 Rust 101; 6 Rust 0 + primary reject; core-equal frozen |
| 1 s / publication / P0–P1 core / 312 | **not this freeze** |

---

## Remaining (do not count closed)

Old T/history/current-head admission, OLD/R/revocation population, core bootstrap/batch, namespace/custody/fences/census, capacity, final age guard, 222 durability, post-S4 minima/completeness/role effects, writers, source selection, M3–M6, 310’s unresolved owners (later-root envelope encoding, same-store core change in P0/P1, which freeze owns a successor S4 input version), and 312 successor codec authorship remain open. 305 1 s is still unqualified. 311 remains a retained-P2 input proposal only.

---

## Verdicts

- [x] **311 as private write-bearing evaluation assembler:** archive verified; existing 125 record only; Keep and NewRequired both construct a fresh evaluation; Keep validates binding; NoWrite ignores unused binding; `time_evidence` vs `evaluation` split matches 227; 232 host decisions match 201/265+125; six field mutants distinguished as Rust-success/oracle-reject; 253/2 ignored, Clippy, fmt11.
- [ ] **Not** complete or durable provenance, current-head proof, invocation identity, publication, OS qualification, completeness, grant, 310 locator close, 312 successor codec, or product installation.
