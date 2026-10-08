use super::{ArchiveConsumer, DecodeError, FileRecord, ProfileError};
use opensip_identity::{LogicalPath, RawSha256};
use std::collections::HashSet;

enum Body {
    Regular {
        left: u128,
        length: u128,
        path: LogicalPath,
        digest: Option<RawSha256>,
    },
    Long {
        left: u128,
        bytes: Vec<u8>,
    },
}
enum Mode {
    Header(usize),
    Body(Body, usize),
    Padding(usize),
    End(usize),
    Failed,
}

pub(super) struct Framer<'a, C: ArchiveConsumer> {
    consumer: &'a mut C,
    prefix: String,
    mode: Mode,
    block: [u8; 512],
    pending: Option<Vec<u8>>,
    seen: HashSet<String>,
    files: Vec<FileRecord>,
    inflated: u128,
    content: u128,
    regular: u128,
    long_records: u128,
}

fn octal(field: &[u8]) -> Option<u128> {
    let start = field.iter().position(|b| !matches!(b, b' ' | 0))?;
    let end = field.iter().rposition(|b| !matches!(b, b' ' | 0))? + 1;
    field[start..end].iter().try_fold(0_u128, |n, &byte| {
        if !(b'0'..=b'7').contains(&byte) {
            return None;
        }
        n.checked_mul(8)?.checked_add(u128::from(byte - b'0'))
    })
}

fn size(field: &[u8; 12]) -> Option<u128> {
    let value = if field[0] & 128 == 0 {
        octal(field)?
    } else {
        if field[0] & 64 != 0 {
            return None;
        }
        let value = field.iter().enumerate().try_fold(0_u128, |n, (i, &byte)| {
            n.checked_mul(256)?
                .checked_add(u128::from(if i == 0 { byte & 127 } else { byte }))
        })?;
        // MC8: GNU base-256 only above the twelve-byte field's octal range.
        if value < (1_u128 << 33) {
            return None;
        }
        value
    };
    Some(value)
}

fn name(field: &[u8]) -> &[u8] {
    &field[..field
        .iter()
        .position(|byte| *byte == 0)
        .unwrap_or(field.len())]
}

impl<'a, C: ArchiveConsumer> Framer<'a, C> {
    pub(super) fn new(package_name: &str, package_version: &str, consumer: &'a mut C) -> Self {
        Self {
            consumer,
            prefix: format!("{package_name}-{package_version}/"),
            mode: Mode::Header(0),
            block: [0; 512],
            pending: None,
            seen: HashSet::new(),
            files: Vec::new(),
            inflated: 0,
            content: 0,
            regular: 0,
            long_records: 0,
        }
    }

    pub(super) fn checkpoint(&mut self) -> Result<(), C::Error> {
        self.consumer.checkpoint()
    }

    fn account(
        &mut self,
        count: usize,
        regular_content: bool,
    ) -> Result<(), DecodeError<C::Error>> {
        self.inflated = self
            .inflated
            .checked_add(count as u128)
            .ok_or(DecodeError::CounterOverflow)?;
        if regular_content {
            self.content = self
                .content
                .checked_add(count as u128)
                .ok_or(DecodeError::CounterOverflow)?;
        }
        let allowance = self
            .regular
            .checked_add(1)
            .and_then(|n| n.checked_mul(18_432))
            .and_then(|n| n.checked_add(10_240))
            .ok_or(DecodeError::CounterOverflow)?;
        let framing = self
            .inflated
            .checked_sub(self.content)
            .ok_or(DecodeError::Invariant)?;
        // D1 cannot cross alone under the selected shape/end/long-record rules.
        // The rule causing a profile breach is checked before this consistency guard.
        if framing > allowance {
            return Err(DecodeError::Invariant);
        }
        Ok(())
    }

