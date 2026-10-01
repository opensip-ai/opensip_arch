Codex re-review: law X10 r2 after your r1 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/codex-read-cli-x10-r2. Law review; no product cargo.

Subject: docs/implementation/m2/read-cli-x10/PROPOSAL.md r2 (pin in hashes.txt). `diff` it against PROPOSAL-r1.md.

## Changes

- **RF-1.** Item 3: both `DoctorOutcome::Report` branches pass the assembled `Invocation5DoctorResult` through unchanged. The unproducible branch includes its nested `kind: "doctor"`. Item 7 adds a negative test: omitting or altering `doctor.kind` must fail validation.
- **RF-2.**
  - Item 4 human rendering prints the termination's error code, fault cause, and carried `domainDetail` (detail, subject, remedy). So `DOCTOR.REPORT_NOT_PRODUCIBLE` and `DOCTOR.DEFECTS_FOUND` appear even when `defects` is empty.
  - `outcome` parity is restored through the envelope `termination` carrier, per `doctor_projection.py`. Tests compare the complete termination facts for the healthy, defects-found, report-not-producible and refused outcomes.
  - `offline-window` alone stays unclaimed.
- **RF-3.** Item 5 replaces r1's in-process `run_with` with layered tests (a lead decision), each built with its crate's ordinary dependency configuration:
  - security real-producer scratch-home tests over `observe_with`;
  - host projection and rendering tests from each `DoctorInstallation` or `InstallationTermination` value;
  - real dev-binary tests.

  A cross-crate test bridge is rejected, with the absence-versus-unreachability reasoning. The pin is widened to the bootstrap path, any `cfg(test)` selector, a single producer call, and no new bridge.

## Decide

Are RF-1 to RF-3 closed? Is the layered arrangement buildable and honest about what each layer covers? Is anything new wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
