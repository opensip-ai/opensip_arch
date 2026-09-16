//! Raw blob hashing and the product H preimage; neither implies admission.
use crate::canonical::{self, Value};
use alloc::{string::String, vec::Vec};
use core::fmt::{self, Write};
use sha2_const_stable::Sha256;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Error {
    Domain,
    FramePrefix,
    FrameDomain,
    FrameLength,
    FrameNoncanonical,
    Canonical(canonical::Error),
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Domain => f.write_str("invalid hash domain"),
            Self::FramePrefix => f.write_str("invalid hash frame prefix"),
            Self::FrameDomain => f.write_str("hash frame domain differs from expected domain"),
            Self::FrameLength => f.write_str("hash frame payload length differs"),
            Self::FrameNoncanonical => f.write_str("hash frame payload is not canonical"),
            Self::Canonical(error) => write!(f, "canonical encoding failed: {error}"),
        }
    }
}

impl core::error::Error for Error {
    fn source(&self) -> Option<&(dyn core::error::Error + 'static)> {
        match self {
            Self::Canonical(error) => Some(error),
            _ => None,
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
    validate_domain(domain)?;
    let canonical = canonical::encode(value).map_err(Error::Canonical)?;
    let mut frame = Vec::new();
    frame.extend_from_slice(FRAME_PREFIX);
    frame.extend_from_slice(domain.as_bytes());
    frame.push(0);
    frame.extend_from_slice(&(canonical.len() as u64).to_be_bytes());
    frame.extend_from_slice(&canonical);
    Ok(frame)
}

pub fn identity(domain: &str, value: &Value) -> Result<[u8; 32], Error> {
    Ok(raw_sha256(&frame(domain, value)?))
}

const FRAME_PREFIX: &[u8] = b"opensip.product.v1\0";

fn validate_domain(domain: &str) -> Result<(), Error> {
    if domain.is_empty()
        || !domain
            .bytes()
            .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || matches!(b, b'-' | b'.'))
    {
        return Err(Error::Domain);
    }
    Ok(())
}

/// Decode an exact H preimage for a separately selected expected domain.
///
/// This checks framing, exact JSON admission and canonical payload bytes. The
/// caller must select the registered domain from its trusted contract, verify
/// the retained blob's digest, and admit the descriptor schema and semantic
/// joins separately. Success is neither a registered descriptor nor a Run.
/// The expected domain is never inferred from the supplied frame.
pub fn unframe(expected_domain: &str, frame: &[u8]) -> Result<Value, Error> {
    validate_domain(expected_domain)?;
    let body = frame.strip_prefix(FRAME_PREFIX).ok_or(Error::FramePrefix)?;
    let body = body
        .strip_prefix(expected_domain.as_bytes())
        .and_then(|rest| rest.strip_prefix(b"\0"))
        .ok_or(Error::FrameDomain)?;
    let length = body.get(..8).ok_or(Error::FrameLength)?;
    let declared = u64::from_be_bytes(length.try_into().expect("exact eight-byte slice"));
    let payload = &body[8..];
    if u64::try_from(payload.len()).ok() != Some(declared) {
        return Err(Error::FrameLength);
    }
    let value = canonical::parse(payload).map_err(Error::Canonical)?;
    if canonical::encode(&value).map_err(Error::Canonical)? != payload {
        return Err(Error::FrameNoncanonical);
    }
    Ok(value)
}
