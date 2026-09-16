use std::io::{self, Write};

/// Deliver required bytes through an owned duplicate of the actual stdout
/// handle. Rust's convenience Stdout wrapper treats EBADF as a successful sink;
/// using File preserves the underlying write error for host outcome policy.
#[cfg(unix)]
pub(crate) fn write_stdout(bytes: &[u8]) -> io::Result<()> {
    use std::os::fd::AsFd;
    let descriptor = io::stdout().as_fd().try_clone_to_owned()?;
    let mut output = std::fs::File::from(descriptor);
    output.write_all(bytes)?;
    output.flush()
}
#[cfg(not(unix))]
compile_error!("This development build selects the macOS/Linux terminal profile only");
