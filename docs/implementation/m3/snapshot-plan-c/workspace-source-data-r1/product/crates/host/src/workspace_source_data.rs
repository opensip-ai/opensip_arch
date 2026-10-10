//! Workspace source-class data over complete supplied opaque-id populations.
//! This is not admitted metadata, activation, filesystem custody or owner authority.

use std::collections::BTreeSet;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum CandidateSourceClass {
    SnapshotMember,
    DependencyClosureMember,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum CandidateIdError {
    DuplicatePackage,
    DuplicateWorkspaceMember,
    UnknownWorkspaceMember,
    UnknownSelectedPackage,
}

/// Check complete supplied package/member populations before classifying any selection.
/// Exact opaque UTF-8 equality is the only join; no parsing, name/version, key,
/// source/null, path prefix, default member or root heuristic is involved.
/// Every selected occurrence is retained in its supplied order, including repeats.
/// These are candidate labels only. The caller still owes one owned observation,
/// activated package proof and all actual source/manifest/profile/custody joins.
pub(crate) fn classify_candidates(
    packages: &[&str],
    workspace_members: &[&str],
    selected_packages: &[&str],
) -> Result<Vec<CandidateSourceClass>, CandidateIdError> {
    let mut package_ids = BTreeSet::new();
    for id in packages {
        if !package_ids.insert(*id) {
            return Err(CandidateIdError::DuplicatePackage);
        }
    }
    let mut members = BTreeSet::new();
    for id in workspace_members {
        if !members.insert(*id) {
            return Err(CandidateIdError::DuplicateWorkspaceMember);
        }
        if !package_ids.contains(id) {
            return Err(CandidateIdError::UnknownWorkspaceMember);
        }
    }
    selected_packages
        .iter()
        .map(|id| {
            if !package_ids.contains(id) {
                return Err(CandidateIdError::UnknownSelectedPackage);
            }
            Ok(if members.contains(id) {
                CandidateSourceClass::SnapshotMember
            } else {
                CandidateSourceClass::DependencyClosureMember
            })
        })
        .collect()
}

#[cfg(test)]
#[path = "workspace_source_data_tests.rs"]
mod tests;
