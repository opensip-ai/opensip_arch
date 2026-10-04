GROK2 review: **M3-B r1**, OpenSIP's M3 configuration and discovery law (B1 resolver, B2 discovery, B3 multi-repository workspaces under D15). This is a **law and fact** review. Claude Opus 5.5 leads, and you are the single reviewer for this round. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok2-config-discovery-b-r1.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs. A timing-sensitive crash-matrix run may be using this machine, so run no `cargo`, no tests and no lead sets.
- Never touch the real home. `~/Library/Application Support/OpenSIP` must stay absent. If you run `git` anywhere, redirect `HOME` to a private 0700 scratch directory and turn hooks off.
- Never read the private 413 UUID fixture.
- If you compute digests, use read-only scratch scripts under your review directory.
- The product is read at main `30c5db1` (`/Users/sb/code/opensip-ai/opensip`). Read files or use `git show`; change nothing. Main has since moved to `3e64266` (F8a), which touches only `tools/contracts/dependency-policy.json` and `tools/identity/dependency-policy.json`. Every product file the law cites is byte-identical at both commits.

## Subject

The pins are in `hashes.txt`. The file is untracked in arch until acceptance.
- `docs/implementation/m3/config-discovery-b/PROPOSAL.md` (r1) is the subject of `subjectSha256`. It is a law with a unit breakdown. There is no separate UNITS file.

**Authority.**
- The M3-B row of the accepted M3 plan (`M3-PLAN.md:162`) and its critical-path row (`:204`).
- The accepted analysis-quality plan's D15 (`analysis-quality/PLAN.md:556`).
- FW-01, FW-13 and FW-14 (COV:7852, 8104, 8125; SMAP:54, 66, 67).
- The accepted T2 corpus (`corpus/`, T2b accepted by GROK2).
- The accepted operability plan's S-OP-5 (OPP §3.5 and §9).
- The contracts AQ §1.1, IE:518, SL S3, NE §1.4 and NE §8, and CH13 §2.
- M2 law X2 r8, which this law amends as X2 r9 (item 21).

## What the law decides (in brief)

1. **B1 (items 1-11).**
   - Six layers, and discovery is not a layer; at M3 the discovery fold into the semantic configuration is empty.
   - Carriers: `I/host/settings.json` (global, CFG-9 allowlist), `<root>/opensip.json`, and `<root>/.opensip/local.json` only when interactive.
   - The CI determination comes from terminal state, never the environment.
   - The pipeline order and its refusal rows; a remedy-text successor for `CONFIG.INVALID`.
   - Provenance, and `resolvedConfigDigest`'s covered and excluded inputs.
   - The S-OP-5 operational slot, with rules but no names.
   - FW-13's registry table.
   - No environment side channel, and no resolver exception to OPP §7.
   - **An amendment to X12 r3 item 8's order** (item 10).
   - Schema-one carriers.
2. **B2 (items 12-18).**
   - Downward discovery runs after the fence, on a new discovery ledger profile above the platform's hard caps.
   - The S3 instrument; U-0..U-9 as obligations; FW-01 controls.
   - Host-side recognition, with the provider consuming only.
   - The disclosure table; recommendation evidence for M4.
3. **B3 (items 19-24).**
   - The admitted D15 shape (W1-W3, M1-M5, a cap of 64).
   - Declarations: explicit, config, and two declaration readers, `cargo-config-patch@1` and `npm-workspaces-members@1`. The npm T2 rendering is fixed as a root `package.json` `workspaces`.
   - **X2 r9:** premise scope, item 3a carrier capture, and item 6b member observation.
   - Member effects on S3, U-8, the snapshot and the contexts.
   - No new flag and no consent; the seven flags and the scope of `grants.rs`.
   - Rows, with no new code.
4. **Successors (item 25).** S1 X2 r9 and S2 X12 r4 are laws. S3 (SL S3 + NE §1.4 + SLS V3), S4 (IE vcs-observation 3), S5 (NE §3.3 Cargo links), S6 (NE §2.4 TS links) and S9 (remedy text) are contract successors. S8 is a T2 record. No SMAP, CINV or NE §8 successor is needed.
5. **Findings (item 26).** F1-F14, including:
   - the ledger caps;
   - config-level `patch` stripped by NE:1750;
   - U-6 making every cross-unit edge unresolved;
   - X2 item 2 against the harness store's location;
   - plan impact of about 3 days on the host chain.

## Decide

1. **Facts.** Check the citations, especially:
   - the X2 lines (X2:29, :68, :74, :144-145, :163-215, :250-280);
   - `git_tracking.rs:5-6`, `:321-346`, `:743-776`, `:807`;
   - `project_admission.rs:240-269`, `:303-384`;
   - `work_ledger.rs:12-13`, `:205-213`;
   - NE:1743-1752 and NE:1786;
   - SL:163-168, SL:250-252, SL:261-262;
   - AQ:104-110, AQ:155-173, AQ:330-332;
   - the T2 workspace rows (T2M:7752-10327; T2R:187-221; T2F:112-125);
   - SLM:632-680 and :832-833 for the waiver's reach.
2. **R1.** Is a recognized native declaration at W enough intent to admit member repositories with no consent flag (items 20 and 23)? If not, what is the minimal lawful consent?
3. **R2.** Is the X12 item 8 amendment sound (item 10)? Is "nothing to clean up" still true after fence acquisition and the carrier reads?
4. **R3.** Is running the downward walk after the fence, on its own ledger profile, compatible with X2 item 9 and with the ledger's no-retry rule (item 12)? Are the provisional caps and the census-margin rule adequate?
5. **R4.** Is the empty discovery fold (item 1) consistent with AQ:104, AQ:155-157 and AQ:330-332?
6. **R5.** CI equals not-interactive, decided by terminal state (item 3).
7. **R6.** Is the waiver's reach correct: member directories yes, member Git evidence and `local.json` no (item 23, against SLM:636, :665, :669-680)?
8. **R7.** Is X2 r9 (item 21) safe as argued, and complete? Do S3-S6 cover everything frozen that stands in D15's way? Did the law miss a contract that forbids its reading?
9. **New errors.** Does anything in r1 contradict an accepted law, contract or plan?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. The design units B-S1 and B-S2 and the S9 remedy text will each need an `ACCEPT-DESIGN-UNIT` review of their own. Do not commit.
