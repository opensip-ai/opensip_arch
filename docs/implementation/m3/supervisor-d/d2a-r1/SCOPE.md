# D2a r1: the common control codec, `crates/components/src/control_protocol.rs` (M3-D r5 item 9)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 1.**

It implements the D2a plan r1 (`../d2a/PLAN-r1.md`; Codex `codex-d2a-plan-r1`, ACCEPT). NBO-1 and NBO-2 are carried in the lead assent:
- the encoder is fallible;
- the bound-plus-four limit is the raw frame buffer's only.

**Base:** product main `56d0eb5` (inventory v214, 173 contract successors).

## What it changes

| File | Change |
| --- | --- |
| `crates/components/src/control_protocol.rs` (new) | **The reader (LD-D2A-2).** `read_json` is an iterative RFC 8259 reader with an explicit container stack over a flat arena. Nothing recurses, and drop, debug and equality are iterative.<br>• Duplicates are compared on the decoded key.<br>• Strings are strict, and a string holding an unpaired surrogate escape is kept as UTF-16 units.<br>• Numbers follow the reference's lexeme rule: a fraction or exponent is a non-integer, more than sixteen digits stay a lexeme, otherwise an `i64`.<br>**The schema interpreter (LD-D2A-3).** The product schema `schemas/sources/control-v3.schema.json` is embedded with `include_str!` and evaluated by a closed interpreter of exactly its keywords, with Draft 2020-12 semantics: `type`, `const`, `enum`, `properties`, `required`, `additionalProperties: false`, the length bounds (in code points), `minimum`/`maximum`, `items`, `minItems`/`maxItems`, `uniqueItems` (structural equality), `allOf`, `if`/`then`/`else`, `not`, and the two known patterns as exact matchers. Loading refuses any other keyword or pattern.<br>**`classify(frame, &ControlContext) -> ControlVerdict`,** the reference's `parse`, in its order (LD-D2A-4):<br>• framing, decided from the prefix before any body;<br>• the frozen envelope;<br>• the unsupported-major hello, whose body stays opaque;<br>• the integer walk and the schema, on a validation copy with seq replaced by the sentinel 1 and the identities substituted;<br>• the UTF-8 walk on the received strings;<br>• the deferred seq fault;<br>• the state, direction, identity, tuple, nonce and effect checks.<br>An accepted frame carries the validated message as the generated `Control3Root`, built by hand through the generated `FromStr` constructors (no serde on wire bytes).<br>**`ControlContext`** holds the reference's sixteen members and the offered refusal major. **`ControlContext::for_session(&AdmittedSelection)`** is the production constructor: the 65,536 bound and offer, and the one admitted tuple (LD-D2A-1).<br>**`ControlSession`,** the two directions' sequences and stopping (LD-D2A-5): a frame on a stopped direction is RF7, unbuffered and unparsed, and stopped directions are reported in name order, as the reference sorts them.<br>**`encode(&Control3Root) -> Result<Vec<u8>, EncodeRefusal>`** writes the host's messages only. It refuses a hello without exactly one offer and a frame over the bound (NBO-1). **`host_hello`** and **`host_select`** build from an admitted selection only (LD-D2A-8). |
| `crates/components/src/lib.rs` | `pub mod control_protocol`; the scaffold text is revised. |
| `crates/components/Cargo.toml` | `opensip-contracts` as the one dependency edge (LD-D2A-9), and `opensip-identity` as a dev-dependency, to read the vendored corpus. Both are among the crate's permitted owners. |
| `Cargo.lock` | The two path edges for `opensip-components`; no external crate. |
| `crates/components/tests/control_protocol_tests.rs` (new) | 9 tests (below). |
| `crates/components/tests/data/control-completion.cases.v5.json`, `control-completion.rf5-proof.v2.json` (new) | Byte copies of the architecture's CC v5 corpus and RF5 proof, pinned by the test to the v5 freeze's SHA-256 (LD-D2A-7). |

## The tests

