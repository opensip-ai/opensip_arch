# MAIN-GENERATE-1 plan r2: restore `generate_contracts.py` on main (LD-Q-304)

```text
Capability route: R2-DEEP
Codex: gpt-6.1-sol / high
Claude: claude-opus-5-5 / medium
Claude long-horizon lead: claude-opus-5-5 / medium
longHorizonLead: false; a small separate unit
Escalate when: a generated-output contract or a verifier must change (a stop back to the coordinator, LD-Q-304); a law question
Escalation route: R3-FRONTIER
Independent review: Codex (different vendor family from the Claude author); R2-DEEP
De-escalate when: the unit lands
Exceptional authorization: none
```

**Author:** the F1 lead. **Base:** product `efcb0c6d`, arch `6b0b05b1`; final parents and numbers are taken at readiness. r2 answers `../review/REVIEW-MG1-PLAN-r1.md` (8566dc1e…): `MG1-EXCEPTION-SCOPE: UNCHANGED`, with RF-1 and RF-2 below.

## 1. What is shown (`evidence/show-1/`, `evidence/rc-1/`)
- **`generate_contracts.py`: rc 0 at `4f70d67e`** (`passed: true`, `changed: []`, 8 outputs). **rc 1 at `b2b4e06f`:** `undeclared generated output present`. Same commands, tools and arch; fresh detached worktrees.
- **Cause: F1-a.** It added 8 files under `providers/typescript/src/generated/` beside the recipe's `protocol.ts`, and `tools/generate_contracts.py`:85-96 refuses any member beyond the recipe's expected set. F1-a's lane ran `check_typescript`'s generator lane, a different command. Nothing in F1's log shows `generate_contracts` was run: **my miss**, and neither lane tool nor gate runs it.
- **LD-Q-304 item 2, answered:** the provider lane's failure is provisioning. In a fresh worktree at `b2b4e06f`, it exits 1 with 14 `could not resolve`; after `npm ci`, rc 0.
- A slip in `01_show_r1.zsh` printed `rc=0` beside the ValueError, because `$?` read a later substitution. `02_rc_r1.zsh` is the record.

## 2. The options, classified
| Option | Touches | Verdict |
|---|---|---|
| **A. Move F1's 8 files to a new directory** | provider imports, emitters, tests, registry inputs, selected policy rows, inventory rows | **Proposed.** No contract or verifier changes; the refusal stays exact. |
| B. Declare the 8 in the recipe | the recipe's `outputs` and generator closure; they aren't its outputs | Refused: a false claim, and a generated-output contract change. |
| C. Move `protocol.ts` | `admission.py`:282 hardwires `providers/typescript/src/generated/` as the consumer | Refused: a shared tool and contract change. |
| D. Allow co-residents in the tool | `generate_contracts.py`, pinned | Refused: loosens the refusal. |

## 3. The change (option A)
**Move, `git mv`, content otherwise unchanged except what a path or import needs:** `carriers-v1.ts`, `control-cases-v5.ts`, `control-schema-v3.ts`, `source-census.ts`, `ts-enums.ts`, `ts2-extern-schemas.ts`, `tsr1-bounds.ts`, `tsr1-tables.ts`, from `src/generated/` to **`src/embedded/`**. `protocol.ts` stays, the directory's only member.

**One relocation mapping (RF-1), `src/generated/X` to `src/embedded/X`, applied to everything below and to nothing else:**
- **The 8 sources.** `protocol.ts` and its `dist/generated/protocol.js` stay.
- **The census's own predicates, which are path-based and an `OUT` change alone would silently break:** `embed-source-census.mjs`:44-55's long-line normalization prefix; `census.test.ts`:44-46's full-source assertion; `context-census.test.ts`:59's code-selection exclusion and :48's bounds-header lookup. Each keeps exactly its existing coverage over the mapped files. No exemption is broadened, and no K-* assertion is weakened. The prefix is an exact mapping, so `src/generated/protocol.ts` keeps the treatment it has today: **check which that is, and keep it.**
- **The three test-only exclusions:** `control-cases-v5.ts`, `source-census.ts`, `tsr1-bounds.ts`, in `tsconfig.build.json`:8-10 and both copies of `TEST_ONLY` (`census.test.ts`:58, :120). Its production-import check (:72-77) and RF-5 edge check (:119-125) stay.
- **The 5 moved runtime outputs:** `carriers-v1`, `control-schema-v3`, `ts-enums`, `ts2-extern-schemas`, `tsr1-tables`, from `dist/generated/` to `dist/embedded/`.

