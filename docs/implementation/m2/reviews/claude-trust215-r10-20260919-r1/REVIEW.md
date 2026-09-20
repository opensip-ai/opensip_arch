# Bounded review — frozen INCOMPLETE WIP215 revision 10 (closure of my r9 Q-1..Q-4)

Reviewer: Claude. Date 2026-09-19. **Scope: the r10 coordination corrections only; not protocol approval; no root/product edit, commit or push.** Root's announced follow-ups (general revoked-before-BEGIN preservation in a new 215 revision; 222 r5 corrections of S-1..S-5) are known and are **not** raised against r10.

## 1. Identity and what I ran
- `subject.tar.xz` SHA-256 `3dcfe284ba69ec2abbcb7736abd770305f16afe85337cbfbe65af4aa8d129f60`, 146,692 bytes, 744 members — equals the request; every `subject.json` member rehashed from the tar before extraction; 0 non-regular/unsafe/extra; end pass `re-verified`.
- `beforeimages-r10/OWNER.md` is byte-equal to the r9 `OWNER.md` I reviewed; both schemas byte-equal to r9. The only OWNER change is the Q-1 paragraph in C.
- Model: my re-run is byte-equal to `ordinary-batch-model-r7.json` (6272; 4096/1024; 80 history cells; 26233 states, 1074794 edges, 12987 closed). `coordination-corpus-r5/baseline.py` equals the model.
- **Corpus r5, executed by report name only** (same guarded runner as r9: names from `report.json`, generator names asserted absent, sources containing `mkdir`/`write_text`/`subprocess` refused, hashes verified, cwd = my directory): **43 named / 41 distinct, 43 rejected, 43/43 observed labels equal the predeclared ones**, baseline passes. *Disclosure:* my runner's first invocation aborted on its own name check (lowercase-only pattern vs the case name `r10-drop-already-U-reset`) **before executing anything**; I widened the pattern to `[A-Za-z0-9-]+` and re-ran. No generator or historical script was executed.

## 2. Closure
| r9 | r10 | Status |
|---|---|---|
| Q-1 redundant RESET from `UNBOOTSTRAPPED` | Root **keeps** the evidenced reset and makes it exact: the ROOT_CHANGED reset identifies the newly replaced shared root and replaces only the *current* reset projection; the reset event retains the exact BEFORE `RoleRecord` including the prior reset `EventRef`; the older reset record stays immutable and retained; "an unchanged state token does not imply an unchanged RoleRecord" | **closed.** This is the second of the two options I offered (evidence as a chain reachable through BEFORE records, with a one-slot projection), it is consistent with 222's single `reset:{cause,by}` slot, and it removes the contradiction with "retaining … reset evidence". Corpus variant `r10-drop-already-U-reset` is rejected by label |
| Q-2 OLD hit on a batch member unasserted | COMMIT event carries an evidence flag `history ∧ hit`; the history table grows to 80 cells over member history × member hit; no `REVOKE` for a selected member; my r9 `q2` and a "lost OLD evidence" variant are in the corpus and rejected | **closed** |
| Q-3 coverage unpinned | all seven counts asserted inside `checks()` (`retained exploration coverage`); my r9 `q5` is in the corpus and rejected | **closed** |
| Q-4 all-established seeds | separate mixed-history two-role profile: never-established BEGIN from `UNBOOTSTRAPPED`, QUORUM-LOST interruption, ABORT with the REVOKED cause masked out for never-established members, restart, history carried through ordinary healing, no never-established REVOKED interruption; limits string says plainly it is not every six-role history | **closed** within the stated bound |

## 3. Independent variants (r10 scope)
Six of my own (`claude-out/probes/model_mutants_r10.py`, `io/model-mutants-r10.json`): never-established REVOKED interruption allowed; history not carried through ordinary healing; evidence flag set for a never-established member; abort input unmasked for never-established; COMMIT marks non-batch history true; ordinary healing leaves history false. **All six rejected, none survive.**

## 4. Observations (no finding)
- Three of those six die on the generic structural precondition of `ordinary()` ("never-established cannot be TRUSTED/REVOKED") rather than on a purpose-named invariant. That is a correct and early kill — the precondition is exactly the F-5/C.2 rule — but if root wants each rule to have its own label, `abort()` could take `history` and refuse a `revoked` cause for a never-established member itself, instead of relying on the harness masking its inputs. Optional.
- Q-1's resolution makes one thing worth a sentence in 222 when it next changes: a reader reconstructing "all resets this role ever took" must walk BEFORE records through the event chain; the capsule projection alone shows only the latest. r10 already says this for 215; it is not a defect here.

## 5. Limits
One conditional model with admitted boolean inputs; I executed the model, the 43 report-named cases and six variants, all inside my review directory. No crypto, S4, format, typed-absence or native behaviour is modelled or reviewed; the mixed-history profile is two roles. Nothing here approves r10.

## 6. Result
**Q-1..Q-4 are closed; no new finding in the r10 scope.**
