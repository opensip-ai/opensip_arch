# D2a r2: the common control codec, `crates/components/src/control_protocol.rs` (M3-D r5 item 9)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 2.** Round 2 answers Codex `codex-d2a-r1` (REQUIRED-FINDINGS: three RFs, two NBOs). The r1 package (`../d2a-r1/`) is history.

## r2 changes

| Finding | Change | Controls |
| --- | --- | --- |
| **RF-1** (component messages encoded as empty bodies) | `encode` refuses each of the component's eight message types (`helloAck`, `selectAck`, `pong`, `healthReport`, `resourceReport`, `fault`, `shutdownAck`, `effectRequest`) with `EncodeRefusal::ComponentMessage(type)` before writing a byte. Their arm in the body writer is now unreachable, so there is one guard. | `the_encoder_writes_every_host_type_and_refuses_every_component_type`: one corpus-accepted message of each of the sixteen types; the eight host types encode to frames their receiver accepts, and the eight component types refuse. The mutation `component-message-encoded`. |
| **RF-2** (constructed output not validated) | The written body is judged as its receiver would judge it, with **no identity substitution**: strict JSON, the integer domain (`0..=2^53 − 1`), the message's closed schema member (its patterns and the refusal's `RF-1`/`RF-6` conditionals included), and every string's UTF-8 bound (`EncodeRefusal::Invalid`). A null optional member refuses (`NullMember`) instead of being silently dropped. The frame bound is checked by `bounded` (exactly 65,536 fits). **`ControlSession::send`** is the selection-bound sending boundary: a hello must carry exactly the policy's identities, platform, offer and offered tuples, and a select one of the offered tuples (`Policy`); then the session must accept the frame as the host's next (`Session(family)`). Only then is the session advanced. A refused send sends and advances nothing. | `the_encoder_refuses_what_its_receiver_would_refuse`: a 128 × `é` nonce (256 bytes); `requestSeq` at 2^53 − 1 and 2^53; RF-6 with and without `decisionClass`, RF-1 with and without `supportedControlMajors`, RF-2 with either; a null `detail`; a hello whose stable id is not a lowercase UUID; the bound exactly and one over. `a_production_session_sends_only_its_policy_and_its_next_lawful_frame`. The mutations `output-not-validated`, `null-member-dropped` and `policy-offer-unchecked`. |
| **RF-3** (the production policy is not enforceable) | `ControlContext` is now a private **`ControlPolicy`** (the bound and offer, the identities and platform, the manifest and offered tuples, the offered refusal major) beside the public **`ControlObservations`** (state, direction, helloSeen, next seq, confirms, selection, nonces, effect evidence). `ControlContext::for_session` is the only constructor outside the module's tests; the policy is read through getters; `ControlSession::observations_mut` replaces `context_mut` and cannot reach the policy. The corpus's contexts, which carry bounds production never makes, are built by a `#[cfg(test)]` `ControlContext::reference`, so the corpus tests moved in-crate, to `crates/components/src/control_protocol_tests.rs`. | Three compile-fail doc tests: a policy cannot be written whole, a copy of one cannot be widened, and a context cannot be assembled around another policy. Each fails only for privacy: with the fields public, all three compile (checked by the mutation `policy-made-public`). The production-context test reads the policy through its getters. |
| **NBO-1** (root keywords) | `Schema::load` closes the document root too: `$schema`, `$id`, `title` and `oneOf` only. | `an_unknown_root_keyword_refuses_the_schema`; the mutation `root-keyword-ignored`. |
| **NBO-2** (prefix classification versus stream acquisition) | Recorded, not changed: `classify` and `receive` take a complete borrowed frame. Their prefix branches inspect and allocate no body, but `body_buffered: false` is a classification result, not evidence that a transport read stopped at four bytes. Bounded acquisition from a stream (a counting reader, split and coalesced frames) is D3a's, at its integration with the supervisor's reader. D2a-T3 claims no more than the classification. | — |

It implements the D2a plan r1 (`../d2a/PLAN-r1.md`; Codex `codex-d2a-plan-r1`, ACCEPT). NBO-1 and NBO-2 are carried in the lead assent:
- the encoder is fallible;
- the bound-plus-four limit is the raw frame buffer's only.

**Base:** product main `56d0eb5` (inventory v214, 173 contract successors).

## What it changes

