# D2A-r1 review

Verdict: **REQUIRED-FINDINGS** — three required findings and two nonblocking observations.

## Exact subject

Verified the 20,765-byte manifest SHA-256 `24e0b1e9963c2259be9ed18f493d01aa5d55103ee2130796577ff0fe2b8ee610` and rehashed all 90 members. All seven mapped candidate files equal their architecture archives and the worktree; all parent pins equal base `56d0eb53a888572dd0129fbc595d0c1be16eaf3a`. The detached candidate remains at that base. Subject and candidate hashes were checked again before writing this review.

## Required findings

### D2A-R1-RF-1: Reject component-only messages instead of encoding empty bodies

Location: `crates/components/src/control_protocol.rs:1903`.

write_body matches all eight component-only variants with an empty successful arm. encode still writes their original type, seq and major, and returns Ok. For example, a generated ShutdownAck produces {"type":"shutdownAck","seq":1,"controlMajor":1,"body":{}} successfully, although shutdownAck is component-to-host only. Other component variants produce an invalid empty body. This contradicts the documented host-only encoder and can author a component response on the host side.

Required change: Return a typed direction/message refusal for every component-only variant, or accept only an opaque host-message type that cannot contain those variants. Add refusal controls for all eight component-only variants, alongside successful coverage of all eight host-sendable types.

### D2A-R1-RF-2: Validate constructed encoder output against the wire rules

Location: `crates/components/src/control_protocol.rs:1974`.

encode checks only the hello offer count and final frame byte length. Public generated carriers do not enforce all wire constraints: the nonce FromStr constructor checks Unicode character count, not x-maxUtf8Bytes, so a ping nonce of 128 copies of U+00E9 is constructible and encoded successfully although its 256 UTF-8 bytes make classify refuse RF2. Public NonZeroU64 fields permit values above 2^53-1, and a Refusal carrier can name RF-6 while decision_class is Missing; both are also emitted successfully. These are precisely the invalid-constructed-output cases carried in D2a plan NBO-1. The current encoder test exercises hello/select and a multi-offer refusal, not all host message types or the over-bound refusal.

Required change: Before returning bytes, validate all host output against the closed message schema, integer domain, original-string UTF-8 bounds and conditional refusal-body requirements, without identity substitution masking invalid outgoing identities. Enforce the applicable production hello/select policy through the selection-bound construction/sending boundary. Refuse invalid FieldPresence states rather than silently converting them into a different presence. Add multibyte byte-limit controls, maximum-plus-one integers, RF-1/RF-6 conditional fields, every host-sendable type, and exact/over-frame-bound tests. Keep this independent of receive-state correlation checks.

### D2A-R1-RF-3: Make the fixed production context policy enforceable

Location: `crates/components/src/control_protocol.rs:904`.

Every ControlContext field is public, ControlSession::new accepts any such value, and context_mut returns unrestricted mutable access to the same policy fields. A production caller can construct a context with a 16 MiB frame bound/multiple offers, or mutate frame_bound and frame_offer immediately after for_session; receive then trusts the altered bound. The corpus uses the same public struct-literal path rather than the plan's test-only constructor. Consequently for_session is a convenience initializer, not the only production construction path enforcing 65,536 and one admitted tuple as LD-D2A-1 requires.

Required change: Separate immutable production policy from mutable session observations. Keep bound/offer, admitted identities and permitted tuple policy private and fixed through the production constructor, and expose only the updates D3 actually needs for state/correlations. Keep arbitrary corpus contexts in a clearly isolated test/reference path rather than opening the production session policy. Add controls showing a production session cannot widen its frame bound or offer set through construction or subsequent context updates.

## Receiver, schema and precedence

The input reader uses an explicit container stack and flat arena. Arrays/objects hold indices, so JSON nesting does not induce recursive parsing, drop, debug or structural equality. Schema evaluation does recurse through the fixed shallow schema; it does not recurse through arbitrary instance nesting. Decoded-key duplicate detection applies at every object depth, including escaped equivalent keys. Strings are strictly escaped, raw controls and non-JSON whitespace refuse, and invalid UTF-8 is rejected before JSON reading. Unpaired surrogate escapes remain UTF-16 units until the applicable UTF-8 walk, preserving the future-major opaque-body distinction. Number scanning follows the reference's lexeme rule, including negative zero, non-integer fraction/exponent tokens and positive/negative oversized lexical integers.

For the frozen schema, the interpreter implements the used object/array/string/integer constraints, structural uniqueItems equality, conditional if/then/else/not rules and the two exact anchored patterns. The separate walk enforces original received string byte bounds; it does not walk substituted identity strings. NBO-1 qualifies the broader claim of closed schema loading.

Source comparison with check.v5.py supports the ordering: prefix/length, strict UTF-8 and syntax, frozen four-member envelope, unsupported-major hello's opaque-body path, integer walk with seq sentinel, identity substitution for schema classification, original-string UTF-8 walk, deferred seq fault, then direction/helloSeen/helloAck/select-state, sequence/state, major, identity/platform, tuple, offer, nonce and effect checks. RF3 identity mismatches and the later helloAck over-offer RF2 keep their reference precedence. Generated messages are constructed by hand after admission; serde does not read wire bytes.

