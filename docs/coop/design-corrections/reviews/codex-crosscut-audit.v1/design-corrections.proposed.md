# Proposed resolutions from the additional author audit

Standing: Codex author proposals against candidate25. These are concrete review
inputs, not accepted replacements or an applied successor. Historical schemas,
review receipts and candidate25 bytes remain unchanged.

## XA-01 — count selected project directories after boundary selection

Security S3 and native §1.4 must apply the 4096-directory admission limit after
nested-authority and custody exclusions, and after explicit workspace-root
selection. An unrelated directory outside that selection cannot reject it.
A directory with co-located language markers counts once. Cargo member roots
retained by the existing explicit-workspace folding rule remain selected input
directories; this change does not remove member semantics or change later Plan
bounds. The refusal must publish the actual selected count and limit, with no
partial successful unit set.

The three-file reference proposal implements this ordering in a separate copy.
The shared enumerator keeps its existing default cap for standalone callers;
security and native composition defer that cap until their selection is known.
This is a reference correction to the existing exclusion/override promise.
It does not implement a filesystem scanner or qualify its work bounds.

## XA-02 — disclose observed counts without requiring hidden-tree enumeration

Replace S3's promise to report the number of hidden markers with this rule:

> Record each encountered pruned directory anchor once without descending into
> it to enumerate markers. A marker count is an observation over an explicitly
> supplied inventory, never a claim about unenumerated contents. Production
> discovery may report the count as unknown. A separately admitted native
> dependency read set does not retroactively make discovery exhaustive.

The proposed successor row is closed:
`{path, reason, markerCount, markerCountBasis}`. `path`/`reason` keep their
existing meanings. `markerCountBasis` is `not-enumerated` or `observed-inventory`.
For `not-enumerated`, `markerCount` is null. For `observed-inventory`, it is a
nonnegative exact integer counting distinct supplied marker paths under that
anchor, with no assertion of filesystem totality. Zero observed is not zero
hidden. The bounded host directory observation supplies pruned anchors even
when no descendant marker is observed. Native composition consumes those
admitted anchors, rather than reconstructing their existence only from marker
paths. Any optional observed count belongs to provenance, not source scope or
Run identity.

This needs an explicit versioned successor to DiscoveryProvenanceV1 and
AdmittedBoundaryInventoryV1, their schema mirrors, native discovery result and
host integration. Do not add the fields to old closed records or silently
reinterpret a frozen exact-count claim. Required controls: unreadable pruned
directory; empty supplied descendant inventory; 4200 synthetic observed
markers; changing only that optional inventory changes provenance but not
selected units/scope; native dependency reads still require separate custody.
The row is specified here; schema/model integration and new frozen-subject
review remain outstanding. The XA-01 reference patch does not claim to fix this.

## XA-03 — make the graph-query availability route an explicit scoped selector

Preserve the already explicit graph-query behavior and its retained goldens:
known `purged`, `expired`, `corrupt` or `unavailable` availability observations at
`execute_graph_query` produce operational-failed / HOST.IO_FAILURE / exit 4,
with their exact evidence detail. They never produce empty graph success.

Amend identity-and-evidence §5's general precondition paragraph to say that
explicit graph operations use query-projection-contract.v3 §7 for this
observation. Reserve exit 2 there for command-specific prerequisites whose
owners actually select request rejection, such as attempting an operation
whose required evidence cannot be supplied at admission. Retained manifest-only
queries can still report a tombstone without reopening unavailable evidence.
Missing promised bytes during replay remain the existing exit-4
EvidenceUnavailable boundary. Do not change an exit based merely on a
filename, exception prefix or a caller-supplied origin.

Add the same narrow applicability selector in the query contract's owning
section. The proposal changes no graph result, D9 code, fault vocabulary or
schema. It resolves overlapping prose so independent implementers can select
one route. The retained positive plus four unavailable-state public calls
support the current behavior; actual independent review must assess the
proposed selector before a successor is accepted.
