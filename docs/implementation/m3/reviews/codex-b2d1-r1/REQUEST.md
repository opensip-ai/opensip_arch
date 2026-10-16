# Review request: B2-D1-r1 (the closed YAML subset reader; M3-B unit B2-d, sub-unit B2-d1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2d1-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 store.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree, `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/host/yaml_subset_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch`;
  - in the candidate worktree, `python3 -I -B tools/tests/test_discovery_fw01.py`;
  - importing the bound B2-d0 reference read-only, to try inputs against `parse_pnpm_packages`.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b2-d1-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 12897 bytes, SHA-256 `5d8578545c72be76b480d2f96160c99624e364620850354f64af852fa444eb3b`, 55 members. Rehash every member.
- **Bases:** product main `c4f8eddd718bf6ef9e37bda6d54bc55fcdcdfb8c`, clean (B2-d0 bound as contract successor 171; inventory v209); architecture `11bd0d3899ec6fb9c6aff83d3987d4b183bf2c34`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b2d1`, detached at the product base, holding the exact bytes `product-map.json` lists.

## Authority

- **The B2-d plan r3, section 2** (your `codex-b2d-plan-r3`).
- **The bound B2-d0 reference** (your `codex-b2d0-reference-r4`): `b2-d-reference/reference/framework_recognition_reference.py`, its `parse_pnpm_packages` and `_scalar`.
- **Law M3-B r9 items 15 and 16.**

## What to review

`SCOPE.md` describes the unit. Judge:
1. **Equivalence.** Is `yaml_subset.rs` rule for rule the reference's reader?
   - The hand-written forms of the regexes: the key and comment tails, the separated empty flow, the block item with separation, the number and date patterns on ASCII digits with their backtracking cases, and the plain-scalar comment split.
   - The quote handling, the character set, the CRLF-only normalization, the BOM and tab checks, the bound, and the null-value rule.

   Construct inputs where the Rust and the reference might differ, and test them against the reference.
2. **The vectors.**
   - Is the grammar table complete for plan section 2 and B2-d0's review rounds?
   - Are the sweep's alphabet and seeds adequate?
   - Is generation correctly gated on the pinned reference?
3. **The tests:** all 1,540 vectors, the reasons, and the full byte sweep.
4. **FW-01:** the reader covered and pure.
5. **Evidence:**
   - the host suite, 8 = 8 base failures with three new tests;
   - Clippy and rustfmt;
   - the seven mutations;
   - attempt 1's history (Clippy only);
   - verify_design.
6. **Mint and environment rules:** no forbidden constructor names, and no environment read.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B2D1-R1-RF-n` / `B2D1-R1-NBO-n`.
