//! Pure descriptor validation helpers over explicitly supplied values.
//! This initial module implements only the selected identity LogicalPath profile.
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

#[cfg(test)]
mod tests {
    use super::*;
    use alloc::{vec, vec::Vec};

    #[test]
    fn refuses_noncanonical_segments_without_normalizing() {
        for path in [
            "",
            "/a",
            "a/",
            "a//b",
            ".",
            "..",
            "a/./b",
            "a/../b",
            "a\\b",
            "a\0b",
            "a\n/../../b",
        ] {
            assert!(LogicalPath::parse(path).is_err(), "{path:?}");
        }
        for path in ["src/lib.rs", "...", " a ", "a:b", "a\nb/c"] {
            let admitted = LogicalPath::parse(path).unwrap();
            assert_eq!(admitted.as_str(), path);
            assert_eq!(admitted.into_string(), path);
        }
    }

    #[test]
    fn unicode_scalar_limits_are_not_byte_or_utf16_limits() {
        assert!(LogicalPath::parse(&"😀".repeat(255)).is_ok());
        assert_eq!(
            LogicalPath::parse(&"😀".repeat(256)),
            Err(LogicalPathError::ComponentLength)
        );
        let mut parts: Vec<String> = vec!["a".repeat(255); 15];
        parts.push("b".repeat(254));
        parts.push(String::from("c"));
        let boundary = parts.join("/");
        assert_eq!(boundary.chars().count(), 4096);
        assert!(LogicalPath::parse(&boundary).is_ok());
        assert_eq!(
            LogicalPath::parse(&(boundary + "x")),
            Err(LogicalPathError::PathLength)
        );
    }

    #[test]
    fn preserves_distinct_unicode_spellings_and_order() {
        let nfc = LogicalPath::parse("é/file").unwrap();
        let nfd = LogicalPath::parse("e\u{301}/file").unwrap();
        assert_ne!(nfc, nfd);
        assert_eq!(nfc.as_str(), "é/file");
        assert_eq!(nfd.as_str(), "e\u{301}/file");
        assert!(nfd < nfc);
    }

    #[test]
    fn preserves_selected_final_lf_not_pattern_edge() {
        for path in [".\n", "..\n", "a/.\n", "a/..\n"] {
            assert_eq!(
                LogicalPath::parse(path),
                Err(LogicalPathError::InvalidComponent)
            );
        }
        for path in ["a\n", ".\n\n", "a/.\r\n", ".\u{2028}", ".\u{2029}"] {
            assert!(LogicalPath::parse(path).is_ok(), "{path:?}");
        }
    }
}
