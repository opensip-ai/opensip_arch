**FA-2 r2 — ACCEPT-DESIGN-UNIT**

Both required r1 findings are resolved. No required findings or new non-blocking observations remain. This acceptance covers the exact pinned design unit; it does not assert implementation, product qualification or root assent.

Subject manifest: `docs/implementation/m3/native-successors-fa/fa-2-subject.json`, **2,394 bytes**, SHA-256 `dca02900a4f030d80021ea889afc73005df9ba4959ebfd682eb23d8118998538`.

Successor: `docs/implementation/m3/native-successors-fa/fa-2/successor.json`, **38,659 bytes**, SHA-256 `f6b105f49ee5c9ae716c1cbb0d05f5288e35870740a572023e5609872e165728`.

All **39 supplied pins matched initially and at the final check**, including `design-lock.json@cd5958b`. The current product HEAD was also `cd5958b3608f44a0035566c9d4500e5005c62e91`. H r1 remains the obligation's source; L r4 is the separately reviewed context, not acceptance authority for this unit.

**Disposition of r1 findings and observations**

| Item | Disposition | Evidence and consequence |
|---|---|---|
| FA2-R1-01 | Resolved | The NE:1927 `after` equals the r1 exact replacement: a symbol key **in a TypeScript or Rust universe** uses the §9.8 census. The generator, README table and LD-F2 host bullet agree; syntax retains its in-host census. |
| FA2-R1-02 | Resolved | X-FA2-C is limited to TS/Rust bindings owing the worker's symbol inventory and to TS/Rust universes requiring a worker. Host-derived inventories and syntax universes are excluded. The two added clauses preserve the requested boundary. |
| FA2-N1-01 | Adequately recorded for implementation | README:17 and 310–315 disclose the historical models' old schema loading and unconditional key check, track the D2b/H follow-up through settlement, and retain old no-token refusal controls. No model byte change was requested in r1; none is required for this design unit. |
| FA2-N1-02 | Resolved | README:306 uses the exact corrected count: seven valid payloads, five payload refusals and two projected-SIS cases. All fourteen outcomes were reproduced. |

The X-FA2-C row at README:280 agrees with unchanged LD-F6:134–139 and §9.8:24–31. Its C r8/CRC-2 reference routes host-inventory ownership to the separate X-H3 work; it does not purport to complete that work or attribute those records to the language worker. That separation follows M3-C r6:447's actual-producer rule and 881–882's host-derived inventory distinction. The explicit syntax/no-child clause agrees with X-FA2-E1 and §9.8's final paragraph. The pinned L r4 X16:958–961 records the same exclusions and routing.

**Scope of r2**

Exactly three of eleven members changed; the other eight retain r1's byte length and SHA-256 and match the current files. See [member-delta.json](member-delta.json) and the full [README](README.diff), [generator](build_fa2.diff) and [successor](successor.diff) diffs.

- README adds the correction/disposition table, narrows the two scope passages, updates status/base/L references, corrects the case count, and records the model and scratch-check limits.
- The generator narrows only the NE:1927 insertion, adds cd5958b to the default lock checks, and updates the record's standing text.
- The successor changes that one `after` value and its standing text, and refreshes the README/generator candidate pins. Its five parents and other eighteen overrides are unchanged.
- The subject manifest refreshes exactly those three member pins. The draft unit record and scratch-check script/log remain outside the subject.

The unchanged eight members are both handshake copies, both census-schema copies, §9.8, the materialization map, the copies report and the vectors. No additional carrier, wire-schema, commitment-value recipe, admission-point or reuse-treatment change was found. All four NE §0 rows are unchanged. The unchanged carrier and admission decisions retain the r1 assessment.

**Selection and evidence**

Both explicitly permitted scripts ran with the pinned Python, `-I -B`, at nice 19 and exited 0. The build check reproduced nine generated files in memory, the scope2 oracle and all fourteen schema cases. It checked the locks at e093e90 (77 successors), 15c0779 (81) and cd5958b (82): accepted parents, no copied-parent override to carry, no already-bound FA-2 selector and fresh candidate paths. B-S1's eleven NE selectors remain disjoint.

The scratch-selection script used the product's actual `tools/verify_design.py@cd5958b`. With the pinned lock's 82 successors plus FA-2 r2, it returned **passed=true**, **46 inputs verified**, **10 candidates**, **19 passage overrides** and **0 supersessions**. Only the two labelled synthetic acceptance paths were redirected; the verifier's admission and chain logic was unchanged. The synthetic records and tool copy were written solely under this review's `verify/` directory.

See [evidence-check.txt](evidence-check.txt), [scratch-verify.txt](scratch-verify.txt), [pin-check-initial.txt](pin-check-initial.txt) and [pin-check-final.txt](pin-check-final.txt). The synthetic selection check demonstrates structural eligibility after real acceptance and matching root assent; it supplies no assent and changes no product lock.

The reference-model follow-up remains implementation work for D2b/H. Neither script exercises a provider, compiler, frame or CBOR codec, or a real Plan-extent join. X-H6 and the existing Rust subject-cap follow-up remain their owners' separate gates. No further FA-2 bytes are requested, so this review introduces no additional forced change for L r4's third delta-round trigger; L's other gates were not reviewed here.

No cargo, builds, product tests, crash-matrix commands, repository edits, commits, pushes or delegation occurred. Output and scratch stayed in this review directory; the r1 dependencies were reused read-only as the request permits. Commands used review-local HOME and TMPDIR (0700). The real OpenSIP home and private 413 UUID fixture were neither read nor created.

Selection still requires actual matching root substantive assent and the authorized binding-only lock update. This report supplies the independent design acceptance for the exact subject hash above.