| File | Change |
| --- | --- |
| `crates/components/src/control_protocol.rs` (new) | **The reader (LD-D2A-2).** `read_json` is an iterative RFC 8259 reader with an explicit container stack over a flat arena. Nothing recurses, and drop, debug and equality are iterative.<br>• Duplicates are compared on the decoded key.<br>• Strings are strict, and a string holding an unpaired surrogate escape is kept as UTF-16 units.<br>• Numbers follow the reference's lexeme rule: a fraction or exponent is a non-integer, more than sixteen digits stay a lexeme, otherwise an `i64`.<br>**The schema interpreter (LD-D2A-3).** The product schema `schemas/sources/control-v3.schema.json` is embedded with `include_str!` and evaluated by a closed interpreter of exactly its keywords, with Draft 2020-12 semantics: `type`, `const`, `enum`, `properties`, `required`, `additionalProperties: false`, the length bounds (in code points), `minimum`/`maximum`, `items`, `minItems`/`maxItems`, `uniqueItems` (structural equality), `allOf`, `if`/`then`/`else`, `not`, and the two known patterns as exact matchers. Loading refuses any other keyword or pattern.<br>**`classify(frame, &ControlContext) -> ControlVerdict`,** the reference's `parse`, in its order (LD-D2A-4):<br>• framing, decided from the prefix before any body;<br>• the frozen envelope;<br>• the unsupported-major hello, whose body stays opaque;<br>• the integer walk and the schema, on a validation copy with seq replaced by the sentinel 1 and the identities substituted;<br>• the UTF-8 walk on the received strings;<br>• the deferred seq fault;<br>• the state, direction, identity, tuple, nonce and effect checks.<br>An accepted frame carries the validated message as the generated `Control3Root`, built by hand through the generated `FromStr` constructors (no serde on wire bytes).<br>**`ControlContext`** holds the reference's sixteen members and the offered refusal major, as the private `ControlPolicy` and the public `ControlObservations` (r2). **`ControlContext::for_session(&AdmittedSelection)`** is the production constructor: the 65,536 bound and offer, and the one admitted tuple (LD-D2A-1).<br>**`ControlSession`,** the two directions' sequences and stopping (LD-D2A-5): a frame on a stopped direction is RF7, unbuffered and unparsed, and stopped directions are reported in name order, as the reference sorts them.<br>**`encode(&Control3Root) -> Result<Vec<u8>, EncodeRefusal>`** writes the host's eight message types only, and validates what it writes (r2). It refuses a hello without exactly one offer and a frame over the bound (NBO-1). **`ControlSession::send`** (r2) sends only the policy's hello and select and the session's next lawful host frame. **`host_hello`** and **`host_select`** build from an admitted selection only (LD-D2A-8). |
| `crates/components/src/lib.rs` | `pub mod control_protocol`; the scaffold text is revised. |
| `crates/components/Cargo.toml` | `opensip-contracts` as the one dependency edge (LD-D2A-9), and `opensip-identity` as a dev-dependency, to read the vendored corpus. Both are among the crate's permitted owners. |
| `Cargo.lock` | The two path edges for `opensip-components`; no external crate. |
| `crates/components/src/control_protocol_tests.rs` (new) | 13 tests (below), in-crate since r2 (round 1's `crates/components/tests/control_protocol_tests.rs` is gone). |
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
  - the production context is the 65,536 bound and offer and the one admitted tuple, read through the policy's getters;
  - **(r2)** the encoder's host and component types, its validation, and the session's sending boundary (above);
  - **(r2)** an unknown root keyword refuses the schema;
  - the host's hello and select, encoded, classify as accepted, and a decoded hello re-encodes to the same bytes;
  - a two-offer hello is refused by the encoder;
  - the embedded product schema loads with sixteen messages, and an uninterpreted keyword (`format`) or another pattern refuses the whole schema.

## Checks

Lane r2, `evidence/d2a-checks-r2/`, on base `56d0eb5`:
- **the components suite** at base (no tests) and candidate: equal failure sets (none), the same two suites (the lib's and the doc tests'), and 16 new passing tests (13 unit, 3 compile-fail doc tests);
- **rustfmt** on the new files and `lib.rs` (clean at base), and warning-denied all-targets Clippy on `opensip-components`;
- **the control protocol tests** (the whole package: lib and doc tests);
- **CC v5's two source pins** (CPC v2 and permission-truth-tables v9, architecture files), checked against the corpus's own `sourcePins`. The 484 reference checks are therefore all accounted for: 482 natively and 2 in the lane (LD-D2A-7);
- **the package edges** (`tools/check_package_edges.py` under the O1-a package policy): components' internal edges are exactly `opensip-contracts` and the dev edge `opensip-identity`;
- **repository checks:** the environment exceptions, the operability source census (no new `from(`, `into(`, `line(`, `pid(` or `issue(` call), the census-closure check (no closure file changed) and verify_design;
- **sixteen mutations,** each failing the control protocol tests:
  - round 1's ten: the seq fault applied early; the sentinel not used; the identities not substituted; the UTF-8 walk run on the copy; helloSeen unchecked; the over-offer unchecked; a duplicate member accepted; a long integer converted; refusal's if/then dropped; a stopped direction parsed;
  - **(r2)** a component message encoded; the written frame not validated; a null member dropped; the session's frame offer unchecked; the policy made public; the root keywords not closed.

Round 1's lane and its three attempts (`../d2a-r1/evidence/`) are history.

## Not claimed

- No caller (D3a), no process and no supervision.
- **(r2)** No bounded acquisition from a stream: the codec classifies complete borrowed frames (NBO-2; D3a's).
- No provider protocol (D2b).
- No Linux-specific code and no qualification.
- D2's completion is not claimed.

## Inventory

`crates/components/src/control_protocol.rs` realizes its planned row ("Encode and validate common control frames without translating provider semantics."). New paths for the inventory after acceptance:
- `crates/components/src/control_protocol_tests.rs` (r2; round 1's `tests/` path is not added);
- the two vendored data files under `crates/components/tests/data/`.