    fn header(&mut self, header: [u8; 512]) -> Result<Mode, DecodeError<C::Error>> {
        if header.iter().all(|byte| *byte == 0) {
            if self.pending.is_some() {
                return Err(DecodeError::Profile(ProfileError::OrphanLong));
            }
            return Ok(Mode::End(512));
        }
        if &header[257..265] != b"ustar  \0" {
            return Err(DecodeError::Profile(ProfileError::TarMagic));
        }
        let sum = header
            .iter()
            .enumerate()
            .map(|(index, &byte)| {
                u128::from(if (148..156).contains(&index) {
                    b' '
                } else {
                    byte
                })
            })
            .sum::<u128>();
        if octal(&header[148..156]) != Some(sum) {
            return Err(DecodeError::Profile(ProfileError::TarChecksum));
        }
        let field: &[u8; 12] = header[124..136]
            .try_into()
            .map_err(|_| DecodeError::Invariant)?;
        let length = size(field).ok_or(DecodeError::Profile(ProfileError::TarSize))?;
        let padding = ((512 - length % 512) % 512) as usize;
        match header[156] {
            b'0' => {
                let effective = if let Some(long) = self.pending.take() {
                    if !long.starts_with(name(&header[..100])) {
                        return Err(DecodeError::Profile(ProfileError::LongPrefix));
                    }
                    long
                } else {
                    name(&header[..100]).to_vec()
                };
                let text = std::str::from_utf8(&effective)
                    .map_err(|_| DecodeError::Profile(ProfileError::Path))?;
                let relative = text
                    .strip_prefix(&self.prefix)
                    .ok_or(DecodeError::Profile(ProfileError::Path))?;
                let path = LogicalPath::parse(relative)
                    .map_err(|_| DecodeError::Profile(ProfileError::Path))?;
                if self.seen.contains(path.as_str()) {
                    return Err(DecodeError::Profile(ProfileError::DuplicatePath));
                }
                self.seen
                    .try_reserve(1)
                    .map_err(|_| DecodeError::Allocation)?;
                self.files
                    .try_reserve(1)
                    .map_err(|_| DecodeError::Allocation)?;
                let mut key = String::new();
                key.try_reserve(path.as_str().len())
                    .map_err(|_| DecodeError::Allocation)?;
                key.push_str(path.as_str());
                self.seen.insert(key);
                self.regular = self
                    .regular
                    .checked_add(1)
                    .ok_or(DecodeError::CounterOverflow)?;
                self.consumer
                    .begin(&path, length)
                    .map_err(DecodeError::Consumer)?;
                Ok(Mode::Body(
                    Body::Regular {
                        left: length,
                        length,
                        path,
                        digest: Some(RawSha256::new()),
                    },
                    padding,
                ))
            }
            b'L' => {
                if self.pending.is_some() {
                    return Err(DecodeError::Profile(ProfileError::LongChain));
                }
                if name(&header[..100]) != b"././@LongLink" || length < 2 {
                    return Err(DecodeError::Profile(ProfileError::LongName));
                }
                if length > 16_385 {
                    return Err(DecodeError::Profile(ProfileError::ControlBound));
                }
                self.long_records = self
                    .long_records
                    .checked_add(1)
                    .ok_or(DecodeError::CounterOverflow)?;
                if self.long_records
                    > self
                        .regular
                        .checked_add(1)
                        .ok_or(DecodeError::CounterOverflow)?
                {
                    return Err(DecodeError::Invariant);
                }
                let mut bytes = Vec::new();
                bytes
                    .try_reserve_exact(length as usize)
                    .map_err(|_| DecodeError::Allocation)?;
                Ok(Mode::Body(
                    Body::Long {
                        left: length,
                        bytes,
                    },
                    padding,
                ))
            }
            _ => Err(DecodeError::Profile(ProfileError::TarType)),
        }
    }

