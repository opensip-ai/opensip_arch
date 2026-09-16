# Independent Grok advisory: M2 schema-pattern trials 01 and 02

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement. Not fresh consumer B.
**Kind:** Advisory technical trial review. **NOT ACCEPT-DESIGN-UNIT.** These results do not authorize a product dependency, runtime matcher, or schema-admission implementation.
**Work tree:** `/tmp/opensip-implementation/m2-grok-schema-pattern-trials-review-01/review` (private copies and probes only). No frozen, live, or original-trial edits.

Exact selected schema `pattern` semantics are required before descriptors or complete replay. Generated Rust carriers remain inert. The selected census is 68 patterns from 40 registry sources. No unknown runtime is selected here.

## Standing

Trials 01 and 02 are archived exploratory probes against currently cached `regress` 0.12.0 (`default-features = false`, features `std` + `prohibit-unsafe`, Unicode `u` flag) using the live identity exact JSON parser as a stdin probe. Trial `std` is test-only. The probe `Cargo.toml` path-depends on live `crates/identity`; that is a harness convenience, not admission of `regress` into identity or host.

This review independently checked custody, independently reimplemented the trial-02 adapter, rebuilt the probe offline in the private copy, and reproduced **bounded** cases only. It did **not** re-run the 63 104 / 74 528 corpora and did **not** execute nested-star or other catastrophic inputs.

## Custody

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Trial 01 `subject.json` | 2149 | `5bb632be82afeab52ccdb3402fecea3992ce78c1c447a0532dc9206cbdbcf17d` |
| Trial 01 archive | 217795 | `0b0ebfbb7d84a870813236bc27893a574504183d931fc1f4e84219e7086a695f` |
| Trial 02 `subject.json` | 2305 | `d678971a2a4b27a5ca7db650b5783cdb520d3e4eeebb5de317c9637b7288df4f` |
| Trial 02 archive | 255204 | `07e544cf6359105199976d20093dba7a8b8b2c1a7c41e16095accf3159698596` |
| Shared census | 89551 | `cc2394260406919a90ed272828c4ff2a5d241166dce23d3f7fa535685ee59f99` |
| Identity source pins | 966 | `459e94cd5dbae9092eb7969589e8e04d6346333f5e0e9375c390b449da492e6d` |
| `regress` 0.12.0 lock checksum | — | `32eef8b209c3c1c15dbad02c1f30f9539f00dc7253e0cbcdaae442a50a09d7c1` |

Original trees `/tmp/opensip-implementation/m2-schema-pattern-trial-01` and `-02` match their manifests: **13/13** and **14/14** members, archives match `archive-pin.json`. Frozen `result.json` bytes equal the originals (`802b9578…7233` / `da8b7b96…400c`). Private probe `Cargo.toml` and `src/main.rs` equal the originals (`2bcbfe9e…5347` / `ed3c48c4…e3b5`).

Live identity still matches the trial pins (5/5). `crates/identity/src/lib.rs` is 776 bytes, `#![no_std]`, `forbid(unsafe_code)`, `sha2-const-stable` only. Live has **no** `descriptors.rs`. Tooling: Cargo/rustc 1.95.0 Homebrew; isolated CPython 3.14.6 `-I -B`.

## What the trials actually showed

**Trial 01** (direct engine, Python `re.search` reference, final-LF `$`): 40 sources, 68 patterns, 63 104 cases, **9 mismatches**, 0 compile errors. All 9 are the three LogicalPath-family patterns on `.\n`, `a/.\n`, `a/..\n`.

Independent private probe, same three texts:

| Pattern family | Python | Raw regress `u` | Adapted |
| --- | --- | --- | --- |
| `(^|/)\.\.?(/|$)` | match | no match | match |
| LogicalPath `*` / `+` with inner `$` | refuse | admit | refuse |

**9/9** archived mismatches reproduce. Direct engine disagrees with Python; the trial-02 adapter agrees.

**Trial 02** rewrites, outside classes and escapes only: unescaped `$` → `(?=\n?(?![\s\S]))` (optional one final LF, then absolute end); unescaped `.` → `[^\n]`. Five patterns change. Claimed comparison: 74 528 cases including targeted security-domain wildcards and line terminators, **0 mismatches**, 0 compile errors. Independent `adapt()` equals archived `adaptations.json` on all 68. Bounded extras (`.\r`, `.\n\n`, `.\r\n`, `.\u2028`, `.\u2029`, `a/.\r\n`, empty) all agree with Python: Python `$` is **not** CR / CRLF / LS / PS / double-LF. Security grant mid-byte `.` / `\r` / `x` / `\u2028` match Python+adapted; mid `\n` refuses. All 68 original and adapted patterns compile on the private probe.

This is **not** a general Python-regex compatibility claim. It is a finite census adapter.

## Dialect authority is the real decision

