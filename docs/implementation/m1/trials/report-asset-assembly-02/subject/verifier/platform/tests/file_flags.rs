//! Descriptor flags regression adopted from actual Claude review01.
use opensip_platform_asset_trial::ReleaseDirectory;
use std::fs::{self, File};
use std::os::fd::AsRawFd;

#[test]
fn probe_returned_file_status_flags() {
    let dir = std::env::temp_dir().join(format!("review-flags-{}", std::process::id()));
    fs::create_dir(&dir).unwrap();
    fs::create_dir(dir.join("d")).unwrap();
    fs::write(dir.join("d/f"), b"x").unwrap();
    let h = ReleaseDirectory::from_retained_handle(File::open(&dir).unwrap()).unwrap();
    let f = h.open_regular("d/f").unwrap();
    // SAFETY: f owns a live descriptor for the duration of both calls.
    let status = unsafe { libc::fcntl(f.as_raw_fd(), libc::F_GETFL) };
    let fd_flags = unsafe { libc::fcntl(f.as_raw_fd(), libc::F_GETFD) };
    eprintln!(
        "PROBE flags: O_NONBLOCK retained={} FD_CLOEXEC={} O_RDONLY={}",
        status & libc::O_NONBLOCK != 0,
        fd_flags & libc::FD_CLOEXEC != 0,
        status & libc::O_ACCMODE == libc::O_RDONLY
    );
    assert!(fd_flags >= 0 && status >= 0, "fcntl must succeed");
    assert!(fd_flags & libc::FD_CLOEXEC != 0);
    assert_eq!(status & libc::O_ACCMODE, libc::O_RDONLY);
    let _ = fs::remove_dir_all(&dir);
}
