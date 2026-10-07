from pathlib import Path
p=Path('/tmp/opensip-implementation/g2-tar-members-authoring/product/providers/rust/src/dependency_inputs.rs')
s=p.read_text();assert 'pub fn observe_declared_tar_members' not in s
addition=r'''
/// A regular member of caller-declared, already-inflated GNU tar bytes.
/// The content borrows those bytes; no extraction or filesystem path is made.
#[derive(Debug)]
pub struct DeclaredTarMember<'a> {
    path: opensip_identity::LogicalPath,
    content: &'a [u8],
}
impl DeclaredTarMember<'_> {
    pub fn path(&self) -> &str { self.path.as_str() }
    pub fn content(&self) -> &[u8] { self.content }
}
/// Local parser errors, never checksum-mismatch labels or public refusal codes.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DeclaredTarError {
    Truncated,
    Header,
    Checksum,
    Size,
    EntryType,
    LongName,
    Path,
    Duplicate,
    EndRegion,
}

/// Observe profile CRATE-ARCHIVE-1's GNU tar members (C r7 item 12, rules
/// 2-6 and D2) in explicitly supplied inflated bytes. Results become available
/// only after the whole tar stream passes. Paths are sorted and unique; every
/// content slice retains its exact archive bytes. Ignored header metadata and
/// padding never enter this observation.
///
/// This does not prove these are the inflation of a locked .crate preimage.
/// It performs no gzip/header/trailer/CRC/ISIZE/D3 validation, streaming D1
/// guard, acquisition or admitted-set counter check, manifest identity/hash
/// join, materialization, activation, registry/provenance/import admission,
/// or NativeContextVerified/Plan/provider authorization. Those remain the
/// importer and full decoder's duties; M3-L's in-effect gate is unchanged.
pub fn observe_declared_tar_members<'a>(
    name: &str,
    version: &str,
    inflated: &'a [u8],
) -> Result<Vec<DeclaredTarMember<'a>>, DeclaredTarError> {
    use DeclaredTarError as E;
    // Caller supplies the exact lock tuple; it is not a directory or a path.
    let root = format!("{name}-{version}/");
    let mut offset = 0usize;
    let mut pending: Option<&[u8]> = None;
    let mut files = BTreeMap::new();
    loop {
        let header_end = offset.checked_add(512).ok_or(E::Truncated)?;
        let header = inflated.get(offset..header_end).ok_or(E::Truncated)?;
        if header.iter().all(|b| *b == 0) {
            let end = &inflated[offset..];
            if pending.is_some() || !(1024..=10240).contains(&end.len())
                || !end.len().is_multiple_of(512) || end.iter().any(|b| *b != 0) {
                return Err(E::EndRegion);
            }
            return Ok(files.into_values().collect());
        }
        if &header[257..263] != b"ustar " || &header[263..265] != b" \0" {
            return Err(E::Header);
        }
        let checksum = tar_octal(&header[148..156]).ok_or(E::Checksum)?;
        let sum: u64 = header.iter().enumerate().map(|(i,b)| {
            u64::from(if (148..156).contains(&i) { b' ' } else { *b })
        }).sum();
        if checksum != sum { return Err(E::Checksum); }
        let size = tar_size(&header[124..136]).ok_or(E::Size)?;
        let size = usize::try_from(size).map_err(|_| E::Size)?;
        let kind = header[156];
        if pending.is_some() && kind != b'0' { return Err(E::LongName); }
        if kind != b'0' && kind != b'L' { return Err(E::EntryType); }
        // D2 is checked before touching or slicing a long-name payload.
        if kind == b'L' && !(2..=16385).contains(&size) { return Err(E::LongName); }
        let content_end = header_end.checked_add(size).ok_or(E::Size)?;
        let content = inflated.get(header_end..content_end).ok_or(E::Truncated)?;
        let padding = (512 - size % 512) % 512;
        offset = content_end.checked_add(padding).ok_or(E::Size)?;
        if offset > inflated.len() { return Err(E::Truncated); }
        let header_name = tar_name(&header[..100]);
        if kind == b'L' {
            if header_name != b"././@LongLink" || content.last() != Some(&0)
                || content[..size-1].contains(&0) {
                return Err(E::LongName);
            }
            let path = &content[..size-1];
            let path_text = std::str::from_utf8(path).map_err(|_| E::Path)?;
            if path_text.chars().take(4097).count() > 4096 { return Err(E::LongName); }
            pending = Some(path);
            continue;
        }
        let effective = match pending.take() {
            Some(long) => {
                if !long.starts_with(header_name) { return Err(E::LongName); }
                long
            }
            None => header_name,
        };
        let effective = std::str::from_utf8(effective).map_err(|_| E::Path)?;
        let relative = effective.strip_prefix(&root).ok_or(E::Path)?;
        let path = opensip_identity::LogicalPath::parse(relative).map_err(|_| E::Path)?;
        let key = path.as_str().to_owned();
        if files.insert(key, DeclaredTarMember { path, content }).is_some() {
            return Err(E::Duplicate);
        }
    }
}
fn tar_name(field: &[u8]) -> &[u8] {
    &field[..field.iter().rposition(|b| *b != 0).map_or(0, |i| i + 1)]
}
fn tar_octal(field: &[u8]) -> Option<u64> {
    let first = field.iter().position(|b| *b != 0 && *b != b' ')?;
    let last = field.iter().rposition(|b| *b != 0 && *b != b' ')?;
    field[first..=last].iter().try_fold(0u64, |n,b| {
        if !(b'0'..=b'7').contains(b) { return None; }
        n.checked_mul(8)?.checked_add(u64::from(*b - b'0'))
    })
}
fn tar_size(field: &[u8]) -> Option<u64> {
    if field.first()? & 0x80 == 0 { return tar_octal(field); }
    // GNU positive base-256 only above the 11-octal-digit size range.
    // Negative or out-of-u64 values cannot describe a borrowed content slice.
    if field[0] & 0x40 != 0 { return None; }
    let value = field.iter().enumerate().try_fold(0u64, |n,(i,b)| {
        n.checked_mul(256)?.checked_add(u64::from(if i == 0 { *b & 0x7f } else { *b }))
    })?;
    (value > 0o77777777777).then_some(value)
}
'''
idx=s.index('\nfn optional_lock_text');s=s[:idx]+addition+s[idx:];p.write_text(s)
