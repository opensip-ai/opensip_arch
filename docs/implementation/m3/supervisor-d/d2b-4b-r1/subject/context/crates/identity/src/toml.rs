//! Full-document TOML 1.0 parsing with the selected tomllib calendar profile.
//! The borrowed view is inert data, not package or retained-input admission.
use ::toml::de::{DeArray, DeTable, DeValue};
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
/// Borrowed array order and elements, with no owner-field interpretation.
#[derive(Clone, Copy)]
pub struct TomlArrayView<'a>(&'a DeArray<'a>);
/// Parser-normalized digits and radix, without narrowing or numeric admission.
/// Digits are from_str_radix-compatible, not the original source spelling.
#[derive(Clone, Copy)]
pub struct TomlIntegerView<'a> {
    digits: &'a str,
    radix: u32,
}
impl<'a> TomlIntegerView<'a> {
    pub fn digits(self) -> &'a str {
        self.digits
    }
    pub fn radix(self) -> u32 {
        self.radix
    }
}
impl<'a> TomlArrayView<'a> {
    pub fn len(self) -> usize {
        self.0.len()
    }
    pub fn is_empty(self) -> bool {
        self.0.is_empty()
    }
    pub fn get(self, index: usize) -> Option<TomlValueView<'a>> {
        self.0
            .get(index)
            .map(|value| TomlValueView(value.get_ref()))
    }
    pub fn iter(self) -> impl ExactSizeIterator<Item = TomlValueView<'a>> + 'a {
        self.0.iter().map(|value| TomlValueView(value.get_ref()))
    }
}

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
    pub fn len(self) -> usize {
        self.0.len()
    }
    pub fn is_empty(self) -> bool {
        self.0.is_empty()
    }
    /// Every key and value, in source order: by the start of each key's
    /// span, which is the order in which the document first defines it.
    pub fn iter(self) -> impl Iterator<Item = (&'a str, TomlValueView<'a>)> + 'a {
        let mut entries: Vec<_> = self.0.iter().collect();
        entries.sort_by_key(|(key, _)| key.span().start);
        entries
            .into_iter()
            .map(|(key, value)| (key.get_ref().as_ref(), TomlValueView(value.get_ref())))
    }
}
impl<'a> TomlValueView<'a> {
    pub fn as_array(self) -> Option<TomlArrayView<'a>> {
        self.0.as_array().map(TomlArrayView)
    }
    pub fn as_integer(self) -> Option<TomlIntegerView<'a>> {
        self.0.as_integer().map(|value| TomlIntegerView {
            digits: value.as_str(),
            radix: value.radix(),
        })
    }

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

#[cfg(test)]
mod view_tests {
    use super::*;
    use alloc::{format, vec::Vec};

