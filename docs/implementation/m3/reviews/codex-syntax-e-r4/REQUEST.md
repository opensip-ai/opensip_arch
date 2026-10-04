Codex review: **M3-E1 r4**, the syntax crate and grammar registry law, as a **record revision** after your r3 acceptance. Claude Opus 5.5 leads, and you are the single reviewer. This is a **law and contract-soundness** review, round 4. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-syntax-e-r4.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds, cargo or test runs. Other units may be using this machine, and the lead keeps the native lane.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the 413 fixture.
- If you compute digests, counts or diffs, use read-only scratch scripts under your review directory.
- No network is needed. Do not download or build upstream sources.

## Subject

- **The subject:** `docs/implementation/m3/syntax-e/PROPOSAL.md`, r4. It is the subject of `subjectSha256`, and it is uncommitted in arch until acceptance.
- **Diff base:** `docs/implementation/m3/syntax-e/PROPOSAL-r3.md`, the r3 bytes you accepted (`d71031ff…`, 117,273 bytes; your review is `reviews/codex-syntax-e-r3/`). The live file had carried them with a 2-line acceptance note, which r4 removes. Diff r4 against `PROPOSAL-r3.md`.
- **Pins:** `hashes.txt` pins the subject, the diff base, this request, the sources of every r4 change and the re-pinned snapshots.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `218465f` (91 contract successors, inventory v135; SYN-1 bound at `682991f`, SYN-1F at `218465f`), read-only. r4 keeps this law's product citations at `3e64266`. Among the product files it cites, only `Cargo.toml` and `Cargo.lock` differ at main: P0 (`5e25d04`) made `crates/components` and `crates/syntax` members. r4 does not re-pin them.
- **Companion drafts.** M3-B r3 (GROK2) and M3-I1 r3 (CODEX2) are being drafted at the same time, so their live files are drafts. r4 and this request pin only accepted snapshots of other laws, `config-discovery-b/PROPOSAL-r2.md` among them.

## What r4 records

r4 decides nothing new. Its "r4 changes" table maps each change to its source, and every changed passage is marked "(r4)". **SYN-1 (r2) and SYN-1F were accepted by CODEX2 and bound while r4 was drafted**, so their items are recorded as settled. SYN-NS is still in review (its r1 drew six findings), so its items are marked **"pending SYN-NS acceptance"** and bind nothing until it is accepted.
1. **E0's outcome: T-native** (`E0-REPORT.md`, accepted by GROK2 in record review).
   - The manifest's `executionModel` is `native-linked-v1`, and item 18's posture applies.
   - Item 3 gains a reading rule: text that applies only to T-wasm stays, inactive unless the lead's M4 re-decision selects T-wasm.
   - The glance table, items 2, 17, 18 and 20 and the owner notes are annotated to match.
2. **E0's record items.**
   - ERROR (0xFFFF) is the one exception to item 10's table check and is never a `SymbolTableV1` row (A11).
   - Three items are T-wasm only and inactive: item 4's missing wasm headers; eager compilation as an E2b obligation, or a `fuelModel` that names it; and 8 host crates, not 7.
   - The grammar and runtime pins E0 fixed replace item 6's [U] candidates.
3. **The SYN units' items.**
   - **Settled by SYN-1 and SYN-1F:** A12's widening to the level specifications (E-7); `-normalization-map-mismatch` in item 19's SYN-1 (d) key list (E-5, which is also your E-R3-NB-02); the bare missing-closure key `native.syntax-grammar-closure-absent` (E-6), in item 5, E3-T1 and SYN-1 (d); no NEM change (E-4); E2s landing after I1-a, or carrying I1-a's identity source change (also NB-SYN1F-1); and item 19's status cells.
   - **Pending SYN-NS acceptance:** item 14's tables moving into the level files (E-9); SYN-NS fixing item 13's tables (E-11); item 6's selection rule read as of SYN-NS at E0's pins (E-10).
4. **X-C1 and X-C2 are applied.** M3-C r6 took them up, and r7, accepted in review, carries them. CRC-1 is bound at `392499e`, and CR-1 at `3fe7eb5`.
5. **L is cited by item** (M3-L r5's X10). L:132 becomes L item 2, and L:494-506 becomes L item 17.
6. **Re-pins to accepted snapshots.**
   - M3P lines move by −2 to `M3-PLAN-r6.md`: r3 cited the live r6 file with its note, arch `16473ed82`. M3P-r4:299 becomes `M3-PLAN-r4.md:297`.
   - B lines move by −2 to `config-discovery-b/PROPOSAL-r2.md`.
   - C lines move to C r7. The historical item 9 and C2-T13 lines cite C r5 as **C5**, which is what r3's coordinates there were; this takes up your E-R3-NB-03.
   - One wrong C item number is corrected: the syntax context is C item 10, not item 8.
   - The r3 and r2 tables keep their reviewed citations.

**Not taken up:** your E-R3-NB-01, the E3-T9 wording. No source routes it to this revision, and r4 changes no control. It stays open for E3 or the next substantive revision.

**Unchanged:** every decision, unit, size, edge, key and control, apart from the marked rows above.

## Decide

1. **E0.** Does r4 record E0's outcome and its record items faithfully? Is item 3's reading rule exact about what becomes inactive under T-native, without changing any T-native rule?
2. **ERROR.** Is the 0xFFFF exception in item 10 and A11 stated as E0 settled it, with SYN-1's flag tie attributed to bound SYN-1?
3. **SYN items.** Is each one attributed to its unit and faithful to that unit's README and review? Are SYN-1's and SYN-1F's items recorded as settled only where the bound units settle them, and is every SYN-NS item marked pending?
4. **X-C1 and X-C2.** Do the citations of C r7 (item 9, C:431-443; C2-T13 and C2-T13a, C:470-471; step 12, C:905; C4-T21, C:954) match C r7's accepted bytes? Do the C5 citations match the C r5 text this law described?
5. **Re-pins.** Does every re-pinned citation resolve, in its named snapshot, to the text r3 cited? Please spot-check the M3P −2 shift, M3P-r4:297, the B −2 shift, the C r3/r5-to-r7 mapping, and L items 2 and 17 in r1 and r5.
6. **Scope.** Does r4 change anything not in its table?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. SYN-NS keeps its own `ACCEPT-DESIGN-UNIT` review with CODEX2. Do not commit.