    fn settle(&mut self) -> Result<(), DecodeError<C::Error>> {
        loop {
            let ready = matches!(
                &self.mode,
                Mode::Padding(0)
                    | Mode::Body(Body::Regular { left: 0, .. }, _)
                    | Mode::Body(Body::Long { left: 0, .. }, _)
            );
            if !ready {
                return Ok(());
            }
            let mode = std::mem::replace(&mut self.mode, Mode::Failed);
            self.mode = match mode {
                Mode::Padding(0) => Mode::Header(0),
                Mode::Body(
                    Body::Regular {
                        length,
                        path,
                        mut digest,
                        ..
                    },
                    padding,
                ) => {
                    let digest = digest.take().ok_or(DecodeError::Invariant)?;
                    if u128::from(digest.byte_length()) != length {
                        return Err(DecodeError::Invariant);
                    }
                    let file = FileRecord {
                        path,
                        content_sha256: RawSha256::finish(digest),
                        byte_length: u64::try_from(length)
                            .map_err(|_| DecodeError::CounterOverflow)?,
                    };
                    self.consumer.end(&file).map_err(DecodeError::Consumer)?;
                    self.files.push(file);
                    Mode::Padding(padding)
                }
                Mode::Body(Body::Long { mut bytes, .. }, padding) => {
                    if bytes.last() != Some(&0) || bytes[..bytes.len() - 1].contains(&0) {
                        return Err(DecodeError::Profile(ProfileError::LongName));
                    }
                    bytes.pop();
                    let text = std::str::from_utf8(&bytes)
                        .map_err(|_| DecodeError::Profile(ProfileError::LongName))?;
                    if text.chars().take(4097).count() > 4096 {
                        return Err(DecodeError::Profile(ProfileError::LongName));
                    }
                    self.pending = Some(bytes);
                    Mode::Padding(padding)
                }
                _ => return Err(DecodeError::Invariant),
            };
        }
    }

    pub(super) fn feed(&mut self, mut bytes: &[u8]) -> Result<(), DecodeError<C::Error>> {
        loop {
            self.settle()?;
            if bytes.is_empty() {
                return Ok(());
            }
            self.checkpoint().map_err(DecodeError::Consumer)?;
            let mode = std::mem::replace(&mut self.mode, Mode::Failed);
            self.mode = match mode {
                Mode::Header(used) => {
                    let count = (512 - used).min(bytes.len());
                    self.block[used..used + count].copy_from_slice(&bytes[..count]);
                    bytes = &bytes[count..];
                    self.account(count, false)?;
                    if used + count == 512 {
                        self.header(self.block)?
                    } else {
                        Mode::Header(used + count)
                    }
                }
                Mode::Body(mut body, padding) => {
                    let (left, regular) = match &body {
                        Body::Regular { left, .. } => (*left, true),
                        Body::Long { left, .. } => (*left, false),
                    };
                    let count = left.min(bytes.len() as u128) as usize;
                    let chunk = &bytes[..count];
                    match &mut body {
                        Body::Regular { left, digest, .. } => {
                            let current = digest.take().ok_or(DecodeError::Invariant)?;
                            *digest =
                                Some(current.update(chunk).map_err(|_| DecodeError::HashLength)?);
                            self.consumer
                                .content(chunk)
                                .map_err(DecodeError::Consumer)?;
                            *left -= count as u128;
                        }
                        Body::Long { left, bytes } => {
                            bytes.extend_from_slice(chunk);
                            *left -= count as u128;
                        }
                    }
                    bytes = &bytes[count..];
                    self.account(count, regular)?;
                    Mode::Body(body, padding)
                }
                Mode::Padding(left) => {
                    let count = left.min(bytes.len());
                    bytes = &bytes[count..];
                    self.account(count, false)?;
                    Mode::Padding(left - count)
                }
                Mode::End(total) => {
                    let count = bytes.len().min(10_241 - total);
                    if total + count > 10_240 || bytes[..count].iter().any(|byte| *byte != 0) {
                        return Err(DecodeError::Profile(ProfileError::TarEnd));
                    }
                    bytes = &bytes[count..];
                    self.account(count, false)?;
                    Mode::End(total + count)
                }
                Mode::Failed => return Err(DecodeError::Invariant),
            };
        }
    }

    pub(super) fn complete(
        mut self,
    ) -> Result<(Vec<FileRecord>, u128, u128), DecodeError<C::Error>> {
        self.settle()?;
        if self.pending.is_some() {
            return Err(DecodeError::Profile(ProfileError::OrphanLong));
        }
        match self.mode {
            Mode::End(bytes) if (1024..=10_240).contains(&bytes) && bytes % 512 == 0 => {}
            Mode::End(_) => return Err(DecodeError::Profile(ProfileError::TarEnd)),
            _ => return Err(DecodeError::Profile(ProfileError::TruncatedTar)),
        }
        if self.files.len() as u128 != self.regular || self.long_records > self.regular {
            return Err(DecodeError::Invariant);
        }
        self.files.sort_by(|left, right| {
            left.path
                .as_str()
                .as_bytes()
                .cmp(right.path.as_str().as_bytes())
        });
        Ok((self.files, self.content, self.inflated))
    }
}
