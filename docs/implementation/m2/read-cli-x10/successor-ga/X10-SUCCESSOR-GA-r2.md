# X10 item 5 successor GA (r2): `opensip-host`'s `[features]` list admits C2b-1b's test-only `profile-allocations`

**r2** corrects r1 (`46fe3fd408b5126f97a2e3463429d3e716598255c69e3d329848836d0868a759`) per `REVIEW-x10-law-note.md`
(`3baa418775f7948866eacda3796e93a7c17c5625993a63aaf074dd7ea468a98e`, `X10-LAW-NOTE: REQUIRED-FINDINGS`):
- XL-1: the parent and the product bytes are now pinned;
- XL-2: a provenance and binding-destination table is added (§5);
- XL-3: the exclusive-consumer claim is removed.

The rule itself is unchanged from r1. **Author:** w2C:p1, the C2b-1b code author (Claude). This note states law; GA-2 is its enforcing control.

## 1. The parent (pinned)

- **Architecture commit:** `9b0eb222816d03eb1db9ee75b6c4eecbfa53ea2d`.
- **File:** `docs/implementation/m2/read-cli-x10/PROPOSAL-r4.md`, SHA-256 `33095e6c13c0e16a5e4fdc87832dbd2f048b01f126b432d49347cc2f116b386a`.
- **Passage:** law X10 r4, item 5, "Pin", third bullet (line 94):

> No cross-crate test bridge reaches the binary, the doctor ingress, or any default or release build. `apps/cli` and
> `opensip-reporting` have no `[features]` table. In `opensip-host`, `opensip-security` and `opensip-storage`, the only
> `[features]` entries allowed are X9's `crash-matrix` and X8's `scenario-fixtures`, each under its own law's release
> guards (r4).

That list has been widened before by law:
- X9 r1 and X8 r3 (X10 r4 item 5, line 89);
- M3-O1 r2 items 10 and 13 (`docs/implementation/m3/operability/o1/PROPOSAL-r2.md` :310-312 and :342). Their forwarded features `operability-dev-sinks` and `harness-instrumentation` are never a default, and are refused without debug assertions.

## 2. The successor text (replaces the parent's sentence for `opensip-host` only)

> In `opensip-host`, the only `[features]` entries allowed are exactly these four, with exactly these forwarding values:
>
> ```toml
> [features]
> crash-matrix = ["opensip-storage/crash-matrix", "opensip-security/crash-matrix", "opensip-platform/crash-matrix"]
> operability-dev-sinks = ["opensip-operability/operability-dev-sinks"]
> harness-instrumentation = ["opensip-operability/harness-instrumentation"]
> profile-allocations = []
> ```
>
> Their sources are:
> - `crash-matrix`: X9 r1 item 2;
> - `operability-dev-sinks` and `harness-instrumentation`: M3-O1 r2 items 10 and 13, forwarded only;
> - `profile-allocations`: TSR-1 funding, unit C2b-1b; LD-Q-165-B.
>
> No `default` exists. Each entry is under its own release guards. For `profile-allocations` these are:
> 1. It forwards nothing, and is never a default.
> 2. No manifest dependency entry of any kind (normal, dev or build) names it. It is enabled only on the command line of host's own test runs.
> 3. Any build with it and without debug assertions fails at `compile_error!`.
> 4. On macOS it compiles two test-only modules:
>    - it exposes the allocation support seam `typescript_profile_support` (`#[doc(hidden)]`), used by host's test target `typescript_profile_allocations`, which requires the feature;
>    - it enables the std-type reference model `typescript_profile_controls`. Those controls are ALSO compiled under `cfg(test)` and used by host's own library tests (`typescript_profile_tests`), with or without the feature.
>
> It is not a doctor bridge. It cannot reach the binary, the doctor ingress, or any default or release build.

The block above is the parsed `[features]` map without comments. It is not a claim to reproduce the manifest section's
physical bytes; those are pinned in §3.

**Unchanged:**
- the lists for `opensip-security` and `opensip-storage`;
- `apps/cli` and `opensip-reporting`, as X10 r4 item 5 and the widenings in §1 state them;
- every other sentence of X10.

## 3. The product bytes this successor describes (pinned at the current code head)

