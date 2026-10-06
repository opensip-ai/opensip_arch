# S-B typed producer-bound projection

S-B extends the same public bounded-request projection to the following producer-owned quantities. Every proven crossing is `request-rejected` (exit2), code `REQUEST.UNSATISFIABLE`, public detail `PROJECT.SCOPE_LIMIT`, without truncation or splitting. The observed quantity and published limit remain in the owner's typed refusal. Count subjects have the existing `field:count>limit` form, with `count` and `limit` replaced by exact decimal observed value and ceiling. Byte subjects use the same numeric form with an explicitly byte-labelled field, not JSON string length, framing or ledger charge. The public field labels below identify producer quantities; they add no schema members, parser coercions, new wire cause, mint list or changed schema bound.

| Typed refusal | Public field | Quantity | Ceiling | Population and boundary |
|---|---|---|---|---|
| SnapshotBound | snapshot.sourceInventory | rows | 100000 | Complete captured source inventory |
| SnapshotBound | snapshot.descriptorBytes | canonical bytes | 4194304 | Full canonical snapshot descriptor |
| SnapshotBound | snapshot.totalFileBytes | content bytes | 8589934592 | Entire retained snapshot, shared by every universe; smallest applicable bound |
| DependencySetBound | dependency-source-set.packages | packages | 4096 | Final admitted, activated, non-path set |
| DependencySetBound | dependency-source-set.files | logical files | 1000000 | Sum of committed fileCount over that same final set |
| DependencySetBound | dependency-source-set.totalBytes | content bytes | 8589934592 | Sum of committed totalBytes over that same final set |
| DependencyAcquisitionBound | dependency-acquisition.sources | candidates | 16384 | Full acquisition candidate population, before activation |
| DependencyAcquisitionBound | dependency-acquisition.files | logical files | 4000000 | Decoded/read candidate regular files, before activation |
| DependencyAcquisitionBound | dependency-acquisition.totalBytes | content bytes | 34359738368 | Decoded/read candidate content, before activation |
| Host subject-scope bound | subject-scope.subjects | subjects | 100000 | Complete host-derived subject census, after execution at H admission |
| Host subject-scope bound | subject-scope.descriptorBytes | canonical bytes | 4194304 | Full canonical host-derived subject-scope descriptor, after execution |

The snapshot remedy is "add ignorePaths or select a narrower project root". Dependency and acquisition remedies narrow the project selection whose complete required populations exceed the ceiling; they never delete required package rows, manufacture activation, partially materialize a candidate or reinterpret rejected packages as admitted ones. The subject-scope remedy narrows explicit project/capability selection before retry; it never truncates, partitions or fabricates the host's complete census.

The set check occurs once after activation and route admission, before descriptor/wrapper/transport. Inactive candidates and rejected archives do not count toward the final set, even when acquired; their acquisition work retains its separate population. A single oversized candidate has no shortcut: acquire to completion subject to acquisition and per-archive decoder limits, admit or reject under its own route, materialize whole only when admitted, then decide activation and the final set bound. Per-archive decoder D1-D4 crossings remain archive-profile breaches and missing/undecodable routes; they are never DependencySetBound or DependencyAcquisitionBound. Ledger exhaustion and adapter scratch/output budgets keep their own existing routes.

Acquisition's first crossing is the owner's deterministic canonical order: candidates ascending by UTF-8 (name, version, sourceId), archive file order or tree ascending logical path within a candidate; a simultaneous crossing is sources, then files, then content. S-B adds no priority across independent producer boundaries. Snapshot, final-set and subject-scope refusal selection remain their owners' typed observations rather than a new guessed tie-break rule.

Snapshot/dependency/acquisition refusals occur before Plan minting and mint no Plan or Run for the refused step. Subject-scope refuses after provider execution at H's atomic admission boundary; S-B does not undo an existing Plan, relabel provider source custody, invent an earlier refusal, or mint an admitted Run from refused assembly. H/J's existing effect, settlement and termination composition continue to govern. Malformed inputs and corrupt retained records retain schema-first origin-dependent refusal routes; the count/byte projection applies only to a proven owner-computed quantity, never a length coerced from null, boolean, string, object or malformed array.

The original seven selection-array fields, their FX-CAP-1 capacities, prospective-Plan declaration order and earlier native-context boundary remain unchanged. No context, feature, dependency, snapshot, prepared-output, request, source-variant, record-byte, frame, stage or ledger bound is widened here. C1a/C3a/H5/J consumer code and real controls remain separately gated; text/arithmetic projection controls are not producer completeness, runtime admission, O7 execution or product qualification.
