//! CVE1 committed capability-manifest value codec. This is not C JSON, an H
//! preimage codec, relation payload CBOR, or capability semantic admission.
use crate::{JsonInteger, JsonValue as V};
use alloc::{collections::BTreeMap, string::String, vec::Vec};
pub const MAX_COLLECTION_ITEMS: usize = 1 << 20;
pub const MAX_NESTING: usize = 64;
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Error {
    Truncated,
    TrailingBytes,
    Tag,
    NegativeRange,
    Utf8,
    NotNfc,
    MapKey,
    MapOrder,
    CountBound,
    DepthBound,
    LengthBound,
}
/// Decode exactly one value under the inherited CVE1 limits. Values are inert.
pub fn decode(raw: &[u8]) -> Result<V, Error> {
    let mut reader = Reader { raw, offset: 0 };
    let value = reader.value(0)?;
    if reader.offset != raw.len() {
        return Err(Error::TrailingBytes);
    }
    Ok(value)
}
struct Reader<'a> {
    raw: &'a [u8],
    offset: usize,
}
impl<'a> Reader<'a> {
    fn take(&mut self, n: usize) -> Result<&'a [u8], Error> {
        let end = self.offset.checked_add(n).ok_or(Error::Truncated)?;
        let chunk = self.raw.get(self.offset..end).ok_or(Error::Truncated)?;
        self.offset = end;
        Ok(chunk)
    }
    fn u32(&mut self) -> Result<u32, Error> {
        let bytes = self.take(4)?;
        Ok(u32::from_be_bytes(
            bytes.try_into().map_err(|_| Error::Truncated)?,
        ))
    }
    fn value(&mut self, depth: usize) -> Result<V, Error> {
        if depth > MAX_NESTING {
            return Err(Error::DepthBound);
        }
        match self.take(1)?[0] {
            0 => Ok(V::Null),
            1 => Ok(V::Bool(false)),
            2 => Ok(V::Bool(true)),
            tag @ (3 | 7) => {
                let number =
                    u64::from_be_bytes(self.take(8)?.try_into().map_err(|_| Error::Truncated)?);
                let value = if tag == 3 {
                    number as i128
                } else {
                    if number < (1 << 63) {
                        return Err(Error::NegativeRange);
                    }
                    number as i128 - (1i128 << 64)
                };
                Ok(V::Integer(
                    JsonInteger::new(value).map_err(|_| Error::NegativeRange)?,
                ))
            }
            4 => {
                let length = self.u32()? as usize;
                let text = core::str::from_utf8(self.take(length)?).map_err(|_| Error::Utf8)?;
                if !unicode_normalization::is_nfc(text) {
                    return Err(Error::NotNfc);
                }
                Ok(V::String(String::from(text)))
            }
            tag @ (5 | 6) => {
                let count = self.u32()? as usize;
                if count > MAX_COLLECTION_ITEMS {
                    return Err(Error::CountBound);
                }
                if tag == 5 {
                    let mut values = Vec::new();
                    for _ in 0..count {
                        values.push(self.value(depth + 1)?)
                    }
                    Ok(V::Array(values))
                } else {
                    let mut values = BTreeMap::new();
                    let mut previous: Option<String> = None;
                    for _ in 0..count {
                        let V::String(key) = self.value(depth + 1)? else {
                            return Err(Error::MapKey);
                        };
                        if previous
                            .as_ref()
                            .is_some_and(|p| p.as_bytes() >= key.as_bytes())
                        {
                            return Err(Error::MapOrder);
                        }
                        previous = Some(key.clone());
                        let value = self.value(depth + 1)?;
                        values.insert(key, value);
                    }
                    Ok(V::Object(values))
                }
            }
            _ => Err(Error::Tag),
        }
    }
}
/// Canonical CVE1 for values within the decoder's admitted limits. Bounds are
/// checked on output too; an unconsumable over-depth value is not emitted.
pub fn encode(value: &V) -> Result<Vec<u8>, Error> {
    let mut out = Vec::new();
    write(value, &mut out, 0)?;
    Ok(out)
}
fn count(out: &mut Vec<u8>, length: usize) -> Result<(), Error> {
    if length > MAX_COLLECTION_ITEMS {
        return Err(Error::CountBound);
    }
    out.extend_from_slice(&(length as u32).to_be_bytes());
    Ok(())
}
fn string(s: &str, out: &mut Vec<u8>) -> Result<(), Error> {
    if !unicode_normalization::is_nfc(s) {
        return Err(Error::NotNfc);
    }
    let length = u32::try_from(s.len()).map_err(|_| Error::LengthBound)?;
    out.push(4);
    out.extend_from_slice(&length.to_be_bytes());
    out.extend_from_slice(s.as_bytes());
    Ok(())
}
fn write(value: &V, out: &mut Vec<u8>, depth: usize) -> Result<(), Error> {
    if depth > MAX_NESTING {
        return Err(Error::DepthBound);
    }
    match value {
        V::Null => out.push(0),
        V::Bool(false) => out.push(1),
        V::Bool(true) => out.push(2),
        V::Integer(n) => {
            let n = n.get();
            out.push(if n < 0 { 7 } else { 3 });
            let bits = if n < 0 {
                (n + (1i128 << 64)) as u64
            } else {
                n as u64
            };
            out.extend_from_slice(&bits.to_be_bytes());
        }
        V::String(s) => string(s, out)?,
        V::Array(a) => {
            out.push(5);
            count(out, a.len())?;
            for v in a {
                write(v, out, depth + 1)?
            }
        }
        V::Object(o) => {
            out.push(6);
            count(out, o.len())?;
            for (k, v) in o {
                if depth + 1 > MAX_NESTING {
                    return Err(Error::DepthBound);
                }
                string(k, out)?;
                write(v, out, depth + 1)?
            }
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use alloc::vec;
    #[test]
    fn types_and_integer_boundaries_have_distinct_tags() {
        let cases = [
            (V::Null, vec![0]),
            (V::Bool(false), vec![1]),
            (V::Bool(true), vec![2]),
            (
                V::Integer(JsonInteger::new(0).unwrap()),
                vec![3, 0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                V::Integer(JsonInteger::new(-1).unwrap()),
                vec![7, 255, 255, 255, 255, 255, 255, 255, 255],
            ),
            (
                V::Integer(JsonInteger::new(-(1i128 << 63)).unwrap()),
                vec![7, 128, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                V::Integer(JsonInteger::new((1i128 << 64) - 1).unwrap()),
                vec![3, 255, 255, 255, 255, 255, 255, 255, 255],
            ),
        ];
        for (value, raw) in cases {
            assert_eq!(encode(&value).unwrap(), raw);
            assert_eq!(decode(&raw).unwrap(), value);
        }
        assert_eq!(
            decode(&[7, 0, 0, 0, 0, 0, 0, 0, 1]),
            Err(Error::NegativeRange)
        );
    }
    #[test]
    fn malformed_bytes_never_get_repaired() {
        for (raw, error) in [
            (vec![], Error::Truncated),
            (vec![3, 0], Error::Truncated),
            (vec![0, 0], Error::TrailingBytes),
            (vec![255], Error::Tag),
            (vec![4, 0, 0, 0, 1, 255], Error::Utf8),
            (vec![4, 0, 0, 0, 3, b'e', 0xcc, 0x81], Error::NotNfc),
            (vec![6, 0, 0, 0, 1, 0, 0], Error::MapKey),
        ] {
            assert_eq!(decode(&raw), Err(error));
        }
        assert_eq!(encode(&V::String("e\u{301}".into())), Err(Error::NotNfc));
        assert_eq!(
            decode(&[4, 0, 0, 0, 2, 0xc3, 0xa9]).unwrap(),
            V::String("é".into())
        );
    }
    #[test]
    fn depth_and_count_limits_apply_before_allocation_or_recursion() {
        for depth in [63, 64, 65] {
            let mut bytes = Vec::new();
            for _ in 0..depth {
                bytes.extend_from_slice(&[5, 0, 0, 0, 1]);
            }
            bytes.push(0);
            if depth <= 64 {
                let value = decode(&bytes).unwrap();
                assert_eq!(encode(&value).unwrap(), bytes);
            } else {
                assert_eq!(decode(&bytes), Err(Error::DepthBound));
            }
        }
        for tag in [5, 6] {
            assert_eq!(decode(&[tag, 0, 16, 0, 1]), Err(Error::CountBound));
            assert_eq!(decode(&[tag, 0, 16, 0, 0]), Err(Error::Truncated));
        }
    }
    #[test]
    fn map_order_is_unsigned_utf8_and_duplicate_keys_refuse() {
        let mut map = BTreeMap::new();
        map.insert("𝄞".into(), V::Bool(true));
        map.insert("é".into(), V::Null);
        let raw = encode(&V::Object(map.clone())).unwrap();
        assert_eq!(&raw[..12], &[6, 0, 0, 0, 2, 4, 0, 0, 0, 2, 0xc3, 0xa9]);
        assert_eq!(decode(&raw).unwrap(), V::Object(map));
        for keys in [[b'b', b'a'], [b'a', b'a']] {
            let mut raw = vec![6, 0, 0, 0, 2];
            for key in keys {
                raw.extend_from_slice(&[4, 0, 0, 0, 1, key, 0]);
            }
            assert_eq!(decode(&raw), Err(Error::MapOrder));
        }
    }
}
