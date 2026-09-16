# Review delta02: common-control generation guard and regression tests

- **Verdict:** ACCEPT-UNIT, narrow delta over the carriers and shape accepted in review01
- **Subject manifest SHA-256:** `0cfd9dd9c80281ceec2385d19ad083d50516ea9ddecd49d359b42cc0a83d8135`
- **Required findings:** none

Subject 02 differs from subject 01 in only a few places:
- a recursive ambiguous-union guard and a title-collision refusal in `prepare.py`;
- 4 new test groups (82 tests in total);
- the closure row for `prepare.py` and the registry closure hash;
- the docs;
- the header hash lines of the 8 outputs.

The guard is correct as a finite, conservative check. It is not a universal proof about how Typify allocates names. This review does not cover source promotion, product integration, or control/native/report semantics, and it is not M1 or release qualification.

## Correction to review01

Review01's evidence text said the malformed bounds `-1n, '0', 1.5, number 0, true, null, {}, []` were all refused. That overstated it.
- My first `work/ts/probe.cjs`, like the author's `check.cjs`, omitted `$schema`. Those schemas were refused for "unsupported schema dialect", not because of the bound.
- My later `ts-direct-probe.json` did supply the dialect. It validly showed bound-specific refusal only for `-1n` and `'0'` (nonnegative-integer error) and for `1.5` and number `0` (`EXACT_JSON_TYPE_REQUIRED`).
- `true`, `null`, `{}` and `[]` were never validly tested in review01. They are now covered by the permanent test, which supplies the dialect and asserts the exact `x-maxUtf8Bytes` error. The test passes here.

## What I verified independently

- **Exact set:** 88/88 files matched before and after, with no symlinks or extra dirs. No `__pycache__` was created in any frozen directory; imports used copies with `-B`.
- **Output bodies:** all 8 match subject 01 apart from the two header lines. The headers carry registry `abe989a7…` and closure `5b19b40b…`.
- **Projections:** I loaded both `prepare.py` versions from copies.
  - The flattened input is identical, and it is not mutated.
  - The Rust and TS projections are identical between 01 and 02 across all 587 definitions.
  - Naming changes only `Control3Root`, and only by the 16 body titles.
  - The new guard refuses the untitled projection ("ambiguous inline union property type: body") and passes the named one.
- **Closure:** toolchain, confinement and the 140 TS package files are identical to subject 01. The node and generator hashes match build04, and the pinned Homebrew Python 3.14 matches its closure pin.
- **Workspace:** the 140 TS files are regular files under my workspace copy. All hashes match, with no symlinks and no extra files.
- **Tests:** `python3.14 -I -B -m unittest discover -s tools/tests` gives 82 tests, all OK, with native node v24.16.0 on PATH. The UTF-8 runtime test ran (it was not skipped).
- **Fresh generation:** `{outputs: 8, changed: [], registrySha256: abe989a7…}`, exit 0.
- **Preflight:** the binding4 `verify_design.py` (sha `1dce4b8a…`, also the live product tool) with its lock `90e0533f…` refuses a subject‑02 copy: exit 1, "generation source is not selected by accepted design". The root refusal record now captures exit code and stderr and is no longer an empty file.
- **Guard probes (39):**
  - A differing array property under `oneOf` or `anyOf` is refused at root, properties, items, additionalProperties, patternProperties, not, then, else, an allOf branch, and a nested-union branch.
  - Also refused: an untitled object under `anyOf` or a nested `oneOf`, differing const strings, the same title on different shapes, one titled and one untitled, an empty title, and a 2‑identical‑plus‑1‑different set.
  - Correctly passed: differing plain strings, differing integer ranges, `$ref` children, distinct titles, and the direct `oneOf` object case that the namer titles.
  - The namer refuses a clash with an existing definition name and with an existing inline title.
- **Test sensitivity (10 mutations, run against copies):**
  - These mutations are each caught by their target test: guard no-op, guard not called, arrays dropped from the needs-name set, reserved check removed, namer disabled, UTF-8 check removed, scalar count instead of bytes, off-by-one `>=`, and `x-maxUtf8Bytes` removed from the typed count keywords.
  - One mutation survives: allowing the same title on different shapes. No permanent test covers that class, though my probe shows the real guard refuses it.

## Advisories

1. **D2A1 – One guard class has no test.** Add a permanent test for the same title on different shapes (and for one titled, one untitled).
2. **D2A2 – Known gaps outside the finite claim.** My probes show these pass without refusal:
   - a title that differs from a definition name only by case or normalization;
   - a private title that equals a name Typify would derive for an untitled property elsewhere (for example a definition `RootVariant0` with property `Property0`);
   - differing `allOf` siblings;
   - branch properties nested inside a branch `allOf`.

   None occurs in the current 587 roots, which have independent roundtrip evidence. If schemas widen, reserve normalized and derived names.
3. **D2A3 – The runtime test finds Node through PATH.** It uses `shutil.which('node')`, not the closure-pinned node. It fails closed if node is absent, but it could run a different Node or TS host. It also compiles the runtime template, not the generated `report.ts`, which is unchanged apart from headers and was covered in review01. Consider pinning node.
4. **D2A4 – Invocation sensitivity.**
   - Without `-I`, the execution tests refuse, as the root observed.
   - With a non-pinned `python3` on PATH, generation refuses and discovery errors. My own first run hit this by mistake; I discarded it and reran with the pinned interpreter.
   - Make the documented test command name the exact interpreter.
5. **Carried over from review01:** CA1 (preflight binding and promotion), CA4 (the Rust carrier is inert and looser than the schema) and CA5 (stale obligation, untracked route) still apply. CA2 and CA3 are substantially addressed, apart from D2A1 and D2A2.

## Limits

- The guard is a heuristic for one identified alias class, not a proof over every Typify naming rule.
- No Rust rebuild or re-roundtrip was done. Carrier bodies are byte-identical to subject 01, whose Rust evidence was accepted in review01, and the build04 closure is unchanged.
- The adapter04 confinement and dependency algorithms were not re-audited.
- Not reviewed: source promotion, exact source bridge, native IDL, report owner, control semantics, integration, and M1/product/release qualification.

Probe scripts and results are under `work/`, with hashes in `review.json`.
