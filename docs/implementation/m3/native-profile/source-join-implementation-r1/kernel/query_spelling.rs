mod core { pub use cargo::core::SourceId; }
#[allow(dead_code)] mod source_join;
fn main() {
    let raw = "git+https://example.com/repo?branch=topic%2Ffoo%2Bbar#same";
    let source = core::SourceId::from_url(raw).unwrap();
    let metadata_json = serde_json::to_string(&source).unwrap();
    let metadata_text: String = serde_json::from_str(&metadata_json).unwrap();
    let encoded_text = source.as_encoded_url().to_string();
    let output = serde_json::json!({
        "standing":"UNREVIEWED EXACTPINNED SOURCE SERIALIZATION OBSERVATION; NO SOURCE ADMISSION OR NEW SERIALIZER SELECTION",
        "originalRawLockSource":raw,
        "stockSerializedMetadataSource":metadata_text,
        "existingEncodedUrlView":encoded_text,
        "stockSerializationPassesSelectedCSJComparison":source_join::compare_nonpath(raw,Some(&metadata_text)).is_ok(),
        "existingEncodedViewPassesSelectedCSJComparison":source_join::compare_nonpath(raw,Some(&encoded_text)).is_ok(),
        "rawTupleChanged":false,"sourceProfilePublished":false,"sourceAdmissionImplemented":false
    });
    println!("{}", output);
}
