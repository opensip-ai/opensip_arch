use super::{ArchiveConsumer, DecodeError, ProfileError, gzip_checksum::GzipChecksum, tar::Framer};
use miniz_oxide::inflate::{
    TINFLStatus,
    core::{DecompressorOxide, decompress_with_limit, inflate_flags::TINFL_FLAG_HAS_MORE_INPUT},
};
use opensip_identity::RawSha256;
use std::io::{self, Read};

struct Input<R> {
    reader: R,
    buffer: [u8; 4096],
    at: usize,
    end: usize,
    eof: bool,
    consumed: u64,
    sha256: Option<RawSha256>,
}

impl<R: Read> Input<R> {
    fn new(reader: R) -> Self {
        Self {
            reader,
            buffer: [0; 4096],
            at: 0,
            end: 0,
            eof: false,
            consumed: 0,
            sha256: Some(RawSha256::new()),
        }
    }

    fn refill<E>(
        &mut self,
        check: &mut impl FnMut() -> Result<(), E>,
    ) -> Result<(), DecodeError<E>> {
        if self.at != self.end || self.eof {
            return Ok(());
        }
        loop {
            check().map_err(DecodeError::Consumer)?;
            match self.reader.read(&mut self.buffer) {
                Ok(n) => {
                    if n > self.buffer.len() {
                        return Err(DecodeError::Invariant);
                    }
                    let digest = self.sha256.take().ok_or(DecodeError::Invariant)?;
                    self.sha256 = Some(
                        digest
                            .update(&self.buffer[..n])
                            .map_err(|_| DecodeError::HashLength)?,
                    );
                    self.at = 0;
                    self.end = n;
                    self.eof = n == 0;
                    return Ok(());
                }
                Err(error) if error.kind() == io::ErrorKind::Interrupted => {}
                Err(error) => return Err(DecodeError::Io(error)),
            }
        }
    }

    fn byte<E>(
        &mut self,
        check: &mut impl FnMut() -> Result<(), E>,
    ) -> Result<Option<u8>, DecodeError<E>> {
        self.refill(check)?;
        if self.at == self.end {
            return Ok(None);
        }
        let byte = self.buffer[self.at];
        self.at += 1;
        self.consumed = self
            .consumed
            .checked_add(1)
            .ok_or(DecodeError::CounterOverflow)?;
        Ok(Some(byte))
    }

    fn required<E>(
        &mut self,
        check: &mut impl FnMut() -> Result<(), E>,
    ) -> Result<u8, DecodeError<E>> {
        self.byte(check)?
            .ok_or(DecodeError::Profile(ProfileError::TruncatedGzip))
    }
}

pub(super) struct Report {
    pub(super) sha256: [u8; 32],
    pub(super) compressed_bytes: u64,
    pub(super) inflated_bytes: u128,
}

fn ratio<E>(compressed: u64, inflated: u128) -> Result<(), DecodeError<E>> {
    let left = u128::from(compressed) * 100;
    let right = inflated
        .checked_mul(101)
        .and_then(|n| n.checked_add(100 * 1_048_576))
        .ok_or(DecodeError::CounterOverflow)?;
    if left > right {
        Err(DecodeError::Profile(ProfileError::CompressedBound))
    } else {
        Ok(())
    }
}

pub(super) fn decode<R: Read, C: ArchiveConsumer>(
    reader: R,
    tar: &mut Framer<'_, C>,
) -> Result<Report, DecodeError<C::Error>> {
    let mut input = Input::new(reader);
    let mut header = [0; 10];
    for byte in &mut header {
        *byte = input.required(&mut || tar.checkpoint())?;
    }
    if header[..3] != [0x1f, 0x8b, 8] || header[3] & !9 != 0 {
        return Err(DecodeError::Profile(ProfileError::GzipHeader));
    }
    if header[3] & 8 != 0 {
        let mut terminated = false;
        // C3FN-1: count the entire on-wire field, including its NUL.
        for _ in 0..4096 {
            if input.required(&mut || tar.checkpoint())? == 0 {
                terminated = true;
                break;
            }
        }
        if !terminated {
            return Err(DecodeError::Profile(ProfileError::FnameBound));
        }
    }
    ratio(input.consumed, 0)?;
    let mut decoder = DecompressorOxide::new();
    let mut ring = [0; 32768];
    let mut offset = 0;
    let mut inflated = 0_u128;
    let mut checksum = GzipChecksum::new();
    loop {
        tar.checkpoint().map_err(DecodeError::Consumer)?;
        input.refill(&mut || tar.checkpoint())?;
        let flags = if input.eof {
            0
        } else {
            TINFL_FLAG_HAS_MORE_INPUT
        };
        let available_output = ring.len() - offset;
        let (status, used, made) = decompress_with_limit(
            &mut decoder,
            &input.buffer[input.at..input.end],
            &mut ring,
            offset,
            available_output,
            flags,
        );
        if used > input.end - input.at || made > available_output {
            return Err(DecodeError::Invariant);
        }
        input.at += used;
        input.consumed = input
            .consumed
            .checked_add(used as u64)
            .ok_or(DecodeError::CounterOverflow)?;
        inflated = inflated
            .checked_add(made as u128)
            .ok_or(DecodeError::CounterOverflow)?;
        ratio(input.consumed, inflated)?;
        let bytes = &ring[offset..offset + made];
        checksum.update(bytes);
        tar.feed(bytes)?;
        offset = (offset + made) % ring.len();
        match status {
            TINFLStatus::Done => break,
            TINFLStatus::NeedsMoreInput | TINFLStatus::HasMoreOutput if used != 0 || made != 0 => {}
            _ => return Err(DecodeError::Profile(ProfileError::Deflate)),
        }
    }
    let mut trailer = [0; 8];
    for byte in &mut trailer {
        *byte = input.required(&mut || tar.checkpoint())?;
        ratio(input.consumed, inflated)?;
    }
    if trailer != checksum.trailer() {
        return Err(DecodeError::Profile(ProfileError::GzipTrailer));
    }
    let compressed_bytes = input.consumed;
    if input.byte(&mut || tar.checkpoint())?.is_some() {
        return Err(DecodeError::Profile(ProfileError::GzipTail));
    }
    let digest = input.sha256.take().ok_or(DecodeError::Invariant)?;
    if digest.byte_length() != compressed_bytes {
        return Err(DecodeError::Invariant);
    }
    Ok(Report {
        sha256: RawSha256::finish(digest),
        compressed_bytes,
        inflated_bytes: inflated,
    })
}
