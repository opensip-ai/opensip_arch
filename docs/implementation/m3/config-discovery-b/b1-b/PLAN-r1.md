# B1-b implementation plan r1 (M3-B unit B1-b: carriers, invocation mode, environment check)

**Lead plan record, 2026-10-14; r1. Not law, not code.** B1-b follows B1-a, which is bound (product code `50cefc64`, inventory v188 at lock `c0151bc`). Codex reviews this plan before any code is written.

**Authority.**
- M3-B r4 (`config-discovery-b/PROPOSAL.md`, cited as MB):
  - item 2: the carriers, their custody and the global location;
  - item 3: invocation mode;
  - item 9: no environment side channel;
  - item 15: no write;
  - the B1-b row of "Units after the law" (MB:876), with its gate cells FW-01, SL:3 and flag `--project`.
- X2 r9 (`m2/project-root-x2/PROPOSAL-r9.md`, cited as X2): item 3a, carrier capture; its lead decision on 3a's order; item 9, the budget; item 10, units.
- AQ §1.1 and HFC §3: CI never probes local; malformed or hostile local bytes never reject CI.
- SL S12 (`CONFIG.CUSTODY_REFUSED`, SL:1302).
- B1-a's resolver, which consumes these captures as `CapturedCarrierV1` (`crates/host/src/configuration.rs`).

## 0. What exists (product `c0151bc`, read for this plan)

**Project selection keeps nothing.**
- `examine` (`crates/security/src/custody/project_admission.rs:240-272`) opens `opensip.json` no-follow and judges it as `ProjectObject::ConfigurationFile`.
- Then it drops the `File`. It keeps no descriptor and reads no bytes.
- `Selected.config` only records "custody-checked file present".

**The capture model to copy.** `RegistryCapture` (`project_admission.rs:420-492`):
1. sample;
2. read through `read_bounded_observed` at a 4 MiB cap, charged to the session ledger;
3. re-sample, and require the two samples to be equal.

**The recheck set.** `ProjectRootAdmission::recheck` (`project_admission.rs:806-826`) holds fixed typed fields (chain, incarnation, marker, registry, `old_name_absent`), each compared by full `DescriptorMetadata` sample.

**The `.opensip` directory.** `observe_marker` (`project_admission.rs:561-618`) already opens `.opensip` and judges it as a project directory.

**Installation private access.**
- `ReadSession::capture`/`capture_with` (`crates/security/src/custody/installation_read.rs:471-505`) read a member of I under `assess_private_descendant_capture` and add it to the full recheck.
- An absent member latches the session ("missing is an error"), so an optional file needs another path.

**Invocation mode.**
- `InvocationModeV1` is defined twice:
  - `crates/host/src/invocation.rs:68-72`, carried by `AdmittedRequest::admit`;
  - `crates/host/src/configuration.rs`, added by B1-a.
- No code computes it.
- No `isatty` or `IsTerminal` use exists anywhere.

**The environment.**
- The only production `std::env::var*` read in host or security is `git_tracking::process_environment` (`git_tracking.rs:343-346`, `vars_os`).
- Test-only reads exist in security and host tests (HOME and fixture variables).
- `crash_barrier.rs`'s reads are in `crates/platform`.
- No `clippy.toml` and no `disallowed_methods` configuration exist.

## 1. What B1-b delivers

### 1.1 Project and local carriers (X2 item 3a)

**Capture by retained descriptor.** S3's selection keeps the `File` of the `opensip.json` it judged; it no longer drops it. When the invocation is interactive, `.opensip/local.json` is opened no-follow under the already-judged `.opensip` directory and judged the same way. In CI it is never looked up: no `lstat`, no open.

Each capture follows `RegistryCapture`:
1. the full metadata sample;
2. `read_bounded_observed` at `MAX_CONFIG_BYTES` (4 MiB, the existing custody bound), charged to the operation's ledger (X2 item 9);
3. a re-sample that must equal the first;
4. the SHA-256 of the bytes.

`ConfigCarrierCapture { relative, metadata, bytes }` is added to the admission.

**Recheck.** Both samples join `recheck` as typed fields, compared by full sample under the held fence (X2 item 3; X2 r9 header).

**Absence.**
- An absent `opensip.json` is no layer. Selection already records that absence.
- An absent `local.json` is no layer. Its absence is a positive lookup result under the judged `.opensip` directory, and it joins the recheck as "still absent".
- An absent `.opensip` directory gives no local layer; the marker path already observes that directory.

**Refusals.** A symlink, a non-regular object, failed custody or a size over 4 MiB is `CONFIG.CUSTODY_REFUSED`, through the existing `ProjectAdmissionRefusal::ConfigCustody` row (`project_admission.rs:110-166`). There is no new code. The subject names `opensip.json` or `local.json`.

### 1.2 The order (X2 r9 item 3a, lead decision): a two-phase admission

After selection, X2 requires:
1. item 2's placement check and item 3's chain walk;
2. then item 3a's reads, configuration resolution and X12 r4's pack admission;
3. then item 5's registry capture.

Today `admit_project_root` runs selection, chain, incarnation, marker and registry capture in one call (`project_admission.rs:859-888`).

**Lead decision LD-B1B-1: split admission at item 5.** The API makes the order enforceable by type:
- `admit_project_root_carriers(..., mode)` → `CarrierAdmission`: selection, chain, incarnation, marker and carriers. It has no registry capture.
- `CarrierAdmission::capture_registry(self, ...)` → `ProjectRootAdmission`, item 5.

