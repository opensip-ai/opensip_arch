Codex review: **S-OP-2 r3**, the safe event vocabulary and sink law, a contract-successor proposal for the DR-125 owners (`docs/implementation/m3/operability/PLAN.md:408`). Claude Opus 5.5 leads, and you are the single reviewer. This is a law and contract-soundness review, round 3. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-s-op-2-r3.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- This is a law review, so run no product builds, cargo or tests. The lead keeps the native lane.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the 413 fixture.
- If you compute digests or encoding bounds, use read-only scratch scripts under your review directory.

## Subject

- **The subject:** `docs/implementation/m3/operability/s-op-2/PROPOSAL.md`, r3.
- **The previous revision:** `docs/implementation/m3/operability/s-op-2/PROPOSAL-r2.md`. It is byte-identical to your r2 subject (`91a2ea45…`, 83,628 bytes). Your r2 review is in `/tmp/opensip-implementation/reviews/codex-s-op-2-r2/`, and `PROPOSAL-r1.md` is the r1 subject.
- **Pins:** `hashes.txt` pins all three, plus the context files.
- **The product:** `/Users/sb/code/opensip-ai/opensip`, read-only. The subject cites `3d2d5b5`. The cited product files are unchanged at the main named in `hashes.txt`.

r3's "r3 changes and review responses" table maps SOP2-R2-01 to -03 and SOP2-R2-NB-01 to -07 to the items that change. Where your fixes offered a choice, the lead's preferences were taken:
- **R2-01: new item 13c, a closed wire schema** shared by writers and readers.
  - **The header.** Mandatory `ts`, `level`, `event`, `requestId` and `fields`. Optional identities, which must form a lawful scope shape. `component` is `"<role>:<ordinal>"`. `omitted` and `truncated` are 1–32, present only when nonzero.
  - **The kinds.** Integer, boolean and composite spellings are separate. K12 accepts only a project-relative path, or `{"elided":…}` with a constrained tail. K14 is `CanonicalIdentifier`, and K15 is the portable environment-name grammar.
  - **Item 13a's read-back** checks the schema exactly, plus level and required-identity consistency with the descriptor and the `truncated` count. Its values are reader-only.
- **R2-02: the full-maxima proof.**
  - **Caps.** The `Phase` and `ComponentRole` header tables are capped at 32 B, asserted for every future registration. `PathAnchor` is capped at 16 B.
  - **Frozen spellings.** Every composite has one; K12's `...` prefix is replaced by the `{"elided":…}` wrapper.
  - **Item 14.** Header maxima are computed from the caps: JSON 646 B and human 724 B, both asserted within R = 768. `MAX_LINE(E) = R + Σ(k + 4 + V)` uses exact key lengths and bounds both forms, asserted ≤ 4,096. Your 1,066-byte case is now at most 1,002 B, within its 1,060 B reservation.
  - **Depth** is counted inside a field value.
- **R2-03: finalization (item 16), before the required envelope is rendered or written.**
  - **Steps.** Cutoff; a bounded settle of in-flight reservations and writer drain; gate closure and abandonment accounting; the freeze; then S-OP-6 renders the frozen summary, and the envelope is written.
  - **Dispositions.** Per-record, per-sink disposition cells and per-reservation cells, first-transition-wins, give exactly one disposition each. Late producer calls and writer callbacks are counted no-ops in a post-freeze tally.
  - **The marker** gains `unconfirmed`.
  - **The bound** (200/100 ms) covers finalization only.
  - **The limitation** that records after the freeze are not logged is stated.

## Decide

1. **Resolution.** Is each of SOP2-R2-01 to -03 resolved? Is each of SOP2-R2-NB-01 to -07 adequately taken up?
2. **Wire schema (R2-01).** Is item 13c complete and unambiguous for every header member and every kind?
   - Is the lawful identity-shape list right against item 9's scope transitions and OPP:151-160?
   - Do the K12 path and elided-tail predicates exclude every absolute or escaping form while accepting every admitted project-relative path?
   - Are item 13a's consistency checks (level, required identities, `truncated` and `omitted`) correct?
   - Is the reader-only rule sufficient?
3. **Bounds (R2-02).** Recompute the header maxima (646 and 724) from item 14's caps.
   - Check that R = 768 covers both and that `R + Σ(k + 4 + V)` bounds both forms, given the per-field costs k + 4 (JSON) and k + 2 (human).
   - Check the counterexample (1,002 within 1,060) and the initial-event maxima (`log.loss.counted` 1,802, `config.value.resolved` 1,345, `provider.process.reaped` 1,319).
   - Does the `{"elided":…}` wrapper fit V = 256?
   - Is the depth convention consistent with OPP:191 and with C-1?
4. **Finalization (R2-03).**
   - Is the sequence well defined and bounded?
   - Do the disposition and reservation cells give exactly one disposition per missed sink projection, with no double count under late completions?
   - Is the frozen summary the one the envelope carries?
   - Are the five marker outcomes honest, in particular `unconfirmed`?
   - Are the post-freeze limitation and the narrowed timing claim stated correctly?
5. **New or changed text.** Look at:
   - the header-table and `PathAnchor` caps;
   - the unexpanded-source and output-byte provenance checks;
   - the frozen K8 maps;
   - the K6 census;
   - the K14 and K15 grammars;
   - the per-field elapsed meanings;
   - the marker's element-wise sum;
   - the rewritten controls.

   Did r3 introduce any new error?
6. **Scope.** Does r3 change anything beyond its table? Does it still stay out of S-OP-1, -5, -6, -7, -9, -10 and -12, O4, O7 and O9?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"findingResolution"`: one entry for each of SOP2-R2-01 to -03;
- `"requiredFindings"`: an array, empty on acceptance. Each finding has `id`, `location`, `problem`, `evidence` and `fix`;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: a single string, r3 PROPOSAL.md's sha256 as pinned in `hashes.txt`.

r3 has no verify_design subject manifest, because item 24 defers recording, so this verdict is on the successor text. The later recording unit will need its own `ACCEPT-DESIGN-UNIT` with a single-string `subjectManifestSha256`. This is not an inventory unit, so give no `inventoryCandidateAssessment`.

Do not commit.
