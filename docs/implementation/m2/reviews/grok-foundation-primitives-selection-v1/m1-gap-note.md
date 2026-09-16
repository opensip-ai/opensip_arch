# M1 remaining duties (not closed by foundation-primitives-selection v1)

This note is **not** an M1 verdict, waiver, or successor. Foundation-primitives-selection v1 is M2 preparation of two existing-owner primitives. Live lock remains **8 inventory / 8 contract**. Do not treat these seven new bytes, host-build-isolation-01, or provider-isolation02 as M1 complete.

## Still required for M1 (do not silently waive)

- **RF05 — checked-in provider workspace/lock.** Isolation02 accepted only a 3-file *probe* over prior contracts/identity sources. Live `providers/rust` is still absent. A real product `Cargo.toml` / `Cargo.lock` / toolchain / `src/main.rs` under inventory owners, independent of the host workspace, remains open. HostAssetPin / single compiled `buildChannel` agreement is retained; do not invent an unused fake pin.
- **Host-build-isolation-01** (`docs/implementation/m1/trials/host-build-isolation-01/subject.json` SHA `071cf047f74271d4e4538a45524763447677ab0ae4abe85b7dea7b63383f99fd`, 53 members) is a clean host build over **prior** source bytes (root: 34 source files / 16 verified archives; 22 tests plus metadata help/version). It does **not** prove the new identity/platform candidate bytes.
- **Fresh blind consumer** still pending. Persistent Grok/Codex sessions are not that consumer.
- **Native provider implementation** (compiler adapter, protocol, sealed VFS, session) is not started by either isolation02 or this identity/platform primitive.

## Do not inflate M1 into later milestones

- **M3:** independently pinned Rust compiler/provider integration and its toolchain/SDK qualification. The isolation probe lock and any later 1.95 development toolchain are not that qualification.
- **M4 / M6:** full report/release asset inventory, offline bundle, private compiled HostAssetPinV1 joined to the selected projection digest, and release publication. Development host tests may use labelled fixture assets; there is still no asset-consuming runtime that closes those duties.

## Related accepted units that do not close the gaps above

- Contracts dependency/source checker: live-installed; 11-dep / 8-source profile. Does not census identity extras or prove native purity.
- Provider-isolation02: shared-library *build probe* only.
- Platform entropy `build.rs` guard: host getrandom backend only.
- This foundation unit: exact H-frame decode and trusted-root regular-file walk. Callers still owe domain registration, blob digest, descriptor schema, root selection, and semantic joins.
