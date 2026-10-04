Codex review: **S-OP-2 r2**, the safe event vocabulary and sink law, a contract-successor proposal for the DR-125 owners (`docs/implementation/m3/operability/PLAN.md:408`). Claude Opus 5.5 leads, and you are the single reviewer. This is a law and contract-soundness review, round 2. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-s-op-2-r2.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- This is a law review, so run no product builds, cargo or tests. The lead keeps the native lane.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the 413 fixture.
- If you compute digests or encoding bounds, use read-only scratch scripts under your review directory.

## Subject

- **The subject:** `docs/implementation/m3/operability/s-op-2/PROPOSAL.md`, r2.
- **The previous revision:** `docs/implementation/m3/operability/s-op-2/PROPOSAL-r1.md`. It is byte-identical to your r1 subject (`e3b117f0…`, 60,424 bytes). Your r1 review is in `/tmp/opensip-implementation/reviews/codex-s-op-2-r1/`.
- **Pins:** `hashes.txt` pins both, plus the context files.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `30c5db1` (D3 integrated), read-only. The subject cites `3d2d5b5`. Every product file it cites (`bootstrap.rs`, `request.rs`, `commit.rs`, the three schemas and `Cargo.lock`) is unchanged between the two; `git diff --stat 3d2d5b5 30c5db1` over those paths is empty.

r2's "r2 changes and review responses" table maps SOP2-R1-01 to -07 and SOP2-R1-NB-01 to -06 to the items that change. Where your fixes offered a choice, the lead's preferences were taken:
- **R1-01.** Sealed `CodeEnum`, implemented only by `code_tables!` in the registry module. A `TableRegistration<E>` token only that module can mint. Each table listed with its provenance: `registry-literal`, `generated-contract` or `protocol-enum`. Members accepted only as `literal` tokens and grammar-checked. Templates under the same rule.
- **R1-02.** Item 13a: closed re-admission of persisted records, with per-kind read-back predicates. Records lacking a valid header or a descriptor are dropped. Retired events keep complete descriptors, and code-table members are never removed. The residual (grammar-valid values placed by a party able to write the log directory) is stated and left with S-OP-1.
- **R1-03.** The atomic load is the admission point, and every syscall needs its own load, including continuations and the marker. The one-unit (≤ 64 KiB) post-closure residual is stated and referred to S-OP-7 with the X3D owner's assent (R8).
- **R1-04.** A timed wait on the termination path, with a producer cutoff, gate closure and the final snapshot at expiry. A blocked writer is abandoned to process exit. The kernel-stall limitation is stated. The marker is best-effort with four observable outcomes.
- **R1-05.** Item 14's whole-line proof: header reserve 768 B (JSON 678, human 756), keys ≤ 32 B, per-field overhead 36 B, each kind's encoded V, and `768 + Σ(36 + V) ≤ 4,096`. K8 is a fixed-index array.
- **R1-06.** Item 13b's rule E for both forms, covering the complete `Bidi_Control` set.
- **R1-07.** `max_rss_native` (Count) plus `rss_unit` (`kib`/`bytes`), matching M3L:405 and Q0:889, with an optional checked `max_rss_bytes`. M3L:286 (SM-10, "bytes") is flagged as a cross-law note, and M3-L is not edited.

## Decide

1. **Resolution.** Is each of SOP2-R1-01 to -07 resolved? Is each non-blocking observation adequately taken up?
2. **Code tables (R1-01).** Does the sealed trait, the private registration token, `literal`-only members, the grammar check and the listed provenance close K1 and K3? Probe for a remaining bypass:
   - a macro-generated literal;
   - a `generated-contract` table whose generator input is not pinned;
   - a `protocol-enum` table that diverges from its schema;
   - a template.
3. **Re-admission (R1-02).** Are item 13a's header grammars and per-kind predicates complete and correct? Are the drop reasons and disclosure bounded? Is the stated residual honest and correctly owned by S-OP-1?
4. **Gate (R1-03).** Is "the load is admission, one load per syscall" stated consistently in item 17, C-7 and the forbidden substitutes? Is the residual bound (one unit per sink writer) right? Is the referral to S-OP-7 and the X3D owner a lawful deferral rather than a decision?
5. **Termination wait (R1-04).** Does item 16's timed wait bound the command's completion independently of a blocked syscall? Are the cutoff, the final snapshot and the disposition of unwritten records well defined? Are the stderr-lock rule and the kernel-stall limitation correct? Can the marker outcomes be observed as C-7 requires?
6. **Encoding proof (R1-05).** Recompute the 678 B and 756 B headers, the per-field overhead and each kind's V, including K3's unrecognized form (65), K6 (157 into 160), K7 (48), K8 (21·n + 1) and K10 (49 into 64). Check the largest initial event (1,905 B). Is anything that can legally be written left out of the bound?
7. **Escaping (R1-06).** Is rule E complete, identical in both forms, applied to every string-bearing kind, and within the bounds? Is the closed-set rule for future Unicode versions sound?
8. **RSS (R1-07).** Do `max_rss_native`, `rss_unit` and `max_rss_bytes` preserve M3L:405's native-unit measurement? Are item 23's interpretations of each measured field correct?
9. **New or changed text.** Look at:
   - the two `storage.commit.*` events and owner-token construction, against `crates/storage/src/commit.rs:66-75`;
   - provider events requiring Project, Plan and Execution;
   - the guard's `p2-name-match` category;
   - counter ownership;
   - `Reduced::from_capture`;
   - the K1 and K5 grammars, including `_`.

   Did r2 introduce any new error?
10. **Scope.** Does r2 change anything beyond its table? Does it still stay out of S-OP-1, -5, -6, -7, -9, -10 and -12, O4, O7 and O9?
11. **Controls.** Do C-1 to C-12 now include every case your r1 review asked for?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"findingResolution"`: one entry for each of SOP2-R1-01 to -07;
- `"requiredFindings"`: an array, empty on acceptance. Each finding has `id`, `location`, `problem`, `evidence` and `fix`;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: a single string, r2 PROPOSAL.md's sha256 as pinned in `hashes.txt`.

r2 has no verify_design subject manifest, because item 24 defers recording, so this verdict is on the successor text. The later recording unit will need its own `ACCEPT-DESIGN-UNIT` with a single-string `subjectManifestSha256`. This is not an inventory unit, so give no `inventoryCandidateAssessment`.

Do not commit.
