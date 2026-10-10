// Unreviewed CSJ-1 nonpath comparison data using the exact pinned Cargo library.
// No source/lock/manifest/custody/owner admission or public route is constructed.
use crate::core::SourceId;

#[derive(Debug)]
pub(crate) enum Refusal {
    EmptyLockSource,
    MissingMetadataSource,
    LockParse(anyhow::Error),
    MetadataParse(anyhow::Error),
    PathInNonpath,
    MissingGitPrecise,
    DifferentSource,
}

#[derive(Debug)]
pub(crate) struct ComparisonData<'a> {
    pub(crate) original_lock_source: &'a str,
    pub(crate) original_metadata_source: &'a str,
    pub(crate) lock_source: SourceId,
    pub(crate) metadata_source: SourceId,
}

pub(crate) fn compare_nonpath<'a>(
    original_lock_source: &'a str,
    original_metadata_source: Option<&'a str>,
) -> Result<ComparisonData<'a>, Refusal> {
    if original_lock_source.is_empty() {
        return Err(Refusal::EmptyLockSource);
    }
    let metadata_text = original_metadata_source.ok_or(Refusal::MissingMetadataSource)?;
    let lock_source = SourceId::from_url(original_lock_source).map_err(Refusal::LockParse)?;
    let metadata_source = SourceId::from_url(metadata_text).map_err(Refusal::MetadataParse)?;
    if lock_source.is_path() || metadata_source.is_path() {
        return Err(Refusal::PathInNonpath);
    }
    for source in [lock_source, metadata_source] {
        if source.is_git() && !source.precise_git_fragment().is_some_and(|s| !s.is_empty()) {
            return Err(Refusal::MissingGitPrecise);
        }
    }
    if lock_source != metadata_source || !lock_source.has_same_precise_as(metadata_source) {
        return Err(Refusal::DifferentSource);
    }
    Ok(ComparisonData {
        original_lock_source,
        original_metadata_source: metadata_text,
        lock_source,
        metadata_source,
    })
}
