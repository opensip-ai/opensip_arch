# Independent Grok advisory: M2 schema-pattern trial 03 (closed matcher)

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement. Not fresh consumer B.
**Kind:** Advisory technical trial review. **NOT ACCEPT-DESIGN-UNIT.** Not runtime selection, not schema-admission selection, not a product dependency.
**Prior trials 01/02:** Advisory already archived unchanged. Root agrees not to select `regress`. This review does not reopen that.
**Work tree:** `/tmp/opensip-implementation/m2-grok-closed-pattern-trial-review-03/review`. No frozen, live, or original-trial edits.

## Standing

Trial 03 is an exploratory closed-predicate table for the exact 68 selected `pattern` **keyword-value** strings. Frozen03 is correctly scoped to that 68; it **cannot** claim complete registered-pattern coverage. Trials 01–03 walked `pattern` values only, so they omitted `patternProperties` keys. Archived claim: 193 936 cases, 0 mismatches, 4 unknown patterns refused, 0 new crates, no heap in the matcher. Finite comparison is not complete schema or resource-budget proof. Generated carriers remain inert. Identity pins are pre-integration; this review reconstructed those sources from the frozen M1 fresh-consumer product rather than live bytes.

## Required strategy correction (census 68 vs registered applicators)

`^.+$` missing from the 68 is a **census construction** fact, not a selected-source fact. jsonschema applies the same `re.search` to `patternProperties` keys. Full interpreter preflight that requires every pattern-bearing applicator to be in the closed table **refuses** `^.+$` because the 68 table returns unknown (`E`). That refusal is a coverage hole, not proof the string is unselected.

Agreed source (prior note’s “control-v3” name was wrong): `schemas/sources/sarif-v2.schema.json` line 88, `messageStrings.patternProperties` key `^.+$`. That is the single selected `patternProperties` occurrence. Independent 40-source walk matches: 68 unique `pattern` values + this key = **69**. The issue remains the omitted applicator key, not a second document. Root’s next census69 (include `patternProperties` keys; closed Python `^.+$` = one-or-more non-LF scalars, optional one final LF, CR/LS/PS allowed) is the correct completion. Do not rewrite frozen03 to pretend 68 was complete.

Python `^.+$` (already probed): `a`, `a\n`, `😀`, `\r`, `\u2028` match; `""`, `\n`, `a\nb`, `a\n\n` do not.

## Custody

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Trial 03 `subject.json` | 3087 | `16880a587fbd24373c47263262ae97924190967086d87aa9aa353c01dc9dad5b` |
| Trial 03 archive | 1195231 | `b8771b999472673b6f22f668e869b556e00dcfcb25b8622d275b2157bb408016` |
| Census (same as 01/02) | 89551 | `cc2394260406919a90ed272828c4ff2a5d241166dce23d3f7fa535685ee59f99` |
| `probe/src/patterns.rs` | 8231 | `00639490f33f8897c78f2e6f3467f1768addfbf483b5becb8372aecc9e607267` |
| `probe/src/table.rs` | 6010 | `a7be8c32dfec72d1e64e463468e6e27ccd82682ee47558f003cea097aa2073d3` |
| Identity source pins | 949 | `1072044f30ba68a9b818156e0573de0bf68362ebdb220dc9a5765a27a519b182` |
| `result.json` | 1009 | `68120364da5184d66587a65a0f98b045b173dc57f06f7b6ffd76b6332aee9f61` |

Original `/tmp/opensip-implementation/m2-schema-pattern-trial-03` matches the manifest **19/19**. Archive matches `archive-pin.json`. `cases.jsonl` (23 409 696 bytes, SHA `4c0af1a1…9064`) verified in place and not duplicated. Private probe `Cargo.toml` was rewritten to reconstructed identity only.

Identity files (Cargo.toml, canonical.rs, canonical_tests.rs, digests.rs, lib.rs) match the trial pins and the frozen consumer tree `m1-fresh-consumer-subject-01/product`. Live currently happens to equal those pins and still has no `descriptors.rs`; the private build did **not** use the live path.

