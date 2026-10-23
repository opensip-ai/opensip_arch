# B1-b implementation plan r3 (M3-B unit B1-b: carriers, invocation mode, environment check)

**Lead plan record, 2026-10-14; r3. Not law, not code.** r3 answers Codex round 2 (`codex-b1b-plan-r2`, REQUIRED-FINDINGS):
- **RF-01:** the real-`HOME` exceptions are stated by their actual use, in this plan and in M3-B r5: one comparison and three named installation-absence probes. The counts are corrected (NBO-01).
- **RF-02:** two controls are corrected.
  - The CI appearance control is narrowed to a custody-valid `.opensip` with no marker, beside a contrasting marker/custody refusal.
  - The environment-equivalence control stops before X2's tracking step, which reads the environment before repository discovery. The permitted Git refusal is asserted separately.

r2 answered Codex round 1 (`codex-b1b-plan-r1`, REQUIRED-FINDINGS):
- **RF-01:** sections 0, 1.1 and 2. Explicit, charged absence observations, rechecked under the fence; the inherited recheck facts corrected.
- **RF-02:** sections 1.5 and 2. The exception list now obeys law: M3-B r5, a one-item correction proposed beside this plan, enumerates every exception. The hostile-environment control is added.
- **RF-03:** sections 1.2 and 2. The legacy admission path stays byte-for-byte non-capturing, and only a new analysis path captures carriers.

r1 and r2 are retained beside this file. B1-b follows B1-a, which is bound (product code `50cefc64`, inventory v188 at lock `c0151bc`). Codex reviews this plan before any code is written.

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

**The recheck set (r2, RF-01).** `ProjectRootAdmission::recheck` (`project_admission.rs:806-826`) holds fixed typed fields. They are not all full-sample comparisons:
- the chain recheck compares identity, birth and custody (`project_chain.rs:59-67`), not directory modification time;
- the incarnation;
- the marker compares `MarkerObservation`, whose `Absent` is the same for a missing `.opensip` and for a `.opensip` without `project-id.v1`;
- the registry compares the full `DescriptorMetadata` sample;
- `old_name_absent`.

So nothing inherited would notice an `opensip.json` appearing after selection, or a `.opensip` containing `local.json` but no marker appearing after an absent observation. `Selected.config` is only a boolean.

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

**Absence (r2, RF-01): explicit negative observations.** Each is a charged no-follow lookup (one status-cost charge on the operation ledger), retained in the admission and repeated under the fence by `recheck`:
- **`opensip.json` absent:** a no-follow lookup of `opensip.json` in the selected root directory (the one the chain walk judged) returned not-found. The recheck repeats it and requires not-found. In every mode, an appearance refuses `CONFIG.CUSTODY_REFUSED`, with subject `opensip.json:appeared`.
- **Interactive mode only:**
  - **`.opensip` absent:** the not-found lookup of `.opensip` under the root is retained and rechecked. A `.opensip` appearing with or without `project-id.v1` or `local.json` refuses on recheck, so the ambiguous `MarkerObservation::Absent` is never relied on.
  - **`.opensip` present and `local.json` absent:** the not-found lookup of `local.json` under the judged `.opensip` descriptor is retained and rechecked.
- **CI:** no lookup of `.opensip/local.json` happens. The `.opensip` lookup is the marker's own, unchanged.

**Refusals.** A symlink, a non-regular object, failed custody or a size over 4 MiB is `CONFIG.CUSTODY_REFUSED`, through the existing `ProjectAdmissionRefusal::ConfigCustody` row (`project_admission.rs:110-166`). There is no new code. The subject names `opensip.json` or `local.json`.

### 1.2 The order (X2 r9 item 3a, lead decision): a two-phase admission

After selection, X2 requires:
1. item 2's placement check and item 3's chain walk;
2. then item 3a's reads, configuration resolution and X12 r4's pack admission;
3. then item 5's registry capture.

Today `admit_project_root` runs selection, chain, incarnation, marker and registry capture in one call (`project_admission.rs:859-888`).

