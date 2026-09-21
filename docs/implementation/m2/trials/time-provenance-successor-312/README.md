# Original-core context successor312 — unselected reference proposal

The first P0/P1 clock proof lacked an encoded path to its original core anchor. This packet proposes explicit S4EvaluationInputV2, preserves V1, and supplies conditional context joins plus bounded embedded-root byte resolution. Read OWNER.md for the retention/version/TCB boundaries.

Verified complete frozen311 and229r3 parents before copying dependencies. Schema125→127 definitions; typed sites134→136, with exactly two S4 clock-event targets changed. V1 record shape is preserved. No product or frozen source edited.

Validation:68 conditional cases; embedded-only baseline9objects17edges22691B, repeat9/34/22691 in the same operation; exact-fit and under-budget checks, failure latch, complete two-root chain with old core cache absent, missing declared envelope candidate and ambiguous pair rejection, P0/P1/P2 and legacy joins. Synthetic signature bytes, not crypto or TCB positives.9 syntactically valid negative controls caught:7 assertion failures,2 inherited early refusals (truncated chain and discarded shared budget). Three initial harness errors were corrected with before-images and logs retained; subsequent local inspection added exact before-head/history/counter joins and tests. No native or complete historical-proof claim.

Run using Python3.12/UCD15 with jsonschema:
`python -I -B check_provenance312.py`
`python -I -B check_registry312.py`
The control script creates controls-r1 once; replay in a separate extracted copy/output directory.

Native311 and all original full125 reference modules remain unchanged. Successor codec/native/reference integration, actual authentication/current context/publication and M2–M6 remain open. USER pushes; no push performed.
