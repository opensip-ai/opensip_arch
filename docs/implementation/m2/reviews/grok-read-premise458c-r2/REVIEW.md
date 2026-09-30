# Review: read premise 458c r2

Grok is the single reviewer. Claude Opus 5.5 leads. Law re-review of the read side's omission premise and the observation path. No repository edits and no product cargo.

Subject `docs/implementation/m2/read-premise-458c/PROPOSAL.md`, 15247 bytes, sha256 `5660fc33e811ebbed59ebf47cbba5d79cfed44663aa573cb0106f486dfd71ebc`. `PROPOSAL-r1.md` preserves the r1 bytes, 12514 bytes, sha256 `4e9b94f52d817ff631b997140bf874e08c25466f82349ddf740e8e1868e9c7dc`. The diff is the header and the four r1 answers.

## Verdict

**REQUIRED-FINDINGS.**

RF-1, RF-2 and RF-3 are closed. RF-4's absence rule for the fixed suffix is consistent with owner §5. Two new rows are wrong.

## What holds

The r1 recheck finding is closed. Steps 2 and 4 run 468 item 3's full set, including the required-file-owner limb: invoking user, private mode, one link, private ACL, for the fence, `project-registry.v2`, `selection.pair`, the endpoint marker, its lineage node chain and the trust current record. Step 2 applies that limb to the fence and to any required file already retained. Step 4 applies it to every file captured in step 3, bound to the identity retained at that capture. A missing, undecodable or wrongly linked member is a structural finding. A recheck failure still latches.

The r1 doctor finding is closed. A reachable incomplete I keeps owner §5 and `doctor-cases.json`: one actual defect entry per structural finding, under the existing classifications, with no new code and no collapse; the note stays off; 256 actual defects is a report; 257 ends on `HOST.IO_FAILURE` / `DOCTOR.REPORT_NOT_PRODUCIBLE`, exit 4, and latches. Doctor does not latch on a structural finding, and it still runs the step 4 recheck. A recheck failure produces no report. Other read commands stay on the incomplete row and latch. The settled branch is unchanged: when minting, the walk, the fence wait or a recheck refuses, doctor uses the 468 row and produces no report.

The r1 busy-wait finding is closed. Attempts sleep `FENCE_POLL` (25 ms, the lifecycle fence wait) and stop at 5 s or at 201 attempts, one try plus 200 retries. There is no re-walk and no reopen. All 201 attempts are reserved at the gate's per-attempt lock cost before the first try. A reservation that does not fit refuses on the budget row before any attempt. After it fits, a held fence cannot turn the wait into `WORK.BUDGET_EXHAUSTED`. The write gate stays a single attempt. 201 times the current flock charge (3 edges, 512 bytes) is 603 edges and 102912 bytes, inside the session caps.

RF-4's suffix rule matches the ban on inferring pristine absence. Owner §5 rejects a present partial installation and refuses to treat a missing child of that installation as pristine absence. §6 sends a present I with a missing registry, pair, marker, node or trust record to the incomplete row, and sends I positively absent to `INSTALLATION.NOT_INITIALIZED`. Step 0 uses the second row only for `ObservedAbsent`: the first missing fixed-suffix component (`Library`, `Application Support`, `OpenSIP`, `preview-v1`) positively observed absent by a no-follow lookup under its retained, admitted parent. A missing child inside a reached I stays item 7's structural finding. A non-directory, a symlink, a custody refusal, an I/O error or a budget failure at that name stays off the absence row and takes its own item 6 row. The write gate keeps its own classification. A missing H is the remaining mis-route, below.

## Required findings

### RF-1 — A missing H is sent to the actor row

Owner §3 says H must already exist, this act never creates H or any ancestor of H, and a missing, inaccessible or unsupported H refuses before any mkdir. `InitialActor` admits UID equality and the home spelling and bounds. It does not admit the home directory. `INSTALLATION.ACCOUNT_REFUSED` is the 468 item 6 actor row: unequal UIDs, home spelling or bounds, or a changed account.

Item 5 cites owner §4 and calls a missing H an account refusal. §4 is the publication section. The directory's absence is not one of the actor facts.

Failure scenario: the account record names `/Users/name`, the spelling was admitted, and that directory is absent. The observation ends on `INSTALLATION.ACCOUNT_REFUSED`. The account predicate succeeded. The write gate already reports a missing open of that path as custody. The reader is told the actor refused.

### RF-2 — An I/O error during the fence wait takes the busy row

`FileLock::try_acquire` returns the lock, `None` when the lock is busy, or `Err` for every other failure. The lifecycle fence wait returns that other error immediately. 468 item 6 sends filesystem and read I/O to `HOST.IO_FAILURE`, fault cause `host-io`, and reserves `LEDGER.BUSY_TIMEOUT` / `PROJECT.BUSY` / `ledger-busy` for the busy fence.

Item 11 says that once the 201 attempts are reserved, the wait ends only in the lock or the busy row, and that any ending other than the lock is the busy row.

Failure scenario: the retained fence descriptor fails `flock` with an I/O error, or the carrier stops being a regular file during the wait. The command ends on `LEDGER.BUSY_TIMEOUT`, detail `PROJECT.BUSY`, fault cause `ledger-busy`. The caller is told a writer holds the fence. The I/O row is the one that describes that failure.

## Not reopened

The receipt, the 465 item 4 scope, the 5 s bound, the 25 ms pace, the full recheck set, the partial doctor report, and positive absence of the first missing suffix component stand. The findings are the missing-H row and the fence-wait I/O row.
