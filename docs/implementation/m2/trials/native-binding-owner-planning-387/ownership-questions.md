# Binding owner372: dependency and producer boundaries to resolve

Working audit, not a selected code move. Current inventory55 allows:

- security → contracts, evaluator, identity, platform; NOT lifecycle/storage/host.
- storage → contracts, identity, evaluator, platform, security.
- lifecycle → contracts, identity, platform, security, components, storage.
- host → all relevant owners.

Current provisional implementation has installation fence/capture in security, selection and lineage pure codecs in lifecycle, native S-marker capture in storage, and composite records/trust/lineage readers in host. These suffice for provisional comparisons but cannot be naively imported into security's authoritative binding constructor: security→lifecycle or security→storage creates the wrong dependency direction/cycle. Host-supplied scalars/booleans must not replace native binding proof just to avoid the dependency.

Options to examine before code:

1. Shared pure operational record codecs in identity (or inert contract types in contracts with canonical decoding in identity), used by lifecycle/storage/security without authority. Security can then own native registry/root/store observations and private authority construction. Lifecycle retains transition/publication orchestration; storage retains evidence mechanisms. Existing lifecycle/storage syntax APIs can re-export wrappers if needed; preserve bytes and test behavior through a separately reviewed move. Identity already owns canonical parsing and schema admission, so no OS/policy dependency is added.
2. Security privately admits exact captured records through identity's generic schema machinery, while lifecycle preserves its supplied-value algorithms. Avoid duplicate hand-coded schemas or canonicalizers. Decide whether one shared typed decoder is needed to prevent drift. A provenance-bound ShapeHandle by itself still is not live custody.
3. Host owns native composite context and passes an opaque capability to security through an interface owned in a lower crate. This is valid only if the capability has an actual non-forgeable producer without public caller-supplied fields/trait implementations. Do not introduce a public bool/marker-trait authority escape or a security→host dependency. A host-TCB assumption must be explicit if chosen, not hidden behind 'verified'.

Root currently favors option1 for inert codecs, with security-owned native/custody admission and lifecycle consuming those opaque observations. No new dependency direction or decoder relocation is implemented. Registry371 scope need not select this whole binding architecture before its owner can be reviewed; actual runtime wiring does require it. A parsed registry remains a value until root/marker/native custody/current operation admission is joined.

Also still open: initial lineage/pair/current publication ordering must avoid circular creation; authoritative shared budgets must include all native captures; post-fence operation context must tolerate unrelated mutable registry/pair replacement while retaining immutable selected-generation owners and S7 leases. These are concrete next review questions, not full binding acceptance.

Additional bootstrap boundary from actual private-trust127 schema and current trust_input_bindings.rs: CreationStoreBindingV1 is closed S/G/K with G=0, no namespace. Installation trust C is store/install scoped. Do not demand an already-admitted N/five-field view to create that first C on an installation whose registry is empty. Root restore/adoption must use the proper concrete source owner; do not broaden CreationStoreBindingV1 G=0 or synthesize an intent to accommodate a loosely described restored G. Ordinary trust-capsule rollback within S is distinct from a newly allocated store-lineage root. These are mandatory next owner joins, not proven by the seven digest vectors.
