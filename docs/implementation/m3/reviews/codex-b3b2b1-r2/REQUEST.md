# Review request: B3-B2B1-r2 (the D15 readers and membership decision core; M3-B unit B3-b, sub-unit B3-b2b1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b2b1-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, tests, builds, the lane or the census tool.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry, store or overlay.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository <tree>`;
  - in the candidate worktree, `python3 -I -B tools/security/workspace_member_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`, which reads no filesystem tree.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b2b1-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 13198 bytes, SHA-256 `e6c9d3b45f50c8386d5c79a32267a5cc2512a12ad1f3fab843e315e34a134bdf`, 55 members. Rehash every member.
- **Bases:**
  - product main `03876532b54d8327db96091fababb1fd994a83d2`, clean (B3-b2a bound, inventory v204, 168 contract successors);
  - architecture `6666ae1abc8f17d01168c715a1d3b4999170ae7f` (A2 published).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b3b2b1`, detached at the product base. It holds the exact bytes `product-map.json` lists.

## Authority

- The B3-b plan r2 with amendments A1 and A2 (`b3-b/PLAN-r2.md`, `PLAN-r2-A1.md`, `PLAN-r2-A2.md`; your `codex-b3b-plan-a2-r2`), A2-1's B3-b2b1.
- Law M3-B r9 items 19 to 24 (`config-discovery-b/PROPOSAL-r9.md`) and B-S1's registry (`b-s1/registry/workspace-declaration-readers.v1.json`).
- B3-b0 (`b3-b-reference/`, contract successor 168): `member_reader_reference.py` and `evidence/check.py`, at their bound bytes.

## Round 2

Your `codex-b3b2b1-r1` (`/tmp/opensip-implementation/reviews/codex-b3b2b1-r1/review.json`) raised four findings, which `SCOPE.md`'s "r2 changes" table resolves:
- **RF-1:** `TomlTableView::iter` is in source order, with two collision controls and the `cargo-key-order` mutation.
- **RF-2:** item 6b is asked per candidate, and branch A short-circuits, with the tripwire control.
- **RF-3:** listings are recorded against the reference's listing scope, with the `boundary-listed` mutation.
- **RF-4:** six JSON byte-bound controls, and a manifest whose bounded read is past the bound is `parse`.

**Judge first** whether each is resolved. Then re-check the questions below.

## What to review

`b3-b2b1-r2/SCOPE.md` describes the unit and lead decisions LD-B3B2B1-1 to 8. Judge:
1. **Fidelity of the core to B3-b0's `discover`** (`crates/security/src/custody/workspace_declarations.rs`):
   - carriers, custody, the cap and the parsers;
   - entry shapes and the grammar;
   - globs over the visible repositories;
   - placement, candidate failures, the cap, branches A and B, root-in-repository and item 6b;
   - links and their dispositions, and the declaration rows.

   Is `phase_one`/`phase_two` faithful to the SLM-first order of branch A? Is LD-B3B2B1-5's batching of item 6b equivalent to the reference's per-candidate order? Is LD-B3B2B1-3's order argument sound?
2. **`WorkspaceObservation`.** Is it the narrowing A2 accepted? Do the test adapter's records (`entry`, `markers` as `_markers` consults, `bytes`) make the subset and forbidden-path assertions meaningful? Does LD-B3B2B1-4 (bytes only after custody) hold?
3. **The vectors** (`tools/security/workspace_member_vectors.py`):
   - Does wrapping `_finish` and `_refuse` record the decision faithfully, without changing reference bytes?
   - Are the 116 cases and the 20 rootless cases complete, with the 38 controls?
   - Are the TOML controls' product expectations, computed by substituting unparseable TOML, a sound statement of A2 r2's `parse` mapping?
   - Do the 32 JSON controls cover the alignment A2 r2 requires, byte bounds included?
4. **The closure re-pin and the projection** (LD-B3B2B1-1): `custody.rs`'s one declaration, and the closure row. `evidence/b3b2b1-checks-r2/equality-projection.json` must show changes only at `closure/6` in both census files.
5. **The identity change** (LD-B3B2B1-7): the read-only `TomlTableView` views and the `dependency-policy.json` pin. The identity dependency check fails at the base, and the lane shows it equal at the candidate. Is that the right handling?
6. **Controls and evidence** (`evidence/b3b2b1-checks-r2/`):
   - the suites: security 14 = 14 failures with five new tests, identity equal;
   - Clippy, rustfmt, the vector checks, FW-01, the census and operability;
   - thirteen mutations, including the forbidden-access mutation that changes no output. Are they meaningful?

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B2B1-R2-RF-n` / `B3B2B1-R2-NBO-n`.