The analysis path (wired later by J1) runs `resolve_analysis_configuration` (B1-a) on the `CarrierAdmission`'s captures before it calls `capture_registry`. Existing callers that resolve no configuration keep `admit_project_root`, which becomes exactly the composition of the two phases, so they behave as before.

**Rejected:** a resolver callback inside security, which would make security depend on the host's resolver. Also rejected: capturing carriers after the registry, which is X2's ordering violation.

### 1.3 The user-global carrier (MB item 2; lead decision there)

`I/host/settings.json` is read through the installation session's private-access judgment, never through X2's project premise. The B1-b work:
- **Optional capture (lead decision LD-B1B-2).** Add `ReadSession::capture_optional_leaf(prefixes, leaf, cap)`. Its result:
  - **absent:** a positive lookup result under the judged parent directory; the absence joins the session's recheck set;
  - **present:** a capture exactly like `capture`;
  - **a custody refusal:** latches the session, as today.

  An absent `I/host` directory is also no layer: X2 item 6 step 3 creates it at first registration.
- **Never created.** Analysis never creates the file or the directory.
- **Allowlist.** The global layer's allowlist is B1-a's; the resolver already refuses any other key `CONFIG.INVALID`.

### 1.4 Invocation mode (MB item 3)

There is one type, `crate::invocation::InvocationModeV1`. B1-a's duplicate in `configuration.rs` is removed, and the resolver imports the existing type (follow-up B1A-FU-1). One function computes it, `invocation_mode(stdin, stderr) -> InvocationModeV1`: `interactive` is exactly `stdin.is_terminal() && stderr.is_terminal()` (`std::io::IsTerminal`). It reads no environment variable.

J1 (the X11 successor) wires the call at the host entry. B1-b adds the function, its tests and no caller.

### 1.5 The environment structural check (MB item 9)

**Scope.**
- A `clippy.toml` in `crates/host` and one in `crates/security` set `disallowed-methods` to `std::env::var`, `var_os`, `vars` and `vars_os`, each with a reason.
- Clippy reads a crate-local `clippy.toml` first, so the lint applies to exactly those two crates and not to platform (`crash_barrier.rs`).

**Audited exceptions (lead decision LD-B1B-3).** Each is an item-level `#[allow(clippy::disallowed_methods)]` with a comment, and the list is pinned by a test:
- `git_tracking::process_environment` (the one production read, X2's refusal-only Git check);
- the existing test-only reads in host and security tests (HOME and fixture variables).

MB item 9 names "the test-only crash-matrix seams". Today's test reads are fixtures, not crash-matrix seams, but they are equally test-only. The plan lists each one and adds none.

**Controls.**
- A planted `std::env::var` in a host production file makes all-targets Clippy fail. This runs as a lane mutation control, like B1-a's.
- A pin test checks that the two `clippy.toml` files are exact and that every `allow(clippy::disallowed_methods)` in host and security is on the audited list.

## 2. Tests and controls

| Area | Controls |
|---|---|
| Carriers | <ul><li>A captured `opensip.json` reaches `CapturedCarrierV1` byte for byte, with path and SHA-256.</li><li>A swapped file between judgment and read refuses on the re-sample.</li><li>A file replaced after capture refuses on the held-fence recheck.</li><li>A file over 4 MiB, a symlink or a non-regular object refuses `CONFIG.CUSTODY_REFUSED`.</li><li>Absence gives no layer.</li><li>A `local.json` appearing after an absent observation refuses on recheck.</li></ul> |
| CI | <ul><li>A hostile `local.json` (malformed, oversized, wrong custody, or a symlink) has no effect in CI, and no lookup of it happens (a counting observer seam).</li><li>An interactive run consumes a valid `local.json` with layer-4 provenance.</li></ul> |
| Order | <ul><li>The phase types make a registry capture before the carriers unrepresentable.</li><li>For a refused project-layer pack ID: no registry capture, no RESERVED row, no lease and no journal (MB item 10's control). The resolve and pack admission run on the `CarrierAdmission`.</li></ul> |
| Global | <ul><li>Present, absent, absent `I/host`, a custody refusal, and an unknown key (`CONFIG.INVALID` through B1-a).</li><li>Absence is rechecked.</li></ul> |
| Mode | <ul><li>Pipes and files give non-interactive.</li><li>A pseudo-terminal on both streams gives interactive, through an injectable `IsTerminal`.</li><li>The function's source reads no environment.</li></ul> |
| Environment | The planted control, the exception-list pin, and all-targets Clippy with warnings denied. |
| FW-01 | Capture and resolution write nothing: no new file, directory or modification time under the project root or I, checked by before and after samples. |

**Verification:**
- `cargo test --locked --offline` for security and host, base versus candidate, with equal failure sets;
- all-targets Clippy with warnings denied, for security and host;
- rustfmt on edited files;
- the operability source census;
- verify_design.

**Inventory successor.** v189 follows the accepted code, which may add the two `clippy.toml` files and new test files.

## 3. Sequence

1. This plan, Codex-reviewed.
2. B1-b code: stage, checks, Codex `ACCEPT-UNIT`, the architecture record, then the product code commit.
3. The inventory successor v189, reviewed and bound by its own lock commit.
4. A status round.

## 4. Not claimed

This plan writes no code and binds nothing. It changes no law and wires no CLI command (J1). It does not do discovery (B2), member carriers (B3), S-OP-5 or qualification.
