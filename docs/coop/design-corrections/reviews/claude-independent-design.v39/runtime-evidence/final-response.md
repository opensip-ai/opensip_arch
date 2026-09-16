**Verdict: CHANGES_REQUIRED.** There are two SHOULD issues, both in `opensip policy test`, and no MUST issue.

The review is in `/tmp/opensip-design-corrections/claude-independent-design.v39/review.json` and `review.md`. I checked the output against the charter: all 107 rows have both application flags false, TCB-SCOPE-01 has 13 dependents, and there are no build gaps.

**SHOULD issues**
- **S39-01: a real gate failure shows as indeterminate.** The authoring test gives up on a rule as soon as a required evidence kind is unavailable, so it loses findings it already knows. Take one known hit where a required import is missing:
  - Production gives verdict fail with 1 finding.
  - The test gives indeterminate with no finding, so the suite reports `fail` as unmet.
  - The two agree when the evidence is present or optional.
  - Section 5 says known findings and gating are unchanged, and the composition owner has a control for exactly this case. The policy test has no such control.
- **S39-02: universe tokens the evaluator refuses are accepted.** The evaluator only accepts `typescript`, `rust` and `syntax`, and says `typescript-v2` is not an alias. The policy test accepts `typescript-v2`, which is the token the checked-in suite uses everywhere, and it also accepts a made-up `no-such-universe`. All three spellings give the same summary, so the token is never checked at all. An author control also asserts that the suite is accepted.

**Advisory**
- **ADV39-01:** `native-evidence.schemas.v2.json` was edited in place (one description string). Native section 10 says those bytes stay unchanged and any edit becomes a successor document. The new digest is applied consistently, but the source38 digest is no longer registered and all 17 package exports have new RunIds.

**Closed or confirmed**
- ADV38-01, ADV38-02 and ADV38-03 are closed. For ADV38-02, all 99 read-only carrier scenarios matched my own reading of the precedence rules. For ADV38-03, both stale phrases were measured as present in source38 and gone in source39.
- The foundation detail census correction is confirmed: exactly the four new workflow details were added and the 289 substrate stays closed. Root reference v1 stays recorded as a failure (3 stale assertions); v2 is the only all-pass receipt.
- These topics were confirmed by my own probes:
  - query carriers: 9 commands, 20 public / 17 non-graph operations, and the delivery failure laws;
  - the repair:2 constructor;
  - the run-termination section 7 admission;
  - comparison presence knowledge (helper level only).
- Package16 was reconstructed, not relabelled. The formal manifest and the files-only projection are different objects with identical file lists. Its 17 exports, 7 queries and 9 membership probes match the root runs in content. The only overlay differences are a filled-in placeholder and an added README header.

**What ran:** subject, archive, all 12,909 members, parent38 and the delta were verified. The six pinned groups, all 17 evaluator3 children, the planning and inventory checks, the package tools and my eight probes all exited 0. Nothing is still running.

**Limitations**
- Five pin ledgers were not line-read; they are covered only by the executed pin gates.
- Two diffs were read only in part: implementation-coverage (first 260 of 1014 lines) and run-termination-goldens.
- Several probes are helper-level rather than full Runs.
- Some earlier probe attempts had harness bugs; I fixed and reran them, and their receipts were overwritten. These are described in the review.
- This is a nonblind review. No blind consumer artifacts, diagnoses or oracles were accessed.

Nothing is granted by this review: no grades or application. All 32 gates stay unperformed and all 54 recovery cases unexecuted, and the D9 successor obligation is carried. Final application needs a new, different Claude origin.
