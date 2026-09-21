# Formal selection — native ProjectId registry owner v1

**Verdict: `ACCEPT-DESIGN-UNIT`**

Formal **registry contract selection only**. Does **not** implement writers, select inventory, change runtime, accept S9.3, or close `StoreGenerationBindingV1`. Does **not** relabel 371r4 OWNER/REFERENCE `ACCEPT-UNIT` (`f1a583f3…4cda`) as this formal acceptance.

**subjectManifestSha256** `f0bbdce06f5d5b3332ef4552b6d042a826a7b4f56b40a8c667c4f4d6f2ec8435`  
`docs/implementation/m2/project-registry-owner-selection-v1-subject.json` **6527** B, **29** members, paths sorted unique, **0** pin mismatches. Successor `candidates` cover the other 28 members.

Archived actual 371r4 review tar in this subject: **229500 B / 256 members / `85275994…51ed5`**. Trial r4 archive also included: **224780 B / 196 members / `b658a9ee…dc1b`**. Both rehashed.

---

## Parents and six overrides

Three parents are **live lock inputs** at the successor pins: identity `c82404f3…`, S7/S9 `a319da39…`, lifecycle schemas `f66d2c61…`. Six `passageOverrides`; each `before` string **exactly matches** the cited parent line; no other selected contract successor currently overrides those selectors.

| # | Parent line | Effect |
|---|---|---|
| 1 | identity 45 | live RESERVED/ACTIVE one-to-one; terminal N unused |
| 2 | identity 48 | missing **whole** established registry is unavailable |
| 3 | identity 51 | this owner supplies 92-byte frame / registry / adoption / lifetime |
| 4 | identity 58 | move: EXCLUSIVE, no live reader or writer |
| 5 | S7 619 | RegistryDocument vs RegisteredNamespaceList vs StartGate |
| 6 | S9 917 | start-gate before new journal; native 4096 does not change maxItems 65536 |

Public 11/20 records, generic NamespaceList schema, five-field digest recipe, inventory v55, and product runtime files are **unchanged**.

---

## Exact r4 owner copy and provenance

`owner.md` / schema / `registry_model.py` are **byte-identical** to frozen 371r4 (`14181ef7…`, `545e0006…`, `b9c1a19a…`). `owner.md` still begins `DRAFT. Not selected…`; README states that **this unit’s** review+assent+lock successor supplies standing, not a silent rewrite of that header.

`provenance/resolved-inputs.v2.json` is the exact `0114205a…` file. `adopted-source-ledger.json` binds **only** named `/projectIdContract` marker/allocation selectors. It **rejects** snapshot1, plan1, opaque registry/lease, and historical deletion/publication protocol. Owner.md remains the carrier/kind/tombstone law.

Native codec placement in identity is **planning only** in this unit: no new inventory path and no DAG edge.

---

## Evidence replay

Independent fresh-dir replay of unit `reference/`: **274** cases (unique `caseId`s), **24** schema checks, capacity **320555**, **8** faults after baseline; `reference-results.r4b.json` **byte-equal** unit evidence. Initial r4 history-reuse mutant remains disclosed, not a kill. No native tests.

Limitations in README stand: no writer, no OS qualification, no S9.3, no five-field acquisition, no M2–M6 close. Root must still record **substantive assent** and compose the lock successor; this file is not that pin.

---

## requiredFindings

None.