JSON Schema Draft 2020-12 specifies ECMA-262 for `pattern`. The selected profile `opensip-exact-schema-reference-1` is executed today by pinned **jsonschema 4.25.1**, whose `pattern` keyword is `re.search` (`tools/contracts/python-packages/jsonschema/_keywords.py`).

Those dialects already diverge on this census:

- Python `$` matches end **or** before a single trailing LF. ECMA `$` (no `m`) is absolute end. That is the entire trial-01 9-mismatch set. The selected LogicalPath unit already encodes this as an imperative suffix rule, not as a regex engine.
- Python `.` fails only on LF. ECMA Unicode `.` also fails on CR, U+2028, U+2029. Trial 01’s short alphabet never presented a full `security.repo-execution-grant.v2:` identifier with those mids, so trial 01 could not have seen this split. Trial 02’s extras did.

Until a later unit explicitly changes profile authority, **selected semantics are Python `re.search` on the current schema bytes**, not raw ECMA. Using `regress` (an ECMA engine) without an adapter is therefore not a drop-in for selected admission. Using it *with* the trial-02 adapter is still not a product runtime: it is a census-specific translation into ECMA so a test harness can mimic Python.

Live `tools/contracts/runtime/pattern-profile.json` is marked **PROPOSED**, 65/68 census strings, plus `^.+$` which is **not** in the selected 40-source census. Census-only strings: `^RP-DO-[0-9]{2}(?![\\s\\S])`, `^owner1:[0-9a-f]{64}(?![\\s\\S])`, and the presentation-catalog control-character class. The proposed table is neither complete nor selected by these trials.

## Rewrite tokenization on the exact 68

The adapter is a one-pass scan: `\` escapes the next character; `[` / `]` toggle class; unescaped `$` / `.` outside a class are rewritten. It does not implement JS first-`]` class, unclosed-class recovery, nested classes, or `$`/`.` inside classes.

On **this** census that is enough:

- 0 first-`]` classes, 0 unclosed escapes/classes.
- 3 patterns with unescaped `$` outside class (the LogicalPath family, 6+3+33 occurrences).
- 4 with unescaped `.` outside class: the two LogicalPath `.*` lookaheads, plus the two unescaped security IDs.
- 1 unanchored pattern (`(^|/)\.\.?(/|$)`), used as jsonschema `not.pattern` via `re.search`. The other 67 are `^`…`(?![\\s\\S])` full-string forms. The high “lookahead” count is almost entirely that absolute-end assertion, not nested search.

Independent adapter bytes equal the archived mapping. Trial-02 `[^\n]` and the proposed profile’s `[^\\n]` are equivalent on the 65 overlapping strings. That does **not** make the tokenizer a general translator: a future `[]]`, `$` inside a class, or `^.+$` (already in the proposed table, absent from the census) is outside the proof.

**Selected-byte widening, not a matcher bug:** `^security.repo-execution-grant.v2:…` and `…grants.v2:…` contain unescaped `.` while sibling IDs use `security\.installation-…`. Under selected Python, `securityxrepo-execution-grantxv2:` + 64 hex **matches**. A closed predicate that silently treats those dots as literals would change selected schema semantics. Preserve the wildcard until a schema-correction unit changes the source bytes.

## Missing counterexamples (finite corpus is not a strategy)

Trial 01 cases are mostly length ≤ 2 over a 12-symbol alphabet, plus some hand-built IDs and codepoints 0..159. That found the `$`/final-LF split and nothing else.

Not covered, and not claimed here:

- Security unescaped `.` versus CR / LS / PS / ordinary scalars (added only in trial 02 extras).
- Identity `MAX_BYTES` (4 MiB) strings. A backtracking `(?!.*(^|/)\.\.?(/|$))` on a long path is a resource question, not a 74k-short-string question.
- Nested-star / overlapping-quantifier inputs. Intentionally not run.
- Tokenizer-hostile syntax absent from the 68: `[]]`, `$` in class, unclosed class, `\Q`, named groups.
- `re.search` versus `fullmatch` except the one unanchored `not.pattern`.
- Unpaired surrogates (identity JSON admits Unicode scalars only).
- `regress` without `u` (crate docs: parser already assumes Unicode).

Zero mismatches on 74 528 short strings is consistent with “this adapter matches Python on this census.” It is not proof of a bounded host/evaluator matcher.

## `no_std`, features, and M6 resource limits

`regress` 0.12.0:

- ECMA syntax, **classical backtracking** as `DefaultExecutor`. Crate docs: the `regex` crate gives linear-time guarantees; `regress` does not. PikeVM is a “pseudo-toy” extra backend, not the default executor.
- Trial features: `default-features = false`, `std` + `prohibit-unsafe`. That drops compiling PikeVM (a default *feature*, not the default *executor*) and still runs the backtracking interpreter. `prohibit-unsafe` does not bound stack or time.
- `#![cfg_attr(not(feature = "std"), no_std)]` exists; `no_std` needs the `alloc` feature (hashbrown). The trial used `std` and therefore `memchr` with `std`. Identity cannot take that graph: it is `no_std` + `sha2-const-stable` only.
- Lookaround and `.*` inside negative lookaheads are exactly why a backtracking engine was tempting — and why it is a poor M6 fit. The LogicalPath closed predicate already implements the same `$` edge in linear time over scalars.