**Emitters run unchanged but for those paths, then re-check** (LD-Q-259's rule): embed-carriers, embed-control-schema, embed-source-census, gen-ts-enums, gen-tsr1-tables. **The census is regenerated from the final inputs, never hand-edited.** Each entry records length, sha256 and text, and the combined digest covers them and the path, plus the build configuration and lane inputs, so **unmoved consumers' entries change too, wherever an import literal does.** Membership and hashes are verified independently.

**Classify each grep hit before editing it.** `test-mutations/f1a.json`:276 is in the **retired** `F1A-RF7-TOKEN` record: keep that history, do not rewrite it. The active gate-flip control stays as it is, for this unit's false gate. Generated files hold old-path text, and `carriers-v1.ts` and the census are resolved by their emitters only.

**Reach, from a `git grep` at `efcb0c6d` (23 paths, reviewer to recheck):** 5 scripts; `src/context/{bounds,context,records}.ts`, `src/context/tsr1/options.ts`, `src/control/classify.ts`, `src/program/adapter.ts`, `src/wire/closed.ts`; 7 tests; `test-mutations/f1a.json`; `tsconfig.build.json`:8-10; `tools/typescript-lanes.json`.
- **`src/context/` and `src/program/` (LD-Q-190; RF-2).** LD-Q-190 says any edit before their own freezes goes through the F1-b and F1-c reviews. **So this unit's code review carries a named, narrow line, `MG1-F1BC-IMPORTS`, covering exactly those hunks, as F1-b's and F1-c's review for this edit only, before MG1's binding.** It requires: import-path lines only; unchanged type and value import kinds; unchanged resolved payloads under the mapping; unchanged initialization and call edges, by the actual import graph, not just a line diff; the false capability gate. **F1-b's and F1-c's freezes still re-review the rebased bytes.** No functional acceptance follows from it. F1-b, F1-c and F1-a's standings are unchanged, and **this unit flips nothing.** The coordinator is told of this route; if they want it otherwise, it changes here.

**Pins that move (checklist 19, 26, 32):**
- **Registry:** 9 lines name that directory. New registry, its parent `d0c2f327`.
- **Selected policy:** new, at a new immutable path, by the F1A-LANE precedent; the old stays. It covers the full new file set and changed bytes, unmoved consumers included. **`gen-ts-enums.mjs` is an output-path edit and an exception file.** `MG1-EXCEPTION-SCOPE: UNCHANGED` for the narrow edit at line 16: filename, kind, site `23:12`, expression, target, precheck order and unfollowed-loader limitation stay; only the sha moves. It can't cheaply be avoided: the CLI has no output override, and staging machinery is worse. **Same line and text alone are not enough (R3 review :9): the whole-file diff is what's reviewed.**
  - **The receipt (LD-Q-305):** the coordinator adopted that exception at R3, so when the new digest exists, they get old digest, new digest, the review line and the file's diff, and sign an erratum beside the adoption, before the binding. No new R3. Anything beyond that narrow edit is a stop, with no code past it.
  - `compiler.ts`'s exception is byte-equal, by this plan, and CP-F1C-COMPILER-VERIFY stays open.
- **Inventory:** 9 rows name the directory. Additive: 8 new rows; old rows stay by additive law (INV-UNTRACKED-ROWS-1).
- **Dist:** **5** `dist/generated/` files move (RF-1). **F4-a's frozen dist is unaffected: that commit's build, 42 files, `b54cd353…`, by digest.** It isn't relabelled and its manifest isn't replaced. No new dist is published here. F1-b's gets its own publication, note and pins.
- **Goldens, Rust:** no crate byte moves; `crates/` has no pin on these paths, by grep. Host-side `include_str!` of them: none found.

**Contract successor and inventory, by the builders, against the then-current parents,** numbers by readiness. Local arch main has since moved to SEC-PREDRAW-1's `6e67c4cd`; v249 and on are expected. Arch status text unchanged unless the reviewer says otherwise.

## 4. Proof
- `generate_contracts.py`: **rc 0 at the fix head,** status captured immediately; `passed: true`, `changed: []`, `write: false`, 8 outputs; a fresh output location; the selected tool and closure pins; clean tree; freshly provisioned worktree. A skipped or failing run stays a named deferral, not a pass.
- **Control, in a scratch copy:** an undeclared file put in `providers/typescript/src/generated/` is still refused with the same error; the tool is unchanged, by digest.
- `npm test` counts unchanged, with the capability still false, so the expected gated skips stay; f1a mutants killed by their intended assertion, under the tightened classifier, once that is reviewed; generators fresh; boundary suite; real selected clean and built provider reports, 0 refusals, exactly the 2 usages; report and generator lanes; verify_design; sweep; lane at the final head with the TS step, then `integrate.zsh`.
- `dist` built locally, compared through the mapping: the complete production file set, payloads preserved, import literals and regenerated census metadata accounted for separately. A control, not a publication.

## 5. It joins the lane (a proposal only; no lane tool is edited here)
**A post-binding-only check is how this got through.** Proposal: `generate_contracts.py` as a named step in **`pre_lane_gate.zsh`'s successor (LT-4's)**, since it's cheap, fails before a lane, and needs only provisioned tools; and listed in the lane's "not run" text until then. **Until it lands, this unit's and F1-b's scripts run it by name, at the final head,** and I'd suggest other units do too.

## 6. Order
**F1-b is delegated and in progress on the same files.** MAIN-GENERATE-1 branches from main separately. F1-b rebases over it: import paths conflict, mechanically. Slot: ask when ready, after SEC-PREDRAW-1 and F4-a, in readiness order. **A binding here renumbers against theirs.** SEC-PREDRAW-1 and F4-a are not held; their deferral is as LD-Q-304 says.

## 7. Not in this unit
The tool, recipe, closure and lane tools; F1-b's work; JS-SYNTH-PROFILE-1; any behaviour change: `CONTEXT_CAPABILITY` stays false at this unit's head.
