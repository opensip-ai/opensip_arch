# Review request: D2B-1-r2 (the strict CBOR profiles, the framing and the commitments; M3-D r5 item 10, D2b sub-unit D2b-1), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2b-1-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - running the package's `evidence/build_cbor_differential.py <arch root> <out> --check` against the candidate's corpus, with `python3 -I -B`;
  - running trial 07's `tools/wirecodec.py` on inputs of your own, with `python3 -I -B`;
  - in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d2b-1-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 9866 bytes, SHA-256 `931d73e381636170d7e929060986798bd896735907b400d89d2a6e966f92234f`, 43 members. Rehash every member.
- **The candidate base and lane base:** product main `a68be52fdb6290ead2beff4adaccefd92c81624c` (C1a3 integrated after round 1). The candidate's paths are disjoint from C1a3's, so the worktree moved onto it unchanged.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d2b`, detached at `a68be52`, holding the exact bytes that `product-map.json` lists (8 files).
- **Your round 1:** `codex-d2b-1-r1` (REQUIRED-FINDINGS: D2B1-R1-RF-1, RF-2), at `/tmp/opensip-implementation/reviews/codex-d2b-1-r1/`, also copied under the architecture repository's `docs/implementation/m3/reviews/`. The round-1 package `d2b-1-r1/` and its subject are history.
- **Main may move while you review,** by inventory v217's lock commit, which changes only `design-lock.json`.

## Authority

As in round 1.

## What to review

`SCOPE.md` opens with a "Round 2" section. Judge:
1. **RF-1:** `FrameAccumulator::push` now returns `Pushed {frames, refusal}`: every completed frame in wire order, then the refusal; `AfterRefusal` follows with no frame. Check that no completed frame can be lost, and that the frames and refusal equal repeated `read_frame` at every split. Check the new control, which covers a valid frame followed by an oversize length, a bad digest or a noncanonical payload, at every two-way split and byte by byte. Check SCOPE's interface note for D3a's participant.
2. **RF-2:** prefix acquisition is now two-phase (`take_prefix(bytes, 8)`, then the bound, then `take_prefix(bytes, 40)` and the allocation). Check that no digest byte is copied before the length and the remaining aggregate are judged. Check the control, which covers a whole oversized prefix in one push, a seven-plus-33 split and an aggregate overrun, each holding exactly 8 bytes with no digest byte copied and nothing allocated.
3. **The lane** `evidence/d2b-1-checks-r2/`:
   - components 0 = 0 failures, 19 new passing tests; identity 0 = 0, none new;
   - Clippy and rustfmt; the provider protocol tests; the differential regenerated; the package edges;
   - the environment exceptions, operability, the unchanged closure and verify_design;
   - eleven mutations, two of them r2's.
4. **No regression** in what round 1 accepted, and the rules: no new mint-census call, no environment read, no `let _ =`.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D2B1-R2-RF-n` / `D2B1-R2-NBO-n`.
