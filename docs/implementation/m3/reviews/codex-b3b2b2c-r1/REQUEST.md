# Review request: B3-B2B2C-r1 (the T2 link-map controls and the joint sweep; M3-B unit B3-b, sub-unit B3-b2b2c)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b2b2c-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, tests, builds, the lane, the census tool or `t2_link_controls.py`.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys or held trees.
- Never open a T2 held-out entry's store or overlay. You may read the lead-readable T2 cache (`/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1`), read-only, to check the controls' inputs. The census tool's `store_path` shows which entries are lead-readable.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - `python3 -I -B tools/check_operability.py source --repository <tree>`.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b2b2c-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 19277 bytes, SHA-256 `3f92df4f77cd2f417100f7e3d370f92fe36cc7318254942cec4118d8fbf403bf`, 79 members. Rehash every member.
- **Bases:**
  - product main `c0a976187d8efd06280aa98a5e1762a7b44e8c60`, clean (B3-b2b2b bound, inventory v206, 170 contract successors);
  - architecture `51d916212d4ace3844fdd02ad734925ec6246b3d`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b3b2b2c`, detached at the product base. It holds the exact bytes `product-map.json` lists (5 files).

## Authority

- The B3-b plan r2:
  - section 3's T2 link-map controls (a) and (b) and the joint sweep;
  - its NBO-1 (the `vcs: none` seam at the link stage, never a production placement bypass);
  - amendment A3's B3-b2b2c (your `codex-b3b-plan-a3-r1`).
- Law M3-B r9:
  - item 20, the first control, and the npm rendering;
  - item 22, the joint control;
  - B-S1 U-8.
- `docs/implementation/m3/corpus/FETCH-SPEC.md` §6 (the Cargo rendering; corpus bytes in no repository) and the reviewed T2 manifest.
- M3-B r5 item 9: the closed environment reads.
- B3-b2b2b (your `codex-b3b2b2b-r5`) and B2-c1's host instrument, as bound on main.

## What to review

`SCOPE.md` describes the unit and lead decisions LD-B3B2B2C-1 to 4. Judge:
1. **The tool** (`tools/security/t2_link_controls.py`):
   - Does it re-verify every member store and the overlay through the census's own verification?
   - Does it refuse held-out entries before any filesystem call, and write only outside the checkouts?
   - Does it reconstruct exactly the overlay's link targets with their verified bytes?
   - Does it render the carriers as FETCH-SPEC §6 and law item 20 state? Cargo's quoted keys are LD-4.
2. **Control (a):**
   - Is the `Supplied` wrapper exactly the plan's seam: placement and item 6b supplied for overlay members only, everything else native?
   - Does it prove the derived links equal the overlay's map, checked by the pinned `overlayDigest`?
3. **Control (b):** the unchanged product discovery over `git init` members with an empty valid index, and the record's completeness.
4. **LD-B3B2B2C-1:** `#[ignore]`d, lane-run controls reading the lane's private `temp_dir()`.
   - Is this an acceptable channel under M3-B r5 item 9 and FETCH-SPEC?
   - Is the lane's evidence that both controls ran (two passed) sufficient?
5. **LD-B3B2B2C-2:** only providing mounts are declared; a consumer-only member stays a nested repository. Is that law item 20's meaning, and is the control honest about it?
6. **The joint sweep** and LD-B3B2B2C-3:
   - Is equality of unit sets, plus boundary records and the native exclusions, the right transfer of SLM's P3 sweep to the product?
   - Is the removed-member refusal the U-8 check?
7. **Evidence** (`evidence/b3b2b2c-checks-r1/`):
   - security 14 = 14 and host 8 = 8 base failures, with one new host test;
   - the census unchanged;
   - Clippy, including host;
   - the T2 run;
   - every vector check, environment, operability and verify_design;
   - seven mutations, and which gate caught each (see SCOPE and the mutation logs).

   Also confirm no corpus byte is in the package.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B2B2C-R1-RF-n` / `B3B2B2C-R1-NBO-n`.