Tooling: Cargo/rustc 1.95.0 Homebrew; isolated CPython 3.14.6 `-I -B`; jsonschema 4.25.1.

## What the matcher is

`table.rs` is 68 exact census strings → `Kind`. Independent parse of the raw-string table equals the census order. Unknown strings return `Err` (probe prints `E`), not `Ok(false)`.

`patterns.rs` is `no_std`-capable, no `alloc`, no regex crate: single-pass scans, `split('/')` iterators, `strip_prefix`, `chars()`/`bytes()`. Private `cargo check` of a `#![no_std]` wrapper around the same sources: exit 0. Private std probe rebuild against reconstructed identity: exit 0. Archived clippy `-D warnings` is recorded on the original tree; this review did not re-clippy the original tmp tree.

No `regress`. Lock has only `opensip-identity` + `sha2-const-stable`.

## Bounded probes (not the 193 936 corpus)

258 targeted rows: Python `re.search` **and** jsonschema 4.25.1 `pattern` versus the private binary. **0 disagreements.** Combined identity-v3 LogicalPath (`Segments255` + `not` DotSegment + minLength 1 + maxLength 4096) also agrees on the targeted texts. Unknown inputs `""`, `.*`, `^.*$`, first pattern + `x`, and `^.+$` all return `E`.

Did not re-run 193 936 cases. Did not run nested-star inputs.

### Final-LF dot segment (Python `$`)

| Text | DotSegment | NegativePath+ | CanonicalPath+ | Segments255 |
| --- | --- | --- | --- | --- |
| `.\n` `a/.\n` `a/..\n` | match | refuse | **admit** | admit |
| `.\n\n` `.\r` `.\r\n` | refuse | admit | admit | admit |
| `.` `..` `./x` | match | refuse | refuse | admit |

CanonicalPath uses `(?![\\s\\S])` (absolute end) inside the segment-forbid lookahead, **not** Python `$`. So `.\n` is a one-segment name whose last scalar is LF, not `.` at absolute end. That is selected regex semantics. Do not “fix” CanonicalPath to refuse `.\n`.

identity-v3 Blob `LogicalPath` is **not** NegativePath. It is Segments255 **and** `not` DotSegment **and** 1..=4096 characters. Combined: `.\n` fails because DotSegment matches as `not.pattern`; `.\n\n` and `.\r` pass.

### Negative lookahead before the first LF

Python `.*` does not cross LF. NegativePath therefore does not see `.` / `..` after the first newline. DotSegment is unanchored `re.search` and **does** see `/./` after a newline.

| Text | DotSegment | NegativePath | CanonicalPath |
| --- | --- | --- | --- |
| `ok\n./x` | refuse | admit | admit |
| `foo\n/./bar` | **match** | **admit** | refuse |
| `./ok` `a/./b` | match | refuse | refuse |
| `foo/.\nbar` | refuse | admit | admit |

NegativePath and `not` DotSegment are **not duals** once a newline is present. identity-v3 relies on `not` DotSegment to refuse `foo\n/./bar`. Full admission must keep exact pattern strings and compose `not` in the schema layer. Do not replace identity LogicalPath with NegativePath.

NegativePath admits `a//b` (empty segments). CanonicalPath and Segments255 refuse it.

### Strict vs loose semver

Both refuse `01.2.3`. Strict refuses `1.2.3-01` and `1.2.3-a..b`; loose admits both. Strict admits `1.2.3-0` and `1.2.3+01` / `1.2.3-rc.1+build.01`. Two census strings map to `Semver(true)` (capturing vs non-capturing); behavior matches.

### Wildcard security separators

Unescaped `security.repo-execution-grant.v2:` treats `.` as Python `.` (any scalar except LF): `x`, CR, U+2028, emoji separators match; LF does not. Plural `grants` is a separate pattern. Escaped `security\.installation-transition-journal\.v1:` is a literal prefix. Preserve selected-byte widening until a schema-correction unit.

### Scalar lengths

Segments255 counts Unicode scalars, not UTF-8 bytes: `a`×255 and `😀`×255 admit; ×256 refuse. Enforcement platform suffix `{1,64}` is ASCII, so byte `len() <= 64` matches. Empty `ENFORCED-PLATFORM:` refuses. These caps are **in the selected patterns**, not new matcher policy.

