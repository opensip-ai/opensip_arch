//! Incremental raw SHA-256 over explicitly supplied bytes.
//!
//! Chunk boundaries enter no preimage. This value proves no filesystem read,
//! custody, completeness, provenance, canonical encoding or descriptor admission.
use sha2_const_stable::Sha256;

/// Largest byte-aligned message below SHA-256's 2^64-bit message limit.
const MAX_MESSAGE_BYTES: u64 = u64::MAX / 8;

/// A stream exceeded SHA-256's message-length domain.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct RawSha256LengthError;

impl core::fmt::Display for RawSha256LengthError {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        f.write_str("raw SHA-256 message exceeds its bit-length domain")
    }
}
impl core::error::Error for RawSha256LengthError {}

/// A constant-space raw SHA-256 accumulator, with no admission authority.
///
/// Updates consume the previous value. A refused update yields no accumulator
/// that could accidentally finish a truncated prefix as a successful stream.
/// Source readers must separately prove whole-read success and custody before
/// using its digest for an admission; this API performs no reads itself.
#[must_use]
pub struct RawSha256 {
    state: Sha256,
    byte_length: u64,
}

impl RawSha256 {
    pub fn new() -> Self {
        Self {
            state: Sha256::new(),
            byte_length: 0,
        }
    }

    /// Append exactly these bytes, without framing or canonicalization.
    pub fn update(self, bytes: &[u8]) -> Result<Self, RawSha256LengthError> {
        let added = u64::try_from(bytes.len()).map_err(|_| RawSha256LengthError)?;
        let byte_length = self
            .byte_length
            .checked_add(added)
            .filter(|&total| total <= MAX_MESSAGE_BYTES)
            .ok_or(RawSha256LengthError)?;
        Ok(Self {
            state: self.state.update(bytes),
            byte_length,
        })
    }

    /// Number of bytes successfully included in the raw preimage.
    pub fn byte_length(&self) -> u64 {
        self.byte_length
    }

    /// Finish the raw digest. This does not attest that an input read completed.
    pub fn finish(self) -> [u8; 32] {
        self.state.finalize()
    }
}

impl Default for RawSha256 {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
#[path = "streaming_digest_tests.rs"]
mod tests;
