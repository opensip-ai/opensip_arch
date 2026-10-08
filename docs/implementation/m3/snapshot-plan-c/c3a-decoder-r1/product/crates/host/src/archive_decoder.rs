//! Complete CRATE-ARCHIVE-1 byte decoder, library only.
//!
//! Output and callbacks are provisional data. They establish no source custody,
//! admission, owner, import, native context or permission. A caller must quarantine
//! content until the complete decoder, raw checksum and owning custody checks pass.

use opensip_identity::LogicalPath;
use std::io;

mod gzip;
mod gzip_checksum;
mod tar;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ProfileError {
    TruncatedGzip,
    GzipHeader,
    FnameBound,
    Deflate,
    CompressedBound,
    GzipTrailer,
    GzipTail,
    TarMagic,
    TarChecksum,
    TarSize,
    TarType,
    LongName,
    ControlBound,
    LongChain,
    LongPrefix,
    OrphanLong,
    Path,
    DuplicatePath,
    TarEnd,
    TruncatedTar,
}

#[derive(Debug)]
pub(crate) enum DecodeError<E> {
    Io(io::Error),
    Profile(ProfileError),
    Consumer(E),
    CounterOverflow,
    HashLength,
    Allocation,
    Invariant,
}

#[derive(Debug)]
pub(crate) struct FileRecord {
    pub(crate) path: LogicalPath,
    pub(crate) content_sha256: [u8; 32],
    pub(crate) byte_length: u64,
}

pub(crate) trait ArchiveConsumer {
    type Error;
    /// The owning caller checks cancellation and resource/IO scheduling here.
    fn checkpoint(&mut self) -> Result<(), Self::Error>;
    fn begin(&mut self, path: &LogicalPath, length: u128) -> Result<(), Self::Error>;
    fn content(&mut self, bytes: &[u8]) -> Result<(), Self::Error>;
    fn end(&mut self, file: &FileRecord) -> Result<(), Self::Error>;
}

#[derive(Debug)]
pub(crate) struct DecodedArchive {
    pub(crate) compressed_sha256: [u8; 32],
    pub(crate) compressed_bytes: u64,
    pub(crate) inflated_bytes: u128,
    pub(crate) content_bytes: u128,
    pub(crate) files: Vec<FileRecord>,
}

/// Decode one complete member; the result is data, never a source capability.
/// Package name/version are the exact original lock-row spelling supplied by the
/// owning importer. This helper cannot authenticate that association.
pub(crate) fn decode<R: io::Read, C: ArchiveConsumer>(
    reader: R,
    package_name: &str,
    package_version: &str,
    consumer: &mut C,
) -> Result<DecodedArchive, DecodeError<C::Error>> {
    let mut tar = tar::Framer::new(package_name, package_version, consumer);
    let gzip = gzip::decode(reader, &mut tar)?;
    let (files, content_bytes, inflated_bytes) = tar.complete()?;
    if inflated_bytes != gzip.inflated_bytes {
        return Err(DecodeError::Invariant);
    }
    Ok(DecodedArchive {
        compressed_sha256: gzip.sha256,
        compressed_bytes: gzip.compressed_bytes,
        inflated_bytes,
        content_bytes,
        files,
    })
}

#[cfg(test)]
mod tests;
