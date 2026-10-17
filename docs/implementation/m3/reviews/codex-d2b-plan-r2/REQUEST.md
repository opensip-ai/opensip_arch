# Review request: D2B-PLAN-r2 (the provider codecs plan, M3-D items 10 and 11), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2b-plan-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries, and running the architecture's own Python references with `python3 -I -B` if you want to check a claim.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d2b-plan-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 566 bytes, SHA-256 `8ace57e56ef41b62aeb7d37af1fec25ebe4d424b40f449f4b64aaf088209b40b`, 2 members: `d2b/PLAN-r2.md` (the subject) and `d2b/PLAN-r1.md` (history, unchanged). Rehash both.
- **Bases:** product main `56d0eb53a888572dd0129fbc595d0c1be16eaf3a`; architecture HEAD `2894884ef33b0434a7c09029d2f727cf5f7a2524`.
- **Your round 1:** `codex-d2b-plan-r1` (REQUIRED-FINDINGS: D2BPLAN-R1-RF-1 to RF-3, NBO-1 to NBO-3).

## Authority

As in round 1: M3-D r5 items 10 and 11; NE §9 with FA-2's §9.8 and RUST3-LIM's §9.3a; DLV; RPP (including `limitPolicy.candidateSpoolAccounting`); P3T, its guard overlay and T2O; the product schemas; `schemas/wire/native-carriers-v1.json` (its `admission` rows and `commitmentMap`) in the product; the FA-2 and RUST3-LIM successor packages under `docs/implementation/m3/native-successors-fa/`.

## What to review

`PLAN-r2.md` opens with an r2 changes table. Judge:
1. **RF-1.** LD-D2B-3's three representations: received-byte commitment preimages bound to `commitmentMap` row by row (including the terminal coverage-stream rows), the constructed and fully charged spool entry, and the one candidate-slice byte-equality assertion. Are the spool accounting order and bounds as RPP states them?
2. **RF-2.** LD-D2B-15's contextual admission (its supplied `DispatchContext`, its live counters, and the retained `framePrecheck`, T016 and T020 before matching), LD-D2B-12's revised order, and §3's allocation of all 55 carrier admission rows. Is each row's owner right, especially the line between D2b's builder and admission, the Plan side (C4) and H?
3. **RF-3.** LD-D2B-16 (X-FA2-D) and LD-D2B-17 (X-RL-D), and §4's successor controls and vendored vectors. Is anything of §9.8 or §9.3a's wire duty missing or misassigned, notably the over-bound census handoff, the H settlement boundary and the token-absent inline path?
4. **The NBOs.** LD-D2B-2's depth bound over the whole closure (timing after D2b-0, the embedded payload's own bound, the deepest-valid and one-over controls); LD-D2B-7's read-side versus send-side Cancel; LD-D2B-3 item 5's `ReceivedBytes` provenance assertion.
5. **Q2's Unicode pin** (LD-D2B-11): both the reference's database version and the tables' version.
6. **No regression** in what round 1 judged sound (LD-D2B-1, -4 to -6, -8, -10, -13, -14's historical scope).

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D2BPLAN-R2-RF-n` / `D2BPLAN-R2-NBO-n`.
