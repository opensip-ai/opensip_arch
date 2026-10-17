//! Charged exclusive rename and unlink of one entry inside one retained
//! directory (M3-C r8 item 1; unit C1a2): what the snapshot's candidate blob
//! custody needs to place a written temporary under its digest name and to
//! discard a duplicate. Mechanisms only. Which directory, which names and
//! what a raw `EEXIST` means belong to the caller. The rename never replaces
//! an existing entry, and an unsupported exclusive rename fails with no
//! overwrite fallback. Every cost is charged before its name copy or native
//! call. No custody or authority, and no durability barrier: the candidate
//! custody is per invocation.
use crate::{RetainedDirectory, WorkCost, WorkFailure, WorkScope};
use std::ffi::CString;
use std::io;
use std::os::fd::AsRawFd;

/// One component, as `RetainedDirectory`'s own creators require it: not
/// empty, `.` or `..`, and holding no `/`, `\` or NUL.
fn component(name: &str) -> io::Result<CString> {
    if name.is_empty() || name == "." || name == ".." || name.contains(['/', '\\', '\0']) {
        return Err(io::Error::new(
            io::ErrorKind::InvalidInput,
            "invalid custody entry name",
        ));
    }
    CString::new(name)
        .map_err(|_| io::Error::new(io::ErrorKind::InvalidInput, "invalid custody entry name"))
}

/// Published work of one `rename_exclusive_accounted` of `from` to `to`,
/// computed without allocation. Objects: the two NUL-terminated name copies.
/// Edges: the one exclusive rename. Bytes: both names and their NULs.
pub fn rename_exclusive_cost(from: &str, to: &str) -> WorkCost {
    WorkCost {
        objects: 2,
        edges: 1,
        bytes: from.len().saturating_add(to.len()).saturating_add(2),
    }
}

/// Published work of one `unlink_entry_accounted` of `name`: its
/// NUL-terminated copy and the one `unlinkat`.
pub fn unlink_entry_cost(name: &str) -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 1,
        bytes: name.len().saturating_add(1),
    }
}

/// A successful charged exclusive rename. `EntryExists` is only a raw
/// `EEXIST`: some entry was already at `to`, nothing moved, and the work
/// scope stays open.
#[derive(Debug, PartialEq, Eq)]
pub enum ExclusiveRenameOutcome {
    Renamed,
    EntryExists,
}

impl RetainedDirectory {
    /// Rename the entry `from` to `to` inside this directory without
    /// replacing anything at `to` (`renameatx_np(RENAME_EXCL)` on macOS,
    /// `renameat2(RENAME_NOREPLACE)` on Linux), charged to `work` first. A
    /// raw `EEXIST` is `Ok(EntryExists)`; every other failure fails the
    /// scope, and none falls back to an overwriting rename.
    pub fn rename_exclusive_accounted(
        &self,
        from: &str,
        to: &str,
        work: &mut WorkScope<'_>,
    ) -> Result<ExclusiveRenameOutcome, WorkFailure<io::Error>> {
        work.run(rename_exclusive_cost(from, to), |_| {
            let (from, to) = (
                component(from).map_err(WorkFailure::Operation)?,
                component(to).map_err(WorkFailure::Operation)?,
            );
            let parent = self.as_file().as_raw_fd();
            // SAFETY: the parent descriptor is live and both names are
            // single-component C strings that outlive the call.
            #[cfg(target_os = "macos")]
            let result = unsafe {
                libc::renameatx_np(
                    parent,
                    from.as_ptr(),
                    parent,
                    to.as_ptr(),
                    libc::RENAME_EXCL,
                )
            };
            // SAFETY: as above.
            #[cfg(target_os = "linux")]
            let result = unsafe {
                libc::renameat2(
                    parent,
                    from.as_ptr(),
                    parent,
                    to.as_ptr(),
                    libc::RENAME_NOREPLACE,
                )
            };
            if result == 0 {
                return Ok(ExclusiveRenameOutcome::Renamed);
            }
            let error = io::Error::last_os_error();
            if error.raw_os_error() == Some(libc::EEXIST) {
                Ok(ExclusiveRenameOutcome::EntryExists)
            } else {
                Err(WorkFailure::Operation(error))
            }
        })
    }

    /// Unlink the non-directory entry `name` in this directory, charged to
    /// `work` first. A failure fails the scope.
    pub fn unlink_entry_accounted(
        &self,
        name: &str,
        work: &mut WorkScope<'_>,
    ) -> Result<(), WorkFailure<io::Error>> {
        work.run(unlink_entry_cost(name), |_| {
            let name = component(name).map_err(WorkFailure::Operation)?;
            // SAFETY: the parent descriptor is live and the name is a
            // single-component C string; flag 0 never removes a directory.
            if unsafe { libc::unlinkat(self.as_file().as_raw_fd(), name.as_ptr(), 0) } == 0 {
                Ok(())
            } else {
                Err(WorkFailure::Operation(io::Error::last_os_error()))
            }
        })
    }
}

#[cfg(test)]
#[path = "custody_entry_tests.rs"]
mod tests;
