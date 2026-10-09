//! Whole supplied-stream raw copying and hashing, plain data only.
//!
//! Successful Read EOF, acknowledged writes and flush do not prove a stable
//! named source, OS custody, durability, CAS admission or checksum authenticity.
//! Caller owns source-attempt charging before intake and retained-source joins.

use opensip_identity::{RawSha256, RawSha256LengthError};
use std::io::{self, Read, Write};

pub(crate) trait CopyCheckpoint {
    type Error;
    /// Caller checks cancellation and its actual read/write/work/resource scope.
    fn checkpoint(&mut self) -> Result<(), Self::Error>;
}

#[derive(Debug)]
pub(crate) enum CopyError<E> {
    Owner(E),
    Read(io::Error),
    Write(io::Error),
    InvalidReadCount,
    InvalidWriteCount,
    NoWriteProgress,
    HashLength(RawSha256LengthError),
}

/// Values computed from this actual supplied stream, never an admission witness.
#[derive(Debug)]
pub(crate) struct CopiedRaw {
    pub(crate) byte_length: u64,
    pub(crate) sha256: [u8; 32],
}

/// Copy every actually read byte in order. No successful summary on any failure.
/// Writer bytes remain provisional, including prefixes left on a refused copy.
/// No arbitrary source-size allowance or inferred filesystem completion is added.
pub(crate) fn copy_raw<R: Read, W: Write, C: CopyCheckpoint>(
    mut reader: R,
    writer: &mut W,
    checkpoint: &mut C,
) -> Result<CopiedRaw, CopyError<C::Error>> {
    let mut buffer = [0_u8; 4096];
    let mut digest = RawSha256::new();
    loop {
        checkpoint.checkpoint().map_err(CopyError::Owner)?;
        let count = match reader.read(&mut buffer) {
            Ok(count) => count,
            Err(error) if error.kind() == io::ErrorKind::Interrupted => continue,
            Err(error) => return Err(CopyError::Read(error)),
        };
        if count > buffer.len() {
            return Err(CopyError::InvalidReadCount);
        }
        if count == 0 {
            break;
        }
        digest = digest
            .update(&buffer[..count])
            .map_err(CopyError::HashLength)?;
        let mut written = 0;
        while written < count {
            checkpoint.checkpoint().map_err(CopyError::Owner)?;
            let added = match writer.write(&buffer[written..count]) {
                Ok(added) => added,
                Err(error) if error.kind() == io::ErrorKind::Interrupted => continue,
                Err(error) => return Err(CopyError::Write(error)),
            };
            if added > count - written {
                return Err(CopyError::InvalidWriteCount);
            }
            if added == 0 {
                return Err(CopyError::NoWriteProgress);
            }
            written += added;
        }
    }
    loop {
        checkpoint.checkpoint().map_err(CopyError::Owner)?;
        match writer.flush() {
            Ok(()) => break,
            Err(error) if error.kind() == io::ErrorKind::Interrupted => continue,
            Err(error) => return Err(CopyError::Write(error)),
        }
    }
    let byte_length = digest.byte_length();
    Ok(CopiedRaw {
        byte_length,
        sha256: RawSha256::finish(digest),
    })
}

#[cfg(test)]
#[path = "raw_stream_copy_tests.rs"]
mod tests;
