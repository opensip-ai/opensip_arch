# S-OP-2c r1: the four record tables

**Draft r1, PROPOSED, not accepted.** 2026-10-17. Claude leads; Codex has not reviewed this unit. It edits no product file, and it does not bind `design-lock.json`.

## Parent

There is one parent: `docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md`, 130,001 bytes, sha256 `ce8d3a4b783328915f0bf550dd111f227aa9901d5efddbcd9ccc8707cd4cb11d`.
- S-OP-2-R selected it as an accepted base.
- S-OP-2b, bound, overrides its line 429. This unit overrides lines 881 and 894, so the two do not overlap.
- Once accepted, this record can bind directly as the next contract successor.

## What it does

It resolves the four tables that block D3a-3's four events (`supervisor-d/d3a-3-r2/BLOCKED-TABLES.md`):

| Table | Class | Source | Members |
|---|---|---|---|
| `StageKind` | protocol-enum | both protocols' stage `operator` | 1 |
| `ProviderState` | protocol-enum | P3T `phases` (T2O ⊂ P3T) | 22 |
| `Signal` | generated-contract | COMMON4 `D9Signal`, for `host.signal.received` | 3 |
| `ChildSignal` (new) | registry-literal | lead decision LD-OPT-4, for `provider.process.reaped` | 20 |
| `ProviderReason` | protocol-enum | the TS2 and Rust3 `Unavailable` payload reasons | 11 |

`PROPOSAL.md` gives the law text (item 23a) and the five lead decisions with their rejected alternatives. `PASSAGES.md` gives the two overrides.

## What a review can re-run

`evidence/check_sop2c.py` is read-only.
- **The parent.** It checks the parent pin and both overrides. The inserted text must equal the `PROPOSAL.md` passage byte for byte.
- **The members.** It re-derives every table's members from the pinned sources:
  - the architecture's P3T, T2O and provider-startup schemas;
  - with `git show` at product `5de9fd4`, the carriers, COMMON4, the identity stage-spec, the generated `protocol.rs` and `evidence.rs`, and the vendored tables;
  - the `libc` 0.2.189 crate archive, checksum-verified against `Cargo.lock`, for the per-platform signal constants.
- **The pins.** It checks the subject pins.

It takes no lock, runs no Cargo, and writes nothing.

```
python3.14 -I -B docs/implementation/m3/operability/s-op-2c/evidence/check_sop2c.py
```

## Not in this unit

There is no product code, no registration and no inventory successor here. D3 registers the four events, and adds `signal` to `tool.process.reaped` if it chooses, in its next code unit after this record is accepted and bound. M3-D's adoption of `supervision.child.settled` belongs to M3-D's next revision (see `PROPOSAL.md`).
