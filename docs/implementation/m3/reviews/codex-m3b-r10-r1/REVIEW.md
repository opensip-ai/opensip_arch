# REQUIRED-FINDINGS — M3-B r10, round 1

Subject manifest SHA-256: `e6a271b406bdec09f5d5c71ba4f4070b9e148c898e370cd0d690455b00e7c7fc`. Its sole member, `PROPOSAL-r10.md`, matches 141,546 bytes and SHA-256 `db52ddf3dde93213a4cb2d8f1b3ee16e012de59ebb4832b76a3310e205248b66`. Product and architecture HEADs match the requested bases. The r9 diff base matches SHA-256 `24fe5a9cc473870dc0b3ea43bb23abb0ddcda4de099a25a41d0cd65cb6069b8e`; the live r9 proposal differs only in its acceptance banner.

## M3BR10-R1-RF-1 — The existing remedy omits both new refusal bounds

At `PROPOSAL-r10.md:43`, the decision table claims that the existing remedy says to “keep the graph within its bounds” and therefore needs no S10 successor. That is item 14a's prose summary, not the exact accepted remedy.

The selected S10 reference carriers (`s10-tsc/reference/native_evidence_model.py:1169` and `native_evidence_model.v2.py:1169`) and the product carrier (`crates/host/src/outcomes.rs:1032`, `REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED`) specify:

> keep each file within 64 KiB and the graph within 32 files

Neither states the new 64-entry or 4,096-character limit. For example, a small, valid entry containing 65 repetitions of `./base.json`, with that base present and empty, has only two nodes, no cycle, correct field types and files well below 64 KiB. It already satisfies the existing remedy, but r10 refuses it. Similarly, the remedy gives no path-shortening instruction for an otherwise valid 4,097-character canonical node path.

The alias to `native.typescript-config-unresolved`, its request-rejected/2 `CONFIG.INVALID` D9 row and bounded internal-key/path subject can remain unchanged. The remedy must cover the expanded refusal domain. Correct the decision table and change declaration to require a narrow successor of the selected remedy authorities and product carrier, naming both limits and appropriate controls. Name that successor as required work or bind it through review; acceptance of the law need not imply completed product integration. Do not claim the old remedy already covers these cases.

## Other requested decisions

- **Completeness:** The proposed input bounds close the two identified representability gaps in `TypeScriptConfigGraphV1`: at most 64 ordered edges per node, repetitions retained, and at most 4,096 characters in each node path. Edges and the entry reuse node paths. The existing 32-node limit is stricter than 1,024; canonical nonempty paths, unique sorted node identities, reachability, closed edges, acyclicity and basename-derived kind supply the remaining graph conditions. The constructor supplies the fixed record fields and exact-content digest. `configGraphPaths` introduces no additional graph-size or path constraint. No further input constraint blocking this amendment was found.
- **Soundness:** Refusing before graph emission preserves the shared pre-Plan/C2 graph requirement. Retaining repetitions preserves declaration-order precedence. Raising the native schema limit, dropping or truncating edges, truncating paths or deferring the refusal until C2 emission would not satisfy this law's stated identity and consistency goals.
- **Order and subject:** The new-node check order preserves LD-B2C2-4: the 32-node check for a new base precedes path length, file size and parsing/types; the entry also receives the path check. Checking every array element's type before the 64-entry bound, and that bound before specifier classification/resolution, makes mixed-error cases deterministic. Depth-first edge declaration order and the existing parent subject for an unresolved edge, cycle or 33rd node remain intact. The new length refusal names the overlong node, and the edge-count refusal names the declaring file.
- **Public termination:** The alias rows and D9 outcome remain suitable, but the remedy is incomplete as detailed in RF-1. The claim that no successor is needed cannot be accepted.
- **Scope and fidelity:** The full r9-to-r10 diff is confined to the banner/history, declared r10 section, item 14a bounds/refusal/control additions and one Not claimed line. No unrelated law change was found. No T2 measurement, margin, TypeScript compatibility or product implementation is inferred.

No non-blocking observations. This was a read-only law review using file reading, hashing, JSON parsing and Git queries; no build, test, generator, network, delegation or prohibited private data access occurred. Only this directory's `REVIEW.md` and `review.json` were written; neither repository was edited.
