# Review request: B3-B2B1-r1 (the D15 readers and membership decision core; M3-B unit B3-b, sub-unit B3-b2b1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b2b1-r1/`).

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

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b2b1-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 12714 bytes, SHA-256 `b1475d5d046ac5deeb40d0bfb01db47109c13b10a33ad4a649e074f4386565b6`, 53 members. Rehash every member.
- **Bases:**
  - product main `03876532b54d8327db96091fababb1fd994a83d2`, clean (B3-b2a bound, inventory v204, 168 contract successors);
  - architecture `6666ae1abc8f17d01168c715a1d3b4999170ae7f` (A2 published).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b3b2b1`, detached at the product base. It holds the exact bytes `product-map.json` lists.

## Authority

- The B3-b plan r2 with amendments A1 and A2 (`b3-b/PLAN-r2.md`, `PLAN-r2-A1.md`, `PLAN-r2-A2.md`; your `codex-b3b-plan-a2-r2`), A2-1's B3-b2b1.
- Law M3-B r9 items 19 to 24 (`config-discovery-b/PROPOSAL-r9.md`) and B-S1's registry (`b-s1/registry/workspace-declaration-readers.v1.json`).
- B3-b0 (`b3-b-reference/`, contract successor 168): `member_reader_reference.py` and `evidence/check.py`, at their bound bytes.

## What to review

`b3-b2b1-r1/SCOPE.md` describes the unit and lead decisions LD-B3B2B1-1 to 8. Judge:
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
   - Are the 116 cases and the 20 rootless cases complete?
   - Are the TOML controls' product expectations, computed by substituting unparseable TOML, a sound statement of A2 r2's `parse` mapping?
   - Do the 26 JSON controls cover the alignment A2 r2 requires?
4. **The closure re-pin and the projection** (LD-B3B2B1-1): `custody.rs`'s one declaration, and the closure row. `evidence/b3b2b1-checks-r1/equality-projection.json` must show changes only at `closure/6` in both census files.
5. **The identity change** (LD-B3B2B1-7): the read-only `TomlTableView` views and the `dependency-policy.json` pin. The identity dependency check fails at the base, and the lane shows it equal at the candidate. Is that the right handling?
6. **Controls and evidence** (`evidence/b3b2b1-checks-r1/`):
   - the suites: security 14 = 14 failures with three new tests, identity equal;
   - Clippy, rustfmt, the vector checks, FW-01, the census and operability;
   - eleven mutations, including the forbidden-access mutation that changes no output. Are they meaningful?

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B2B1-R1-RF-n` / `B3B2B1-R1-NBO-n`.
