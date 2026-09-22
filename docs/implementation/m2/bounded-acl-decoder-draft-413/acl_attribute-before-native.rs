//! Allocation-free decoding of one bounded native ACL attribute response.
//! All results are claims. NotReturned is unavailable evidence, never empty ACL.

const RETURNED_ATTRS: u32 = 0x8000_0000;
const EXTENDED_SECURITY: u32 = 0x0040_0000;
const FILESEC_MAGIC: u32 = 0x012c_c16d;
const NO_ACL: u32 = u32::MAX;
const MAX_ENTRIES: usize = 128;
const ATTR_SET_END: usize = 24;
const REFERENCE_END: usize = 32;
const FILESEC_HEADER: usize = 44;
const ACE_SIZE: usize = 24;

#[derive(Debug, PartialEq, Eq)]
enum Error {
    Truncated,
    Header,
    UnexpectedAttribute,
    Offset,
    Length,
    Magic,
    Count,
}
#[derive(Debug, PartialEq, Eq)]
enum Attribute<'a> {
    NotReturned,
    Present(Acl<'a>),
}
#[derive(Debug, PartialEq, Eq)]
struct Acl<'a> {
    raw: &'a [u8],
    count: usize,
    explicit_no_acl: bool,
}
#[derive(Debug, PartialEq, Eq)]
struct Ace<'a> {
    qualifier: &'a [u8; 16],
    flags: u32,
    rights: u32,
}
fn word(bytes: &[u8], offset: usize) -> Result<u32, Error> {
    let end = offset.checked_add(4).ok_or(Error::Length)?;
    Ok(u32::from_ne_bytes(
        bytes
            .get(offset..end)
            .ok_or(Error::Truncated)?
            .try_into()
            .map_err(|_| Error::Length)?,
    ))
}
impl<'a> Attribute<'a> {
    // The caller must supply a successful native response made with
    // FSOPT_REPORT_FULLSIZE. This parser cannot prove those native premises.
    fn decode(buffer: &'a [u8]) -> Result<Self, Error> {
        let full = usize::try_from(word(buffer, 0)?).map_err(|_| Error::Length)?;
        if full > buffer.len() {
            return Err(Error::Truncated);
        }
        if full < ATTR_SET_END {
            return Err(Error::Header);
        }
        let bytes = &buffer[..full];
        let common = word(bytes, 4)?;
        if common & RETURNED_ATTRS == 0 || common & !(RETURNED_ATTRS | EXTENDED_SECURITY) != 0 {
            return Err(Error::UnexpectedAttribute);
        }
        for offset in [8, 12, 16, 20] {
            if word(bytes, offset)? != 0 {
                return Err(Error::UnexpectedAttribute);
            }
        }
        if common & EXTENDED_SECURITY == 0 {
            return Ok(Self::NotReturned);
        }
        if full < REFERENCE_END {
            return Err(Error::Truncated);
        }
        let relative = i32::from_ne_bytes(bytes[24..28].try_into().map_err(|_| Error::Length)?);
        let relative = usize::try_from(relative).map_err(|_| Error::Offset)?;
        let start = ATTR_SET_END.checked_add(relative).ok_or(Error::Offset)?;
        if start < REFERENCE_END || start % 4 != 0 {
            return Err(Error::Offset);
        }
        let length = usize::try_from(word(bytes, 28)?).map_err(|_| Error::Length)?;
        let end = start.checked_add(length).ok_or(Error::Length)?;
        let raw = bytes.get(start..end).ok_or(Error::Length)?;
        if raw.len() < FILESEC_HEADER {
            return Err(Error::Length);
        }
        if word(raw, 0)? != FILESEC_MAGIC {
            return Err(Error::Magic);
        }
        let count = word(raw, 36)?;
        let explicit_no_acl = count == NO_ACL;
        let count = if explicit_no_acl {
            0
        } else {
            usize::try_from(count).map_err(|_| Error::Count)?
        };
        if count > MAX_ENTRIES {
            return Err(Error::Count);
        }
        let expected = FILESEC_HEADER
            .checked_add(count.checked_mul(ACE_SIZE).ok_or(Error::Length)?)
            .ok_or(Error::Length)?;
        if raw.len() != expected {
            return Err(Error::Length);
        }
        Ok(Self::Present(Acl {
            raw,
            count,
            explicit_no_acl,
        }))
    }
}
impl<'a> Acl<'a> {
    fn flags(&self) -> u32 {
        word(self.raw, 40).expect("validated fixed header")
    }
    fn entry(&self, index: usize) -> Option<Ace<'a>> {
        if index >= self.count {
            return None;
        }
        // Construction checked count, multiplication and total record length.
        let start = FILESEC_HEADER + index * ACE_SIZE;
        let qualifier = self.raw[start..start + 16].try_into().ok()?;
        Some(Ace {
            qualifier,
            flags: word(self.raw, start + 16).ok()?,
            rights: word(self.raw, start + 20).ok()?,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn put(b: &mut [u8], offset: usize, word: u32) {
        b[offset..offset + 4].copy_from_slice(&word.to_ne_bytes());
    }
    fn fixture(count: usize) -> Vec<u8> {
        let length = FILESEC_HEADER + ACE_SIZE * count;
        let mut b = vec![0; REFERENCE_END + length];
        let size = b.len() as u32;
        put(&mut b, 0, size);
        put(&mut b, 4, RETURNED_ATTRS | EXTENDED_SECURITY);
        put(&mut b, 24, 8);
        put(&mut b, 28, length as u32);
        put(&mut b, 32, FILESEC_MAGIC);
        put(&mut b, 68, count as u32);
        b
    }
    #[test]
    fn one_entry_is_borrowed_without_principal_or_permission_admission() {
        let mut b = fixture(1);
        b[76..92].copy_from_slice(&[7; 16]);
        put(&mut b, 92, 1);
        put(&mut b, 96, 2);
        let Attribute::Present(acl) = Attribute::decode(&b).unwrap() else {
            panic!()
        };
        assert_eq!(acl.count, 1);
        assert!(!acl.explicit_no_acl);
        assert_eq!(acl.flags(), 0);
        let entry = acl.entry(0).unwrap();
        assert_eq!(entry.qualifier, &[7; 16]);
        assert_eq!(entry.flags, 1);
        assert_eq!(entry.rights, 2);
        assert!(std::ptr::eq(entry.qualifier.as_ptr(), b[76..].as_ptr()));
        assert!(acl.entry(1).is_none());
    }
    #[test]
    fn omitted_attribute_is_not_an_explicit_empty_or_no_acl_record() {
        let mut absent = vec![0; 32];
        put(&mut absent, 0, 32);
        put(&mut absent, 4, RETURNED_ATTRS);
        assert_eq!(Attribute::decode(&absent), Ok(Attribute::NotReturned));
        let empty = fixture(0);
        let Attribute::Present(acl) = Attribute::decode(&empty).unwrap() else {
            panic!()
        };
        assert_eq!(acl.count, 0);
        assert!(!acl.explicit_no_acl);
        let mut explicit = fixture(0);
        put(&mut explicit, 68, NO_ACL);
        let Attribute::Present(acl) = Attribute::decode(&explicit).unwrap() else {
            panic!()
        };
        assert!(acl.explicit_no_acl);
    }
    #[test]
    fn full_size_detects_successful_native_truncation_and_ignores_spare_capacity() {
        let b = fixture(1);
        assert_eq!(Attribute::decode(&b[..32]), Err(Error::Truncated));
        let mut oversized = b.clone();
        oversized.extend_from_slice(&[255; 20]);
        assert_eq!(Attribute::decode(&oversized), Attribute::decode(&b));
        for n in 0..b.len() {
            assert!(Attribute::decode(&b[..n]).is_err());
        }
    }
    #[test]
    fn offsets_cannot_point_back_into_headers_outside_response_or_unaligned() {
        for relative in [0, 4, 7, 9, u32::MAX, i32::MAX as u32] {
            let mut b = fixture(1);
            put(&mut b, 24, relative);
            assert!(Attribute::decode(&b).is_err());
        }
        let mut b = fixture(1);
        put(&mut b, 28, u32::MAX);
        assert!(Attribute::decode(&b).is_err());
    }
    #[test]
    fn record_count_magic_and_length_are_bounded_before_entry_access() {
        let max = fixture(128);
        let Attribute::Present(acl) = Attribute::decode(&max).unwrap() else {
            panic!()
        };
        assert_eq!(acl.count, 128);
        assert!(acl.entry(127).is_some());
        assert!(acl.entry(128).is_none());
        assert_eq!(Attribute::decode(&fixture(129)), Err(Error::Count));
        let mut b = fixture(1);
        put(&mut b, 32, 0);
        assert_eq!(Attribute::decode(&b), Err(Error::Magic));
        let mut b = fixture(1);
        put(&mut b, 68, 2);
        assert_eq!(Attribute::decode(&b), Err(Error::Length));
        let mut b = fixture(1);
        put(&mut b, 68, NO_ACL);
        assert_eq!(Attribute::decode(&b), Err(Error::Length));
    }
    #[test]
    fn unexpected_attribute_sets_are_not_misparsed_as_the_fixed_layout() {
        for (offset, value) in [
            (4, EXTENDED_SECURITY),
            (4, RETURNED_ATTRS | EXTENDED_SECURITY | 1),
            (8, 1),
            (12, 1),
            (16, 1),
            (20, 1),
        ] {
            let mut b = fixture(1);
            put(&mut b, offset, value);
            assert_eq!(Attribute::decode(&b), Err(Error::UnexpectedAttribute));
        }
    }
}
