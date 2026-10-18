# D3B-0-r1 review

**REQUIRED-FINDINGS:** one required finding and one non-blocking observation.

## Subject and boundaries

The 6,752-byte manifest has SHA-256 `ae101c3401fe4fe079fca06941913bae916a10c408a22af9cdc68fff66515d8d`; all 30 members rehash exactly. All three product-map candidates, archives and base files match. The candidate is detached at `2ead5cf1796bb85f363c34fa8ff8fba715462369`, and its changed-file set is exactly the three mapped platform files. The four authority pins and product design-lock pin match. No new paths or inventory successor are needed.

I ran the permitted `python3 -I -B tools/check_operability.py source --repository .` in the candidate: passed, 114 rows, no findings. All other review work was read-only source/evidence inspection, hashing, JSON parsing, Git queries and reading/parsing the system's native library bytes. No Cargo, rustc, build, test, lane, network, other pane, delegation or prohibited private/store material was used. Only this directory's REVIEW.md and review.json were written; neither repository was edited.

## Required finding

### D3B0-R1-RF-1 (P2): Do not turn libproc listing failures into Complete(empty)

Location: `crates/platform/src/process.rs:2183-2187, 2198-2205`.

Both bounded listings test only for a negative native return. On this host, the libproc wrappers return zero on a failed underlying proc_info call: proc_listpids converts -1 to 0; proc_listchildpids converts -1 to 0 and otherwise divides bytes by sizeof(pid_t). Consequently a failure with errno set reaches listing(buf, 0, capacity) and becomes Ok(Listing::Complete(vec![])). The snapshot cannot distinguish ListingFailed from a complete empty child set, and group sampling/confirmation receives false successful enumeration evidence. M3-D item 18 and LD-D3B-3 require listing failure to remain distinguishable. The six positive-path controls and eight mutations do not cover zero-with-error returns.

Evidence: Read-only inspection of this host's dyld shared cache, image /usr/lib/system/libsystem_kernel.dylib, exports _proc_listpids at unslid 0x180852ef0 and _proc_listchildpids at 0x18085cc64: the former ends its underlying-call return handling with cmn w0,#1; csel w0,wzr,w0,eq (words 0x3100041f, 0x1a8003e0). The latter uses asr w8,w0,#2; cmn w0,#1; csel w0,wzr,w8,eq (0x13027c08, 0x3100041f, 0x1a8803e0). Thus -1 is explicitly returned to these Rust callers as zero, not negative. No native API probe or build was run.

Required: Handle the wrappers' zero-on-error convention with per-call errno discipline, distinguishing a legitimate empty list from a failure without consulting stale errno. Preserve the call name and errno in LaunchError::Io. Add deterministic controls for zero-with-error on each listing, successful empty children, and stale incoming errno; mutations that read a listing error as Complete(empty) must fail. Keep the single fixed capacity-plus-one buffer and the count-versus-bytes distinction.

## Explicit answers

**Q1: Yes.** LD-D3B0-1 is an acceptable staged implementation adjustment: the new bounded mechanism introduces no policy or production caller, while the existing supervisor continues using its unchanged mechanism until D3b-1 owns the migration. D3b-1 must move the sampler and confirm callers to the bounded API and remove the unbounded doubling API. This unit does not establish bounded production supervision.

**Q2: Yes.** `Err(LaunchError::Io {call, error})` preserves the failed call and errno, and satisfies the plan's intended `Failed(errno)` information without adding a redundant KillOutcome variant. D3b-1 must carry those errors into the per-pid evidence. RF-1 concerns errors incorrectly turned into successful listings, not this result-type choice.

## Remaining assessment

The listing allocation and capacity arithmetic are correct: exactly one vector of capacity-plus-one initialized pid slots, checked addition/multiplication/conversion before allocation, no growth loop, and Exceeded when the returned count exceeds the caller's capacity. A completely filled sentinel buffer therefore cannot be accepted as a truncated complete list. The child count is used directly, while the group byte count is divided by pid size. The exact-two-children control detects their confusion and checks capacities 0, 1, 2 and 4; the group control checks three members at capacities 2, 3 and 8. Both cover usize::MAX rejection. Native failure handling needs RF-1.

`process_identity` uses PROC_PIDTBSDINFO's pgid and both start-time fields. It accepts only an exact-sized result, maps ESRCH on a nonpositive return to None, and retains every other failure as Io. Treating the observed zombie ESRCH as no live identity is appropriate for this mechanism. The tests hold the zombie's parent alive and separately check an already-reaped root.

`Child::kill_descendant` refuses AfterReap, Root, pid ≤ 1 and Host before calling process_identity. It then compares pid and both start-time components for equality only; a changed identity produces no kill. Only a matching identity reaches one SIGKILL. ESRCH becomes Exited; other kill errors retain call `kill`. The protected-root context remains the owned Child. The code neither checks ancestry nor invents an eligibility policy. The reread-to-send window is the law's disclosed best effort, and Sent means only successful signal submission. Non-macOS stubs consistently refuse PlatformUnsupported.

The six tests cover the stated positive mechanisms, protected outcomes and RF-4. Both sides of the escapee fork attempt setpgid before publishing its pid, and the identity test verifies the resulting pgid. The lower-start-time control intentionally supplies another test-owned process, demonstrating that the platform is not an ancestry filter. The syscall recorder demonstrates no kill on changed identities or protected cases; source order confirms the early protections precede identity reads. The tests lack the native-listing failure case identified above.

The archived lane reports platform 331→337, seven suites on each side, no failures, and exactly six focused tests passing serially. I checked the corresponding log summaries. All ten checks.json rows report success: comparison, rustfmt, warning-denied platform Clippy, workspace all-targets check, focused tests, environment exceptions, operability source, unchanged census closure, verify_design and mutations. All three files are base-clean and candidate-clean in the formatting classification. All eight mutation logs contain actual test failures rather than compilation failures. These are archived results, not tests rerun by this reviewer.

The runner acquires its lane lock before comparing main and candidate bases, checks ancestry and disjoint changed paths before a conditional detached checkout, and then checks equal HEADs before the suites. The missing packaged rebase record is NBO-1 below. The available attempt-2 checks identify only operability as failed, and attempt 3 identifies only rustfmt as failed, matching SCOPE. Attempts 0/1's opening-base refusals remain lead-reported history. The final process_id accessor avoids the added pid( mint-census member without changing its exception list, and the live source check passes.

No added environment read or `let _ =` appears in the three-file diff. The archived closure check reports 19 bound files with no intersection. No new third-party dependency, production caller, walk, eligibility rule, cancellation policy, Linux qualification or complete macOS tree-kill claim is introduced.

## Non-blocking observation

**D3B0-R1-NBO-1 (P3): Archive the rebase record under its actual attempt.** REQUEST/SCOPE refer to the packaged lane's rebased.json, but that file is absent from both the package and its 30-member manifest. The actual record is /tmp/opensip-implementation/d3b0-checks-r1-attempt2/rebased.json: 274dccc5eced53828f444fa44e62cdeffabc2d0c to 2ead5cf1796bb85f363c34fa8ff8fba715462369. Git independently confirms that record's changed-file set and that both this move and the complete d704ed4-to-lane-base change set are disjoint from the three candidate paths. The final lane is correctly pinned at 2ead5cf, so this is a provenance correction, not a base mismatch.

Requested: Archive and hash the attempt-2 rebase record and correct the references to its attempt; do not imply the final already-aligned attempt itself performed that move.
