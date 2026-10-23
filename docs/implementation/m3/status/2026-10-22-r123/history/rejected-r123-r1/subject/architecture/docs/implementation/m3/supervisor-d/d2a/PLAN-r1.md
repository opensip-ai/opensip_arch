# D2a implementation plan r1: the control codec, `crates/components/src/control_protocol.rs` (M3-D item 9)

**Lead plan, 2026-10-16. Proposed; it needs Codex review.**

**Bases:**
- product main `56d0eb5` (inventory v214; 173 contract successors);
- architecture as the subject manifest names.

**What precedes it.** D2a's row in M3-D r5's units table is "`components/control_protocol.rs`: item 9, with the CC v5 corpus", depending on P0 (met). Its order is D1a → D2a ∥ D2b → D3a.
- **D1a** is accepted and integrated (`e4e7158`, inventory v213).
- **D2a** does not depend on D1a. It is a pure codec: no process, descriptor or file is opened.
- **Its consumer** is D3a's supervisor, later.

**Authority:**
- **The law:** M3-D r5 item 9 (`supervisor-d/PROPOSAL.md`, "`control_protocol.rs`: CC v5 exactly, and the select tuple"), with controls D2a-T1 to T4, and item 11 ("no translation"), which bounds what the codec may do.
- **CC v5:** `docs/coop/completion/control-completion.contract.v5.md`.
- **The reference corpus and checker** (`control-completion.cases.v5.json`, `.check.v5.py`, `.rf5-proof.v2.json`, `.report.v5.json`, `.freeze.v5.json`), which pin each other, and **CPC** (`docs/coop/artifacts/control-protocol-contract.v2.json`).
- **The product schema** `schemas/sources/control-v3.schema.json`. It is byte-identical to `control-completion.schema.v3.json` (sha256 `2929de62…ac46a98c`, pinned by `admission-registry.json`), with its generated `Control3Root` (`crates/contracts/src/generated/protocol.rs:10`).

## 0. What D2a delivers, and what it does not

**Delivers** `crates/components/src/control_protocol.rs`, library only, with no caller until D3a:
- **The reader:** a bounded, iterative, first-party JSON reader for one control frame body.
- **The classifier:** `classify(frame: &[u8], context: &ControlContext) -> ControlVerdict`. It decides one received frame exactly as CC v5's reference does: the framing, the reader's refusals, the closed schemas of the sixteen messages, the UTF-8 byte bounds, RF precedence with both repairs, the eight states and their 256 cells, and the identity, tuple, nonce and effect correlations. An accepted verdict carries the validated message as the generated `Control3Root`, built by hand from the reader's values (serde never reads wire bytes).
- **The session driver:** `ControlSession`, the two directions' sequence and stopping rule (CC:137-140; CPC:274), which is the reference's `run_session`.
- **The encoder:** `encode(&Control3Root) -> Vec<u8>` for the host's own frames. It is a first-party writer of the closed fields, with a 4-byte big-endian prefix. Its output must classify as ACCEPT in the matching state, which a test checks for every message.
- **The host's hello and select** (item 9's lead decisions), built only from an admitted selection's values:
  - `hello` with `expectedStableId`, `admittedManifestDigest`, `platform {os, arch}`, the offer 65,536 and exactly one tuple;
  - `select` naming that same tuple.
- **The vendored corpus** and its byte-exact replay (D2a-T1).