**Lead decision LD-B1B-1 (r2, RF-03): a separate analysis path; the legacy path is untouched.**
- **Legacy, unchanged.** `admit_project_root` and its read-session and write-gate callers (`installation_read.rs:171-224`, `first_registration.rs:2098-2137`, `ordinary_writer.rs:95-109`) keep their exact reads, charges, refusals, rechecks and latching.
  - They capture no carrier and take no mode.
  - Their `examine` still drops the `File`. The retaining variant is a separate function the analysis path uses.
  - They gain no new recheck field. The absence and carrier fields are `Option`s, `None` on the legacy path, and `recheck` skips `None`.
- **Analysis, new.**
  - `admit_project_root_for_analysis(..., mode)` → `CarrierAdmission`: selection with retention, chain, incarnation, marker, the carrier captures and absence observations. It has no registry capture.
  - `CarrierAdmission::capture_registry(self, ...)` → `ProjectRootAdmission`, item 5, with the carrier fields `Some`.
  - `ReadSession` and the write gate each get an analysis wrapper with their existing ledger scope, latching and recheck.
  - J1 wires the analysis path, running `resolve_analysis_configuration` (B1-a) on the `CarrierAdmission`'s captures before `capture_registry`. The phase types make a registry capture before the carriers unrepresentable.

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

**Audited exceptions (LD-B1B-3, r2, RF-02).** These are exactly M3-B r5's enumerated list. r5 is proposed beside this plan and reviewed with it; B1-b's code waits for its acceptance.
- **The production exception:** `git_tracking::process_environment`, the only one.
- **Test-only exceptions.** Each is in a test target:
  - `commit_matrix_tests.rs:1980, 2007, 2033, 2107` (X9 crash-matrix rows);
  - `admission_tests.rs:1257, 1283` (`RUSTC` and `CARGO`), and `admission_tests.rs:2341, 2482` (the X8c helper and its input);
  - `journal_store.rs:1277` (test child);
  - `installation_fence.rs:305, 311` and `installation_root.rs:779` (test children);
  - `installation_root.rs:787`, in `installation_root_native_source_ignores_environment_child` (the real `HOME`, compared against the account-derived home only);
  - three installation-absence probes: `installation_routing_tests.rs:1024` (`a_development_build_ends_at_f0_with_no_notice_and_no_installation_path`), and `ordinary_writer_tests.rs:116` and `read_premise_tests.rs:104` (both `a_development_build_ends_in_the_no_embedded_release_row`). Each reads the real `HOME` only to assert that no installation exists under it;
  - the new hostile-environment control's child marker.

Each gets an item-level `#[allow(clippy::disallowed_methods)]` with its reason. The pin test parses host and security sources for every `allow(clippy::disallowed_methods)` and every `std::env::var*` call, and requires both sets to equal the enumerated list exactly (by file, enclosing item and variable name), each one inside `#[cfg(test)]` code or a `tests/` file except `process_environment`.

**Controls.**
- A planted `std::env::var` in a host production file, and one in a security production file, each make all-targets Clippy fail. These run as lane mutation controls, like B1-a's.
- The pin test above, and the two exact `clippy.toml` files.
- **The hostile-environment control (MB item 9; r2, RF-02).**
  1. A host test re-executes its own binary for one ignored child test, with the inputs in a file named by the enumerated child marker. It runs once with the environment cleared, and once with hostile `HOME`, `PATH`, `CI`, `TERM`, `NO_COLOR` and `XDG_*` values (set through `Command::env`, no `unsafe`).
  2. The child runs the carrier capture steps over a fixture project and global settings, calling the capture and absence-observation functions directly. It does **not** run X2's tracking step: `observe_tracking` checks the environment before repository discovery (`git_tracking.rs:321-339, 692-718`), so a hostile `HOME` or `XDG_CONFIG_HOME` refuses there even with no repository. The child then runs `resolve_analysis_configuration` and writes the canonical bytes of the resolved record, provenance and digest.
  3. The two outputs must be byte-identical.
  4. **The permitted Git refusal, asserted separately.** The full analysis admission over the same fixture succeeds with a clean environment. With the hostile environment it refuses with exactly X2's refusal-only Git-environment row, and with no other difference.

