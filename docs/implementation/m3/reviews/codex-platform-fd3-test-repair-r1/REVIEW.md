# CODEX2 review — platform FD3 test repair r1

## Verdict

**ACCEPT-UNIT**

The frozen two-path unit safely isolates the legacy descriptor-3 kernel test without changing production behavior or selecting a new descriptor channel. Existing O1 r2, S-OP-2b, and accepted O1-p authority is sufficient for this test repair; no new design selection is required.

## Frozen subject and scope

The requested `subject.json` SHA-256 is exact: `752e4ffb8a3015490012d10287d4d11d716a83c7fa568e950edae418cc1376e3`. All 96 declared members are present and unique, every byte count and SHA-256 matches, and the frozen subject has no undeclared members.

The product and architecture heads match the requested `5dfe28ea69ff488cf931bceed1d911c15e48da2e` and `8a590c708384454144a90c90f099df043eb394a7`. The candidate worktree has exactly the two declared existing paths modified, and both match the frozen product map. There are no new paths or dependencies.

The first 3,813 bytes of `harness_descriptor.rs`, containing the complete production implementation, are byte-identical to the parent. The original legacy kernel-test body is also byte-identical after removing the single new isolation wrapper. The second path adds exactly one conservative process-census row; all existing exception rows and every other top-level field remain equal by value.

## Failure and isolation mechanism

The inherited workspace evidence records the platform failure accurately: the platform library process aborts with an IO Safety violation and SIGABRT, without an individual failed-test name. It is not represented as an empty failure set. The isolated red probe demonstrates the causal ownership defect without placing the unsafe old behavior back into the parallel platform suite: the legacy body changes the descriptor flags of an unrelated `File` owner at fd 3.

The repaired legacy test reexecutes the same test case in a new program image. The parent platform suite remains at its normal parallel setting and never closes, replaces, or owns the process-global fd 3 for that legacy body. A child recognizes itself only when its arguments contain the exact case, the private skip marker, and `--test-threads=1`. Parent acceptance requires both a successful child exit and output showing exactly one passing test, so an empty exact filter cannot satisfy the wrapper.

The `pre_exec` closure used by the retained-owner probe performs only `dup2` and `fcntl`, clears close-on-exec on the child's fd 3, and leaves the source owner alive in the parent while `output()` waits. After exec, the child has no inherited Rust owner for fd 3; the selected probe takes ownership once with `File::from_raw_fd(3)`. It then verifies the same device and inode, preserves descriptor flags across the isolated legacy call, writes through the retained file, and lets the parent observe the exact retained contents. This establishes that the repaired test no longer corrupts an unrelated owner.

The unchanged legacy body still exercises closed, read-only, directory, writable regular-file, duplicate ownership, close-on-exec, and FIFO behavior. Isolation changes test-process custody only; it does not weaken the accepted kernel duties or confer production spawning authority.

## Evidence assessment

Owning r1 records three complete default-parallel platform library runs, each with 296 passed, zero failed, one pre-existing ignored, and zero filtered tests. Warning-denied all-target platform Clippy also passes.

All three runtime mutations use fresh compiled artifacts and fail at their stated witnesses: placing the legacy test back in the parent corrupts the retained fd 3 flags; omitting exact child-case identity does the same; and selecting an empty child filter is rejected by the one-pass requirement. Each mutation restores the exact source hash and is followed by a fresh positive run.

Repository r2 is the valid repository lane. It preserves both candidate source pins and passes the feature-enabled platform unit, integration, and documentation tests; default and feature-enabled all-target Clippy; package edges; source and environment-exception checks; design verification; diff validation; and public receipt-binding comparison. Repository r1 stopped on a precondition before tests or source mutation after a generic census proposal attempted to alter an existing explicit owner; it supplies no passing claim and is correctly superseded by r2.

The final census moves from 114 to 115 rows by adding only the `harness_descriptor.rs` process row with lexical count two for the test-only import and command construction. The 453-row mint audit and every existing owner remain unchanged. No `invocation.rs` refresh or production process permission is implied.

Both public receipt comparisons match, with zero blind invocations and no private or installation data access. The doctor repair remains a separate unaccepted unit. A fresh whole-workspace run, integration and archive, descriptions, status publication, pushes, and all platform and product qualification gates remain outside this unit.

## Required findings

None.

## Non-blocking observations

None.
