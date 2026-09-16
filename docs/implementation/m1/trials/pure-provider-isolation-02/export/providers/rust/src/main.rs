// Build probe only; not a provider implementation or wire transaction.
fn main() {
    let digest = opensip_identity::raw_sha256(b"isolated-provider-build-probe");
    assert_eq!(digest.len(), 32);
    let _ = std::mem::size_of::<opensip_contracts::generated::output::Metadata1BuildMetadataV1>();
}
