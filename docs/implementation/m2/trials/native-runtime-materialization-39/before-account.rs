//! Bounded account-database lookup, not actor admission or home-directory custody.
//! `getpwuid_r` fills caller-owned storage; no HOME/USER/SUDO_UID fallback.
//! OS name-service providers can block or consult their configured services/cache:
//! the byte/retry bounds below are not a wall-clock or no-OS-side-effects guarantee.
use std::{
    ffi::OsString,
    io,
    os::unix::ffi::OsStringExt,
    path::{Path, PathBuf},
};

const INITIAL_BUFFER: usize = 1024;
const MAX_BUFFER: usize = 64 * 1024;

/// Sampled process credentials and the real user's account-database home.
/// Private construction prevents substituting environment data for an OS lookup.
/// These samples do not exclude credential ABA or account-database changes, admit
/// elevated execution, authorize any group, or establish filesystem custody.
pub struct AccountObservation {
    real_uid: u32,
    effective_uid: u32,
    home: PathBuf,
}
// Account details stay behind explicit getters; routine debug output must not
// disclose a home path or account identifiers.
impl std::fmt::Debug for AccountObservation {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("AccountObservation").finish_non_exhaustive()
    }
}
impl AccountObservation {
    pub fn real_uid(&self) -> u32 {
        self.real_uid
    }
    pub fn effective_uid(&self) -> u32 {
        self.effective_uid
    }
    /// Raw absolute OS path, possibly non-UTF-8 or containing symlink components.
    /// The consumer must separately resolve/admit it under its discovery policy.
    pub fn home(&self) -> &Path {
        &self.home
    }
}

#[derive(Debug)]
pub enum AccountObservationError {
    Lookup(io::Error),
    MissingAccount,
    RecordTooLarge,
    MalformedRecord,
    CredentialsChanged,
}

fn credentials() -> (u32, u32) {
    // SAFETY: zero-argument OS credential observations, no pointers.
    unsafe { (libc::getuid(), libc::geteuid()) }
}

/// Observe real/effective UIDs and query the real UID's account entry.
/// A mismatch between real and effective UID is reported as data, not endorsed
/// as an authorized invocation. No environment value selects the UID or home.
/// Samples before/after the lookup must agree; this is not lifetime exclusion.
/// At most seven lookup calls use buffers of 1..64 KiB. OS service latency and
/// cache activity are outside that memory bound. No directory is created here.
pub fn observe_account() -> Result<AccountObservation, AccountObservationError> {
    observe_with(credentials, os_lookup)
}

fn observe_with(
    mut sample: impl FnMut() -> (u32, u32),
    lookup: impl FnMut(u32, &mut [u8]) -> Result<LookupReply, AccountObservationError>,
) -> Result<AccountObservation, AccountObservationError> {
    let before = sample();
    let home = lookup_home(before.0, lookup)?;
    if sample() != before {
        return Err(AccountObservationError::CredentialsChanged);
    }
    Ok(AccountObservation {
        real_uid: before.0,
        effective_uid: before.1,
        home,
    })
}

enum LookupReply {
    LargerBuffer,
    Missing,
    Found { uid: u32, home_address: usize },
}

fn os_lookup(uid: u32, bytes: &mut [u8]) -> Result<LookupReply, AccountObservationError> {
    // SAFETY: libc::passwd consists of integers and raw pointers; zero is a valid
    // initial representation. The selected OS API fills the record on success.
    let mut record: libc::passwd = unsafe { std::mem::zeroed() };
    let mut result = std::ptr::null_mut();
    // SAFETY: record/result are live aligned writable objects, and bytes is a
    // live writable allocation of exactly the passed length. The reentrant API
    // stores pointed-to strings in this caller-provided buffer. No pointer escapes.
    let code = unsafe {
        libc::getpwuid_r(
            uid,
            &mut record,
            bytes.as_mut_ptr().cast(),
            bytes.len(),
            &mut result,
        )
    };
    if code == libc::ERANGE {
        return Ok(LookupReply::LargerBuffer);
    }
    if code != 0 {
        return Err(AccountObservationError::Lookup(
            io::Error::from_raw_os_error(code),
        ));
    }
    if result.is_null() {
        return Ok(LookupReply::Missing);
    }
    if !std::ptr::eq(result, &record) {
        return Err(AccountObservationError::MalformedRecord);
    }
    Ok(LookupReply::Found {
        uid: record.pw_uid,
        home_address: record.pw_dir as usize,
    })
}

