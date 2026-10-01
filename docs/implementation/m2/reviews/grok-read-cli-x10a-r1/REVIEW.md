# Review: read CLI X10a and X10b

X10a verdict: ACCEPT-UNIT. X10b verdict: ACCEPT-DESIGN-UNIT.

Worktree `/Users/sb/code/opensip-ai/opensip-x10a` is HEAD `f7acb6d7f8acadcbc0bf81d141f39077d817f043`. `product.diff` is `git diff` of the intent-to-add tree: 54287 bytes, sha256 `b9e5717cbd28b04f48e4ab734318828a012b5de3e5c0008af890a7eb999c729f`. Twelve files. The real OpenSIP support directory is absent before and after the tests. Hashes.txt matches every pinned product and architecture file.

## X10a

Law X10 r3 items 1 to 7 are implemented.

`opensip doctor` takes no command flags. `--format agent` stays `OUTPUT.FORMAT_NOT_APPLICABLE`. Other commands keep their refusals. The ingress calls `observe_installation_for_doctor()` once and passes `other` empty. Doctor stays `InstallationEntry::Outside`. Off macOS the command is the existing unknown-command rejection. A development build ends at `CORE.NO_EMBEDDED_RELEASE`, exit 2, with a schema-valid `kind: failure` envelope, and the binary test leaves the real installation untouched.

The envelope matches item 3. A produced report and a report that cannot be produced are `kind: doctor`, and both pass the assembled result through, including the nested `kind: doctor` on the unproducible branch (`reportProduced: false`, `defectsFound: 0`, `defects: []`). An unreachable installation is `kind: failure` with no `doctor` member. The host I/O row puts `HOST.IO_FAILURE` in `errors` and puts no `domainDetail` on `termination`. Exit codes come from the class (0, 2, 4). `retentionDisclosure` is not emitted.

Remedies. `DOCTOR.DEFECTS_FOUND` is now the selected golden's text, `CI must inspect doctor.defectsFound; exit 0 means the report was produced`, replacing 458c-c's `inspect doctor.defects` constant. The backup row uses 468a's golden remedy, `pass --allow-backup-custody or choose --ephemeral`. `DOCTOR.REPORT_NOT_PRODUCIBLE` keeps 458c-c's `Resolve the report-production failure and run doctor again.`; X10b moves the golden to that text. Every other 468c detail has one fixed remedy in `doctor_ingress.rs`. `row_remedy` matches those details and returns `MetadataError::Projection` for any other code. The public detail registry records the codes and does not fix a different remedy string.

Human rendering uses one shared termination block, so a carried fault cause is shown and an absent one is not invented. A failure may omit `diagnostics` only when `errors` is non-empty. The metadata startup tests still pass, including the human failure display. The durability note is labelled `Informational: durability not checked`. Parity is built from the JSON envelope. The negative test rejects an unproducible envelope whose `doctor.kind` is omitted or altered.

The source pin covers `apps/cli/src/*`, `doctor_ingress.rs`, `outcomes.rs` and `request.rs`, strips comment lines, requires one `observe_installation_for_doctor()` call, and refuses a `[features]` table on cli, host, security and reporting. Its cut is the first `#[cfg(test)]\nmod tests`. In this tree that module is at the end of `doctor_ingress.rs` and `request.rs`, and the other pinned files have no test module, so the cut drops no production. The pin test passes. No new code reads an environment variable, `home_dir`, or a `cfg` to choose a home, profile or release. `observe_installation_for_doctor` takes `HomeSource::Native` and the read receipt's own producers. A release build has no other selector.

Tests replayed here, `--locked --offline`, target dir under this review directory: security `installation_doctor` 11 passed; host tests matching `doctor_` 19 passed (the ingress cases plus the existing report assembler); CLI `doctor_tests` 4 passed and `startup_tests` 6 passed. The workspace suite of 1172, clippy, rustfmt and `check_package_edges` were not replayed.

## Inventory v82

v82 is 754 files, 318189 bytes, sha256 `f2423742f09beb94364085570e1a5b30f60c220c30932b4d3426b3e3994c1154`. Parent v81 is 751 files, 315495 bytes, sha256 `68fdcfb4fec76618b5880481d1d3075c3c53a0443fa2f498bdec632bac75accc`. The three added rows are `doctor_tests.rs`, `doctor_ingress.rs` and `doctor_ingress_tests.rs`. No row was removed, and every carried row is equal by value, including packages, dependencies and pending decisions. The projection is the sixteen effective descriptions bound to v81. `verify_projection.py` passed with 83 corruptions refused. `verify_scratch.py` for X10b alone selected v81, and the combined scratch selected v82, both with 16 inheritance rows.

`doctor_report.rs`'s carried description still ends "Library only: nothing emits it yet." That sentence is now false. The unit records it as a later description-only successor, the same shape as 461b. It is not a finding in this review.

## X10b

Six overrides, golden index 26, id `doctor-report-not-producible`, in command-inventory v3 (45 goldens), metadata-v2 v4 (45) and the composed-owners proposal (46). Each parent still has situation `the private store cannot be opened to produce the report` and remedy `check permissions on the private store root`, class `operational-failed`, exit 4, `HOST.IO_FAILURE`, `DOCTOR.REPORT_NOT_PRODUCIBLE`. The overrides change only situation and remedy. The new situation is the bound failure X10 actually produces, and the new remedy is the product's existing `NOT_PRODUCIBLE_REMEDY`. No schema, registry, generated code or product file changes. Subject manifest sha256 `05f1aecd8a34a24cf022841c6bd61e3e79f927e55f2d44431e5541809d7be94c`.
