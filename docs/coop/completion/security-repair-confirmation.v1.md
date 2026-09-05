# Security repair confirmation — failed

Authoritative JSON: `security-repair-confirmation.v1.json`, SHA-256 `4c7f3c29e5bd58b4b4530a838cb71293a60071fa432d3f262a9fd3cc17014497`.

Frozen dispatch: `security-repair-confirmation-dispatch.v1.md`, SHA-256 `16780a1e0d79b3d51ae250fd0ad52eb72e203a63c0ec28ce690d58b91430acd3`.

**OBJECT — 4 MUST-FIX, 0 SHOULD-FIX within the six-finding scope. The unit remains CONTESTED.** This is the single bounded D-368 confirmation by the same independent adjudicator. All v3/v4 pins and the exact diff map check: 12 changed, 5 added, 53 identical copies, 0 removals. Subject files remain untouched.

| Prior finding | Disposition | Evidence |
|---|---|---|
| SEC3-M1 | UNRESOLVED | Original negatives refuse, but publicly constructed or mutated `AdmittedRoot` values bypass closed shape validation and still return VERIFIED. |
| SEC3-M2 | RESOLVED | Both traversal negatives and global-only traversal refuse; descendant/sibling controls behave correctly. |
| SEC3-M3 | UNRESOLVED | Original malformed cases quarantine; COMMITTED0 missing `bodySha256` passes shape admission then raises KeyError instead of quarantining. |
| SEC3-M4 | UNRESOLVED | Missing context, foreign/empty scopes and newline refs refuse; empty identity bindings admit, and malformed request correlation or scratch mode 0000 still returns bytes. |
| SEC3-M5 | UNRESOLVED | Forward ordering improves, but new RCO REVERTED is rejected by the frozen journal schema; receipt text remains RCO-only and all twelve recovery cases omit REV. |
| SEC3-M6 | RESOLVED | Measured class series/flavor replaces fixed 6.8 generic identity; Azure/wrong-series controls pass; the four-class runner file is unchanged. |

The inseparable new defect **SEC4-REG-M5-OUTCOME** is recorded separately in the JSON and counted under unresolved M5: recovery emits an outcome its own closed journal cannot store.

The retained checker passes **283/283** with all check results identical to the frozen report. The specified Python environment differs from the author environment; the JSON records both. Independent probe source and exact results are embedded in the ruling, including a schema-valid FAILED outcome control against the rejected REVERTED record.

Supplemental policy duplicate handling and scratch-cap changes are not confirmed here. No product/platform qualification or row grade is conferred. **No row is SATISFIED and no unit is adopted.** Register edit: none. The failed confirmation returns/remains CONTESTED without an automatic new exchange or confirmation.