    #[test]
    fn borrowed_package_tables_and_dependency_array_keep_document_order() {
        let doc = parse_toml(b"version=4\n[[package]]\nname='z'\nversion='1.0.0'\ndependencies=['b','a','b']\n[[package]]\nname='a'\nversion='2.0.0'\n").unwrap();
        let version = doc.table().get("version").unwrap().as_integer().unwrap();
        assert_eq!((version.digits(), version.radix()), ("4", 10));
        let packages = doc.table().get("package").unwrap().as_array().unwrap();
        assert_eq!(packages.len(), 2);
        let names: Vec<_> = packages
            .iter()
            .map(|v| v.as_table().unwrap().get("name").unwrap().as_str().unwrap())
            .collect();
        assert_eq!(names, ["z", "a"]);
        let dependencies = packages
            .get(0)
            .unwrap()
            .as_table()
            .unwrap()
            .get("dependencies")
            .unwrap()
            .as_array()
            .unwrap();
        assert_eq!(
            dependencies
                .iter()
                .map(|v| v.as_str().unwrap())
                .collect::<Vec<_>>(),
            ["b", "a", "b"]
        );
        assert!(packages.get(2).is_none());
        assert!(packages.get(usize::MAX).is_none());
    }
    #[test]
    fn array_views_keep_nested_arrays_tables_and_empty_arrays_distinct() {
        let doc = parse_toml(b"v=[[],[1],{items=['x']}]\n").unwrap();
        let v = doc.table().get("v").unwrap().as_array().unwrap();
        let empty = v.get(0).unwrap().as_array().unwrap();
        assert!(empty.is_empty());
        assert_eq!(empty.len(), 0);
        assert_eq!(empty.iter().len(), 0);
        assert!(empty.get(0).is_none());
        assert_eq!(
            v.get(1)
                .unwrap()
                .as_array()
                .unwrap()
                .get(0)
                .unwrap()
                .as_integer()
                .unwrap()
                .digits(),
            "1"
        );
        assert_eq!(
            v.get(2)
                .unwrap()
                .as_table()
                .unwrap()
                .get("items")
                .unwrap()
                .as_array()
                .unwrap()
                .get(0)
                .unwrap()
                .as_str(),
            Some("x")
        );
    }
    #[test]
    fn wrong_toml_types_do_not_coerce_into_arrays_or_integers() {
        let doc = parse_toml(b"v=['3',3,3.0,true,{v=3},[3],1979-05-27]\n").unwrap();
        let v = doc.table().get("v").unwrap().as_array().unwrap();
        for i in [0, 2, 3, 4, 5, 6] {
            assert!(v.get(i).unwrap().as_integer().is_none());
        }
        for i in [0, 1, 2, 3, 4, 6] {
            assert!(v.get(i).unwrap().as_array().is_none());
        }
        assert_eq!(v.get(1).unwrap().as_integer().unwrap().digits(), "3");
        assert_eq!(v.get(5).unwrap().as_array().unwrap().len(), 1);
    }
    #[test]
    fn integer_parts_preserve_sign_value_and_radix_without_source_spelling_claims() {
        for (literal, expected, radix) in [
            ("3", 3, 10),
            ("+3", 3, 10),
            ("-3", -3, 10),
            ("0x3", 3, 16),
            ("0o3", 3, 8),
            ("0b11", 3, 2),
            ("3_000", 3000, 10),
            ("0xCA_FE", 51966, 16),
        ] {
            let raw = format!("v={literal}\n");
            let doc = parse_toml(raw.as_bytes()).unwrap();
            let value = doc.table().get("v").unwrap().as_integer().unwrap();
            assert_eq!(value.radix(), radix);
            assert_eq!(
                i128::from_str_radix(value.digits(), value.radix()).unwrap(),
                expected
            );
        }
    }
    #[test]
    fn oversized_integer_views_do_not_narrow_or_reject_the_document() {
        let decimal = "340282366920938463463374607431768211456";
        let raw = format!("v=[{decimal},-{decimal},0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF]\n");
        let doc = parse_toml(raw.as_bytes()).unwrap();
        let v = doc.table().get("v").unwrap().as_array().unwrap();
        let positive = v.get(0).unwrap().as_integer().unwrap();
        assert_eq!(positive.digits(), decimal);
        assert!(u128::from_str_radix(positive.digits(), positive.radix()).is_err());
        let negative = v.get(1).unwrap().as_integer().unwrap();
        assert_eq!(negative.digits(), format!("-{decimal}"));
        assert!(i128::from_str_radix(negative.digits(), negative.radix()).is_err());
        let hex = v.get(2).unwrap().as_integer().unwrap();
        assert_eq!(hex.radix(), 16);
        assert!(u128::from_str_radix(hex.digits(), hex.radix()).is_err());
    }
    #[test]
    fn array_access_requires_complete_document_parse_without_recovery() {
        for raw in [
            b"v=[1,2]\nbroken=[".as_slice(),
            b"v=[1,2]\nv=[3]",
            b"v=[0x]",
            b"v=[1]\ninvalid=1979-05-27T07:32:60Z",
        ] {
            assert!(matches!(parse_toml(raw), Err(TomlError::Syntax)));
        }
    }
    #[test]
    fn iterator_is_repeatable_and_keeps_exact_remaining_length() {
        let doc = parse_toml(b"v=[0,1,2]\n").unwrap();
        let v = doc.table().get("v").unwrap().as_array().unwrap();
        let mut iter = v.iter();
        assert_eq!(iter.len(), 3);
        assert_eq!(iter.next().unwrap().as_integer().unwrap().digits(), "0");
        assert_eq!(iter.len(), 2);
        assert_eq!(v.iter().count(), 3);
        assert_eq!(iter.next().unwrap().as_integer().unwrap().digits(), "1");
        assert_eq!(iter.next().unwrap().as_integer().unwrap().digits(), "2");
        assert_eq!(iter.len(), 0);
        assert!(iter.next().is_none());
    }
}
