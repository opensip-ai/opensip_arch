# Adoption receipt: C2B1A-MOVE, the verbatim move of law formulas and data types into lower crates (2026-10-30)

**Decision LD-COORD-MOVE (coordinator, session 9ce22ffd): ADOPTED, owner-delegated under OD-AUTO-1, after R3 review.**
It is a law-file refactor that changes no values.

The MOVE-MAP erratum v2 (`move-map-v2/ERRATUM-MOVE-MAP-v2.md`) is adopted. Authority: LD-Q-125 (B1), LD-Q-126,
LD-Q-130/-B and LD-Q-135. What moves:
- the pure law formulas and `DescriptorShape` from host's `snapshot`, `snapshot_admission` and `node_modules_layout`
  into the law crate;
- MB14a's config types into the metered crate;
- C2b-1b's jsonc types;
- the security items `owned_record`, `RECORD` and `owned` into the ungated `opensip_security::cost`.

All are byte-identical except for the declared deltas, and every old path keeps its items through a re-export. The
declared deltas:
- the 11 field widenings from `pub(crate)` to `pub` on TableRow, DescriptorShape and AdmissionPrice, limited to fields
  host reads (`field-deltas-law.json`);
- `RECORD` from private to `pub(crate)`;
- `use` lines.

The citation remap (`citations-v2-all.txt`) re-points every law and FUNDING citation of the moved lines. No price, cap,
BOUND-1 term or published figure changes.

| Artifact | sha256 |
|---|---|
| **The subject, `move-map-v2/ERRATUM-MOVE-MAP-v2.md`** (the delivery manifest is `S4-v2-DELIVERY-SHA256SUMS.txt`, `0ffd3e67…`) | `0274f704e459123467be7a3303cb64af75d0c06f0bac2cd4d8eb1524c8243c97` |
| **The request, `review/REQUEST-r9.6-design.md`** | `8f33f6c11c4823ca87ad9cf2fd47eec576f48f97f1090eff75990cc9a92b4569` |
| **R3 review, `review/REVIEW-r9.6-design.md`** (verdict line `C2B1A-MOVE: ACCEPT`) | `66e22fd525916d42d9190a5d76513b2cff4752388d485e42b00c8a32925350e5` |

- **The reviewer:** codex-c2b1-ownfund-r3, gpt-6-astra/high, R3-FRONTIER. It is a different vendor from the Claude
  authors (w2A, w28).
- **Not accepted by this receipt:** the code itself (that waits on the code review and the lane), and the design line,
  which is still REQUIRED-FINDINGS at r9.6.
- **Re-pinned premises:** security `snapshot_source.rs` and `custody/discovery_walk.rs` (F1 reconciles them on resume).
- **Binding:** with C2b-1a's integration. It needs description successors for the edited law files and package rows
  for the new crates (LD-COORD-PKG-METERED, -2).
- **Owner notification:** flagged as an owner-delegated law-file refactor with no value change.
