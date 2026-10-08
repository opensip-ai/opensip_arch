# S-OP-2b r1, the harness instrumentation sink

**Draft r1, PROPOSED, not accepted.** 2026-10-05. Grok leads. Codex has not reviewed this unit. It edits no product file and does not bind `design-lock.json`.

The accepted law M3-O1 r2 says the lead drafts S-OP-2b as its own design unit. The owed text is the body of `PROPOSAL.md`, byte-for-byte the blockquote in `o1/PROPOSAL-r2.md`. Quoting that text inside M3-O1 did not accept this unit.

## Parent

One parent: `docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md`, 130001 bytes, sha256 `ce8d3a4b783328915f0bf550dd111f227aa9901d5efddbcd9ccc8707cd4cb11d`. That file is a candidate of the unbound S-OP-2-R record. `verify_design` admits a contract parent only after it is an accepted base. S-OP-2-R selects it. Until that bind, a live append of this record refuses with `contract parent is not an accepted base or selected inventory`. That refusal is the bind order, not a defect in the override.

Bind order when the time comes: S-OP-2-P, then S-OP-2-R, then this unit. S-OP-2-P and S-OP-2-R stay unbound until O1-a integrates. This unit does not wait on O1-p.

## The one passage change

Item 12's sink table gains one row. The override selects line 429, the `P3` row, and its `after` text is the new `harness` row followed by that same `P3` row. The parent file is not edited. Item 12's projection bullet is not overridden: the owed text says that rule applies unchanged. No other sink, ceiling, kind, class, bound, escaping rule or reader rule is overridden. `passageSupersessions` is empty.

The `Sink` member named by rule 5 is this new row. S-OP-2 r6 does not publish a second closed member list for that K1 table, and this unit does not invent one.

## What a review can re-run

`evidence/check_sop2b.py` is read-only. It checks the parent pin, the line-429 override, the owed-body copy, and that the subject pins match the files. It does not take the lane lock and it does not run cargo.

## Not in this unit

No product code, no Cargo feature, no inventory successor, and no edit of O1-a or O1-p. The harness sink itself is code unit O1-b, which still waits on O1-a, O1-p, this unit's acceptance and binding, and the RequestId scope.
