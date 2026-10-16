# B2-D0-REFERENCE-r2 review

**Verdict: REQUIRED-FINDINGS.** The three prior counterexamples are fixed. Two additional YAML boundary defects prevent acceptance of the closed reader as the product oracle.

## Subject and execution evidence

Verified the 1,783-byte subject manifest, SHA-256 `d6be804422d788f42997ba25c185d514a6afb1412328f49b710604f93d83e36e`. All seven manifest members, all nine successor parent pins and all six successor candidate pins match their recorded byte counts and hashes. Live product HEAD is `a50ae9646c9cf6b6c3600c2c28c816f7a77ab609`, clean; architecture HEAD is `1e938a466923ca2c7d1c45c6ddb7761c9019ed25`.

Ran the checker and mutants from a reviewer-owned temporary copy using the required Python 3.14 executable with -I -B and the specified architecture and python-packages arguments. Fresh results: **131 checks, zero failures; 15 mutants, all caught**. The request's later reference to 110/12 is stale; the actual r2 evidence is 131/15. Synthetic probes against the temporary reference confirmed the new findings below. No product test was run.

## Prior findings

- **B2D0REF-R1-RF-1:** resolved. A block key with no items now raises OutsideSubset. Bare-key/comments-only controls and the null-acceptance mutant cover the correction. The empty-flow form remains supported.
- **B2D0REF-R1-RF-2:** the original NUL/DEL/Unicode-break counterexamples are corrected. The character predicate itself equals the documented narrowing of YAML c-printable: LF, printable ASCII, U+00A0 through U+D7FF except U+2028/U+2029, U+E000 through U+FFFD except U+FEFF, and U+10000 through U+10FFFF. UTF-8 decoding excludes surrogates; checks cover comments too. However, the preprocessing still erases an EOF bare CR before this predicate sees it: R2-RF-2.
- **B2D0REF-R1-RF-3:** resolved for this isolated, sequential reference. The digit limit is lifted around tomllib.loads and restored in finally, including parse errors. Additional probes accepted 5,000-digit unsigned/signed decimal and hexadecimal/octal/binary forms and confirmed restoration on success and malformed input. Decimal underscores do not introduce another conversion path; power-of-two bases are not subject to the decimal conversion cap. The byte and node bounds remain in force. No new integer-form admission defect was found. This is reference machinery, not a proposed concurrent product parser.

## Required findings

### B2D0REF-R2-RF-1: Require separation after the block mapping key before the empty flow sequence

Location: reference/framework_recognition_reference.py:349.

The empty-flow regex uses zero or more spaces after the colon, so parse_pnpm_packages(b'packages:[]\n') returns []. The same happens for b'packages:[] # comment\n'. In block YAML, this unseparated text is a plain scalar rather than the packages mapping with an empty sequence. Thus the reader still accepts a document that is not a packages sequence of strings. recognize emits no unresolved choice and state none for it, rather than the mandatory outside-subset disclosure. The accepted plan's empty form is packages: [].

Required change: Require at least one separating space after packages: for the empty-flow form. Add separated positive and unseparated negative controls, with and without comments and through recognize; require config-requires-evaluation/partial for the negative forms, and add a mutation control for removal of separation.

### B2D0REF-R2-RF-2: Do not discard an unpaired carriage return at end of input

Location: reference/framework_recognition_reference.py:334-339; README.md r2 changes RF-2.

The r2 character profile excludes a bare CR and permits CR only as CRLF, but the split/strip logic removes a trailing CR from every split element, including the final element not followed by LF. Consequently b'packages:\n  - a\r' is accepted as ['a'], and b'packages: []\r' is accepted as []. The whole-document character predicate never sees the forbidden CR. The existing bare-cr negative vector tests an internal CR followed by another character, so it misses this EOF boundary. This is a mismatch with the declared closed subset, even though CR alone can be a line break in general YAML.

Required change: Normalize only actual CRLF pairs, then reject every remaining CR before parsing. Add EOF bare-CR cases for block items, empty flow and comment text, preserving positive LF/CRLF and no-final-newline controls. Check the outside-subset disclosure through recognize and add a mutation control for this boundary.

## Other requested decisions

**Fidelity and TOML profile.** The source diff from r1 contains the three intended repairs; model loading/calling and the five-change structure remain intact. Invalid UTF-8 package.json still becomes empty model text while evidence hashes retain original bytes. Cargo table replacement, sorted order, successful result fields and the unparseable target/ disclosure are unchanged. The model's first tsconfig.json/jsconfig.json remains selected. The byte cap, UTF-8/BOM handling and below-root node walk agree with the inspected parse_toml implementation; the parser recursion limit remains the one stated product-only divergence. No additional TOML profile blocker found.

**YAML scalars.** Reserved/numeric/date filtering is conservative and can reject strings as well as non-string scalar spellings; that restriction is safe for this selected narrow subset. No additional admitted typed scalar was demonstrated. That filtering does not protect the top-level mapping separator (RF-1), and character checking does not protect bytes discarded before checking (RF-2). Both counterexamples are accepted without config-requires-evaluation by recognize.

**FR-4/FR-2/state.** Structural bounds, distinct-union overflow handling, all-or-nothing suppression under explicit overrides, explicit-empty versus None, retained discovery disclosure and the automatic state rule remain correct as reviewed in r1. The reference receives an already-extracted optional explicit list; actual resolve-output provenance and higher-empty replacement remain host implementation controls. The promised explicit-nonempty single-result overflow vector is still absent, although cross-result explicit-nonempty and single-result explicit-empty vectors exist. Add it when refreshing the matrix; it is not a separate blocking finding.

**Identity and provenance.** The unchanged unit_recognition hashes the canonical recognition in native.framework-recognition.v1 and uses sha256 text as closure.rs requires. The checker spells the preimage independently and exercises version-sensitive hashing. DISCOVERED:<id>@<version> rendering is unchanged and correct.

**Evidence.** The new positive/negative controls and three added mutants exercise the prior fixes. All 15 mutants are caught, including the schema-rejected skipped-under-override mutant. Evidence remains insufficient for acceptance because all 131 checks pass despite the two demonstrated boundary violations. Their requested controls should be added to the design oracle before product agreement tests depend on it.

**Binding.** successor.json has the expected model/loading closure, archived JSONC reader, NE and accepted-plan parents, six candidate artifacts, and no passage override. All pins match. The product currently has 170 contract successors, so 171 remains the next proposed slot. No independent binding-format defect found. Corrected bytes and their outputs must be repinned for review; no acceptance or binding is granted here.

## Boundaries

No repository edits, builds, product tests, network, other panes or delegation. No prohibited private fixture, signing key, installation, held tree or T2 store was accessed. Checker/mutant execution and outputs stayed in the permitted temporary copy. Only REVIEW.md and review.json were written in the requested review directory. This is a design-unit review, not implementation acceptance or qualification.