A passing finite corpus does not place `regress` in identity, host, or evaluator. Even a later `no_std`+`alloc` build would still be unbounded backtracking on schema-admitted strings up to 4 MiB.

## Closed predicates versus a library

Reviewer classification of the **exact 68** (not a product table):

| Kind | Count | Implication |
| --- | ---: | --- |
| Prefixed / hex digest, UUID, even-hex | 36 | Closed scan |
| Identifiers / flags / `$defs` / slash-path / dates / enums / RP-DO / codepoint classes | 18 | Closed scan |
| Escaped `security\.…` IDs | 4 | Closed literal prefix + hex |
| Unescaped security grant/grants IDs | 2 | Closed, but `.` is selected wildcard `[^\n]`, not `\.` |
| Semver (three spellings) | 3 | Closed parser, already a known shape |
| Segment / glob-like paths | 2 | Closed segment walk; no `$` |
| LogicalPath family (`not.pattern` + `*` / `+`) | 3 | Closed predicate already exists in the accepted, not-installed LogicalPath unit |

The only patterns that *look* like they need a regex engine are the LogicalPath-family `.*` lookaheads — and those are the ones already replaced by an imperative rule that preserves Python `$`. Importing a backtracking crate to re-encode a law the project already wrote in `no_std` Rust is the wrong direction.

## Concrete tests and constraints before selecting any runtime

If a later unit proposes *any* matcher (library or generated), it must pin and pass at least:

1. **Dialect pin.** Selected jsonschema 4.25.1 `re.search` versus ECMA-262, written as authority, not as “compatibility.”
2. **Exact census.** All 68 compile; the 9 `$`/final-LF cases; extras `.\n\n`, `.\r`, `.\r\n`, LS, PS; security mids `.` / `\n` / `\r` / `\u2028` / `\u2029` / `x` / emoji; escaped `security\.` siblings remain literals.
3. **Schema-byte fidelity.** Unescaped grant dots stay wildcards until a schema unit changes source. Matcher must not “fix” them.
4. **Input bound.** Match only against a declared scalar/byte cap far below identity `MAX_BYTES`, or refuse. No nested-star catastrophic execution; refusal tests use length-capped inputs only.
5. **Linear / closed remainder.** `.*` inside lookaheads is a segment scan, not a backtracking search. Prefer the existing LogicalPath predicate over a translated regex.
6. **Crate graph.** Identity stays `no_std` + no `regress` / `memchr` / `hashbrown`. A host-only test probe is not an identity dependency. Feature matrix: default features off, no silent `std`.
7. **Tokenizer / syntax corpus** if any rewrite remains: first-`]` class, `$` in class, `\$`, `\.`, unclosed class — even if absent from the 68 — as explicit admit/refuse rows.
8. **Oracle.** Same cases through pinned jsonschema 4.25.1, not only `re.search` in isolation (`pattern` vs `patternProperties` vs `not.pattern`).

Absent those, do not select a runtime.

## Next implementation decision (advisory)

**Do not select `regress` as a product dependency.** Trial 01 shows raw ECMA `$` is wrong for the selected profile. Trial 02 shows a local rewrite can mimic Python on this census; that is harness evidence, not host/evaluator architecture.

**Prefer a closed selected-pattern table** keyed by the exact 68 census strings (or per-kind predicates), dispatched from registered schema admission (M2-A03). Reuse the LogicalPath `$`/final-LF rule already reviewed. Treat the two unescaped security IDs as selected wildcards until schema bytes change. Keep generated carriers inert.

A backtracking ECMA library is the wrong default for bounded pure identity/evaluator, even if every short test passes.

## Limits

- Advisory only. Not ACCEPT-DESIGN-UNIT, not runtime selection, not M2 complete, not descriptor admission, not replay.
- Did not re-run 63 104 or 74 528 cases; did not run catastrophic inputs; did not execute original `run-trial.py` against the original tmp trees.
- Did not treat proposed `pattern-profile.json` as selected.
- Did not read or join the separate fresh-consumer asset-channel session.
- Probe rebuild used live identity path; pins currently match live; that coupling is harness-only.
- Reviewer kind-table is analysis of this census, not an installed registry.

## Evidence (private review tree)

- `review/results/analysis.json` — 5437 bytes, SHA `398421291cd4e7dfa7b539bf6368f68e7bc526addda7510d0c8c533a610dccb4` (bounded probes).
- `review/results/classification.json` — 59305 bytes, SHA `95549ed8481fbea11b290f972b9534e469277c04a73ecab8ada25f7b18ee19e9`.
- `review/copy/probe/` — private probe sources; `CARGO_TARGET_DIR` under `review/probes/probe-target`.
- `review/probes/analyze.py`, `review/probes/classify.py`.