fn lookup_home(
    uid: u32,
    mut lookup: impl FnMut(u32, &mut [u8]) -> Result<LookupReply, AccountObservationError>,
) -> Result<PathBuf, AccountObservationError> {
    let mut size = INITIAL_BUFFER;
    loop {
        let mut bytes = vec![0u8; size];
        match lookup(uid, &mut bytes)? {
            LookupReply::LargerBuffer if size < MAX_BUFFER => size *= 2,
            LookupReply::LargerBuffer => return Err(AccountObservationError::RecordTooLarge),
            LookupReply::Missing => return Err(AccountObservationError::MissingAccount),
            LookupReply::Found {
                uid: found,
                home_address,
            } => {
                if found != uid {
                    return Err(AccountObservationError::MalformedRecord);
                }
                return home_from_buffer(&bytes, home_address);
            }
        }
    }
}

fn home_from_buffer(bytes: &[u8], address: usize) -> Result<PathBuf, AccountObservationError> {
    let malformed = || AccountObservationError::MalformedRecord;
    let offset = address
        .checked_sub(bytes.as_ptr() as usize)
        .ok_or_else(malformed)?;
    // Never dereference the OS-returned pointer. Reborrow only validated storage
    // inside the original allocation, and search for NUL within that bound.
    let tail = bytes.get(offset..).ok_or_else(malformed)?;
    let length = tail.iter().position(|b| *b == 0).ok_or_else(malformed)?;
    let path = PathBuf::from(OsString::from_vec(tail[..length].to_vec()));
    if !path.is_absolute() {
        return Err(malformed());
    }
    Ok(path)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::os::unix::ffi::OsStrExt;

    #[test]
    fn home_is_owned_bounded_os_bytes_without_utf8_conversion() {
        let bytes = b"ignored\0/Users/\xffperson\0rest";
        let path = home_from_buffer(bytes, bytes.as_ptr() as usize + 8).unwrap();
        assert_eq!(path.as_os_str().as_bytes(), b"/Users/\xffperson");
        for (bytes, offset) in [
            (&b"relative\0"[..], 0),
            (&b"\0"[..], 0),
            (&b"/unterminated"[..], 0),
            (&b"/a\0"[..], 3),
            (&b"/a\0"[..], 4),
        ] {
            assert!(matches!(
                home_from_buffer(bytes, bytes.as_ptr() as usize + offset),
                Err(AccountObservationError::MalformedRecord)
            ));
        }
        assert!(matches!(
            home_from_buffer(b"/a\0", 0),
            Err(AccountObservationError::MalformedRecord)
        ));
    }

    fn found(uid: u32, bytes: &mut [u8]) -> Result<LookupReply, AccountObservationError> {
        bytes[..8].copy_from_slice(b"/sample\0");
        Ok(LookupReply::Found {
            uid,
            home_address: bytes.as_ptr() as usize,
        })
    }

    #[test]
    fn erange_retries_are_bounded_and_only_erange_retries() {
        let mut sizes = vec![];
        let result = lookup_home(23, |uid, bytes| {
            assert_eq!(uid, 23);
            sizes.push(bytes.len());
            Ok(LookupReply::LargerBuffer)
        });
        assert!(matches!(
            result,
            Err(AccountObservationError::RecordTooLarge)
        ));
        assert_eq!(sizes, [1024, 2048, 4096, 8192, 16384, 32768, 65536]);
        let mut calls = 0;
        let path = lookup_home(23, |uid, bytes| {
            calls += 1;
            if calls == 1 {
                Ok(LookupReply::LargerBuffer)
            } else {
                found(uid, bytes)
            }
        })
        .unwrap();
        assert_eq!(calls, 2);
        assert_eq!(path, Path::new("/sample"));
        let mut calls = 0;
        let result = lookup_home(23, |_, _| {
            calls += 1;
            Err(AccountObservationError::Lookup(
                io::Error::from_raw_os_error(libc::EIO),
            ))
        });
        assert_eq!(calls, 1);
        assert!(
            matches!(result,Err(AccountObservationError::Lookup(e))if e.raw_os_error()==Some(libc::EIO))
        );
        assert!(matches!(
            lookup_home(23, |_, _| Ok(LookupReply::Missing)),
            Err(AccountObservationError::MissingAccount)
        ));
        assert!(matches!(
            lookup_home(23, |_, b| found(24, b)),
            Err(AccountObservationError::MalformedRecord)
        ));
    }

    #[test]
    fn sample_joins_real_account_uid_and_preserves_effective_uid_without_endorsement() {
        let mut samples = 0;
        let observed = observe_with(
            || {
                samples += 1;
                (23, 91)
            },
            |uid, b| {
                assert_eq!(uid, 23);
                found(uid, b)
            },
        )
        .unwrap();
        assert_eq!(samples, 2);
        assert_eq!(observed.real_uid(), 23);
        assert_eq!(observed.effective_uid(), 91);
        assert_eq!(observed.home(), Path::new("/sample"));
        for after in [(24, 91), (23, 92)] {
            let mut samples = 0;
            assert!(matches!(
                observe_with(
                    || {
                        samples += 1;
                        if samples == 1 { (23, 91) } else { after }
                    },
                    found
                ),
                Err(AccountObservationError::CredentialsChanged)
            ));
        }
    }

    #[test]
    fn actual_account_lookup_matches_os_credentials_and_ignores_environment_location() {
        // Host isolation removes HOME/TMPDIR; no test mutates process environment.
        // Do not log account names, home paths, or the unused passwd fields.
        let expected = credentials();
        let observed = observe_account().unwrap();
        assert_eq!((observed.real_uid(), observed.effective_uid()), expected);
        assert!(observed.home().is_absolute());
        #[cfg(target_os = "macos")]
        {
            // Independent, non-reentrant API oracle. macOS documents this API's
            // returned storage as thread-specific; copy before any further account
            // lookup on this thread. This oracle is deliberately not used on Linux,
            // where a process-global static result could race other test threads.
            // SAFETY: zero-pointer-argument account query of the sampled real UID.
            let entry = unsafe { libc::getpwuid(expected.0) };
            assert!(!entry.is_null(), "native account oracle returned no entry");
            // SAFETY: getpwuid returned a live passwd in libc-owned storage. No
            // intervening lookup occurs before copying its documented NUL-terminated
            // pw_dir string. The pointer is checked for null before CStr conversion.
            let home = unsafe {
                let dir = (*entry).pw_dir;
                assert!(!dir.is_null(), "native account oracle returned no home");
                std::ffi::CStr::from_ptr(dir).to_bytes().to_vec()
            };
            // Boolean assertion deliberately avoids printing either private path.
            assert!(
                observed.home().as_os_str().as_bytes() == home,
                "observed home differs from native account oracle"
            );
        }
    }
    #[test]
    #[cfg(target_os = "macos")]
    fn actual_adapter_reports_erange_for_a_one_byte_buffer() {
        let uid = credentials().0;
        assert!(matches!(
            os_lookup(uid, &mut [0u8; 1]),
            Ok(LookupReply::LargerBuffer)
        ));
    }

    #[test]
    fn debug_omits_account_identifiers_and_home() {
        let observation = observe_with(|| (23, 91), found).unwrap();
        assert_eq!(format!("{observation:?}"), "AccountObservation { .. }");
    }
}