- **D2a-T1:** all 480 cases replay byte for byte against their expected outcome dicts, including the trace case through `ControlSession`. The corpus and the proof are pinned by SHA-256. `coverage/RF5-unreachable-preview` is checked as the reference states it.
- **D2a-T2:** the full 16 × 8 × 2 matrix, every state and direction holding all sixteen message types. This is stronger than the reference's distinct-triple count.
- **D2a-T3:** a zero prefix, or one over the bound (65,537, 131,073, 2^32 − 1), refuses with the body unbuffered; fewer than four bytes too; a body one short of its prefix refuses buffered.
- **D2a-T4:** on a thread with a 64 KiB stack, a frame of 65,000 nested arrays is decided (RF2) without recursion, and a 5,000-digit seq is RF7.
- **Supplementary:**
  - `-0` as seq is RF7, and as a body integer it is accepted as 0;
  - an unpaired surrogate inside a future-major hello's opaque body reaches RF1, and inside a known body it is RF2 (the reference's UTF-8 walk);
  - a duplicate member inside a body is RF2, both literally and as an escaped spelling of the same decoded key, and the body without it is accepted;
  - the production context is the 65,536 bound and offer and the one admitted tuple;
  - the host's hello and select, encoded, classify as accepted, and a decoded hello re-encodes to the same bytes;
  - a two-offer hello is refused by the encoder;
  - the embedded product schema loads with sixteen messages, and an uninterpreted keyword (`format`) or another pattern refuses the whole schema.

## Checks

Lane r1, attempt 3, `evidence/d2a-checks-r1/` (the lane of record):
- **Attempt 1** (`evidence/d2a-checks-r1-attempt1/`) passed every check but the base comparison's suite count (unnoticed until attempt 2; below) and two mutations:
  - `duplicate-member-accepted` survived: the corpus's two duplicate cases are top-level, where the envelope's exact four-member check refuses them too. A new test, `a_duplicate_member_in_a_body_is_rf2_on_the_decoded_key`, puts the duplicate inside a body, both literally and through an escape (`check.v5.py`:75 refuses a duplicate at any depth, in the parser).
  - `refusal-if-then-dropped` did not compile (the runner's replacement text was malformed). It now replaces the `if` arm with `true` and keeps the old arm under a dead name.
- **Attempt 2** (`evidence/d2a-checks-r1-attempt2/`) passed every check and all ten mutations except, again, the base comparison's suite count. The runner required the candidate to run as many test suites as the base, but the new test binary `tests/control_protocol_tests.rs` is one more suite. The comparison now requires exactly one more (`NEW_SUITES`), alongside equal failure sets and exactly 9 new passing tests.

- **the components suite** at base (no tests) and candidate: equal failure sets (none), exactly one new suite (the test binary) and 9 new passing tests;
- **rustfmt** on the new files and `lib.rs` (clean at base), and warning-denied all-targets Clippy on `opensip-components`;
- **the control protocol tests;**
- **CC v5's two source pins** (CPC v2 and permission-truth-tables v9, architecture files), checked against the corpus's own `sourcePins`. The 484 reference checks are therefore all accounted for: 482 natively and 2 in the lane (LD-D2A-7);
- **the package edges** (`tools/check_package_edges.py` under the O1-a package policy): components' internal edges are exactly `opensip-contracts` and the dev edge `opensip-identity`;
- **repository checks:** the environment exceptions, the operability source census (no new `from(`, `into(`, `line(`, `pid(` or `issue(` call), the census-closure check (no closure file changed) and verify_design;
- **ten mutations,** each failing the control protocol tests:
  - the seq fault applied early;
  - the sentinel not used;
  - the identities not substituted;
  - the UTF-8 walk run on the copy;
  - helloSeen unchecked;
  - the over-offer unchecked;
  - a duplicate member accepted;
  - a long integer converted;
  - refusal's if/then dropped;
  - a stopped direction parsed.

## Not claimed

- No caller (D3a), no process and no supervision.
- No provider protocol (D2b).
- No Linux-specific code and no qualification.
- D2's completion is not claimed.

## Inventory

`crates/components/src/control_protocol.rs` realizes its planned row ("Encode and validate common control frames without translating provider semantics."). New paths for the inventory after acceptance:
- `crates/components/tests/control_protocol_tests.rs`;
- the two vendored data files under `crates/components/tests/data/`.
