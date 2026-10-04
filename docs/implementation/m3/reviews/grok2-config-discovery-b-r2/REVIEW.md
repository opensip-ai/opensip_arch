# M3-B r2 — ACCEPT

Subject: `docs/implementation/m3/config-discovery-b/PROPOSAL.md`, 94762 bytes, sha256 `92e6582534d3f59443bade8e1dd7c32f9a3fed9249b979ae2ed56cfcc15becaa`. The preserved r1 bytes match `PROPOSAL-r1.md` (`da014f54d1beff4a7187fc716205319ba5facf41a9caddec5c29e0464b618e2f`, 85905 bytes). Read-only. No cargo. `~/Library/Application Support/OpenSIP` was absent. The twenty pins in `hashes.txt` match.

The diff against r1 is the title, the r2 response table, and the ten passages that table names: item 10, item 12's census sentence, item 13's unit-source row, item 20, item 22's two new bullets, item 23's `--workspace-root` cell, one item 24 row, the S2 and S3 cells, the reviewer note, and one forbidden-substitute bullet. Units, sizes, order, and F1–F14 are unchanged. r2 adds no public code. The new item 24 row is a disclosure in `workspaceDeclarations[].unresolved`, with subject `—`.

## RF-1 is resolved

Item 20 chooses on one fact: whether the resolved semantic configuration holds an admitted `discovery.workspaceRoots` array (AQ:115-117). An admitted array is nonempty; `[]` is refused.

Branch A, the array present, covers the project layer, the local layer, and `--workspace-root`, which replaces a lower array whole (item 2). The array alone decides membership. Discovery is restricted to exactly those roots, with `provenance=EXPLICIT`, and is never widened into a scan (NE:917-921), inside a member as anywhere else. A member contributes only the units its named roots are. The readers declare no member. They record a link only when its directory lies inside a member the array already admitted, and every other reader entry is dropped. That link rule does not add a root and does not fall through to automatic discovery, which is what NE:917-921 and SLM:771-785 require. SLM:774-785 is an exclusive `if` / `elif` / `else`: a config array never reaches the automatic branch.

Branch B runs the readers only when the array is absent, which is AQ:115's automatic case.

The same rule is in item 13's unit-source row, item 22's Config2-join bullet, item 23, the new item 24 row, the forbidden substitutes, and S3's content cell. Item 22 keeps the exact-roots sentence and adds only that an exact root may lie inside a member. The controls cover a project-layer array, a local-layer array, and `--workspace-root`.

## RF-2 is resolved

Item 10 no longer cites I1:381-388 as standing in full. I1:383-386, the three row-count changes, stands. I1:388's clause that the X12 order stands is withdrawn. I1:388's other clauses stand: rows 1 to 4, the `Supplied` refusal, the `cfg(test)` registry, `check_plan_pack`, and X12d. I1:388 is that sentence.

S2's replacement is the order paragraph only. It keeps admission pure: no I/O, no lock, no ledger charge (X12:125). It runs immediately after resolution, which runs immediately after selection and the carrier captures, and before registry capture, registration, any lease, any effect, and the rest of X12:127-130. The withdrawal paragraph names X12:126, the ordering sense of X12:136, and the words "the order" in I1:388.

X12:136 is one correction: "X12 does not depend on X1: it is pure and runs before any custody." The order half is the same claim as X12:126, so withdrawing it is the completion of RF-2, not a new amendment. The dependency half stays: admission still does not depend on X1, because it performs no custody of its own and its only dependency is the current product. X12:132-134 and X12:138 stay, including `AdmittedPack` as the Plan builder's only policy source (X12:134) and "nothing to clean up" (X12:132).

## NBOs

NBO-1 is stated correctly. The census bounds objects and edges. Bytes are bounded by the 64-member cap, X2:272's 4 MiB index and 64 KiB config ceilings, and the 4 MiB file-custody limit. SL:126-127 states that limit for a config file; SL:182 requires every marker to pass file custody, and the reference applies the same 4 MiB ceiling there (`MAX_CONFIG_BYTES`, SLM:120 and SLM:564).

NBO-2 is the sentence that was missing. U-9 still keys off no explicit roots and no surviving `rust` or `tsjs` unit (NE:879-883). Units inside members count, because members are not boundaries. The one fallback unit is at W's root `""`. A member is not a second fallback site. S3's cell cites item 22.

## Nothing new is wrong

Branch A's link rule, S2's X12:136 reading, and the two NBO sentences match the texts they cite. No other decision changed.
