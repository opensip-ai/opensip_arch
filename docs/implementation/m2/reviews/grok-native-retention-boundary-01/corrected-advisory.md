# Corrected advisory (not fresh-blind): closure kind vs `visit` memo

**Follow-up to** initial `report.md` / `report.json` (`eea20602…b740` / `25e4ae15…9982`), preserved as `initial-report.md` / `initial-report.json`. No production or trial-13 edit. Root remains lead.

Root’s current suite (286 AST-extracted `admit_frame`+`path_values`+`snapshot_joins` cases plus separate actual native bind; 98 workspace/Clippy) is taken as given. This note only retracts **item 2**. **Item 1 is already implemented** (those three functions + separate `N.bind_*`, not fullRun) and is not restated as missing work.

## Item 2 — retracted

The initial advisory said `visit()` memo hides kind, so two `closureJoins` to the same id with different `kind` would pass a naive `visit` shim and fail Rust.

That mislocated the gate.

Selected `identity_model.py` `619d6e3c…` `admit_frame` (~1625–1631):

```text
closure=get(key,'closure')
if closure['kind']!=join['kind']: raise NATIVE_CONTEXT_CLOSURE_KIND
visit(key,'closure')
```

Kind is checked **on every join** in that loop, **before** `visit`. `visit`’s `if key in seen: return` only skips the later schema walk of that closure’s tree. Rust matches: `object` + kind, then `closures.insert` skips tree bytes (`native_universe.rs` 990–1010).

An oracle that extracts **actual `admit_frame`** already has the correct kind gate. Dual-kind is still a good **control** against that gate (`ClosureKind` / `NATIVE_CONTEXT_CLOSURE_KIND`). It is not a visit-memo hole.

What **does** skip kind (already noted, still true): the **same-frame** parsed memo

```text
if ('frame', digest, domain_set) in parsed: return parsed[...]
```

A second `admit_frame` of the same context digest skips the whole function, including the closure loop and `admit_native_context`. Rust skips only the join walk on `frames.insert` and still reruns `inspect_native_context`. That is a different memo than `visit`. Do not conflate them when adding rekeyed length / noncanonical / dual-kind / depth cases.

## Unchanged from the initial advisory

Nested-record blobJoins have no `lengthField` in `admit_frame`; file-manifest and prepared-output lengths apply after nested **H** admission. Rust `configProjectionSha256` `bare-hex` without `retainedAs` is a Nested H-preimage for the walk, not only a binder rehash. Binder `MissingBlob`→`None` is not the retention/`blob()` contract. `inspect_native_context` stays descriptor-only. Rust universe file manifests need `depth >= 2`. Error classes stay `Law` / `SnapshotPath` / `BlobLength` / `Refused` / `Limit`. Plan/grant/pruned-tree/identity-walker native joins remain out of scope.

## Dual-kind control (still proposed, correctly aimed)

Same context frame, two `closureJoins`, same id, different `kind`: both reference `admit_frame` and Rust must refuse on the **second join’s kind check**, even if the closure tree was already retained. Do not expect `visit` memo to be the failing layer.
