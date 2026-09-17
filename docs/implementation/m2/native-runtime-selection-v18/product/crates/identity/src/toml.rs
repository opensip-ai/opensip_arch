//! Full-document TOML 1.0 parsing with the selected tomllib calendar profile.
//! The borrowed view is inert data, not package or retained-input admission.
use ::toml::de::{DeTable, DeValue};
use alloc::vec::Vec;
use serde_spanned::Spanned;

/// Local development bounds, not TOML grammar or aggregate CPU guarantees.
const MAX_NODES: usize = 1_000_000;
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum TomlError {
    ByteLimit,
    RecursionLimit,
    NodeLimit,
    InvalidUtf8,
    Syntax,
}
/// Owns parser containers while borrowing unchanged input bytes.
/// Numeric literals are never narrowed or converted to JSON numbers.
pub struct TomlDocument<'a>(Spanned<DeTable<'a>>);
#[derive(Clone, Copy)]
pub struct TomlTableView<'a>(&'a DeTable<'a>);
#[derive(Clone, Copy)]
pub struct TomlValueView<'a>(&'a DeValue<'a>);
impl TomlDocument<'_> {
    pub fn table(&self) -> TomlTableView<'_> {
        TomlTableView(self.0.get_ref())
    }
}
impl<'a> TomlTableView<'a> {
    pub fn get(self, key: &str) -> Option<TomlValueView<'a>> {
        self.0.get(key).map(|value| TomlValueView(value.get_ref()))
    }
    pub fn contains_key(self, key: &str) -> bool {
        self.0.contains_key(key)
    }
}
impl<'a> TomlValueView<'a> {
    pub fn as_table(self) -> Option<TomlTableView<'a>> {
        self.0.as_table().map(TomlTableView)
    }
    pub fn as_str(self) -> Option<&'a str> {
        self.0.as_str()
    }
}
/// Development execution profile: parse and drop on a host stack of at least
/// 2 MiB. The pure helper cannot inspect or provision its caller's stack.
/// Parser depth limits do not prove stack safety on arbitrary small threads.
/// Parse all bytes before exposing fields. Errors elsewhere in the document
/// cannot be hidden by a usable package name. Resource errors remain distinct
/// from syntax and invalid UTF-8. Parser recovery is deliberately not used.
pub fn parse_toml(raw: &[u8]) -> Result<TomlDocument<'_>, TomlError> {
    if raw.len() > crate::MAX_BYTES {
        return Err(TomlError::ByteLimit);
    }
    let text = core::str::from_utf8(raw).map_err(|_| TomlError::InvalidUtf8)?;
    // DeTable permits a leading BOM; the selected tomllib profile rejects it.
    if text.starts_with('\u{feff}') {
        return Err(TomlError::Syntax);
    }
    let tree = DeTable::parse(text).map_err(|error| match error.message() {
        // Pinned parser versions expose messages, not a typed resource cause.
        "recursion limit" | "cannot recurse further; max recursion depth met" => {
            TomlError::RecursionLimit
        }
        _ => TomlError::Syntax,
    })?;
    let mut pending = Vec::new();
    for (_, value) in tree.get_ref().iter() {
        pending.push(value.get_ref());
    }
    let mut remaining = MAX_NODES;
    while let Some(value) = pending.pop() {
        remaining = remaining.checked_sub(1).ok_or(TomlError::NodeLimit)?;
        // Parse-only DeInteger can retain an empty literal after 0x/0o/0b.
        // Validate nonemptiness without narrowing lawful large integers.
        if value
            .as_integer()
            .is_some_and(|integer| integer.as_str().is_empty())
        {
            return Err(TomlError::Syntax);
        }
        // CPython datetime rejects year zero and leap seconds. The pinned
        // TOML crate accepts both, including in fields unrelated to package.
        if value.as_datetime().is_some_and(|date| {
            date.date.is_some_and(|d| d.year == 0) || date.time.is_some_and(|t| t.second > 59)
        }) {
            return Err(TomlError::Syntax);
        }
        if let Some(array) = value.as_array() {
            for child in array {
                pending.push(child.get_ref());
            }
        }
        if let Some(table) = value.as_table() {
            for (_, child) in table.iter() {
                pending.push(child.get_ref());
            }
        }
    }
    Ok(TomlDocument(tree))
}

#[cfg(test)]
mod tests {
    use super::*;
    use alloc::{format, string::String, vec};
    #[test]
    fn full_document_and_borrowed_views() {
        let raw = b"[package]\nname='p'\n[unused]\nint=99999999999999999999999999999999999\nfloat=1e9999\ntime=1979-05-27T07:32:00Z\n";
        let doc = parse_toml(raw).unwrap();
        assert_eq!(
            doc.table()
                .get("package")
                .unwrap()
                .as_table()
                .unwrap()
                .get("name")
                .unwrap()
                .as_str(),
            Some("p")
        );
        assert!(doc.table().get("unused").unwrap().as_str().is_none());
        assert!(matches!(
            parse_toml(b"package.name='p'\nx=???"),
            Err(TomlError::Syntax)
        ));
    }
    #[test]
    fn utf8_bom_and_calendar_profile() {
        for raw in [
            b"\xef\xbb\xbfpackage.name='p'".as_slice(),
            b"package.name='p'\nx={a=[{b=0000-01-01}]}",
            b"package.name='p'\nx=[[23:59:60]]",
        ] {
            assert!(matches!(parse_toml(raw), Err(TomlError::Syntax)));
        }
        assert!(matches!(
            parse_toml(b"x='\xff'"),
            Err(TomlError::InvalidUtf8)
        ));
        assert_eq!(
            parse_toml("x='\u{feff}'".as_bytes())
                .unwrap()
                .table()
                .get("x")
                .unwrap()
                .as_str(),
            Some("\u{feff}")
        );
    }
    #[test]
    fn byte_and_recursion_limits_are_not_syntax() {
        assert!(matches!(
            parse_toml(&vec![b' '; crate::MAX_BYTES + 1]),
            Err(TomlError::ByteLimit)
        ));
        let raw = format!("x={}0{}", "[".repeat(128), "]".repeat(128));
        assert!(matches!(
            parse_toml(raw.as_bytes()),
            Err(TomlError::RecursionLimit)
        ));
        let raw = format!("{}x=1", "a.".repeat(100));
        assert!(matches!(
            parse_toml(raw.as_bytes()),
            Err(TomlError::RecursionLimit)
        ));
    }
    #[test]
    fn calendar_walk_node_limit_is_distinct() {
        let mut raw = String::from("x=[");
        raw.push_str(&"0,".repeat(MAX_NODES));
        raw.push(']');
        assert!(raw.len() < crate::MAX_BYTES);
        assert!(matches!(
            parse_toml(raw.as_bytes()),
            Err(TomlError::NodeLimit)
        ));
    }
}
