//! M3-D r5 item 10 (unit D2b-3a): the components crate's copy of the exact
//! raw schema sources that the selected registry pins, for the provider
//! codecs' payload schema checks (each payload against its closed product
//! schema, D2b plan r3 section 0). The components crate cannot reach the
//! host's embedded copy, so it embeds the same files, as storage does (law
//! X3d r6). `RegisteredSchemas::from_sources` refuses any absent, extra,
//! reordered or replaced source by its full-document pin. No runtime path
//! lookup or ambient I/O.
use opensip_identity::RegisteredSchemas;
use std::sync::OnceLock;

const SOURCES: &[&[u8]] = &[
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/dispatch-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/enumeration-plan-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/execution-inputs-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/fact-batch-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/framework-recognition-plan-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/incoming-search-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/occupancy-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/handshake-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/startup-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/relation-payload-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/rust-subject-scope-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/subject-inventory-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/symbol-census-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/target-attribution-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/control-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/preview-configuration-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/product-configuration-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/evaluator-emission-plan-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/identity-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/import-source-context-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/native-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/policy-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/configuration-disclosure-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/explicit-history-panel-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/explicit-history-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/common-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/baseline-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/envelope-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/envelope-v4.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/command-envelope-v7.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/inventory-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/inventory-v4.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/command-inventory-v6.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/common-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/common-v4.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/comparison-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/detector-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/graph-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/graph-query-v4.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/invocation-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/invocation-v5.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/policy-test-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/repair-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/report-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/review-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/sarif-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/imported-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/metadata-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/policy-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/policy-test-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/presentation-catalog-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/test-execution-v1.schema.json"
    )),
];

/// The immutable embedded sources, in the registry's order, for codec
/// work-bound derivation and depth controls. Consumers must first obtain
/// the selected registry, which verifies the complete source set's pins.
pub(crate) fn sources() -> &'static [&'static [u8]] {
    SOURCES
}

/// The selected registry, compiled once per process. `None` if the embedded
/// sources do not satisfy the registry's pins, which no lawful build reaches.
pub(crate) fn registry() -> Option<&'static RegisteredSchemas> {
    static REGISTRY: OnceLock<Option<RegisteredSchemas>> = OnceLock::new();
    REGISTRY
        .get_or_init(|| RegisteredSchemas::from_sources(SOURCES).ok())
        .as_ref()
}

#[cfg(test)]
mod tests {
    use super::*;

    /// The embedded sources are exactly the registry's pinned sources, in its
    /// order, and they compile.
    #[test]
    fn the_embedded_sources_are_the_pinned_registry() {
        let pins = RegisteredSchemas::source_requirements();
        assert_eq!(SOURCES.len(), pins.len());
        let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
        for (raw, pin) in SOURCES.iter().zip(pins) {
            assert_eq!(
                *raw,
                std::fs::read(root.join(pin.source_path()))
                    .unwrap()
                    .as_slice()
            );
        }
        assert!(registry().is_some());
    }
}
