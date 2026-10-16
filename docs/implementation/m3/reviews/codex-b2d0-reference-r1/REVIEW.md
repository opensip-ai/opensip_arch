# B2-D0-REFERENCE-r1 review

**Verdict: REQUIRED-FINDINGS.** Three required corrections remain in the proposed reference. Passing supplied checks and mutants does not cover these counterexamples.

## Subject and evidence

Manifest: 1,691 bytes, SHA-256 `4abce7de3770195f56dcf1c212ba6a2fbb08c69ce26b4a96bba4543c0aa936ee`.

Rehashed all seven members, all nine successor parent pins and all six successor candidates: every byte count and hash matches. Live product HEAD is `a50ae9646c9cf6b6c3600c2c28c816f7a77ab609`, clean; architecture HEAD is `1e938a466923ca2c7d1c45c6ddb7761c9019ed25`.

Copied the reference directory to a reviewer-owned temporary directory and ran its checker and mutants with `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B`, supplying the requested architecture checkout and python-packages snapshot. Fresh results: **110 checks, zero failed; 12 mutants, all caught**. The skipped-under-explicit mutant fails by schema validation, as described in the request. Additional synthetic probes used the temporary reference copy and confirmed the findings below, including the end-to-end recognition dispositions.

## Required findings

### B2D0REF-R1-RF-1: Reject a null packages value instead of treating it as an empty sequence

Location: reference/framework_recognition_reference.py:318-343; evidence/check.py:193.

parse_pnpm_packages(b"packages:\n") returns [], as does a packages key followed only by comments. Those documents give packages a null value, not a sequence of strings. The checker explicitly blesses this as accept-empty-block. Plan section 2 permits an empty sequence as packages: []; accepting a missing sequence makes the pnpm recognizer emit no unresolved choice for bytes outside the promised subset. Through recognize this reports state none instead of the outside-subset partial disclosure.

Required change: Require at least one block item after a block-form packages key; keep packages: [] as the empty-sequence form. Replace the empty-block positive control with negatives for bare-key and comments-only values, assert config-requires-evaluation/partial through recognition, and add a mutant for this distinction.

### B2D0REF-R1-RF-2: Validate YAML characters before accepting scalar or comment text

Location: reference/framework_recognition_reference.py:258-300 and 303-343.

UTF-8 decoding plus BOM/tab/CR checks do not establish YAML-valid input. Both b'packages:\n  - a\x00b\n' and b'packages:\n  - "a\x00b"\n' are accepted as strings containing a literal NUL, although a raw NUL is not permitted in YAML, even inside quotes. Raw DEL is also accepted, and ignored comment text bypasses character validation. recognize accepts the NUL example without config-requires-evaluation. Thus the closed reader admits documents that are not YAML packages sequences. Non-LF YAML break characters also need an explicit disposition: it retains U+0085 and U+2028 literally inside quoted scalars rather than applying YAML line handling or rejecting them.

Required change: Validate the whole document against the selected YAML character/line subset, including comments, before scalar parsing. Reject forbidden controls and unsupported line-break forms with OutsideSubset; keep allowed Unicode strings and LF/CRLF behavior explicit. Add negatives for literal NUL/control characters in plain, single/double-quoted scalars and comments, plus unsupported Unicode breaks, with recognition disclosure assertions and a mutation control.

### B2D0REF-R1-RF-3: Remove the undeclared Python decimal-digit limit from the TOML oracle

Location: reference/framework_recognition_reference.py:102-128; evidence/check.py:170-182.

The required isolated Python 3.14 interpreter has sys.get_int_max_str_digits() == 4300, including after Reference.load. A 5022-byte document consisting of [package], name="a", and x=<5000 decimal nines> makes tomllib raise ValueError; parse_cargo turns it into None and recognition emits Cargo.toml-not-toml, loses src/main.rs and reports partial. Product parse_toml deliberately retains integer literals without narrowing, and its walk rejects empty radix literals rather than limiting decimal digit count. This shallow three-node document is below both selected resource bounds. The oracle therefore has another admission divergence beyond the plan's sole labelled parser-recursion divergence.

Required change: Make TOML integer admission independent of Python decimal conversion limits while retaining the selected byte/node limits, or obtain an explicit revised contract for any additional divergence. Add below/above-4300-digit decimal controls beside usable package and workspace tables, checking recognition effects and workspace fact, and a mutant that restores the unwanted limit.

## Other requested decisions

**Model fidelity.** The reference loads the pinned model and calls recognize_frameworks without editing it. Retained evidence hashes are recomputed from original bytes; invalid UTF-8 package.json is handed to the model as empty text and disclosed as unparseable while retaining its original byte hash. Cargo regex results are removed and replaced by parsed-table results, sorted by recognizer ID. Successful Cargo shapes preserve the model's fields and entry order; the unparseable cargo-package disclosure retains target/ consistently with the documented design. The selected first tsconfig.json/jsconfig.json is the model's selection, and JSONC failure modifies that result. The intended five-change structure is present; the required findings prevent treating it as a correct oracle yet.

**TOML profile.** Byte cap, UTF-8/BOM handling and the iterative below-root value-node walk match the inspected product algorithm. Deep/wide and exact/past-bound controls exist. Product parser recursion is explicitly deferred as a labelled product-only divergence. Python integer conversion adds an undeclared divergence (RF-3).

**YAML.** Dash separation, colon rejection, quote escapes, indentation, flow-form restriction, bounds and typed failure are implemented. Reserved/numeric/date filtering is conservative, but does not make the overall reader sound: it misses a null-valued collection and document character validity. The checker codifies the former error and lacks controls for the latter. The grammar sweep promised for B2-d1 remains future product evidence; these concrete grammar failures must be corrected in the oracle first.

**FR-4/FR-2/state.** The structural validator enforces 32 results and 1 through 64 evidence files per result. Entry overflow uses the distinct union across results, clears all entry-bearing results without truncating, and retains their overflow disclosures. It runs before explicit precedence, including explicit empty arrays. None represents automatic mode; a supplied explicit list, including empty, selects all/explicit while keeping bounded discovery disclosure. The automatic state rule follows the accepted plan. Actual resolver absence/provenance extraction and higher-layer replacement remain host implementation controls; the reference receives the already-extracted optional list.

**Identity/provenance.** unit_recognition uses sha256 text over the canonical FrameworkRecognitionV1 record in native.framework-recognition.v1, matching the special closure.rs check. The checker independently spells the preimage framing and checks version-sensitive hashing. DISCOVERED:<recognizerId>@<recognizerVersion> rendering is correct.

**Evidence adequacy.** Existing checks and mutants cover the intended changes and bounds, but are insufficient because they pass despite the counterexamples. The single-result overflow loop also omits explicit-nonempty, although the r3 changes table promises it; add that case when updating the matrix. The cross-result explicit-nonempty case is present, so this is not a separate blocker.

**Binding.** successor.json's parent and candidate sets are internally consistent and fully hash-verified; passageOverrides is empty. The product lock has 170 contract successors, so 171 is the next proposed slot. No separate binding-format defect was found. Corrected reference/checker/output bytes must be repinned and reviewed before acceptance/binding; this review supplies no assent or passage override.

## Boundaries

No repository edits, product builds/tests, network access, other panes or delegation. No private fixture, signing key, installation, held tree or T2 store was accessed. Executable evidence and outputs stayed in the permitted reviewer-owned temporary copy. Only REVIEW.md and review.json were written in the requested review directory. This is a design-unit review, not product qualification.
