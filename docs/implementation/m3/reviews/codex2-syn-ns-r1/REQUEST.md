CODEX2 review: **SYN-NS**, the syntax normalizer specification of the accepted syntax law **M3-E1 r3**: the identity-bearing normalization bytes of items 13 and 14. This is a **design unit** (a `verify_design` contract successor whose candidates are new design files). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-syn-ns-r1`.

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** A timing-sensitive crash-matrix lead set may be using this machine. Run no cargo, no tests and no crash-matrix binary or checker. Run no parser over any repository.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** `evidence/verify_scratch.py` runs the real tool over an in-memory lock and writes nothing.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. Every file is untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/syntax-e/syn-ns-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 20 members** are:
  - `syn-ns/successor.json` and `README.md`;
  - **the six closure members**, under `syn-ns/closure/opensip-interface/`, in canonical bytes at their exact tree paths:
    - `grammar/normalizer.v1.json`;
    - `normalization/specification-map.v1.json`;
    - `normalization/levels/{L0-verbatim,L1-lexical,L2-comment-insensitive,L3-identifier-insensitive}.v1.json`;
  - their pretty-printed twins under `syn-ns/readable/`, which are not normative;
  - `materialization-map.json`;
  - `evidence/spec_syn_ns.py` (the documents as data), `build_syn_ns.py`, `check_syn_ns.py`, `verify_scratch.py` and `kinds-report.json`.
- **Not part of the subject:** `syn-ns-unit.json`, the lead's DRAFT-PENDING-REVIEW record.

**Product.** Main is `cd5958b`, read-only, with 82 contract successors. SYN-NS changes no product byte. E2a places the bytes in the grammar closure, and E2c implements them.

**Law and grammars.**
- **Law:** `docs/implementation/m3/syntax-e/PROPOSAL-r3.md` (`d71031ff…`). This unit is item 19's SYN-NS row (E1:693), and it fixes items 13 and 14.
- **E0** (`E0-REPORT.md`, `c1011e83…`) chose T-native. These bytes are the same on both branches.
- **The grammars are E0's pins:**
  - tree-sitter-rust `v0.24.2`;
  - tree-sitter-typescript `v0.23.2`, both the typescript and tsx grammars;
  - tree-sitter-javascript `v0.25.0`;
  - runtime `v0.27.0`.

  Per-file pins are in `syntax-e/e0-probe/pins/*.pins.tsv`. The bytes are in E0's SCRATCH, `/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/e0/src/`, which you may read but must not modify.

## What it says

The README has the full description. In brief:
- **`normalizer.v1.json`**, with one row per code grammar:
  - NE §6.2's parameters;
  - the body table and import-only exclusion;
  - the syntax subject identity law (`syntax:` + esc(path) + `#` + `tag:esc(name)@ordinal` segments, with injective ASCII escaping and no offsets);
  - the declares and literal tables, including the `valueText` rule;
  - statement-level control flow: sixteen edge rules and two stated simplifications;
  - `near-v1`.
- **Four level specifications, each complete for its level:**
  - **L0:** the raw span.
  - **L1, the token law:** visible leaves plus atomic kinds, with non-whitespace gap tokens kept so the stream is lossless except for ASCII whitespace. Kind ids are `n:` or `a:` plus the symbol name.
  - **L2:** removes non-directive comments.
  - **L3:** renames a local name, to `opensip:local` tokens, only when conditions R1 to R5 make the renaming sound. Each row carries its scope tables, and the Rust pattern case rule carries a stated limit.
- **IE's map:** the four rows, each a level file's digest. It validates against IDS's `normalization-specification-map`.

## Lead decisions and deviations, for you to rule on

- **LD-NS1** — One unit for items 13 and 14, written now.
- **LD-NS2** — **Self-contained levels.** FIP's `levelVersionDefinition` says a level specification *includes* its lexical, token-kind, directive and transform rules. So the comment, directive and local-binding tables live in the level files, not only in `normalizer.v1.json`, and A12 must check them too (E-7, E-9).
- **LD-NS3** — The grammar pins are E0's; item 6's selection rule is read as of this unit (E-10).
- **LD-NS4** — Gap tokens.
- **LD-NS5** — Kind ids, and the collision-free replacement kind.
- **LD-NS6** — Directives.
- **LD-NS7** — The L3 soundness conditions.
- **LD-NS8** — The Rust case rule and its stated limit.
- **LD-NS9** — Macro conservatism.
- **LD-NS10** — Bodies.
- **LD-NS11** — Subjects.
- **LD-NS12** — Declares coverage.
- **LD-NS13** — `valueText`.
- **LD-NS14** — Statement-level control flow.
- **LD-NS15** — `near-v1`.
- **LD-NS16** — The parents, with no ordering dependency.
- **LD-NS17** — `readable/`.
- **E-11** — E1 item 13 said E2c would write the tables and SYN-NS would review them. Here SYN-NS fixes the tables and E2c implements them.

## Decide

1. **Levels.** Is each level file complete for its level, and is LD-NS2's reading of FIP and IE right? Is the token law lossless except for ASCII whitespace, and are the kind ids canonical?
2. **L3 soundness.** Do R1 to R5 make every L3 equality a true identifier-insensitive identity? Is any scope or binding rule wrong for JavaScript, TypeScript or Rust in a way that renames a free name? Are the stated limits acceptable?
3. **Control flow.** Are the sixteen rules complete and unambiguous at statement granularity? Are the simplifications acceptable for `control-flow@syntactic`?
4. **Tables.** Are the body, declares, literal and role tables right for each grammar? Is anything missing or misclassified?
5. **Subjects and literals.** Are subject identities injective, offset-free and within `SubjectIdV1`? Is the `valueText` rule admissible as `CanonicalText`?
6. **near-v1.** Is the definition deterministic and consistent with `CloneCandidateGroupV2` and E1 item 14a?
7. **Deviations.** Rule on E-7 and E-9 to E-11. Is anything else wrong for selection?

## Running the evidence (optional)

Use `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, from `docs/implementation/m3/syntax-e/`.
1. **Dependencies for the map validation.** The design encoder imports `jsonschema`. Install it offline into your review directory: `python3.14 -m pip install --no-index --no-cache-dir --find-links ~/opensip-deps/wheels --target /tmp/opensip-implementation/reviews/codex2-syn-ns-r1/deps jsonschema==4.25.1`.
2. **Checks.** `syn-ns/evidence/check_syn_ns.py --deps <that dir>`. It:
   - verifies each grammar's `parser.c` and `node-types.json` against E0's pins;
   - extracts the symbol census;
   - checks every kind, anonymous token and field named, on a closed-key walk;
   - re-encodes each member with the real `canonical.py`;
   - validates the map with `ExactValidator`;
   - compares the parameters with NE §6.2;
   - compares its report with `kinds-report.json`. Leave out `--write`.
3. **Build check.** `syn-ns/evidence/build_syn_ns.py --check`.
4. **verify_design.** `syn-ns/evidence/verify_scratch.py --rev cd5958b` binds, 82 → 83. `--chain` appends SYN-1, CRC-1, SYN-1F and SYN-NS, 82 → 86.

The lead ran each of these, and each passed. The lead also ran negative probes, and the checker refused:
- a wrong kind;
- a wrong field;
- a field not on its kind;
- an unchecked key;
- an anonymous token named as a named kind;
- a hidden supertype.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `syn-ns-subject.json`. The lead's value is `35f1a60c0e0b9fb7ba981c0f29cdf8616c891affc217dadecf1d6b688ded0469`.
- `"successor"`: `{path, bytes, sha256}` of `syn-ns/successor.json`. The lead's value is 6330 bytes, `fab4cf5394db0bfa308e2bbeb2a60183cf08ce3691a61d1d5fe96777e065a864`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change bytes, give the exact replacement as data for `spec_syn_ns.py`. Do not commit.