**Not delivered:**
- the supervisor (D3a), the session factory and manifest admission (D4), and every process concern;
- the provider protocols (D2b);
- the SD-2 manifest-owner record (item 29's successor);
- Linux-specific code (none is needed: the codec is platform-free).

## 1. Lead decisions

- **LD-D2A-1. A pure classifier over an explicit context, with the policy constants outside it.**
  - **Why a context.** The corpus decides each frame against a context of sixteen members: state, direction, helloSeen, frameBound, frameOffer, nextSeq, the identities, platform, the tuple sets, pending nonces, and the authorization and outcome evidence. Byte-exact replay therefore needs those as inputs.
  - **The context.** `ControlContext` holds exactly those sixteen, plus `offeredControlMajor`, which one case uses. The codec holds no session policy of its own.
  - **Production values.** Item 9's constants are supplied by the session: the bound and offer 65,536, the single tuple, and the identities from the admitted selection. `ControlContext::for_session(selection)` builds them, and is the only production constructor. The corpus builds contexts through a test-only constructor.
  - **Why the bound is a parameter.** The corpus needs frame bounds of 131,072 and 16,777,216 (eight FRAMING cases) to replay exactly. The law fixes production at 65,536, so the bound is a context parameter and the 65,536 policy is enforced by the production constructor.
- **LD-D2A-2. The reader** (item 9's "own bounded reader"; CC:187-195):
  - **No recursion.** An explicit container stack, bounded by the frame's bytes, builds a flat arena of values. Nothing recurses: there is no recursive descent, no recursive `Drop` (the arena is a `Vec`), no recursive `Debug` and no recursive equality. A 64 KiB frame of `[` is therefore one bounded allocation, not a stack overflow (D2a-T4).
  - **Strict input.** The body must be strict UTF-8 first; failure is RF2. Whitespace is space, tab, CR and LF only, so a BOM is RF2. Trailing commas, missing colons, multiple roots and trailing garbage are refused.
  - **Duplicates** are compared on the **decoded** key, at every depth, so `"a"` and `"a"` are duplicates.
  - **Strings.** Escapes are strict, and raw control characters are refused. A string is kept as UTF-16 code units when it holds an unpaired surrogate escape. Such a string is not an error at parse time: it is refused (RF2) only where the reference's UTF-8 walk reaches it. Inside an unsupported-major hello's opaque body it therefore reaches RF1, as the reference does (`check.v5.py:29-30`, `:125-131`).
  - **Numbers** follow the reference's lexeme rule (`check.v5.py:39`, `:93-94`):
    - a token with `.`, `e` or `E` is a non-integer;
    - one with more than sixteen digits (ignoring the sign) stays a lexeme;
    - otherwise it is an `i64` integer, with `-0` as 0.
- **LD-D2A-3. The product schema itself is the validator, through a closed interpreter.** The workspace's policy has no JSON Schema crate, and the reference's schema use is not plain validation: it dispatches on `type`, substitutes the context's identities first, and enforces `x-maxUtf8Bytes` (a non-standard keyword with a 1,024-byte default) in a separate walk.
  - **The interpreter.** D2a embeds `schemas/sources/control-v3.schema.json` (`include_str!`) and evaluates each message's `oneOf` member with a small interpreter. It implements Draft 2020-12's semantics for exactly the keywords that schema uses: `type`, `const`, `enum`, `properties`, `required`, `additionalProperties: false`, `minLength`/`maxLength` (code points), `minimum`/`maximum`, `items`, `minItems`/`maxItems`, `uniqueItems` (structural equality), `allOf`, `if`/`then`/`else` and `not`.
  - **Patterns.** `pattern` is supported for the schema's two patterns only (the lowercase UUID and the 64-hex digest, each anchored at both ends), as exact matchers. Under the reference's substitution, both apply only to the context's own values.
  - **Closed loading.** Loading the schema refuses any other keyword or pattern, so a schema change fails the tests rather than being silently ignored. `title`, `$schema` and `$id` are inert. `x-maxUtf8Bytes` is read by the UTF-8 walk.
  - **The typed result.** The accepted message is then built by hand into the generated `Control3Root`, through its own `FromStr` constructors. The generated types are never deserialized from wire bytes.
- **LD-D2A-4. Precedence exactly as the reference orders it** (`check.v5.py:107-180`):
  - framing;
  - the reader;
  - the frozen envelope;
  - the unsupported-major path (with its five ordered checks, ending in RF1);
  - the structural checks, run on a validation copy with seq set to the sentinel 1 and the identities substituted, then the UTF-8 walk over the original body;
  - the deferred seq fault (RF7; CCR-1, CCR4-1);
  - the state and semantic checks in their thirteen-step order.

  **Recorded readings,** where the corpus decides against a plain reading of CC's prose:
  - hello in CLOSED and FAULTED is RF8, not RF7, because helloSeen is checked before the state;
  - helloAck over the offer is RF2, ranked after RF3 and RF4.
- **LD-D2A-5. Direction stopping is the session driver's.** `classify` decides one frame; `ControlSession` owns the two directions' sequences and stopping:
  - a frame on a stopped direction is RF7, not buffered and not parsed;
  - a refusal verdict stops its direction and sets FAULTED;
  - an accepted refusal or shutdownAck stops its direction;
  - when both directions are stopped, the session is CLOSED.

  D3a will drive it; the corpus's trace case replays it.
- **LD-D2A-6. Stream framing.** A frame is read as exactly four prefix bytes, then exactly that many body bytes. EOF before the body completes is RF2 with the body counted as buffered, which is the reference's `len(raw) != 4 + n`. Bytes after a frame are the next frame, never part of it. The reader never allocates more than the context's bound plus four, and decides a zero or oversized prefix before allocating anything (D2a-T3).
- **LD-D2A-7. The corpus is vendored with pins, and its two source pins stay architecture-side.**
  - **Vendored:** `crates/components/tests/data/control-completion.cases.v5.json` and `control-completion.rf5-proof.v2.json`, byte copies of the architecture's files, which the test pins by SHA-256.
  - **Replayed:** all 480 cases, plus `coverage/16x8x2` and `coverage/RF5-unreachable-preview` as the reference states them. D2a also strengthens the matrix check: it asserts the full 16 × 8 × 2 product, where the reference counted only distinct triples and types.
  - **Architecture-side:** the reference's two source-pin checks hash files inside the architecture repository (CPC v2 and permission-truth-tables v9), which the product repository cannot read. The lane's tool checks them against the freeze and records them, so the 484 checks are all accounted for, 482 natively and 2 in the lane.
- **LD-D2A-8. The select tuple** is item 9's: role `analyzer`, the provider id as `roleSubprotocol`, and the protocol major as `subprotocolVersion`, from the admitted manifest's `role` and `compatibility.providerProtocol`.
  - **Confirm-only.** The host's `hello` offers exactly that one tuple, and its `select` names it. The encoder refuses to build a `hello` with any other offer list.
  - **No extra receiver rule.** The receiver applies only the reference's rules: confirms must be a subset of the offers, and select and selectAck must be confirmed. Under the one-offer hello these leave no runtime choice.
  - **The synthetic tuples** in the corpus (`semantic-provider/typescript/1`, and the preview's `analyzer/typescript/1`) appear only in the vendored corpus's contexts, never in a production constructor.
- **LD-D2A-9. Dependencies.** `opensip-components` takes `opensip-contracts` (for `Control3Root`), one of the three crates its scaffold permits. Nothing else is added: no serde on wire bytes, and no JSON or CBOR crate.

## 2. The unit (one product unit, one lane)

**New files:**
- `crates/components/src/control_protocol.rs`, with the reader, validators, classifier, session driver and encoder;
- `crates/components/tests/control_protocol_tests.rs`;
- the two vendored data files.

**Changed files:**
- `crates/components/src/lib.rs` (the module and its public items);
- `crates/components/Cargo.toml` (the `opensip-contracts` edge);
- `Cargo.lock`, for the path dependency edge only, with no new external crate.

**Controls:**
- **D2a-T1:** the corpus, byte for byte. Every one of the 480 cases gives exactly its expected outcome dict: verdict, type, next state, body buffered, terminal family and decision class, or for the trace, each step's verdict, buffered flag, state, stopped directions and next sequences. The two coverage checks run as well.
- **D2a-T2:** the 256 matrix cells, all asserted, and the full product.
- **D2a-T3:** an oversized prefix is refused before any body allocation. It is checked with a counting reader that the classifier must not read past four bytes, and through the session's `read_frame`, which never requests more than the bound.
- **D2a-T4:** the five 1,500-container and 5,000-digit probes, plus a 64 KiB all-`[` frame. Each is refused or decided with no recursion and no stack growth: the reader runs on a thread with a 64 KiB stack.
- **Supplementary lead controls:**
  - `-0` in seq is RF7, and in a body it is accepted as 0;
  - an unpaired-surrogate string inside an unsupported-major body reaches RF1;
  - the schema interpreter refuses an unknown keyword or pattern at load, and evaluates every member of the embedded product schema (LD-D2A-3);
  - every encoded host message classifies as ACCEPT in its state;
  - `ControlContext::for_session` gives the 65,536 bound and offer and the single tuple;
  - the encoder refuses a multi-tuple hello.

**Lane:**
- the components suite at base and candidate, and the workspace's other suites unchanged, with equal failure sets;
- rustfmt and warning-denied Clippy;
- FW-01 and the environment exceptions;
- the operability source census, including the mint census: no `from(`, `into(`, `line(`, `pid(` or `issue(` call;
- verify_design, and the census-closure check (no closure file changed);
- **mutations,** each failing D2a's tests: the deferred seq fault applied early; the sentinel not used; identities not substituted; the UTF-8 walk on the copy rather than the original; helloSeen checked after the state; the over-offer check moved before RF3; a duplicate member accepted; a 17-digit integer converted; refusal's if/then dropped; and a stopped direction parsed.

## 3. Questions for the reviewer

- **Q1.** Is LD-D2A-1's context-parameterized classifier, with the 65,536 policy in the production constructor, a faithful reading of item 9's bound decision, given that the corpus needs larger bounds to replay exactly?
- **Q2.** Is LD-D2A-7's split of the 484 checks (482 natively, the two architecture-side source pins in the lane) acceptable?
- **Q3.** Is LD-D2A-2's handling of unpaired surrogates (decided where the reference's UTF-8 walk reaches them, so RF1 inside an opaque future-major body) the right reading? No corpus case covers it.

## 4. Not claimed

- No caller, no process and no supervision.
- No provider protocol (D2b).
- No qualification.
- D2's completion is not claimed: D2b is beside it.
