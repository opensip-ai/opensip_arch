**ACCEPT-DESIGN-UNIT — registry owner selection v3, round 2.** RF-JRW-S2-1 is **RESOLVED**. Required findings: none. Non-blocking observations: none.

The accepted subject is `docs/implementation/m2/project-registry-owner-selection-v3-subject.json`, 455 bytes, SHA-256 `f931f3155b9508450e900f14afcfc706ec7f0be253a7bbf880e1290fdbf0b8f9`. Its exact two members are:

| Member | Bytes | SHA-256 |
|---|---:|---|
| `project-registry-owner-selection-v3/README.md` | 11045 | `4de5f14f4d236151317488c9bf4766244332ef10489143c7c320ca99465e101d` |
| `project-registry-owner-selection-v3/successor.json` | 14684 | `974ef73f539fb20386b57b2063c49c40573da27e72c443443b666da6ab3d6691` |

1. **The prior finding is resolved exactly.** `successor.json:54-82` replaces r1's raw REG:9 override with one contract passage supersession. It names the selected IRB record (`initial-root-binding-owner-selection-v1/successor.json`, 43921 bytes, `3a713c5c39a3feca2db3a05924103d49c10f11bef3c32f93d8c286fecd813e54`), v2's exact owner parent and the integer selector `{"line":9}`. Independent byte comparisons prove that `before` equals IRB's full selected `after` at `:343`, and that the new `after` equals that full text, one space and exactly r1's J-RW appendix. Every accepted initial-root sentence survives. The entry has SD-7's five-field form; its target record belongs in `supersedes`, with no additional parent required.

2. **The rest of r1 is preserved.** REG:60, :74 and :76 remain raw-parent overrides (`successor.json:16-53`). Their complete serialized objects are byte-identical to r1; each `before` matches its pinned v2 line. Parents and `inheritedSelectedRegistryRecord` are unchanged. The candidate list keeps the single README form and updates only its digest and length. The manifest contains exactly the sorted README and successor pins. Neither candidate path is already selected. The record diff has no other change beyond standing, that candidate pin and the REG:9 conversion.

3. **The README is accurate.** Its new r2 section and IRB source entry, change table, V3-1/V3-2 and Binding requirement describe three raw overrides and one reviewed supersession of the current meaning. The introduction and preservation paragraph are conformed accordingly. There is also a factual context update at `:27`: X2 r10 was accepted beside r1. I checked that verdict in the exact prior batch review and that the archived `PROPOSAL-r10.md` equals its accepted subject bytes. The appended-text section, V3-3/V3-4 and J4b product-binding paragraph are unchanged. No unexplained substantive diff remains.

4. **The record can extend the selected chain.** I read `tools/verify_design.py` at product `d2c00a96c3136fe45b901bc067b6d0ca51f0c9c1` (43946 bytes, SHA-256 `7b313de629f2c958a1e62538b909d6f01545be2519238ba9b3d86ab7e7ba3326`) and checked all 97 selected contract record pins. IRB is the 55th record, index 54, at `design-lock.json:4051-4071`; its manifest, accepting independent review, root assent and joins match. It supplies the only selected passage on v2's owner document: REG:9. There is no later override or supersession on that document. Both v3 parent pins are selected through v2's accepted binding.

   The supersession therefore satisfies the verifier's earlier-record, published-target, same-physical-passage, exact-before and current-tail checks (`:348-369`). The three remaining raw keys are unused, so the conflict checks at `:409-413` have no collision. This review's exact `supersededPassages` list satisfies `:420-426`. A future four-pin binding still needs valid root assent. No verifier change, removal of IRB or withdrawal of its meaning is needed.

   I read and hash-checked the lead's pinned Python script and result; I did **not** rerun the verifier. Its unchanged-tool/pinned-bytes overlay leaves ordinary pins with the real verifier and uses exact scratch acceptance bytes. The lead reports r2 passing with and without the implementation checkout, 98 successors and 2 contract supersessions, with the other source and inventory selections unchanged. Its missing-list, empty-list and exact-r1 refusals match the source checks above. These are lead-run results, corroborating the independent static assessment. The request's separate literal-CLI scratch-file refusal is not recorded in `local-binding-check.json` and is not claimed as independently observed here.

5. **It still records exactly RW-S2.** J-RW r4 `:680`, item 2 `:189-193`, C-SUFFIX `:242-250` and C-REG `:346-371` authorize the unchanged appendices: ordinary random-kind reservation completion on the same admitted root; a later separately admitted durable-write step; missing-suffix completion without rewriting existing bytes; and a complete namespace whenever any marker is present, with the join decided before effects. Adoption and other operation owners stay separate. The observation table, read refusals, labelled reference model, carrier/schema and public vocabulary remain unchanged. Preserving IRB's existing text adds no new creator authority.

6. **No further problem found.** All 21 request pins match. The exact r1 snapshots are diff bases only, and evidence files are outside the two-member subject. `static-audit.json`, `README.md.diff`, `successor.json.diff`, `pinned/` and `product-d2c00a9/` retain the comparisons and inspected bytes.

The machine-readable review carries this exact superseded passage, by value and in record order:

```json
[
  {
    "record": {
      "path": "docs/implementation/m2/initial-root-binding-owner-selection-v1/successor.json",
      "bytes": 43921,
      "sha256": "3a713c5c39a3feca2db3a05924103d49c10f11bef3c32f93d8c286fecd813e54"
    },
    "parent": {
      "path": "docs/implementation/m2/project-registry-owner-selection-v2/owner.md",
      "bytes": 32488,
      "sha256": "2d4b65c9b0bc088b2667c35e75bf82d1702d13703be6effb1df975e7c67c179f"
    },
    "selector": {
      "line": 9
    }
  }
]
```

Acceptance covers this frozen RW-S2 contract design unit. Root assent, product binding and J4b implementation/controls remain separate. No runtime qualification is claimed. I ran only my own static data audit at low priority; no product code, cargo, tests, build, matrix, lead set or verifier was executed. All writes are under this review directory; no repository/Git write, delegation, real OpenSIP-home access, private 413 UUID-fixture read, commit or push occurred.