## Linearity, allocation, `no_std`, resource refusal

The matcher is a viable bounded direction: `no_std`, no heap, no backtracking, O(n) over the instance string, table scan of 68. That is stronger M6 evidence than trial 02’s `regress` harness.

It still does **not** implement resource refusal. `matches` is `Result<bool, unknown pattern>` only:

- **Unknown pattern** (`Err`): engine cannot evaluate. Correct for a string **outside the table**. For frozen03’s 68 that includes `^.+$`. For complete registered admission that same `E` is a **missing predicate**, not an unselected source string. This is not instance-false.
- **Pattern false** (`Ok(false)`): selected pattern does not match.
- **Resource refusal** does not belong here. Identity already refuses JSON above `MAX_BYTES` (4 MiB) at parse. Schema `maxLength` (LogicalPath 4096 **characters**) is a separate keyword. Do **not** invent a tighter cap inside the matcher that would silently fail admitted schema inputs.

## Gap for full registered schema admission

Corrected: absence from the 68-value census ≠ absence from selected sources. The 68 is incomplete for **all pattern-bearing applicators**. Complete coverage is those 68 plus the one `patternProperties` key `^.+$` (**69**). Frozen03 still correctly scoped the keyword-value 68 and must not be silently widened.

Census construction for the next trial must include `patternProperties` keys (and any later `propertyNames.pattern`). Unknown remaining regexes stay engine faults, not silent `false`.

## Next implementation (advisory)

1. **Keep the closed table** for the exact frozen03 68. Do not select `regress`. Do not claim that 68 is complete registered-pattern coverage.
2. **Census 69:** include `patternProperties` keys; add a closed predicate for `^.+$` = one-or-more non-LF scalars, optional one final LF; CR, U+2028, U+2029 allowed. That is selected Python `.` + `$`, not ECMA Unicode `.`.
3. **Compose keywords outside the matcher:** `type`, `minLength`/`maxLength`, `not`, `allOf`/`anyOf`/`oneOf`, `$ref`, `items`, `patternProperties`. identity-v3 LogicalPath is Segments255 ∧ ¬DotSegment ∧ 1..=4096 characters — not NegativePath.
4. **Three outcomes:** unknown pattern (registry/engine), pattern false (instance), resource refused (parse `MAX_BYTES` / declared schema length). Never collapse the first or third into false.
5. **Dispatch by exact pattern bytes.** Keep CanonicalPath `.\n` admission, NegativePath first-LF `.*`, unescaped security wildcards, strict/loose semver.
6. **Oracle** pinned jsonschema 4.25.1 on `pattern`, `not.pattern`, and `patternProperties` for the same rows. Reuse the accepted LogicalPath closed predicate only where the schema actually uses that grammar.
7. **Place the table** in a `no_std` identity-adjacent module when a selection unit exists. Probe JSON parsing may keep a std binary; the matcher must not.

This trial is a sound strategy sketch for M2-A03 pattern evaluation. It is not that unit.

## Limits

- Advisory only. Not ACCEPT-DESIGN-UNIT, not runtime/schema-admission selection, not M2 complete.
- Did not re-run 193 936 cases; did not execute original `run-trial.py`; did not run catastrophic inputs.
- Did not treat proposed `pattern-profile.json` as selected.
- Did not read the separate asset-channel session.
- Private `Cargo.toml` path rewrite is review-only.
- Prior 01/02 reports were not modified (including their “`^.+$` only in proposed profile / not in census” wording, which remains true of that incomplete census).
- Frozen trial03 subject, archive, and original tmp tree were not modified.

## Evidence (private review tree)

- `review/results/probes.json` — 96660 bytes, SHA `4eefacea9d6ff6756a43d4a333c9124e94e97103f228559a7c3b4ad359c1cfc8`
- `review/copy/identity/` — reconstructed pre-integration sources
- `review/copy/probe/` — matcher + rewritten path dep
- `review/probes/nostd/` — `no_std` compile wrapper
- `review/probes/run_probes.py`
