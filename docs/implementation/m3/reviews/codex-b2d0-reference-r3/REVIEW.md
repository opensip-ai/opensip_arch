# B2-D0-REFERENCE-r3 review

**Verdict: ACCEPT-DESIGN-UNIT.** Both round-2 required findings are resolved. No new blocking defect found. One nonblocking evidence-matrix observation remains.

## Subject verification

Manifest: 1,873 bytes, SHA-256 `ae983bcd6fbeddd986616e303aec1b8f720c4bde562124b59c0f129e60402641`.

Rehashed all seven subject members, all nine successor parent pins and all six successor candidates. Every byte count and hash matches. Live product HEAD is `a50ae9646c9cf6b6c3600c2c28c816f7a77ab609`, clean; architecture HEAD is `1e938a466923ca2c7d1c45c6ddb7761c9019ed25`.

Reviewed the r3 source and checker diffs against the prior temporary copy, the full YAML reader, the recognition/identity and TOML code, the README and successor, and the relevant accepted-plan, NE and product authorities.

## Executed evidence

Copied the reference directory into a reviewer-owned temporary directory. With `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` and the specified architecture/python-packages arguments, fresh results are **143 checks, zero failures; 17 mutants, all caught**. The request's later 110/12 wording is historical. Both new mutants are caught by their intended negative controls. The skipped-under-override mutant is caught by schema validation, as expected.

Additional synthetic probes against the temporary copy confirmed 11 rejected inputs with recognition disclosure and six accepted scalar/sequence cases. These included both round-2 counterexamples, null-valued packages, invalid characters, mapping-valued items, typed plain scalars, empty quoted strings, quote escapes, embedded hashes, empty flow with comments, CRLF and no final newline.

## Prior-finding disposition

**B2D0REF-R2-RF-1: resolved.** The empty-flow production now requires one or more spaces after packages:. Unseparated forms, with and without comments, raise OutsideSubset and become config-requires-evaluation with partial state. The separated empty-flow forms remain accepted. The dedicated mutant is caught.

**B2D0REF-R2-RF-2: resolved.** Only actual CRLF pairs are normalized; every remaining CR is rejected before character validation or parsing. EOF CR after a block item, empty flow or comment is refused. LF, CRLF and no-final-newline positives remain valid. The dedicated mutant is caught.

The round-1 repairs remain intact: block-form packages requires at least one item; character validation covers the whole document, including comments; Python's decimal integer conversion limit is lifted only around TOML parsing and restored in finally. No regression found.

## Requested contract decisions

**Five-change fidelity and bytes.** The pinned B-S9 model is called unchanged. The wrapper retains its registry, hints, non-Cargo shapes, selected evidence files and sorting, while applying the five accepted changes. Non-UTF-8 package.json is passed to the model as empty text for strict-JSON refusal; every retained evidence hash is recomputed from original bytes. Cargo regex rows are replaced by parsed package/workspace table rows, sorted by recognizer ID, preserving successful entry order. Unparseable Cargo produces the documented inferred cargo-package disclosure with target/. TypeScript configuration still selects the model's first tsconfig.json/jsconfig.json.

**TOML profile.** The byte limit, UTF-8/BOM checks and iterative below-root node count match parse_toml. Decimal conversion limits no longer impose an extra admission bound; the selected byte/node bounds remain in force. The product parser's recursion bound is explicitly the labelled product-only divergence. Its differential controls remain a B2-d2 obligation. No new profile mismatch found in this revision.

**YAML subset.** The selected character ranges implement the documented narrowing of YAML c-printable, and CRLF normalization no longer erases forbidden bare CR. Mapping separation, block indentation/item separation, nonempty block sequences, single/double quote handling and scalar exclusions now compose consistently. Plain scalar filtering is deliberately conservative: some YAML strings can be excluded, but that is compatible with this closed subset. No accepted document outside a packages sequence of strings was demonstrated in this round. Acceptance is based on inspection and the stated finite controls, not exhaustive YAML conformance or support for full YAML.

**FR-4/FR-2/state.** Structural bounds remain 32 recognizers and 1 through 64 evidence files per result. The distinct entry union is bounded per unit; overflow suppresses every entry-bearing result without truncation and retains uncertainty. This runs under explicit overrides too. None denotes absent explicit configuration, while [] remains explicit and wins with all/explicit. Automatic state is partial on unresolved choices, otherwise all with entries, otherwise none. Actual resolver provenance extraction and higher-layer empty replacement remain product implementation controls.

**Identity/provenance.** unit_recognition derives sha256 text from the canonical recognition in native.framework-recognition.v1, matching closure.rs. The checker independently spells the framing preimage and checks version-sensitive hashing. DISCOVERED:<recognizerId>@<recognizerVersion> rendering is correct.

**Evidence scope.** The checker and mutants cover the five changes and the defects from both prior rounds sufficiently for this design unit, subject to the nonblocking matrix observation below. Product FW-01, parser-recursion divergence controls, actual resolver outputs, grammar sweep and implementation agreement remain later gates; this review does not claim those were executed.

**Binding.** successor.json's model/loading closure, archived JSONC reader, NE and plan parents are correct and hash-verified. Its six candidates match the reviewed subject; passageOverrides is empty. The product lock has 170 contract successors, so 171 is the next proposed slot. No binding defect found. This verdict accepts the design unit; assent and actual binding are separate actions.

## Nonblocking observation

**B2D0REF-R3-NBO-1 — advertised single-result overflow matrix (evidence/check.py:162-169).** The single-result overflow loop omits explicit-nonempty, although the evidence description advertises it. Existing cross-result explicit-nonempty and single-result explicit-empty cases cover the mechanism. Add the missing combination for B2-d2 or narrow the description; this does not block design-unit acceptance.

## Boundaries

Neither repository was edited. No product build/test, network, other pane or delegation was used. No prohibited private fixture, signing key, installation, held tree or T2 store was accessed. Checker/mutant writes stayed in the permitted temporary copies. Only REVIEW.md and review.json were written in the requested review directory. No implementation, integration, qualification or B2/M3-B completion is claimed.
