The gap is real, and I've corrected it in my capture. In U-4b.2 the TS/JS `unitKind` was never specified, so two readers could give the same allowJs project different `membershipDigest`s. On the unchanged capture, a full `close_run` admitted both values. Every affected check passes after the fix, except the pin-gated owner launchers, which stop at their pin checks.

**Custody.** I verified the LIVE frozen39 manifest (SHA `f71a5992…`) and all 12909 members against their hash and length, with no mismatches. My regular-file capture is under `work/source`. At the end, exactly the 5 changed files differ from frozen39; the other 12904 members are unchanged, and there are no new files.

**Diagnosis.**
- **Text:** U-4b.2 assigns the Rust `unitKind` and the TS/JS marker, mode and `recognizerId`, but not the TS/JS `unitKind`. The schema enum allows both `ts-program` and `js-program`.
- **Model:** the only decision is `discover_units` line 3948, which picks `ts-program` only for `ts-tsconfig`.
- **Enforcement:** nothing checked it. `admit_unit_roots` explicitly ignores `unitKind`, the enumeration admission law ran during Run closure but never looked at unit fields, and no other owner assigns or checks the value.
- **Run closure:** on the unchanged capture, complete Runs with a `ts-tsconfig`, `js-allowjs` (from a `tsconfig.json` with `allowJs`) or `js-synthesized` unit closed. They also closed with the kind swapped before hashing. That is two `PlanId`s for one project.

**Law, following the current model.**
- **U-4b.2:** a TS/JS unit's `unitKind` is `ts-program` exactly when its mode is `ts-tsconfig`, and `js-program` for `js-allowjs` or `js-synthesized`. The kind follows the mode, not the marker file name.
- **U-4b.5:** a TS/JS unit with a kind that doesn't match its mode, or a TS/JS kind on another family's unit, refuses `ENUMERATION_MEMBERSHIP_ORDER`. U-4b.5 already assigns "mismatched projections" to that key, and the enumeration-plan schema already lists it, so no schema bytes change.
- **Code:** the mapping is one table, `TSJS_UNIT_KIND`, in the native model. `discover_units` now uses it, with identical output, and the enumeration check reads the same table.

**Controls.** I added them before the fix, so they failed first:
- **consumer24 checker:** 25 new rows.
  - They cover discovery, a lawful kind and a swapped kind for `ts-tsconfig`, `js-allowjs` (tsconfig and jsconfig markers) and `js-synthesized`.
  - They add wrong kinds on Rust, fallback and non-TS/JS-mode units, and real-Run closes and refusals.
- **Enumeration checker:** 2 new rows, with the digest recomputed, to show the published kind is admitted and the swapped kind refused.

**Results.**

| Run | Result |
|---|---|
| Unchanged capture | all 17 evaluator children exit 0 (consumer24 183/183); native 380/380 |
| Before the fix | consumer24 195/208 (13 new rows fail as designed); enumeration admitted the swapped kind |
| After the fix | all 17 children exit 0 (consumer24 208/208; other counts unchanged); swapped kinds refuse at Run closure with `ENUMERATION_MEMBERSHIP_ORDER`; integration 412; security body (pin gate bypassed) 464/464 with 11/11 sweeps |
| Native checker, real pin gate | stops at `PIN-MISMATCH` |
| Native checker, pin gate bypassed (labelled) | 380/380 |
| `run-evaluator3-checks.py`, `run-reference-checks.py` | invalid pins for exactly the 5 files; no child run |

**Limitations and observations.**
- **Pins:** the pin ledgers are stale for the 5 files, and the in-tree native report was not regenerated.
- **Admission is narrower:** memberships a reader of the old text could have produced now refuse. Lawful memberships and identities are unchanged.
- **Not checked at closure:** TS/JS mode against its marker, `recognizerId`, and the Rust workspace-versus-package choice.
- **Mode discrepancy, not fixed:** `discover_units` treats every `jsconfig.json` as `js-allowjs`, but the §1.2 mode table says one that writes `allowJs: false` is `ts-tsconfig`. The new law follows whichever mode is decided, so this is a separate question for you.
- **Receipt quirk:** my runner overwrote the enumeration checker's receipt file of the same name. Its full report is kept in `enumeration.stdout`.
- **Integration run:** the first attempt failed only because its report directory didn't exist; the rerun passed.
- **No claim:** none of this is an acceptance or readiness claim.

Files are in `/private/tmp/opensip-design-corrections/claude-tsjs-unitkind-author.v1`:
- review.md (sha 4fd4f58f…)
- review.json (sha ec5a4d47…)
- correction.patch (202 lines, sha ab1826f0…)
- delta-manifest.json (sha 5a353d68…)
