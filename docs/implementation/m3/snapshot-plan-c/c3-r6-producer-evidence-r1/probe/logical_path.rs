//! Pure descriptor validation helpers over explicitly supplied values.
//! Lexical paths, exact collection order and shape-checked candidate identities.
//! Candidate identities do not establish retained closure or replay authority.
use alloc::string::String;
use core::fmt;

/// A string admitted by the selected identity schema's LogicalPath definition.
///
/// This is a lexical value, never filesystem custody or authorization. No
/// normalization, filesystem access or snapshot join occurs. Use it for the
/// direct Blob.path / import-blob.path profile, not scope paths (where `.` can
/// mean root) or the differently constrained fingerprint logicalPath member.
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub struct LogicalPath(String);

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum LogicalPathError {
    Empty,
    PathLength,
    InvalidComponent,
    ComponentLength,
}
impl fmt::Display for LogicalPathError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{self:?}")
    }
}
impl core::error::Error for LogicalPathError {}

impl LogicalPath {
    pub fn parse(value: &str) -> Result<Self, LogicalPathError> {
        if value.is_empty() {
            return Err(LogicalPathError::Empty);
        }
        // Schema character limits count Unicode scalars, not UTF-8 bytes or
        // UTF-16 code units. Stop counting once the admitted bound is exceeded.
        if value.chars().take(4097).count() > 4096 {
            return Err(LogicalPathError::PathLength);
        }
        if value.contains(['\\', '\0']) {
            return Err(LogicalPathError::InvalidComponent);
        }
        for part in value.split('/') {
            if matches!(part, "" | "." | "..") {
                return Err(LogicalPathError::InvalidComponent);
            }
            if part.chars().take(256).count() > 255 {
                return Err(LogicalPathError::ComponentLength);
            }
        }
        // Preserve the selected pattern's Python-compatible `$` behavior in
        // `not: (^|/)\.\.?(/|$)`: it also matches before one final LF.
        // Do not silently widen that schema while enforcing semantic segments.
        if value
            .strip_suffix('\n')
            .is_some_and(|prefix| matches!(prefix.rsplit('/').next(), Some("." | "..")))
        {
            return Err(LogicalPathError::InvalidComponent);
        }
        Ok(Self(String::from(value)))
    }
    pub fn as_str(&self) -> &str {
        &self.0
    }
    pub fn into_string(self) -> String {
        self.0
    }
}
impl core::str::FromStr for LogicalPath {
    type Err = LogicalPathError;
    fn from_str(value: &str) -> Result<Self, Self::Err> {
        Self::parse(value)
    }
}

