//! Descriptor-native exact name sample; no ambient path or directory census.
//! Relative attachment and exclusion remain independent caller obligations.
#[cfg(target_os = "macos")]
use std::os::{fd::AsRawFd, unix::ffi::OsStrExt};
use std::{ffi::OsStr, fs::File, io};
#[cfg(target_os = "macos")]
const BUFFER_BYTES: usize = 32 + 1024;
#[cfg(target_os = "macos")]
fn invalid() -> io::Error {
    io::Error::new(io::ErrorKind::InvalidData, "invalid native name attributes")
}
#[cfg(target_os = "macos")]
fn name(buffer: &[u8]) -> io::Result<&[u8]> {
    // u32 total, five u32 returned-attribute words, one attrreference (i32/u32).
    // Decode bytes explicitly: no alignment-dependent Rust struct dereference.
    if buffer.len() < 32 {
        return Err(invalid());
    }
    let word = |i: usize| u32::from_ne_bytes(buffer[i..i + 4].try_into().unwrap());
    let total = word(0) as usize;
    if !(32..=buffer.len()).contains(&total) {
        return Err(invalid());
    }
    let common = word(4);
    if common & libc::ATTR_CMN_NAME == 0
        || common & !(libc::ATTR_CMN_NAME | libc::ATTR_CMN_RETURNED_ATTRS) != 0
        || [8, 12, 16, 20].into_iter().any(|i| word(i) != 0)
    {
        return Err(invalid());
    }
    let offset = i32::from_ne_bytes(buffer[24..28].try_into().unwrap());
    if offset < 8 || offset % 4 != 0 {
        return Err(invalid());
    }
    let start = 24usize.checked_add(offset as usize).ok_or_else(invalid)?;
    let length = word(28) as usize;
    if !(2..=1024).contains(&length) {
        return Err(invalid());
    }
    let end = start.checked_add(length).ok_or_else(invalid)?;
    if end > total {
        return Err(invalid());
    }
    let value = &buffer[start..end];
    if value.last() != Some(&0)
        || value[..length - 1].contains(&0)
        || value[..length - 1].contains(&b'/')
    {
        return Err(invalid());
    }
    Ok(&value[..length - 1])
}
#[cfg(target_os = "macos")]
pub(super) fn matches(file: &File, expected: &OsStr) -> io::Result<bool> {
    let mut attributes = libc::attrlist {
        bitmapcount: libc::ATTR_BIT_MAP_COUNT,
        reserved: 0,
        commonattr: libc::ATTR_CMN_RETURNED_ATTRS | libc::ATTR_CMN_NAME,
        volattr: 0,
        dirattr: 0,
        fileattr: 0,
        forkattr: 0,
    };
    let mut buffer = [0u8; BUFFER_BYTES];
    // SAFETY: file owns the live descriptor; both pointers refer to initialized
    // writable storage for the entire call. Buffer length is exact. Request only
    // returned bitmap and name; REPORT_FULLSIZE exposes truncation to the decoder.
    let rc = unsafe {
        libc::fgetattrlist(
            file.as_raw_fd(),
            (&mut attributes as *mut libc::attrlist).cast(),
            buffer.as_mut_ptr().cast(),
            buffer.len(),
            libc::FSOPT_REPORT_FULLSIZE,
        )
    };
    if rc != 0 {
        return Err(io::Error::last_os_error());
    }
    Ok(name(&buffer)? == expected.as_bytes())
}
#[cfg(not(target_os = "macos"))]
pub(super) fn matches(_file: &File, _expected: &OsStr) -> io::Result<bool> {
    Err(io::Error::new(
        io::ErrorKind::Unsupported,
        "native name observer unavailable",
    ))
}
#[cfg(all(test, target_os = "macos"))]
mod tests {
    use super::*;
    use crate::RetainedDirectory;
    use std::os::unix::fs::{MetadataExt, symlink};
    use std::{fs, path::PathBuf};
    struct Fixture(PathBuf);
    impl Fixture {
        fn new() -> Self {
            let random = crate::request_entropy().unwrap();
            let id: String = random.iter().map(|b| format!("{b:02x}")).collect();
            let path = std::env::temp_dir().join(format!("opensip-native-name-{id}"));
            fs::create_dir(&path).unwrap();
            Self(path)
        }
        fn parent(&self) -> RetainedDirectory {
            RetainedDirectory::from_retained_handle(File::open(&self.0).unwrap()).unwrap()
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.0);
        }
    }
    fn encoded(raw: &[u8]) -> Vec<u8> {
        let mut b = vec![0; 32 + raw.len() + 1];
        let n = b.len() as u32;
        b[0..4].copy_from_slice(&n.to_ne_bytes());
        b[4..8]
            .copy_from_slice(&(libc::ATTR_CMN_NAME | libc::ATTR_CMN_RETURNED_ATTRS).to_ne_bytes());
        b[24..28].copy_from_slice(&8i32.to_ne_bytes());
        b[28..32].copy_from_slice(&(raw.len() as u32 + 1).to_ne_bytes());
        b[32..32 + raw.len()].copy_from_slice(raw);
        b
    }
    #[test]
    fn directory_names_decodes_only_complete_bounded_name_attributes() {
        for raw in [&b"child"[..], &b"A-a"[..], &b"\xff"[..], &vec![b'x'; 1023]] {
            assert_eq!(name(&encoded(raw)).unwrap(), raw);
        }
        for raw in [&b""[..], &b"a/b"[..], &b"a\0b"[..], &vec![b'x'; 1024]] {
            assert!(name(&encoded(raw)).is_err());
        }
        let good = encoded(b"child");
        for (at, value) in [
            (0, 0u32),
            (0, 99999),
            (4, 0),
            (4, libc::ATTR_CMN_NAME | libc::ATTR_CMN_DEVID),
            (8, 1),
            (12, 1),
            (16, 1),
            (20, 1),
            (24, 0),
            (24, 4),
            (24, 9),
            (24, u32::MAX),
            (24, 0x7ffffffc),
            (28, 0),
            (28, 1),
            (28, 1025),
            (28, 999),
        ] {
            let mut b = good.clone();
            b[at..at + 4].copy_from_slice(&value.to_ne_bytes());
            assert!(name(&b).is_err(), "{at} {value}");
        }
        for n in 0..good.len() {
            assert!(name(&good[..n]).is_err());
        }
        let mut b = good.clone();
        *b.last_mut().unwrap() = b'x';
        assert!(name(&b).is_err());
    }
    #[test]
    fn directory_names_actual_case_alias_is_not_exact_spelling() {
        let f = Fixture::new();
        fs::create_dir(f.0.join("Canonical")).unwrap();
        let parent = f.parent();
        let exact = parent
            .bind_child_directory(OsStr::new("Canonical"))
            .unwrap();
        assert!(exact.recheck_exact_name().unwrap());
        match parent.bind_child_directory(OsStr::new("canonical")) {
            Ok(alias) => {
                assert!(alias.recheck().unwrap());
                assert!(!alias.recheck_exact_name().unwrap());
            }
            Err(e) => assert_eq!(e.kind(), io::ErrorKind::NotFound),
        }
        fs::create_dir(f.0.join("other")).unwrap();
        assert!(exact.recheck_exact_name().unwrap());
    }
    #[test]
    fn directory_names_retained_name_tracks_rename_without_adopting_decoy() {
        let f = Fixture::new();
        let path = f.0.join("child");
        fs::create_dir(&path).unwrap();
        let parent = f.parent();
        let edge = parent.bind_child_directory(OsStr::new("child")).unwrap();
        let original = File::open(&path).unwrap();
        let inode = original.metadata().unwrap().ino();
        assert!(matches(&original, OsStr::new("child")).unwrap());
        fs::rename(&path, f.0.join("renamed")).unwrap();
        fs::create_dir(&path).unwrap();
        assert!(!matches(&original, OsStr::new("child")).unwrap());
        assert!(matches(&original, OsStr::new("renamed")).unwrap());
        assert_eq!(original.metadata().unwrap().ino(), inode);
        assert!(!edge.recheck_exact_name().unwrap());
        fs::remove_dir(&path).unwrap();
        symlink("renamed", &path).unwrap();
        assert!(edge.recheck_exact_name().is_err());
    }
    #[test]
    fn directory_names_case_only_rename_rejects_even_if_inode_lookup_still_matches() {
        let f = Fixture::new();
        let path = f.0.join("child");
        fs::create_dir(&path).unwrap();
        let parent = f.parent();
        let edge = parent.bind_child_directory(OsStr::new("child")).unwrap();
        fs::rename(&path, f.0.join("CHILD")).unwrap();
        assert!(!edge.recheck_exact_name().unwrap());
        assert!(
            parent
                .bind_child_directory(OsStr::new("CHILD"))
                .unwrap()
                .recheck_exact_name()
                .unwrap()
        );
    }
    #[test]
    fn directory_names_equal_leaf_name_does_not_replace_relative_inode_binding() {
        let f = Fixture::new();
        fs::create_dir(f.0.join("child")).unwrap();
        fs::create_dir(f.0.join("old")).unwrap();
        let edge = f
            .parent()
            .bind_child_directory(OsStr::new("child"))
            .unwrap();
        fs::rename(f.0.join("child"), f.0.join("old/child")).unwrap();
        fs::create_dir(f.0.join("child")).unwrap();
        assert!(matches(&edge.directory().0, OsStr::new("child")).unwrap());
        assert!(!edge.recheck_exact_name().unwrap());
    }
}
