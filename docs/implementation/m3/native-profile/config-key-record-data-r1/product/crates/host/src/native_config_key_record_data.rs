//! NCA-1 key-record recipes over supplied paths and supplied classifications.
//!
//! These results are inert data. This module discovers no configuration, checks
//! no snapshot/cwd/Definition custody, and decides no semantic retention policy.
//! Callers remain responsible for complete actual populations and provenance.
//! There is no production caller, public failure projection, or resource-priced
//! native traversal here. No identity, schema handle, or source grant is minted.
use std::collections::BTreeSet;

use opensip_identity::{CanonicalError, JsonValue, canonical_bytes};

const MAX_KEY_SCALARS: usize = 256;
const MAX_KEYS_PER_SET: usize = 64;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum PathPart<'a> {
    Name(&'a str),
    /// An actual list position in the supplied path, never a wildcard.
    Index(usize),
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum Error {
    MissingInitialName,
    MissingFinalName,
    KeyTooLong,
    TooManyKeys,
    CrossClassification,
    CanonicalEncoding(CanonicalError),
}

/// Complete unique sorted sequences for the supplied classifications only.
#[derive(Debug, PartialEq, Eq)]
pub(crate) struct KeySetsData {
    pub(crate) honored: Vec<String>,
    pub(crate) stripped: Vec<String>,
}

/// Encode exactly one supplied real path without normalization or truncation.
pub(crate) fn key(path: &[PathPart<'_>]) -> Result<String, Error> {
    if !matches!(path.first(), Some(PathPart::Name(_))) {
        return Err(Error::MissingInitialName);
    }
    if !matches!(path.last(), Some(PathPart::Name(_))) {
        return Err(Error::MissingFinalName);
    }
    let mut result = String::new();
    let mut scalars = 0;
    for part in path {
        let text = match part {
            PathPart::Name(name) => {
                // Quoting never decreases scalar length. This derived guard
                // prevents copying a name that cannot fit the existing record.
                if name.chars().take(MAX_KEY_SCALARS + 1).count() > MAX_KEY_SCALARS {
                    return Err(Error::KeyTooLong);
                }
                let encoded = if !name.is_empty()
                    && name
                        .bytes()
                        .all(|b| b.is_ascii_alphanumeric() || b == b'_' || b == b'-')
                {
                    (*name).to_owned()
                } else {
                    let bytes = canonical_bytes(&JsonValue::String((*name).to_owned()))
                        .map_err(Error::CanonicalEncoding)?;
                    // The canonical encoder emits UTF-8 for a Rust String.
                    String::from_utf8(bytes)
                        .map_err(|_| Error::CanonicalEncoding(CanonicalError::InvalidUtf8))?
                };
                if result.is_empty() {
                    encoded
                } else {
                    format!(".{encoded}")
                }
            }
            PathPart::Index(index) => format!("[{index}]"),
        };
        scalars += text.chars().count();
        if scalars > MAX_KEY_SCALARS {
            return Err(Error::KeyTooLong);
        }
        result.push_str(&text);
    }
    Ok(result)
}

fn unique(paths: &[&[PathPart<'_>]]) -> Result<BTreeSet<String>, Error> {
    let mut result = BTreeSet::new();
    for path in paths {
        result.insert(key(path)?);
        if result.len() > MAX_KEYS_PER_SET {
            return Err(Error::TooManyKeys);
        }
    }
    Ok(result)
}

/// Compute complete supplied sets or return an error without a partial result.
/// Repeated supplied paths coalesce; their original observations do not.
/// Errors carry no public route, owning origin, or cross-owner precedence.
pub(crate) fn key_sets(
    honored: &[&[PathPart<'_>]],
    stripped: &[&[PathPart<'_>]],
) -> Result<KeySetsData, Error> {
    let honored = unique(honored)?;
    let stripped = unique(stripped)?;
    if !honored.is_disjoint(&stripped) {
        return Err(Error::CrossClassification);
    }
    Ok(KeySetsData {
        honored: honored.into_iter().collect(),
        stripped: stripped.into_iter().collect(),
    })
}

#[cfg(test)]
#[path = "native_config_key_record_data_tests.rs"]
mod tests;
