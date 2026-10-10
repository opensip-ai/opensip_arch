// Proposed compatible producer metadata view, pending complete profile review.
// Original lock tuple/key inputs are never replaced by this rendering.
use crate::core::SourceId;
use serde::Serialize;

pub(crate) fn serialize<S>(source: &SourceId, serializer: S) -> Result<S::Ok, S::Error>
where
    S: serde::Serializer,
{
    if source.is_path() {
        None::<String>.serialize(serializer)
    } else {
        serializer.collect_str(&source.as_encoded_url())
    }
}
