The verdict on the source39 kit is **CHANGES_REQUIRED**, because one MUST-level gap remains. That is my own independent standing; root admission of the exported Runs has not been observed, and nothing here claims product qualification.

**The remaining gap (s39-M1).** The native membership law says every choice in the unit membership record is identity-bearing, since the record feeds the PlanId (native-evidence.md lines 730–732). But it never says which `unitKind` a TypeScript/JavaScript unit gets (lines 744–748). The schema offers `ts-program|js-program` with no mapping. I measured it on one `tsconfig.json` with `allowJs`:
- spelled either way, the record is schema-valid and passes every published membership check;
- the two spellings produce different membership digests (`34d0e48f…` vs `52a0e505…`), so two conforming hosts get different PlanIds for the same repository.

The fix in the kit would be one mapping row in that section. No SHOULD issues remain.

**Your previous findings.** All five MUSTs (M1–M5) and seven SHOULDs (S1–S7) from my prior review are fixed in source39, and I re-measured each one. For example, `ts-clones-required` now seals pass, and the membership-reordered mutation is refused. Of the 14 prior advisories, 11 are resolved and three are carried (A8 in part, A10, A14). There are six new advisories. None blocks acceptance; the main one is that reason (3) in the new comparison reason order can never be reached, because reason (1) always applies first.

**What was executed**
- **Custody:** the manifest (`c2f2f88d…`, parent `f71a5992…`) and all 104 files verified at the start and again at the end.
- **First run, before any fix:** my ported helpers made every one of the 26 Runs fail on the new schema. The original bytes and logs are preserved in `preserved/s39-original/`.
- **Corrections:** HC-14 to HC-32, each tied to a kit selector, listed in `tools/hc_source39.py`. Several corrections failed on their first attempt; those logs are kept too.
- **Complete Runs:** 27 claimed positives (TypeScript, Rust, syntax-only and the comparison family) pass schema validation (including published kit keywords), retained closure, and full proof replay, each in a fresh process. All are exported with object tables and every blob.
- **Mutations and tamper tests:** all 62 stores were replayed. The designed negative and every input mutation are refused, except two controls that are lawful by design; semantic tamper controls are refused by replay.
- **New vectors for source39 laws:**
  - discovery and membership rules, including the syntax-only fallback unit;
  - Run termination under the new termination contract, reproducing the D9 `analysis-budget-exhausted` golden;
  - the two new comparison absence reasons (`baseline-absence-unknown`, `current-absence-unknown`);
  - all 45 termination goldens;
  - 53 graph-query vectors using the new published envelope carrier.

**Status and limits**
- All 131 IDs are executed and none failed; the 3 future-qualification items are unperformed and not claimed.
- Checkpoints 0–11 are written, and no subprocesses are still running.
- Two parts of the termination contract are exercised only through the code paths, not on a real Run: the "required closure not installed" detail row and stage-terminal carriers.

Everything is in `output/`; start with `blind-review.md`, `blind-review.json` and `notes/10-gaps.md`.
