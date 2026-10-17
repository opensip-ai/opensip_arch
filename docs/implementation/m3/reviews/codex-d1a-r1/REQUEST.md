# Review request: D1A-r1 (the spawn primitive, `crates/platform/src/process.rs`; M3-D r5 items 1 to 8, macOS)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d1a-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 store.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d1a-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 19489 bytes, SHA-256 `d50ef70a21ea42d838204b4c75e3c268abcabc68674f1e1646944b03cc0229ed`, 85 members. Rehash every member.
- **Bases:** product main `808ad6476fb848f84e732ee233a47229370081f4`, clean (inventory v212, 173 contract successors).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d1a`, detached at the product base, holding the exact bytes `product-map.json` lists.

## Authority

- **The D1a plan r2** (`supervisor-d/d1a/PLAN-r2.md`; your `codex-d1a-plan-r2`, ACCEPT; NBO-1 carried in `reviews/codex-d1a-plan-r2/lead-assent.json`).
- **Law M3-D r5** section A, items 1 to 8.
- **The contracts:** BBC (`docs/coop/completion/broker-bootstrap.contract.v2.md`) and DRJ2 (`docs/coop/artifacts/delivery-rust-provider-join.v2.json`).
- **The macOS SDK 27 headers** at `/Library/Developer/CommandLineTools/SDKs/MacOSX27.sdk/usr/include`, and the pinned libc 0.2.189.

## What to review

`SCOPE.md` describes the change, the SDK lines, the findings while building, and the three lane attempts. Judge:
1. **Fidelity to the plan and items 1 to 8.** Check each of the following:
   - the closed classes;
   - the protocol constructors (BBC's and DRJ2's exact argv and environment), with the tool gated;
   - `VerifiedLaunch`;
   - spawn by path with `SETSID`, `CLOEXEC_DEFAULT`, `SETSIGDEF` and `SETSIGMASK`;
   - the pipes, including the moved child ends and `F_SETNOSIGPIPE`;
   - `addchdir` through `dlsym`;
   - `RLIMIT_CORE`;
   - the exit source, `WNOWAIT`, `wait4` and the reap-last rule;
   - `proc_listpids`;
   - the scratch root and child scratch, with `confstr`, `flock` and the no-follow sweep;
   - the unsupported build on other targets.
2. **The FFI.** Is every `unsafe` block sound: buffer sizes, ownership of descriptors, the `posix_spawn` attribute and action lifetimes, `fdopendir` ownership, and the `dlsym` transmute? Is `Drop`'s last-resort kill and reap correct?
3. **The tests.**
   - Do the 15 tests establish the macOS rows of D1-T1 to T9 and T7b, with the fixture's runtime effects accounted for as LD-D1A-4 says (plan r2, RF-2)?
   - Do the 12 mutations each prove a rule?
4. **The lane.**
   - Is attempt 3's serial platform suite the right lane of record, given `evidence/base-platform-flakiness.md` and attempts 1 and 2?
   - Equal failure sets, 15 new tests, Clippy, rustfmt, FW-01, the environment exceptions, the operability census (unchanged, LD-D1A-5), verify_design, and the census closure unchanged.
5. **Rules:** no new `from(`, `into(`, `pid(`, `line(` or `issue(` call, no new environment read, and no Linux claim.
6. **Inventory:** two new paths for an inventory successor.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D1A-R1-RF-n` / `D1A-R1-NBO-n`.