## 2. Tests and controls

| Area | Controls |
|---|---|
| Carriers | <ul><li>A captured `opensip.json` reaches `CapturedCarrierV1` byte for byte, with path and SHA-256.</li><li>A swapped file between judgment and read refuses on the re-sample.</li><li>A file replaced after capture refuses on the held-fence recheck.</li><li>A file over 4 MiB, a symlink or a non-regular object refuses `CONFIG.CUSTODY_REFUSED`.</li><li>Absence gives no layer.</li><li>(r2) Each appearance refuses on recheck:<ul><li>`opensip.json` after an absent observation;</li><li>`.opensip` containing `local.json` but no `project-id.v1`, after an absent `.opensip` (interactive);</li><li>`local.json` under a present `.opensip`.</li></ul></li><li>(r3) In CI, a custody-valid `.opensip` with no `project-id.v1` and a `local.json` inside, appearing after admission, causes no `local.json` lookup and no refusal attributable to `local.json`. The marker observation is unchanged in every mode. In contrast, a wrong-custody `.opensip`, or a changed marker, still refuses through the marker's own recheck, in CI too.</li></ul> |
| CI | <ul><li>A hostile `local.json` (malformed, oversized, wrong custody, or a symlink) has no effect in CI, and no lookup of it happens (a counting observer seam).</li><li>An interactive run consumes a valid `local.json` with layer-4 provenance.</li></ul> |
| Order | <ul><li>The phase types make a registry capture before the carriers unrepresentable.</li><li>For a refused project-layer pack ID: no registry capture, no RESERVED row, no lease and no journal (MB item 10's control). The resolve and pack admission run on the `CarrierAdmission`.</li></ul> |
| Legacy (r2, RF-03) | <ul><li>The legacy `admit_project_root` and its read-session and write-gate wrappers spend exactly the base ledger charges, objects, edges and bytes, compared against a base-computed expectation over the same fixtures.</li><li>They read no carrier bytes and make no `local.json` or extra `.opensip` lookup (a counting observer seam).</li><li>Their refusal sets and rechecks are unchanged; existing tests pass unchanged.</li></ul> |
| Global | <ul><li>Present, absent, absent `I/host`, a custody refusal, and an unknown key (`CONFIG.INVALID` through B1-a).</li><li>Absence is rechecked.</li></ul> |
| Mode | <ul><li>Pipes and files give non-interactive.</li><li>A pseudo-terminal on both streams gives interactive, through an injectable `IsTerminal`.</li><li>The function's source reads no environment.</li></ul> |
| Environment | <ul><li>The two planted controls (host and security).</li><li>The exact exception-list pin.</li><li>The hostile-environment byte-equivalence control.</li><li>All-targets Clippy with warnings denied.</li></ul> |
| FW-01 | Capture and resolution write nothing: no new file, directory or modification time under the project root or I, checked by before and after samples. |

**Verification:**
- `cargo test --locked --offline` for security and host, base versus candidate, with equal failure sets;
- all-targets Clippy with warnings denied, for security and host;
- rustfmt on edited files;
- the operability source census;
- verify_design.

**Inventory successor.** v189 follows the accepted code, which may add the two `clippy.toml` files and new test files.

## 3. Sequence

1. This plan, Codex-reviewed together with M3-B r5 (the item 9 correction). Both are published on acceptance, and the live `PROPOSAL.md` becomes r5 with its acceptance note.
2. B1-b code: stage, checks, Codex `ACCEPT-UNIT`, the architecture record, then the product code commit.
3. The inventory successor v189, reviewed and bound by its own lock commit.
4. A status round.

## 4. Not claimed

This plan writes no code and binds nothing. Its one law change is M3-B r5's item 9 exception list, proposed and reviewed separately in the same round. It and wires no CLI command (J1). It does not do discovery (B2), member carriers (B3), S-OP-5 or qualification.
