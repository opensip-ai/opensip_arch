//! Fixed-buffer native descriptor/ACL samples with original-operation accounting.
//! Omission is unavailable ACL evidence. Neither a NOACL sentinel nor matching
//! metadata establishes per-vnode support, private custody or future authority.
use super::DescriptorMetadata;
use crate::{ReservedPostchecks, WorkCost, WorkFailure, WorkScope};
use std::{fmt, fs::File, io};
const BUFFER_BYTES: usize = 3244;
const MAX_ENTRIES: usize = 128;
const COMMON: u32 = 0x8247_8c0a;
const EXTENDED_SECURITY: u32 = 0x0040_0000;
const FILESEC_MAGIC: u32 = 0x012c_c16d;
const HEADER_BYTES: usize = 44;
const ENTRY_BYTES: usize = 24;

#[derive(Debug)]
pub enum DescriptorAclCaptureError {
    Io(io::Error),
    Unsupported,
    Malformed(&'static str),
    Changed,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CapturedAclState {
    /// Native response omitted the ACL attribute; not proof there is no ACL.
    NotReturned,
    /// Native structure carries NOACL; support/absence semantics still need a profile.
    NoAclSentinel,
    /// A present ACL, including a distinct zero-entry ACL.
    Entries(usize),
}
#[derive(Clone, Copy, PartialEq, Eq)]
pub enum CapturedAclPrincipal {
    User(u32),
    Group(u32),
    Unresolved,
}
impl fmt::Debug for CapturedAclPrincipal {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(match self {
            Self::User(_) => "User(<redacted>)",
            Self::Group(_) => "Group(<redacted>)",
            Self::Unresolved => "Unresolved",
        })
    }
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CapturedAclEntry {
    /// Raw flags include the low four-bit kind and all inheritance/unknown bits.
    pub flags: u32,
    /// No rights are dropped, including unknown or nonmutating read/search bits.
    pub rights: u32,
    pub principal: CapturedAclPrincipal,
}
#[derive(Debug, Clone, Copy)]
struct Layout {
    state: CapturedAclState,
    acl_start: usize,
    directory_links: Option<u32>,
}
/// A finite sample from one original descriptor, not an authorization token.
/// Before/after full metadata matched. Common security fields were also sampled
/// jointly with ACL data. Regular-file links/size matched jointly; directory
/// linkcount has different semantics and directory size was NOT jointly sampled.
/// The existing observe_descriptor triple-comparison API is not replaced.
pub struct DescriptorAclCapture {
    metadata: DescriptorMetadata,
    buffer: [u8; BUFFER_BYTES],
    layout: Layout,
    principals: [CapturedAclPrincipal; MAX_ENTRIES],
}
impl fmt::Debug for DescriptorAclCapture {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("DescriptorAclCapture")
            .field("acl_state", &self.layout.state)
            .finish_non_exhaustive()
    }
}
impl DescriptorAclCapture {
    pub fn metadata(&self) -> &DescriptorMetadata {
        &self.metadata
    }
    pub fn acl_state(&self) -> CapturedAclState {
        self.layout.state
    }
    /// Native ATTR_DIR_LINKCOUNT, explicitly NOT stat.st_nlink. None for a file.
    pub fn directory_attribute_linkcount(&self) -> Option<u32> {
        self.layout.directory_links
    }
    pub fn entry(&self, index: usize) -> Option<CapturedAclEntry> {
        let CapturedAclState::Entries(count) = self.layout.state else {
            return None;
        };
        if index >= count {
            return None;
        }
        let offset = self.layout.acl_start + HEADER_BYTES + index * ENTRY_BYTES;
        Some(CapturedAclEntry {
            flags: word(&self.buffer, offset + 16).ok()?,
            rights: word(&self.buffer, offset + 20).ok()?,
            principal: self.principals[index],
        })
    }
    pub fn acl_flags(&self) -> Option<u32> {
        if self.layout.state == CapturedAclState::NotReturned {
            None
        } else {
            word(&self.buffer, self.layout.acl_start + 40).ok()
        }
    }
}
/// Conservative caller-owned storage and outer API allowance, not allocator RSS,
/// whole stack frames, kernel/service allocations, IPC/network work or latency.
/// Counts the retained sample, scratch attribute buffer, two native stat output
/// buffers and request structure; reserves3metadata/attribute +128resolver calls.
/// Unused allowance is consumed. Linux refuses capture, after conservative charge.
pub fn descriptor_acl_capture_cost() -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 3 + MAX_ENTRIES,
        bytes: std::mem::size_of::<DescriptorAclCapture>()
            + BUFFER_BYTES
            + 2 * std::mem::size_of::<libc::stat>()
            + request_bytes(),
    }
}
#[cfg(target_os = "macos")]
const fn request_bytes() -> usize {
    std::mem::size_of::<libc::attrlist>()
}
#[cfg(not(target_os = "macos"))]
const fn request_bytes() -> usize {
    24
}
pub fn capture_descriptor_acl_accounted(
    file: &File,
    work: &mut WorkScope<'_>,
) -> Result<DescriptorAclCapture, WorkFailure<DescriptorAclCaptureError>> {
    #[cfg(target_os = "macos")]
    {
        capture_accounted_in(file, work, libc::fgetattrlist, resolve_native)
    }
    #[cfg(not(target_os = "macos"))]
    {
        work.run(descriptor_acl_capture_cost(), |_| {
            capture_native(file).map_err(WorkFailure::Operation)
        })
    }
}
pub fn capture_descriptor_acl_reserved(
    file: &File,
    post: &mut ReservedPostchecks<'_>,
) -> Result<DescriptorAclCapture, WorkFailure<DescriptorAclCaptureError>> {
    #[cfg(target_os = "macos")]
    {
        capture_reserved_in(file, post, libc::fgetattrlist, resolve_native)
    }
    #[cfg(not(target_os = "macos"))]
    {
        post.scope(|post| {
            post.spend(descriptor_acl_capture_cost())?;
            capture_native(file).map_err(WorkFailure::Operation)
        })
    }
}
#[cfg(target_os = "macos")]
type AttrCall = unsafe extern "C" fn(
    libc::c_int,
    *mut libc::c_void,
    *mut libc::c_void,
    libc::size_t,
    u32,
) -> libc::c_int;
#[cfg(target_os = "macos")]
fn capture_accounted_in(
    file: &File,
    work: &mut WorkScope<'_>,
    call: AttrCall,
    resolver: impl FnMut(&[u8; 16]) -> CapturedAclPrincipal,
) -> Result<DescriptorAclCapture, WorkFailure<DescriptorAclCaptureError>> {
    work.run(descriptor_acl_capture_cost(), |_| {
        capture_with(file, call, resolver).map_err(WorkFailure::Operation)
    })
}
#[cfg(target_os = "macos")]
fn capture_reserved_in(
    file: &File,
    post: &mut ReservedPostchecks<'_>,
    call: AttrCall,
    resolver: impl FnMut(&[u8; 16]) -> CapturedAclPrincipal,
) -> Result<DescriptorAclCapture, WorkFailure<DescriptorAclCaptureError>> {
    post.scope(|post| {
        post.spend(descriptor_acl_capture_cost())?;
        capture_with(file, call, resolver).map_err(WorkFailure::Operation)
    })
}
fn malformed(s: &'static str) -> DescriptorAclCaptureError {
    DescriptorAclCaptureError::Malformed(s)
}
fn word(b: &[u8], at: usize) -> Result<u32, DescriptorAclCaptureError> {
    let end = at
        .checked_add(4)
        .ok_or_else(|| malformed("word overflow"))?;
    Ok(u32::from_ne_bytes(
        b.get(at..end)
            .ok_or_else(|| malformed("short word"))?
            .try_into()
            .map_err(|_| malformed("word"))?,
    ))
}
fn quad(b: &[u8], at: usize) -> Result<u64, DescriptorAclCaptureError> {
    let end = at
        .checked_add(8)
        .ok_or_else(|| malformed("quad overflow"))?;
    Ok(u64::from_ne_bytes(
        b.get(at..end)
            .ok_or_else(|| malformed("short quad"))?
            .try_into()
            .map_err(|_| malformed("quad"))?,
    ))
}
fn decode(b: &[u8], m: &DescriptorMetadata) -> Result<Layout, DescriptorAclCaptureError> {
    // Pinned64bit Darwin ABI: returned set at4, dev24, type28, times32/48,
    // owner64/group68/mode72/flags76, ACL reference80, inode88, links96,
    // regular data length100. PACK_INVAL_ATTRS reserves even omitted ACL's slot.
    let dir = match m.mode & 0o170000 {
        0o040000 => true,
        0o100000 => false,
        _ => return Err(DescriptorAclCaptureError::Unsupported),
    };
    let fixed = if dir { 100 } else { 108 };
    let full = word(b, 0)? as usize;
    if full > BUFFER_BYTES || full > b.len() || full < fixed {
        return Err(malformed("truncated attribute response"));
    }
    let b = &b[..full];
    let common = word(b, 4)?;
    if common & !EXTENDED_SECURITY != COMMON & !EXTENDED_SECURITY
        || word(b, 8)? != 0
        || word(b, 12)? != if dir { 1 } else { 0 }
        || word(b, 16)? != if dir { 0 } else { 0x201 }
        || word(b, 20)? != 0
    {
        return Err(malformed("attribute bitmap"));
    }
    let mt = (quad(b, 32)? as i64, quad(b, 40)? as i64);
    let ct = (quad(b, 48)? as i64, quad(b, 56)? as i64);
    if !(0..1_000_000_000).contains(&mt.1) || !(0..1_000_000_000).contains(&ct.1) {
        return Err(malformed("timestamp"));
    }
    // dev_t is signed32bit; match its widening in the existing stat adapter.
    let dev = word(b, 24)? as i32 as u64;
    if dev != m.device
        || word(b, 28)? != if dir { 2 } else { 1 }
        || word(b, 64)? != m.uid
        || word(b, 68)? != m.gid
        || word(b, 72)? & !0o170000 != m.mode & !0o170000
        || word(b, 76)? != m.flags
        || quad(b, 88)? != m.inode
        || mt != m.modified
        || ct != m.changed
    {
        return Err(DescriptorAclCaptureError::Changed);
    }
    let links = word(b, 96)?;
    if !dir && (u64::from(links) != m.links || quad(b, 100)? != m.size || m.size > i64::MAX as u64)
    {
        return Err(DescriptorAclCaptureError::Changed);
    }
    let relative = word(b, 80)? as i32;
    if relative < 0 {
        return Err(malformed("negative ACL reference"));
    }
    let start = 80usize
        .checked_add(relative as usize)
        .ok_or_else(|| malformed("ACL offset overflow"))?;
    let length = word(b, 84)? as usize;
    if start != fixed || start % 4 != 0 || start.checked_add(length) != Some(full) {
        return Err(malformed("ACL reference extent"));
    }
    let state = if common & EXTENDED_SECURITY == 0 {
        if length != 0 {
            return Err(malformed("omitted ACL has data"));
        }
        CapturedAclState::NotReturned
    } else {
        if length < HEADER_BYTES || word(b, start)? != FILESEC_MAGIC {
            return Err(malformed("ACL header"));
        }
        let count = word(b, start + 36)?;
        if count == u32::MAX {
            if length != HEADER_BYTES {
                return Err(malformed("NOACL length"));
            }
            CapturedAclState::NoAclSentinel
        } else {
            let count = count as usize;
            if count > MAX_ENTRIES || length != HEADER_BYTES + count * ENTRY_BYTES {
                return Err(malformed("ACL count/length"));
            }
            CapturedAclState::Entries(count)
        }
    };
    Ok(Layout {
        state,
        acl_start: start,
        directory_links: if dir { Some(links) } else { None },
    })
}
fn resolve(
    b: &[u8],
    layout: Layout,
    call: &mut impl FnMut(&[u8; 16]) -> CapturedAclPrincipal,
) -> [CapturedAclPrincipal; MAX_ENTRIES] {
    let mut principals = [CapturedAclPrincipal::Unresolved; MAX_ENTRIES];
    if let CapturedAclState::Entries(count) = layout.state {
        for (i, p) in principals.iter_mut().enumerate().take(count) {
            let start = layout.acl_start + HEADER_BYTES + i * ENTRY_BYTES;
            // decode checked count, exact extent and complete fixed header.
            let uuid = b[start..start + 16].try_into().expect("validated ACE UUID");
            *p = call(uuid);
        }
    }
    principals
}
#[cfg(not(target_os = "macos"))]
fn capture_native(_file: &File) -> Result<DescriptorAclCapture, DescriptorAclCaptureError> {
    Err(DescriptorAclCaptureError::Unsupported)
}
#[cfg(target_os = "macos")]
fn resolve_native(uuid: &[u8; 16]) -> CapturedAclPrincipal {
    unsafe extern "C" {
        fn mbr_uuid_to_id(uuid: *const u8, id: *mut u32, kind: *mut i32) -> i32;
    }
    let mut id = 0;
    let mut kind = -1;
    // SAFETY: complete borrowed16byte UUID and valid SDK id_t/int output slots.
    let result = unsafe { mbr_uuid_to_id(uuid.as_ptr(), &mut id, &mut kind) };
    match (result, kind) {
        (0, 0) => CapturedAclPrincipal::User(id),
        (0, 1) => CapturedAclPrincipal::Group(id),
        _ => CapturedAclPrincipal::Unresolved,
    }
}
#[cfg(target_os = "macos")]
fn capture_with(
    file: &File,
    call: unsafe extern "C" fn(
        libc::c_int,
        *mut libc::c_void,
        *mut libc::c_void,
        libc::size_t,
        u32,
    ) -> libc::c_int,
    mut resolver: impl FnMut(&[u8; 16]) -> CapturedAclPrincipal,
) -> Result<DescriptorAclCapture, DescriptorAclCaptureError> {
    use std::os::fd::AsRawFd;
    let before =
        DescriptorMetadata::from_metadata(&file.metadata().map_err(DescriptorAclCaptureError::Io)?);
    let dir = match before.mode & 0o170000 {
        0o040000 => true,
        0o100000 => false,
        _ => return Err(DescriptorAclCaptureError::Unsupported),
    };
    let mut attrs = libc::attrlist {
        bitmapcount: libc::ATTR_BIT_MAP_COUNT,
        reserved: 0,
        commonattr: COMMON,
        volattr: 0,
        dirattr: if dir { libc::ATTR_DIR_LINKCOUNT } else { 0 },
        fileattr: if dir {
            0
        } else {
            libc::ATTR_FILE_LINKCOUNT | libc::ATTR_FILE_DATALENGTH
        },
        forkattr: 0,
    };
    let mut buffer = [0u8; BUFFER_BYTES];
    // SAFETY: original live File, initialized writable request/output, exact
    // bounded output size; the two flags expose fullsize and fixed invalid slots.
    let result = unsafe {
        call(
            file.as_raw_fd(),
            (&mut attrs as *mut libc::attrlist).cast(),
            buffer.as_mut_ptr().cast(),
            buffer.len(),
            libc::FSOPT_REPORT_FULLSIZE | libc::FSOPT_PACK_INVAL_ATTRS,
        )
    };
    let pending = if result != 0 {
        Err(DescriptorAclCaptureError::Io(io::Error::last_os_error()))
    } else {
        decode(&buffer, &before).map(|layout| {
            let principals = resolve(&buffer, layout, &mut resolver);
            (layout, principals)
        })
    };
    // Observe the original again even after ordinary syscall/decoder failure.
    // Resolver errors are unresolved evidence, not successful principal admission.
    let after =
        DescriptorMetadata::from_metadata(&file.metadata().map_err(DescriptorAclCaptureError::Io)?);
    if before != after {
        return Err(DescriptorAclCaptureError::Changed);
    }
    let (layout, principals) = pending?;
    Ok(DescriptorAclCapture {
        metadata: before,
        buffer,
        layout,
        principals,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    fn put(b: &mut [u8], at: usize, v: u32) {
        b[at..at + 4].copy_from_slice(&v.to_ne_bytes());
    }
    fn put64(b: &mut [u8], at: usize, v: u64) {
        b[at..at + 8].copy_from_slice(&v.to_ne_bytes());
    }
    fn fixture(dir: bool, state: CapturedAclState) -> ([u8; BUFFER_BYTES], DescriptorMetadata) {
        let mut b = [0u8; BUFFER_BYTES];
        let fixed = if dir { 100 } else { 108 };
        let length = match state {
            CapturedAclState::NotReturned => 0,
            CapturedAclState::NoAclSentinel => 44,
            CapturedAclState::Entries(n) => 44 + n * 24,
        };
        let m = DescriptorMetadata {
            device: 12,
            inode: 45,
            mode: if dir { 0o40700 } else { 0o100600 },
            uid: 51,
            gid: 52,
            links: if dir { 4 } else { 1 },
            size: 73,
            modified: (123, 456),
            changed: (124, 457),
            flags: 0,
        };
        put(&mut b, 0, (fixed + length) as u32);
        put(
            &mut b,
            4,
            if state == CapturedAclState::NotReturned {
                COMMON & !EXTENDED_SECURITY
            } else {
                COMMON
            },
        );
        put(&mut b, 12, if dir { 1 } else { 0 });
        put(&mut b, 16, if dir { 0 } else { 0x201 });
        put(&mut b, 24, m.device as u32);
        put(&mut b, 28, if dir { 2 } else { 1 });
        put64(&mut b, 32, m.modified.0 as u64);
        put64(&mut b, 40, m.modified.1 as u64);
        put64(&mut b, 48, m.changed.0 as u64);
        put64(&mut b, 56, m.changed.1 as u64);
        put(&mut b, 64, m.uid);
        put(&mut b, 68, m.gid);
        put(&mut b, 72, m.mode & 0o7777);
        put(&mut b, 76, m.flags);
        put(&mut b, 80, (fixed - 80) as u32);
        put(&mut b, 84, length as u32);
        put64(&mut b, 88, m.inode);
        put(&mut b, 96, 1);
        if !dir {
            put64(&mut b, 100, m.size)
        }
        if state != CapturedAclState::NotReturned {
            put(&mut b, fixed, FILESEC_MAGIC);
            put(
                &mut b,
                fixed + 36,
                match state {
                    CapturedAclState::NoAclSentinel => u32::MAX,
                    CapturedAclState::Entries(n) => n as u32,
                    _ => unreachable!(),
                },
            );
        }
        (b, m)
    }
    #[test]
    fn acl_capture_distinguishes_omission_sentinel_and_empty_without_admitting_absence() {
        for dir in [false, true] {
            for state in [
                CapturedAclState::NotReturned,
                CapturedAclState::NoAclSentinel,
                CapturedAclState::Entries(0),
                CapturedAclState::Entries(128),
            ] {
                let (b, m) = fixture(dir, state);
                let layout = decode(&b, &m).unwrap();
                assert_eq!(layout.state, state);
                assert_eq!(layout.directory_links, dir.then_some(1));
                let sample = DescriptorAclCapture {
                    metadata: m,
                    buffer: b,
                    layout,
                    principals: [CapturedAclPrincipal::Unresolved; MAX_ENTRIES],
                };
                match state {
                    CapturedAclState::NotReturned => assert_eq!(sample.acl_flags(), None),
                    _ => assert_eq!(sample.acl_flags(), Some(0)),
                }
                assert!(
                    sample.entry(0).is_none() || matches!(state, CapturedAclState::Entries(128))
                );
            }
        }
    }
    #[test]
    fn acl_capture_refuses_a_129th_directory_entry_and_an_oversize_file_record() {
        let (directory, metadata) = fixture(true, CapturedAclState::Entries(129));
        assert!(decode(&directory, &metadata).is_err());
        let (file, metadata) = fixture(false, CapturedAclState::Entries(129));
        assert!(decode(&file, &metadata).is_err());
    }
    #[test]
    fn acl_capture_omitted_attribute_with_a_matching_extent_is_not_empty() {
        let (mut buffer, metadata) = fixture(false, CapturedAclState::NotReturned);
        put(&mut buffer, 0, 152);
        put(&mut buffer, 84, 44);
        assert!(decode(&buffer, &metadata).is_err());
    }
    #[test]
    fn acl_capture_exposes_present_acl_flags_and_hides_omitted_ones() {
        let (mut buffer, metadata) = fixture(false, CapturedAclState::Entries(0));
        put(&mut buffer, 108 + 40, 0x15);
        let layout = decode(&buffer, &metadata).unwrap();
        let sample = DescriptorAclCapture {
            metadata,
            buffer,
            layout,
            principals: [CapturedAclPrincipal::Unresolved; MAX_ENTRIES],
        };
        assert_eq!(sample.acl_flags(), Some(0x15));
        let (omitted, omitted_metadata) = fixture(false, CapturedAclState::NotReturned);
        let omitted_layout = decode(&omitted, &omitted_metadata).unwrap();
        let omitted_sample = DescriptorAclCapture {
            metadata: omitted_metadata,
            buffer: omitted,
            layout: omitted_layout,
            principals: [CapturedAclPrincipal::Unresolved; MAX_ENTRIES],
        };
        assert_eq!(omitted_sample.acl_flags(), None);
        assert!(omitted_sample.entry(0).is_none());
    }
    #[test]
    fn acl_capture_keeps_all_rights_flags_and_resolved_principals_with_finite_calls() {
        let (mut b, m) = fixture(false, CapturedAclState::Entries(128));
        for i in 0..128 {
            let at = 108 + 44 + i * 24;
            b[at..at + 16].fill(i as u8);
            put(
                &mut b,
                at + 16,
                if i % 2 == 0 { 1 | 0x100 } else { 2 | 0x10 },
            );
            put(&mut b, at + 20, 0x8000_0002);
        }
        let layout = decode(&b, &m).unwrap();
        let mut calls = 0;
        let principals = resolve(&b, layout, &mut |uuid| {
            assert_eq!(uuid[0] as usize, calls);
            calls += 1;
            match uuid[0] % 3 {
                0 => CapturedAclPrincipal::User(91),
                1 => CapturedAclPrincipal::Group(92),
                _ => CapturedAclPrincipal::Unresolved,
            }
        });
        assert_eq!(calls, 128);
        let sample = DescriptorAclCapture {
            metadata: m,
            buffer: b,
            layout,
            principals,
        };
        for i in 0..128 {
            let e = sample.entry(i).unwrap();
            assert_eq!(e.rights, 0x8000_0002);
            assert_eq!(e.flags, if i % 2 == 0 { 1 | 0x100 } else { 2 | 0x10 });
            assert_eq!(
                e.principal,
                match i % 3 {
                    0 => CapturedAclPrincipal::User(91),
                    1 => CapturedAclPrincipal::Group(92),
                    _ => CapturedAclPrincipal::Unresolved,
                }
            );
        }
        assert!(sample.entry(128).is_none());
        assert!(!format!("{sample:?}").contains("91"));
        assert_eq!(
            format!("{:?}", CapturedAclPrincipal::User(91)),
            "User(<redacted>)"
        );
    }
    #[test]
    fn acl_capture_no_resolution_for_nonentry_states() {
        for state in [
            CapturedAclState::NotReturned,
            CapturedAclState::NoAclSentinel,
            CapturedAclState::Entries(0),
        ] {
            let (b, m) = fixture(false, state);
            let l = decode(&b, &m).unwrap();
            resolve(&b, l, &mut |_| panic!("no ACE to resolve"));
        }
    }
    #[test]
    fn acl_capture_rejects_malformed_bitmap_fixed_area_references_and_acl() {
        let (b, m) = fixture(false, CapturedAclState::Entries(1));
        for (at, value) in [
            (0, 32),
            (0, BUFFER_BYTES as u32 + 1),
            (4, COMMON | 1),
            (4, COMMON & !8),
            (8, 1),
            (12, 1),
            (16, 0),
            (20, 1),
            (40, 1_000_000_000),
            (80, u32::MAX),
            (80, 0),
            (80, 29),
            (84, 67),
            (108, 0),
            (144, 129),
        ] {
            let mut bad = b;
            put(&mut bad, at, value);
            assert!(
                decode(&bad, &m).is_err(),
                "accepted mutation at {at} value {value}"
            );
        }
        for len in [0, 3, 23, 99, 107, 175] {
            assert!(decode(&b[..len], &m).is_err());
        }
        let (mut absent, mm) = fixture(false, CapturedAclState::NotReturned);
        put(&mut absent, 84, 44);
        assert!(decode(&absent, &mm).is_err());
        let (mut sentinel, mm) = fixture(false, CapturedAclState::NoAclSentinel);
        put(&mut sentinel, 0, 176);
        put(&mut sentinel, 84, 68);
        assert!(decode(&sentinel, &mm).is_err());
    }
    #[test]
    fn acl_capture_joint_metadata_preserves_file_fields_and_distinct_directory_links() {
        let (b, m) = fixture(false, CapturedAclState::Entries(0));
        for at in [24, 28, 32, 40, 48, 56, 64, 68, 72, 76, 88, 96, 100] {
            let mut bad = b;
            let old = word(&b, at).unwrap();
            put(&mut bad, at, old ^ 1);
            assert!(decode(&bad, &m).is_err(), "metadata at {at}");
        }
        let (b, m) = fixture(true, CapturedAclState::Entries(0));
        assert_ne!(word(&b, 96).unwrap() as u64, m.links);
        assert!(decode(&b, &m).is_ok());
        // Type comes from OBJTYPE, not unsupported ACCESSMASK file-type bits.
        let (mut b, m) = fixture(false, CapturedAclState::Entries(0));
        put(&mut b, 72, (m.mode & 0o7777) | 0o040000);
        assert!(decode(&b, &m).is_ok());
        put(&mut b, 28, 2);
        assert!(matches!(
            decode(&b, &m),
            Err(DescriptorAclCaptureError::Changed)
        ));
    }
    #[cfg(target_os = "macos")]
    struct Scratch(std::path::PathBuf);
    #[cfg(target_os = "macos")]
    impl Scratch {
        fn new() -> Self {
            let nonce = crate::request_entropy().unwrap();
            let suffix: String = nonce.iter().map(|x| format!("{x:02x}")).collect();
            let path = std::env::temp_dir().join(format!("opensip-acl447-{suffix}"));
            std::fs::create_dir(&path).unwrap();
            Self(path)
        }
        fn file(&self) -> File {
            use std::os::unix::fs::OpenOptionsExt;
            std::fs::OpenOptions::new()
                .read(true)
                .write(true)
                .create_new(true)
                .mode(0o600)
                .open(self.0.join("record"))
                .unwrap()
        }
    }
    #[cfg(target_os = "macos")]
    impl Drop for Scratch {
        fn drop(&mut self) {
            let _ = std::fs::remove_dir_all(&self.0);
        }
    }
    #[test]
    #[cfg(target_os = "macos")]
    fn acl_capture_native_original_regular_and_directory_accounting_and_full_rights() {
        use std::os::unix::fs::MetadataExt;
        let scratch = Scratch::new();
        let f = scratch.file();
        let dir = File::open(&scratch.0).unwrap();
        for file in [&f, &dir] {
            let mut owner = crate::WorkLedger::new();
            let sample = owner
                .scope(|w| capture_descriptor_acl_accounted(file, w))
                .unwrap();
            assert_eq!(sample.metadata().inode, file.metadata().unwrap().ino());
            assert_eq!(owner.used(), descriptor_acl_capture_cost());
            assert!(owner.used().edges >= 3 + 128);
            assert!(owner.used().bytes >= BUFFER_BYTES);
            match sample.acl_state() {
                CapturedAclState::NotReturned => {
                    assert_eq!(sample.acl_flags(), None);
                    assert!(sample.entry(0).is_none());
                }
                CapturedAclState::NoAclSentinel => {
                    assert!(sample.acl_flags().is_some());
                    assert!(sample.entry(0).is_none());
                }
                CapturedAclState::Entries(count) => {
                    assert!(sample.acl_flags().is_some());
                    assert!(sample.entry(count).is_none());
                }
            }
            let uid = file.metadata().unwrap().uid();
            crate::macos::set_probe_acl(file, false, uid, 1, 2).unwrap();
            let mut reserved = crate::WorkLedger::new();
            let observed = reserved
                .effect(WorkCost::default(), descriptor_acl_capture_cost(), |p| {
                    capture_descriptor_acl_reserved(file, p)
                })
                .unwrap();
            assert_eq!(reserved.used(), descriptor_acl_capture_cost());
            assert_eq!(observed.acl_state(), CapturedAclState::Entries(1));
            let entry = observed.entry(0).unwrap();
            assert_eq!(entry.flags & 15, 1);
            assert_eq!(entry.rights, 2);
            assert_eq!(entry.principal, CapturedAclPrincipal::User(uid));
            let gid = file.metadata().unwrap().gid();
            crate::macos::set_probe_acl(file, true, gid, 1, 2).unwrap();
            let mut grouped = crate::WorkLedger::new();
            let group_sample = grouped
                .scope(|w| capture_descriptor_acl_accounted(file, w))
                .unwrap();
            assert_eq!(group_sample.acl_state(), CapturedAclState::Entries(1));
            assert_eq!(
                group_sample.entry(0).unwrap().principal,
                CapturedAclPrincipal::Group(gid)
            );
        }
    }
    #[test]
    #[cfg(target_os = "macos")]
    fn acl_capture_refuses_charge_before_native_work_and_preserves_original_after_unlink() {
        use std::os::unix::fs::MetadataExt;
        let scratch = Scratch::new();
        let file = scratch.file();
        let mut limits = descriptor_acl_capture_cost();
        limits.edges -= 1;
        let mut owner = crate::WorkLedger::with_limits(limits).unwrap();
        assert!(matches!(
            owner.scope(|w| capture_descriptor_acl_accounted(&file, w)),
            Err(WorkFailure::Budget(_))
        ));
        assert_eq!(owner.used(), WorkCost::default());
        assert!(owner.is_failed());
        let inode = file.metadata().unwrap().ino();
        std::fs::remove_file(scratch.0.join("record")).unwrap();
        let mut owner = crate::WorkLedger::new();
        let got = owner
            .scope(|w| capture_descriptor_acl_accounted(&file, w))
            .unwrap();
        assert_eq!(got.metadata().inode, inode);
        assert_eq!(got.metadata().links, 0);
        use std::sync::atomic::{AtomicUsize, Ordering};
        static SYSCALLS: AtomicUsize = AtomicUsize::new(0);
        unsafe extern "C" fn counting_syscall(
            _: libc::c_int,
            _: *mut libc::c_void,
            _: *mut libc::c_void,
            _: libc::size_t,
            _: u32,
        ) -> libc::c_int {
            SYSCALLS.fetch_add(1, Ordering::SeqCst);
            -1
        }
        SYSCALLS.store(0, Ordering::SeqCst);
        let mut owner = crate::WorkLedger::with_limits(limits).unwrap();
        assert!(matches!(
            owner.scope(|w| capture_accounted_in(&file, w, counting_syscall, |_| {
                panic!("resolver runs only after a successful charge")
            })),
            Err(WorkFailure::Budget(_))
        ));
        assert_eq!(SYSCALLS.load(Ordering::SeqCst), 0);
        let mut short = descriptor_acl_capture_cost();
        short.edges -= 1;
        let mut owner = crate::WorkLedger::new();
        assert!(matches!(
            owner.effect(WorkCost::default(), short, |post| {
                capture_reserved_in(&file, post, counting_syscall, |_| {
                    panic!("resolver runs only after a successful spend")
                })
            }),
            Err(WorkFailure::Budget(_))
        ));
        assert_eq!(SYSCALLS.load(Ordering::SeqCst), 0);
    }
    #[test]
    #[cfg(target_os = "macos")]
    fn acl_capture_postchecks_after_attribute_failure_and_detects_concurrent_permission_change() {
        use std::os::unix::fs::MetadataExt;
        let scratch = Scratch::new();
        let file = scratch.file();
        let uid = file.metadata().unwrap().uid();
        crate::macos::set_probe_acl(&file, false, uid, 1, 2).unwrap();
        let result = capture_with(&file, libc::fgetattrlist, |_| {
            file.set_permissions({
                use std::os::unix::fs::PermissionsExt;
                std::fs::Permissions::from_mode(0o640)
            })
            .unwrap();
            CapturedAclPrincipal::User(uid)
        });
        assert!(matches!(result, Err(DescriptorAclCaptureError::Changed)));
        unsafe extern "C" fn changed_error(
            fd: libc::c_int,
            _: *mut libc::c_void,
            _: *mut libc::c_void,
            _: libc::size_t,
            _: u32,
        ) -> libc::c_int {
            // SAFETY: fixture's original fd remains live; change only its mode.
            unsafe {
                assert_eq!(libc::fchmod(fd, 0o600), 0);
                *libc::__error() = libc::EACCES;
            }
            -1
        }
        let result = capture_with(&file, changed_error, |_| {
            panic!("failed capture must not resolve")
        });
        assert!(matches!(result, Err(DescriptorAclCaptureError::Changed)));
    }
}
