# C2a-3 M storage sub-bound: source proof draft

This proves only a proposed **storage** sub-bound under stated target-ABI
assumptions. It is not the complete M(c), a native allocation measurement,
acceptance, census or production-fit result. Inputs are frozen in INPUTS.json.

## Published storage price

`snapshot_source::owned_record(n)` delegates to
`custody::discovery_walk::owned(n)`. The pinned definition is one object, zero
edges and **n + 128 bytes**, with saturating addition. C2a-3 will check arithmetic
before calling the shared price; overflow becomes latched Budget/Arithmetic.
No local duplicate of the published record price is introduced.

That allowance is storage. A sink's new writes into its own payload buffer are
separate byte-copy work; CI transfer's shared-buffer read/hash does not charge
the sink's copy. K's later re-hash remains its existing separate price.

## BTreeMap node population

The selected construction is `BTreeMap::new()` followed by individual inserts
of unique candidate paths; no bulk collect, deletion, caller comparison function
or mutable key is involved. The pinned Rust path is map.rs/map/entry.rs and
node.rs. The first insertion allocates a root leaf. Splits allocate a new right
node; root growth allocates an internal node. Insert recursion climbs a parent
at a time. Existing left nodes are reused rather than copied into replacement
heap nodes. Keys/values are borrowed references and cannot execute user drop or
comparison code.

Completed nonempty nodes each contain at least one key, so their count is no
greater than the inserted key count. In the non-panicking unique-insert path,
new nodes remain in the resulting tree; no repeated allocation/deallocation
cycle grows cumulative allocation beyond its final count. A prospective bound
of **2F node allocations** for F>0 conservatively includes transient creation;
F=0 allocates no node. The stronger final-node bound is F, but this plan does not
depend on charging the tightest value.

This source argument must be challenged against every selected allocation path
before the implementation price is accepted. Allocator failures or process
abort are not a successful admission or a completed cost/qualification result.

## Per-node storage allowance

The pinned node has B=6, capacity 11, and internal edge capacity 12. For borrowed
`&str` keys and `&[u8]` values on the supported 64-bit targets, the proposed ABI
assumptions are pointer/usize 8 bytes, each fat reference 16 bytes, u16 2 bytes,
and field alignment at most 8. Allow even a 16-byte parent Option pointer rather
than depending on its niche layout.

The five leaf field groups have sizes at most [16, 2, 2, 176, 176]. Reserving
seven padding bytes after every group, then rounding to alignment, gives a
408-byte leaf upper bound. The repr(C) internal node adds twelve thin child
pointers (96 bytes), yielding at most 504 bytes. **512 bytes per allocated node**
therefore covers either shape under those assumptions.

The existing owned-record price adds its 128-byte overhead. The proposed map
storage allowance is consequently:

```
objects = 2F
edges   = 0
bytes   = 2F * (512 + 128)
```

Node visits, key comparisons, insertion movement, parent-link repairs and drop
traversal are **not included** in this storage expression and must be separately
priced in complete M. ABI checks over the public primitive/reference/Box types
and a reviewed field-layout proof are required before using this allowance in
accepted implementation evidence. No private std type size is asserted to have
been measured by this draft.

## Other retained storage

One pre-reserved `Vec<Vec<u8>>` stores F headers. Its storage allowance uses the
target's actual `size_of::<Vec<u8>>()`; no unverified literal is baked into the
product. Every payload gets the published owned-record allowance for its checked
expected byte length. Paths and the map's slice values are borrowed. Candidate
slot/result-vector storage belongs to the operation aggregate and cannot be
omitted or charged once per component by accident.

Whole buffers stay private until transfer succeeds. Building the borrowed map
only after the buffer vector is finished avoids borrowing a growing vector.
Dropping the temporary map/buffers after K does not refund the admission ledger.

Complete movement/callback/drop prices, native ABI and allocation controls,
independent source acceptance and X-SD9-2 completion remain open.
