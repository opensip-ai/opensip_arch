# S-OP-2c r1 passages

Two passage overrides on one parent. The parent file is not edited.

- **Parent:** `docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md`, 130,001 bytes, sha256 `ce8d3a4b783328915f0bf550dd111f227aa9901d5efddbcd9ccc8707cd4cb11d`.
- **Line 881, the `provider.process.reaped` row.** This override replaces one field's table. Within the row, `` `signal` K1 (Signal), optional `` becomes `` `signal` K1 (ChildSignal, item 23a), optional ``. The rest of the row is unchanged.
- **Line 894, item 23's closing sentence.** This override is insertion-only. Its `after` is the same sentence, a blank line, and then item 23a: the text between the two markers in `PROPOSAL.md`, byte for byte.

`passageSupersessions` is empty. No other line of S-OP-2 r6 is overridden. Item 22's row for closed terminal responses (line 845) is not changed: item 23a names the successors that row already refers to.