- **Product code head H6:** `d2729979f0ff264711620f74b42fce84fb36e34c` (on H5 `76ce532aa1191aa79791d4822c0855de9bf5e55a`).
  H6 changes only C2a's `btree_height` line in `crates/host/src/lib.rs`, the operability census fix. C2b-1b's lines are byte-identical.
- **`crates/host/Cargo.toml` at H6:** SHA-256 `0d9cf05ce826c07c29c41dea1da541cc13785272809d0fe2d400b10bcaebcbc9`. Identical at H5. Its parsed `[features]` map is §2's block.
- **`crates/host/src/lib.rs` at H6:** SHA-256 `7f949da827df1364aebd1e20cc4b89674d5d3334d02f51afa26267fb223f9298`. At H5 it was `dadee895cc3029ad51f330cc71fe1c8313988f009711e11a50af1f05686bbda0`; the two differ only by C2a's line. It holds the release guard `#[cfg(all(feature = "profile-allocations", not(debug_assertions)))] compile_error!(…)` and the two module declarations in §2.
- **H7, the FINAL head,** is the pending design-lock-only commit on H6 that binds this note (§5). It changes no product source, so the bytes above hold at H7. Its sha is not yet known, so it is not pinned here; the binding manifest pins it.

## 4. Enforcement (the pins this law selects)

- **The doctor guard, GA-2**, `apps/cli/tests/doctor_tests.rs` at H6, SHA-256 `f50f76b81b637ed76d348518aca3046451e0917af22d7a9fa8f102e733ca92bc` (the GA-r1 accepted after-copy):
  - `allowed_feature_declarations()` gives opensip-host's exact set, by exact equality;
  - `guarded_feature()` includes `profile-allocations`, with no dev-dependency exception;
  - the planted controls of `doctor_feature_declarations_keep_the_accepted_opt_in_graph` refuse: profile-allocations in a default; forwarding from it; a feature forwarding into it; and a dependency entry enabling it, of each kind.
- **The creator guard, GA-1** (X11, intent-only; no law text changes): `apps/cli/tests/creator_commands_tests.rs` at H6, SHA-256 `9e73b5d790fd2cf7b85be99d943255fbc792ac0da905f710fea47eca1b919c4f`. Host `lib.rs`'s `compile_error!`, `#[doc(hidden)]` and feature `cfg` lines are admitted only verbatim, bound to their two module declarations, at most once.

## 5. Provenance and binding destination

This note and its provenance are bound BY VALUE in the joint C2b architecture binding (w2A's restage `stage-joint-r3`, with
the owning record the binding's contract 193 law-by-value set). They are placed beside the parent law, at:

| Member | Architecture destination (relative) | SHA-256 of the source |
| --- | --- | --- |
| this successor note (r2) | `docs/implementation/m2/read-cli-x10/successor-ga/X10-SUCCESSOR-GA-r2.md` | pinned by the binding manifest (not self-hashed here) |
| receipt v1 (historical; no binding clause) | `docs/implementation/m2/read-cli-x10/successor-ga/ADOPTION-GUARD-AMENDMENT.md` | `e33e273a3adc7cbeeccba702f421393a20e2523a3b308a79e2208414dbf730a2` |
| receipt v2 (v1's binding-clause successor) | `docs/implementation/m2/read-cli-x10/successor-ga/ADOPTION-GUARD-AMENDMENT-v2.md` | `375e410806556584901e66039a22a9488583f28f6e9570c4877c3248a7c01cb7` |
| the GA R3 review (`GUARD-AMENDMENT: ACCEPT`) | `docs/implementation/m2/read-cli-x10/successor-ga/REVIEW-guard-amendment.md` | `243c5cce7bfc5dd564ecde2d1b28bc624ececf820bf5eca5ea0e7bf9dd3d2c89` |

- The source files are under `c2b1/guard-amendment/` (receipts) and `c2b1/guard-amendment/review/` (the review).
- This note's own review verdict, when it is accepted, joins the same directory in the same binding.
- The binding is PENDING. It is complete only when the staged binding manifest pins this note and the H7 design-lock commit exists.

## 6. Not claimed

- No new public behaviour.
- No change to the doctor's binary tests, its ingress pin or its source checks.
- No change to any other crate's features.
- No claim about the "X10 r5" that a doctor test comment cites for platform's `measurement` (carried in `CARRIED-HARDENING-v15.md`); this successor does not rely on it.