ControlSession mirrors the retained run_session behavior for per-direction sequences, stopping, faulting, accepted terminal messages and name-sorted stopped directions. A stopped direction is refused before classification. D3 remains responsible for the documented evolving correlation inputs. RF-3 above concerns the public production-policy escape, not a disagreement with the recorded reference trace.

## Replay and lane evidence

The two vendored data files are byte-identical to the architecture corpus/proof; their SHA-256 values match the tests' pins. The product schema is byte-identical to control-completion.schema.v3.json. Independently verified both corpus source pins against CPC v2 and permission-truth-tables v9.

The replay code compares all 480 expected outcome dictionaries, including trace state/stopped-direction/sequence outputs. It adds the RF5 proof check and matrix coverage, with 256 distinct matrix coordinates and sixteen message types per state/direction; the replay validates their outcomes. The 482 native checks plus the two architecture-side source hashes account for the reference's 484 checks. The new body-duplicate test includes literal and escaped duplicate keys and a valid control.

The archived 64 KiB-stack probe executes a 65,000-level array and a 5,000-digit seq. Its deep frame is about 130 KiB and deliberately uses a larger corpus-style bound; the smaller retained corpus probes provide the other nesting/integer cases. Prefix tests exercise zero, over-bound, short-prefix and truncated-body decisions. NBO-2 distinguishes these slice-level results from transport acquisition.

Inspected the pinned raw logs, runner and comparison artifacts for all three attempts:

- Attempt 1: the duplicate-member mutant survives; refusal-if-then-dropped fails compilation due to a malformed replacement. Neither is counted as caught. The old equal-suite-count comparison also fails; there are eight new passing tests at this point.
- Attempt 2: the new body-duplicate control and corrected compilable conditional mutant catch both mutations. Nine tests pass; only the old suite-count comparison fails.
- Attempt 3: base has zero tests across two suites; candidate has nine passing tests across three suites, equal empty failure sets and exactly one added suite. NEW_SUITES=1 and NEW_TESTS=9 correctly express this structural change. The printed `host` label is cosmetic; the recorded comparison is for components.

All ten final mutants compile and fail their intended control tests. Final logs record successful rustfmt, warning-denied all-targets components Clippy, source pins, package-edge validation, environment exceptions, operability, unchanged census closure and design verification. The runner's mutation correction leaves the old conditional arm under a dead name while the real if arm returns true, so the resulting runtime failure is meaningful.

The encoder controls do not establish the host-only or all-constructed-output guarantees: only hello/select success and a multi-offer hello refusal are tested. RF-1/RF-2 require additional controls rather than discounting the valid receiver replay.

## Independent command, rules and inventory

Ran only the expressly permitted candidate command `python3 -I -B tools/check_operability.py source --repository .`: passed, 114 rows, no findings. No Rust build/test/lane or reference checker was executed by this review; reference behavior and Rust findings were compared through source and pinned evidence.

The components dependency is opensip-contracts; opensip-identity is dev-only. Cargo.lock adds those two path edges and no external crate. The package-policy log confirms the same distinction. No new prohibited call forms, environment reads or `let _ =` bindings were found in the new product Rust files. Independently found no intersection between the seven changed/new paths and the census's 19 pinned Rust closure files. No census-closure file or generator closure changed.

Inventory v214 already contains the planned `crates/components/src/control_protocol.rs` codec row with the stated description. Realize that row; add the integration-test file and two data files as three new rows. This review accepts no inventory successor or binding.

The preparatory scope correctly claims no caller, process, supervision, D2b provider codec, Linux-specific qualification or D2 completion. The outstanding findings must be resolved before accepting this unit.

## Nonblocking observations

**D2A-R1-NBO-1 — Close schema loading at the document root too** (`crates/components/src/control_protocol.rs:456`). check_subschema checks oneOf members, but Schema::load never validates the document-root keyword set. An extra unsupported root keyword is silently ignored, despite the broad closed-loading claim. The frozen current root is only $schema/$id/title/oneOf, so this does not alter present corpus classification. Explicitly allow those inert metadata fields and oneOf, reject additional root keywords, and add a root-level unknown-keyword control before relying on this guard for future schema changes.

**D2A-R1-NBO-2 — Distinguish prefix classification from bounded stream acquisition** (`docs/implementation/m3/supervisor-d/d2a-r1/SCOPE.md:1`). The candidate exposes classify/receive over a complete borrowed byte slice; there is no read_frame or incremental stream reader. Its prefix branches inspect no body and allocate no body, but body_buffered=false is a classification result, not evidence that a real transport read stopped at four bytes. The accepted plan LD-D2A-6 and its T3 control description also named a counting reader/session read_frame. Record that acquisition/control gap explicitly and settle its D3a integration boundary; do not claim this slice-only control proves bounded transport reads or split/coalesced-stream handling.

## Boundaries

No repository, candidate worktree or control file was edited. No Cargo/rustc/build/lane, network, other pane or delegation was used. No private fixture, installation, signing key, held tree, T2 store or cache was read. Only REVIEW.md and review.json in the requested directory were written. The encoder and context counterexamples are established by source inspection, not by an unpermitted product execution.
