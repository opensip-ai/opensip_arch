# X10 r4 — doctor test-bridge pin narrowed to reach

ACCEPT. The narrowing is lawful. It keeps what r3 protected: no home, profile or release selector, and no test seam that reaches the binary, the doctor ingress, or a default or release build. X9 r1 and X8 r3 fit inside the new pin. Nothing else in X10 conflicts with them.

## Subject

`docs/implementation/m2/read-cli-x10/PROPOSAL.md`, r4, 17619 bytes, sha256 `33095e6c13c0e16a5e4fdc87832dbd2f048b01f126b432d49347cc2f116b386a`. r3 is `PROPOSAL-r3.md`, 16059 bytes, sha256 `0f263d12d38d2d43f8dfe5f999efbbd9f79f2f3fbd3145ef7c3804c39804fca2`. Both pins match `hashes.txt`. Codex r3's `review.json` is ACCEPT on that r3 hash. No product cargo. `~/Library/Application Support/OpenSIP` is absent.

The unified diff is two hunks. The title says r4. The header adds that Codex accepted r3 on 2026-09-30, that r4 narrows item 5's test-bridge pin so X9's and X8's guarded features can exist in host, security and storage, and that r3 bytes are preserved in `PROPOSAL-r3.md`. Item 5 gains the lead-decision paragraph and replaces the pin bullet `No new cross-crate test bridge exists.` The source-check bullet, the single-producer bullet, the binary-test paragraph, the environment-variable rejection, and the rest of the file are unchanged. The amendment adds no public code and no diagnostic route.

## The narrowing

r3 rejected a cross-crate test-support bridge, such as a `pub` test-only module or feature in `opensip-security`, because it would put a scratch-home and profile selector on the security crate's compiled surface, and it pinned that no new cross-crate test bridge exists. That absolute pin conflicts with laws accepted later.

X9 r1 item 1 requires one never-default `crash-matrix` feature on `opensip-platform`, `opensip-security`, `opensip-storage` and `opensip-host`. Item 2's guards are a `compile_error` when the feature is set and `debug_assertions` is not, so a release-profile build with the feature fails, and no `[dependencies]`, `[dev-dependencies]` or `[build-dependencies]` entry names it. Item 6 requires one `#[doc(hidden)] pub mod crash_matrix_support` in security, storage and host, compiled under the feature only.

X8 r3 item 4a requires `scenario-fixtures` declared on security and forwarded by storage, with storage's and host's `[dev-dependencies]` the only enablement, and one `#[doc(hidden)] pub mod scenario` in security and one in storage. Item 4f is the release guard: a source pin allows the name only in security's and storage's `[features]` and in `[dev-dependencies]`, never as a default and never in `[dependencies]`, and plain `cargo check -p opensip-host` (the surface `opensip-cli` builds) has no `scenario`.

r4's paragraph matches those guards. "No manifest dependency names it" is X9 item 2's dependency-table rule, and the release build fails at `compile_error`. "Enabled only from `[dev-dependencies]`" is X8 item 4a's enablement rule, and item 4f pins the name out of default features and out of `[dependencies]`, so a release build of the binary does not compile it. The two rejected alternatives are real: another crate's `cfg(test)` is invisible, so a separate test crate would duplicate the fixtures or make them `pub`, and dropping the pin would leave doctor's seam unstated.

The new pin bullet is a reach rule plus a name ceiling. No bridge reaches the binary, the doctor ingress, or any default or release build. `apps/cli` and `opensip-reporting` have no `[features]` table. In host, security and storage the only `[features]` names allowed are `crash-matrix` and `scenario-fixtures`, each under its own law's release guards. That last clause keeps X8's placement: host's `[features]` takes X9's `crash-matrix`, and `scenario-fixtures` stays in security's and storage's `[features]` and in storage's and host's `[dev-dependencies]`. Platform's `crash-matrix` sits outside the three-crate ceiling; the reach sentence and X9 item 2 cover it.

## What r3 still protects

The unchanged source check still forbids `std::env::var`, `var_os`, `home_dir`, and any `cfg(feature` or `cfg(test)` item that selects a home, profile or release, over `apps/cli`, the host doctor ingress, and the bootstrap path's non-test text. The ingress still has exactly one producer call, `observe_installation_for_doctor()`, with the native account and the authenticated release and profile producers. A test-only environment variable read by the binary stays rejected under owner §1a. Doctor's own tests stay the three layers r3 accepted: security's private scratch-home fixtures, host tests that start from observation and termination values, and the real development binary. Item 8 still describes that ingress as having no producer-injection seam and no doctor test bridge. The forbidden substitute that bars a feature or `cfg` override of installation, profile or release in the binary is unchanged.

X9's and X8's `pub` modules are the kind of bridge r3 named, and r4 confines that rejection to doctor's own arrangement. Both modules are feature-gated. Neither feature is default. Neither is enabled by a dependency of the binary. `crash_matrix_support` is absent unless `crash-matrix` is requested explicitly, and a release build with that feature fails at `compile_error`. `scenario` is absent from the plain host surface the CLI builds. Shared fixture sites, including `HomeSource::Fixture`, are `cfg(test)` unless one of those features is on, so the binary's build does not compile them. They sit in security, outside the doctor source check's files. The features are test surfaces for the crash matrix and the refusal suite. They are not a selector on the doctor ingress.

## Verdict

ACCEPT. No required finding.
