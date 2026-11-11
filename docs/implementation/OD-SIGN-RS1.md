# OD-SIGN-RS1: ad-hoc launcher signing extends to the Rust stage

Status: accepted owner decision; effective 2026-11-10.
Scope: which launcher identity development launches may use during M3's Rust
stage. It does not change what distribution or release qualification require.

## Owner instruction

The lead proposed: "Extend ad-hoc signing to the Rust stage. Unblocks Rust
launches for development; same terms as TS1 (real signature before distribution
or qualification)." The owner answered:

> Extend ad-hoc signing to the Rust stage - granted

Earlier the same day the owner said they would likely not have an Apple
Developer account until the project nears completion. On 2026-10-30 they had
chosen ad-hoc signing for the TypeScript stage for the same reason (OD-SIGN-1c).

The details below are the lead's. They are not further quotations from the owner.

## What is decided

- Launches of the Rust provider's sidecar and of the Rust `cargo` tool closure
  under the confined launcher, made by the owner's project on the owner's
  machine during M3, may use the ad-hoc signed, hardened-runtime launcher,
  identified by its code hash. These are the keys CF-1 calls G-RS3.
- The terms are those already accepted for TS1: no Team ID, no notarization,
  and the same evidence limits.

## What is not changed

- Any distribution to another person or machine, and any release qualification,
  still require the Developer ID signature and notarization. So does any
  customer or third-party use.
- Linux rows keep their own mechanism.

## What is still owed before the first such launch

The adopted confinement law names notarization for these keys, and the TS1
amendment (CF-1-A1) is scoped to TS1 only. A matching amendment for the Rust
stage, modelled on CF-1-A1 and reviewed by two reviewers because it concerns
signing, is written when the Rust sidecar is ready to launch. This decision is
its basis. Rust-stage code can be written and tested without it.
