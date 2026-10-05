**J4a r2 — ACCEPT-UNIT**

J4A-RF-01 is **closed**. There are no required findings. This acceptance binds the exact r2 product diff and carries the lead’s recorded integration constraints.

Subject: `9c6496aeaca917a489a9ac2bc997c424339f7169942a57559ce717cc0aa60461` (137310 bytes; 11 existing files, +2826 / −42), against `1d24900230397e4959cfd6734879259341e5cb93` in `/Users/sb/code/opensip-ai/opensip-j4a`. All 31 supplied pins matched. The diff, HEAD and status were unchanged after both rerun lanes. [Pins](pin-verification.json), [subject diff](subject.diff), [final state](output-state.json).

**Closure of J4A-RF-01**

In [private_access.rs](product/crates/security/src/private_access.rs), lines 929–966, the whole reservation is taken before C-ACL or the suffix write. The platform suffix write retains its early verification and F_FULLFSYNC. The parent directory barrier follows. Only then does the helper reopen the fixed name without following a link, compare device and inode with the written handle, and invoke the final reader through that confirmed reopened object.

The native reader (lines 848–860) makes at most four positioned reads from offset zero into a buffer of expected length plus one. It returns a length only after observing EOF. Completion requires exactly the expected length and bytes; longer, shorter, different or unended input refuses Confirm, and read failure refuses ConfirmIo. This supplies [J-RW r4 item 3.2](pins/docs/implementation/m3/resume-repair-jrw/PROPOSAL-r4.md), line 247, in its stated order.

The final buffer/read allowance is one object, four edges and expected length plus one byte (lines 805–839). It is included in the single reservation before the first effect and spent before allocation/read. The early platform verification remains a separate check and is no longer the only byte confirmation. Platform write_new_regular and write_regular_suffix are byte-for-byte unchanged from r1.

The new regression (line 2363) changes a prefix byte, appends, truncates, fails the read or reports no end at the final confirmation point; each refuses, and the intact confirmed-inode case succeeds with one reader call. Native cap cases cover EOF, full buffer and empty file. The strengthened RW-C12 test (line 2269) refuses with one edge or one byte short before mutation, for private and ACL-omitted inputs, and confirms that exact limits cover the complete action and final read. Both tests passed in both independently rerun lanes.

**Delta and rebase**

Reconstructing the 11 base files at 1d24900 and applying the pinned r1 subject reproduces r1. Only private_access.rs differs from the live r2 subject. Applying the pinned r1-to-r2 delta reconstructs all 11 current files exactly. The delta changes only C-SUFFIX’s final confirmation/private helper and its tests. [Reconstruction and rebase verification](delta-verification.json).

All 11 owned base files are identical between d2c00a9 and 1d24900. The selected 16 existing harness/primitive source and required-runs paths retain identical blob IDs. X4-F3’s operation_handoff change is guard-start error mapping; the OperationFloor handoff remains. No changed J4a callee or seam was found. The carried C-ACL/P-ACL and P-PREFIX judgments, RW-P1/P2/P3 uses, typed results and repair scopes remain as reviewed in r1.

**Carried rulings**

Calls 1–3, 5–7 and 10 remain accepted as the lead’s rulings. Call 4’s correction and call 8’s finding are closed by the reserved final read. Call 9 remains accepted with its integration constraints: the four exact store-directory repair names and RW-K5’s empty kill set stay as ruled; no broader repair scope is required. Typed completion results remain the seam until O1/J4e add their assigned joining/event work.

**Independent validation**

| Lane | Passed | Failed | Ignored | Evidence |
|---|---:|---:|---:|---|
| `cargo test -p opensip-platform -p opensip-security -p opensip-storage --lib --locked --offline --no-fail-fast` | 1413 | 0 | 3 | [log](lanes/libs.log), [exit/time](lanes/libs.result) |
| `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast --locked --offline` | 1671 | 0 | 3 | [log](lanes/feature.log), [exit/time](lanes/feature.result) |

Both lanes passed all 23 J4a tests, including the new final-confirmation regression and strengthened budget test. The feature lane also passed both unchanged first-commit census pins, the feature-site allowlist and no-manifest-enable checks. Every invocation used nice -n 19, --locked --offline, a private 0700 Darwin-user TMPDIR and Cargo state under this review directory. The lane lock was acquired by mkdir after waiting, then released with rmdir immediately after Cargo finished and only when acquired by this reviewer. [Validation details](validation.json).

Pinned lead workspace, doc, build/fmt/clippy, drift/design/policy results inspected; only the requested minimum lanes were independently rerun. No crash-matrix run set ran.

**Integration constraints**

- X3c-3 integrates first.
- Hold J4a product integration until X9 r17 section RW is accepted.
- Integrate in one commit with exactly the six RW-F00 storage re-transcriptions and a full storage lead set; this review does not judge those six rows.
- Section RW records the four exact repair names and RW-K5's empty kill set.
- The three stale descriptions go to the next description batch.
- Rebase onto the integration base after acceptance, preserving the reviewed change and validating the integration context.

No file added, removed or renamed. No inventory successor, subjectManifestSha256 or inventoryCandidateAssessment is required. The three descriptions remain owed to the next description batch.

No repository edit, commit, push or delegation was performed. Git was read-only and confined to the named worktree. The real OpenSIP home and private 413 UUID fixture were not accessed. Review artifacts are under the requested r2 output directory.
