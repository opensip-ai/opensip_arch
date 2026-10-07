# VCS-1 exact M3 dirty-meaning design successor r1

ACCEPT-DESIGN-UNIT. requiredFindings empty. passageOverrides 1. inventoryUnchanged 167. productCodeUnchanged true. consumerRan false. fullC1bComplete false. productQualification false.

This is the passage successor accepted M3-C r8 item 4 names before C1b. It adds one meaning to identity-and-evidence line 546 and leaves that line's original text in place. No physical contract, product source, inventory, or lock edit is in this unit. Binding still needs substantive lead assent and `verify_design`; the product lock commit stays separate from the architecture archive.

## Pins

Subject manifest `docs/implementation/m3/snapshot-plan-c/vcs-1-r1-subject.json` is 942 bytes, sha256 `9ba4bbeb8bdad833c2f9dcdda7f331f7e994db7aff6d602f125f2edd8a5879a5`. All 4 members are sorted and unique, and each byte and hash pin matches.

Product HEAD is base `bf1ce2566120bcb7db339c3c8a1ee3853f300c8c`, and that worktree is clean. Architecture HEAD is base `7f9bc1e73958edd065def9331431b463bd9711a5`. At that commit, `PROPOSAL-r8.md` is 183744 / `578c186ec9fc239f42d88713b8c31ec7085ab507251691f6cbba01e49b6607e1`, and the Codex r8 review is 10106 / `e40064c75209e426568ecbc5312ad9c350b25ab5f5380b66a35101a5d699c42c` with verdict ACCEPT and empty required findings. `identity-and-evidence.md` is 135448 / `c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f`. `native-evidence.md` is 329013 / `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`. Both of those pins are current design-lock inputs.

The parent is that same identity-and-evidence pin. The successor's one candidate set is the subject minus `successor.json`, and each candidate pin equals its subject row. `successor.json` is 2849 / `dcca6976860869e2da1730c1b4f03fa0b7d015650229a0fdba126e5866027e3e`. It has one passage override and no passage supersession. The override's fields are parent, selector, before, and after. The selector is line 546. Its before text is the parent's line, `runtime-to-source correspondence.` The after text keeps that sentence and then the VCS-1 paragraphs. `CONTRACT.md` is the heading plus those paragraphs.

## Line 546 is unbound

The current lock has 131 contract successors. The only bound overrides of this parent among lines 542, 546, and 547 are B-S2's line 542 and line 547. That bound record is `docs/implementation/m3/config-discovery-b/b-s2/successor.json`, 4600 / `1f089c83f8c80751145dde78623e79c8298bb2ac094e576f52b1791cc61467ad`. No bound override or supersession selects line 546. This unit does not restate B-S2's cardinality or schema-member selections.

The selected inventory remains `repository-file-inventory.v167.json`, 618550 / `718cde32c35771b11527e45715a662c0850228d82b7bf611bfca541553bbbf2b`. This successor adds no inventory row.

## Item 4

The added passage follows accepted item 4. At M3, `dirty: true` on a Git observation means cleanliness has not been established: the host reads no Git object and cannot compare the working tree with HEAD's tree. That flag is not a claim that a particular path changed, and it is not a basis for `dirty: false` from index stat data or for an inferred change set. `NoRepository` stays `kind: none`, `commitId: null`, and `dirty: false`. The flag does not prove a clean revision, so an M3 Git observation cannot satisfy a `vcs-revision` correspondence that requires a clean commit, and no runtime, test, or history evidence import consumes one at M3.

The same meaning applies to each admitted D15 member's schema-3 Git observation. The schema-3 root stays `kind: none`, `commitId: null`, and `dirty: false`. Schema fields, admission, member order, canonical bytes, inventory-digest meaning, and historical retained observations stay as they are. The passage publishes no Git object reader, per-path change set, correspondence grant, record member, schema version, or C1b implementation, and it does not backfill an observed value. Item 4's separate duty, that `vcs-change@vcs-reported` stays non-complete unknown Coverage, is not minted here.

C1b, L, day 0, owner assent, and product qualification remain open. No consumer, Cargo, parser, or producer ran. `~/Library/Application Support/OpenSIP` is absent. Neither repository was edited. The architecture worktree still has its eleven pre-existing untracked operability and E2s paths; they are outside this subject.
