I've finished the round-4 correction in `m1-report-projection-author-04`. The checker passed from the pinned subject and from a strict frozen copy with its own TMPDIR. Nothing was committed or pushed, and this is not an acceptance claim. The carrier unit is ready for review, but the report design is still blocked and AUDIT-G10 stays open.

**Frozen subject:** `subject-files.json` has SHA-256 `c66c1e34ba8710cebc5b9a20bbdae6dd789f7b1dbc7b3a9b72e9c350b9a39a37` and lists 17 files:
- **Code:** `check.py`, `report_model.py`, `build_owner.py`, `build_fixtures.py`, `seal.py`
- **Schema and owner data:** `report-projection.schema.json` (sha `32b2bc0e…`), plus seven files under `owner/`: envelope5 schema, inventory5 schema and data, coverage overlay, passage overrides, `design-obligations.v1.json`, `budget-derivations.v1.json`
- **Other:** `fixtures.json`, `source-pins.json`, `successor.json`, `contract.md`

**Reference closure:** 79 pinned external files and 2 directory listings. The mutable `docs/implementation/README.md` is not among them.
- Files are re-hashed at every open (1,421 times in the run), listings are re-checked each time they are read, and all 20 executed external modules were compiled from their pinned source.
- The historical metadata checker now runs inside the same process, so there is no child process.
- A stale bytecode file with a valid header runs under the normal loader but not under the checker's loader.
- The `declaredOutWrites: 0` counter is recorded before the result file is written, so it doesn't count that write.

**Results:**
- 146 report cases (25 accepted) and 22 envelope cases, each matching its expected code.
- 14 D9/cancellation cases, 28 delivery goldens (7 scenarios × human/json/agent/html) and 14 static-parity goldens.
- The coverage validator runs in full on both base and overlay; the byte-law scenario passes.

| Finding | Outcome |
|---|---|
| RPR3-1 | G1, its truncated-page variant, G2 and G3 are all refused (`J-GRAPH-COUNT`). A page at the public 100,000-item cap is accepted; mislabelled continuations are refused. |
| RPR3-2 | The placeholder allowance is gone. The document cap is derived from owner schemas: 27,827,964 B. B1 (10,490,063 B) and a maximal legal document (19,058,518 B) are accepted; anything over the cap is refused. |
| RPR3-3 | Your D9 correction is applied: D1 now gives `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`, and earlier step terminations are never rewritten. D2 is a typed refusal instead of a `ValueError`. |
| RPR3-4 | Closure enforced as described above. |
| RPR3-5 | Unscoped, base and overlay stop at the same pre-existing "Missing/extra module milestone prerequisite" failure. With one recorded in-memory fix (adding `assets.rs` → M1), both are valid. The C2 control (old fit fields) still fails with "Command metadata drift". |
| RPR3-6 | 12 design obligations, each with owning unit, milestone and gate (M4 exit; DR-G20 where relevant), closure criterion and a finite successor. |
| A1, A2 | S1 is now refused (`J-SLOT-RESOLUTION-CONTRADICTED`). An uncontradicted re-plan and H1 are still accepted as host assertions, but their counts are shown in the static section; hiding them is refused. |
| A3–A9 | Closed: `--out` handling, provenance names, baseline exclusion, listing drift, stale bytecode. Still open: A7 older-Run selection is blocker RP-DO-12, and A9 (generator) was not run. |

**Cancellation:** a report is built while the required render step is still running. A signal at that point cancels the render, so a delivered report can only carry cancellation phase `none`; anything else is refused. The interrupted (130) result is still delivered, as a run envelope that names the earlier Run.

**Still qualified or open:**
- **Design blockers:** eleven blockers (RP-DO-01, 03–12) keep report-design readiness blocked, including F03 package coupling and F05 entry points (gaps in existing owners), step duration and explicit older-Run selection. RP-DO-02 is conditional and not selected.
- **RP-OBL-C01 (envelope owner):** an invocation interrupted before any Run is committed has no valid envelope5 failure form. `errors` must be non-empty and no detail code names an interruption. I did not invent one.
- **Not built or run:** browser, accessibility, host delivery, measurement and generator lanes. The byte sizes are upper bounds, not performance figures.
- **Trusted host:** the host and the pin files as read at start are trusted, and a concurrent writer between verification and read is not excluded.
- **Pre-existing edits:** the architecture checkout already had uncommitted changes, which the pins record exactly. I did not modify it.

Everything is in `/tmp/opensip-implementation/m1-report-projection-author-04`; `contract.md` has the full outcome table. The run results are `scratch/pinned-result.json` and `scratch/strict-result.json`.
