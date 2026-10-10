// Proposed first-party metadata source field; not a selected full producer profile.
// The view neither replaces the original lock tuple nor grants source authority.
use cargo::core::SourceId;
use serde::Serialize;

pub(crate) struct MetadataSourceView(pub(crate) SourceId);

impl Serialize for MetadataSourceView {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        if self.0.is_path() {
            None::<String>.serialize(serializer)
        } else {
            serializer.collect_str(&self.0.as_encoded_url())
        }
    }
}
