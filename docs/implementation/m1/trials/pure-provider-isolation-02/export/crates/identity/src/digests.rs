//! Raw blob hashing and the product H preimage; neither implies admission.
use crate::canonical::{self, Value};
use alloc::{string::String, vec::Vec};
use core::fmt::{self, Write};
use sha2_const_stable::Sha256;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Error {
    Domain,
    Canonical(canonical::Error),
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Domain => f.write_str("invalid hash domain"),
            Self::Canonical(error) => write!(f, "canonical encoding failed: {error}"),
        }
    }
}

impl core::error::Error for Error {
    fn source(&self) -> Option<&(dyn core::error::Error + 'static)> {
        match self {
            Self::Canonical(error) => Some(error),
            Self::Domain => None,
        }
    }
}

pub fn raw_sha256(bytes: &[u8]) -> [u8; 32] {
    Sha256::new().update(bytes).finalize()
}

pub fn hex(digest: &[u8; 32]) -> String {
    let mut value = String::with_capacity(64);
    for byte in digest {
        write!(value, "{byte:02x}").expect("writing to String cannot fail");
    }
    value
}

/// Complete H preimage. Callers must separately admit the registered descriptor.
pub fn frame(domain: &str, value: &Value) -> Result<Vec<u8>, Error> {
    if domain.is_empty()
        || !domain
            .bytes()
            .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || matches!(b, b'-' | b'.'))
    {
        return Err(Error::Domain);
    }
    let canonical = canonical::encode(value).map_err(Error::Canonical)?;
    let mut frame = Vec::new();
    frame.extend_from_slice(b"opensip.product.v1\0");
    frame.extend_from_slice(domain.as_bytes());
    frame.push(0);
    frame.extend_from_slice(&(canonical.len() as u64).to_be_bytes());
    frame.extend_from_slice(&canonical);
    Ok(frame)
}

pub fn identity(domain: &str, value: &Value) -> Result<[u8; 32], Error> {
    Ok(raw_sha256(&frame(domain, value)?))
}
