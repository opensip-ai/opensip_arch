CODEX2 re-review: **SYN-NS r2**, the syntax normalizer specification of the accepted syntax law **M3-E1 r3** (items 13 and 14), after your r1 findings. This is a **design unit** (a `verify_design` contract successor whose candidates are new design files). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** with `subjectManifestSha256`, or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-syn-ns-r2`.

**Lead note (reviewer change).** CODEX2 reviewed r1. **GROK2** reviews r2, because CODEX2 is busy with I1 r3 and I1-a. CODEX2's r1 review is copied in `codex2-syn-ns-r1/`, so judge whether each of its six findings is resolved. The directory keeps its name, because the builder emits this review path. Write your output under `/tmp/opensip-implementation/reviews/codex2-syn-ns-r2`. Don't run cargo.


**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** A timing-sensitive crash-matrix lead set may be using this machine. Run no cargo, no tests and no crash-matrix binary or checker. Run no parser over anything: the fixtures' trees are hand-written data.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** Run it only through `evidence/verify_scratch.py`, which writes nothing and holds a synthetic review and assent in memory. Never edit the product or its lock.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. The SYN-NS files are still untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/syntax-e/syn-ns-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 22 members** are r1's twenty plus two new evidence files: `syn-ns/evidence/fixtures.json` and `syn-ns/evidence/reference_syn_ns.py`.
- **Not part of the subject:** `syn-ns-unit.json`, the lead's DRAFT-PENDING-REVIEW record. The builder now emits it, with the review path `docs/implementation/m3/reviews/codex2-syn-ns-r2/review.json`.

**Product.** Main is `218465f` (`218465fb71fd62ca01856d40d26ec822f45233be`), read-only, with 91 contract successors. SYN-1 is bound at `682991f` and SYN-1F at `218465f`. r2 is built and checked against `design-lock.json@218465f`, read with `git show`, not the live file. The checkout may move during your review (NB-SYNNS-2); the frozen revision is what counts.

**Law and grammars.** `docs/implementation/m3/syntax-e/PROPOSAL-r3.md` (`d71031ff…`), M3-E1 r3, item 19's SYN-NS row (E1:693). The grammars are E0's pins:
- tree-sitter-rust `v0.24.2`;
- tree-sitter-typescript `v0.23.2`;
- tree-sitter-javascript `v0.25.0`;
- runtime `v0.27.0`.

The per-file pins are in `syntax-e/e0-probe/pins/*.pins.tsv`. The bytes are in `/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/e0/src/`; read them, do not modify them.

**The rule r2 follows** (the lead's): where the pinned grammar cannot prove that a transform preserves meaning, it is not applied. A missed clone costs little; a false equality is a correctness defect.

## What r2 changes

The diff base is the r1 subject, `35f1a60c…`, which you reviewed. Its exact bytes are in this directory's `r1-members/`: the r1 subject manifest and all nineteen r1 members, each verified against the r1 pins. **Every r1 member changes**, and two are new. The README's **r2 changes** table has the detail; the rules chosen are:

| Finding | Rule | Where |
|---|---|---|
| **RF-SYNNS-1** | Every JavaScript-family row has `lineTerminators: significant`.<br>- **L1:** a whitespace gap holding CR or LF is one `opensip:line-break` token (value `0x0A`); spaces, tabs, VT and FF alone are dropped.<br>- **L2:** a non-directive comment holding a line terminator (LF, CR, U+2028, U+2029) becomes a line-break token, and runs of line-break tokens merge.<br>- Rust rows stay `insignificant`.<br>This is the lead's simple rule. An exact "ASI cannot apply" rule was not adopted (README LD-NS18). | `TOKEN_LAW[2]`, `TOKEN_LAW[4]`, `L2_LAW[0]`; `lineTerminators` on every L1/L2/L3 row |
| **RF-SYNNS-2** | **Rust bindings only by explicit binding forms:** `ref x`, `mut x`, `x @ p`, `let mut x`, a `mut x: T` parameter, `S { mut a }` and `S { ref a }`, each by grammar structure. Every other identifier inside a pattern is an **ambiguous pattern identifier**: it binds nothing, and its name is non-renamable (R4). That covers plain let, parameter, closure and `for` patterns, every match-arm, `if let`, `while let` and let-else identifier, `r#X`, and primitive names. Declares extraction uses the same law, so plain locals and parameters are not declared, and the precision loss is stated. | `RUST_PATTERN_LAW` (`bindingForms`, `law`, `statedLimit`); `SCOPE_LAW_RUST[0-1]`; `RUST_L3.bindingRules`; `L3_LAW[4]`; README LD-NS8 |
| **RF-SYNNS-3** | `token_tree` is **atomic** at L1 to L3: exact bytes, with no gap dropping, comment removal or renaming inside. A Rust body with any `macro_invocation`, `attribute_item` or `inner_attribute_item` gets **no L3 renaming at all**. The visible-name and format-capture guards are removed as redundant. | `RUST_ATOMIC`, `L2_LAW[0]`, `L2_LAW[2]`, `SCOPE_LAW_RUST[6]`, `RUST_L3.bodyDisqualifiers` / `disqualifying` |
| **RF-SYNNS-4** | An explicit **Lists** section (`List(L)` with and without a field). An explicit **Selection** section: the role tables are the only authority; the Rust effective node; else-clause unwrapping; transparent lists against single statements; opacity before roles. The Rust `unsafe_block` role is removed, since it is a body of its own. Both `roleLaw` texts are rewritten. | `CONTROL_FLOW_LAW[1-2]`, `[4-5]`; `TS_CONTROL.roleLaw`; `RUST_CONTROL.roles`, `.roleLaw` |
| **RF-SYNNS-5** | **Posttest entry:** every edge target passes through `enter`, which goes to a do…while's first body statement. The two exceptions are the body's end and `continue`, which reach the test. The test's true edge returns to the body as `branch-true`, and its false edge leaves. | `CONTROL_FLOW_LAW[6]`, rule 6 and rule 15 in `[7]` |
| **RF-SYNNS-6** | Identity prefix P is the owner's **full** subject chain, including the owner's own segment. entry and exit are `P/entry:@0` and `P/exit:@0`, and ordinals count within the graph. | `CONTROL_FLOW_LAW[3]` |
| **NB-SYNNS-1** | Your text, adopted: a binding-site occurrence resolves to its own binding. | `L3_LAW[3]` |
| **NB-SYNNS-2** | The base is frozen as `design-lock.json@218465f`. | build, request |

**Also new:**
- **The fixtures.** Six fixtures: your `return item;` against `return\nitem;` case, a line-terminating comment, a positive comment control, the atomic macro token tree, your two-function case, and a do…while with a `continue`. Each has a hand-written source and visible tree and hand-derived expected token streams and graphs. `reference_syn_ns.py` is a small oracle that applies the documents' own tables. `check_syn_ns.py` compares, and re-applies r1's rules to show each finding's defect reproduces.
- **The IDS parent** is now the selected identity copy, SYN-1F's `design/foundation/identity-schemas.v3.json`, instead of the superseded frozen file. Its `normalization-specification-map` definition is byte-identical.
- **SYN-NS's `verify_scratch.py`** now skips units the lock already binds, so `--chain` works at `218465f`.

## Decide

1. **RF-SYNNS-1 to -6.** Is each resolved by the stated rule, without a new false-equality path? In particular:
   - the line-break rule at L1 to L3 for every JavaScript-family row, including JSX (README LD-NS4);
   - the closed set of Rust binding forms, and the R4 ambiguous-identifier disqualifier;
   - the macro and attribute body disqualifier;
   - the traversal's completeness, and the posttest entry rule;
   - identity injectivity.
2. **The stated limits.** Are the recall losses (Rust declares and L3; no line-break normalisation in JavaScript) stated clearly enough, and acceptable under the lead's rule?
3. **Fixtures.** Do the hand-written trees match what the pinned grammars produce for those sources, at least in visible leaves and the structure the oracle reads? Do the fixtures discriminate the r1 defects? Is the oracle a faithful reading for what it covers?
4. **The IDS parent change** and the verify_scratch change: right?
5. **Anything else** wrong for selection under `verify_design`?

## Running the evidence (optional)

Use `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, from `docs/implementation/m3/syntax-e/`.
1. **Dependencies.** The design encoder imports `jsonschema`. Reuse your r1 offline install, or install it again into your review directory: `python3.14 -m pip install --no-index --no-cache-dir --find-links ~/opensip-deps/wheels --target /tmp/opensip-implementation/reviews/codex2-syn-ns-r2/deps jsonschema==4.25.1`.
2. **Checks.** `syn-ns/evidence/check_syn_ns.py --deps <that dir>`. Leave out `--write`. It checks the grammar pins, the census, every reference, canonical bytes, the map (validated with `ExactValidator` against the selected IDS copy), the parameters, the fixtures and the r1-defect reproductions, and compares with `kinds-report.json`.
3. **Build check.** `syn-ns/evidence/build_syn_ns.py --check`. It also compares the emitted `syn-ns-unit.json`.
4. **verify_design.** `syn-ns/evidence/verify_scratch.py --rev 218465f` binds, 91 → 92. With `--chain` the result is the same, because SYN-1 and SYN-1F are bound. Without `--rev`, on the checkout at `218465f`, it also verifies the 40 generation and 48 admission sources.

The lead ran each of these, and each passed. The builds were byte-identical across two `--check` runs. The lead also ran negative probes, and the checker refused all of:
- a wrong kind;
- a wrong field;
- a field not on its kind;
- an unchecked key;
- an anonymous token named as a named kind;
- a hidden supertype;
- a misspelled `whenAnonymous`;
- a wrong `lineTerminators`.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `syn-ns-subject.json`. The lead's value is `adc20c45caf7c28b4f590ebae7cf38f08d826ba632d592e566db9ad865da85ed`.
- `"successor"`: `{path, bytes, sha256}` of `syn-ns/successor.json`. The lead's value is 6975 bytes, `180f49350f5fb243ff535f472df60226928fb46089f978a0e647d49ed0bb3e58`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change bytes, give the exact replacement as data for `spec_syn_ns.py`, as in r1. Do not commit.
