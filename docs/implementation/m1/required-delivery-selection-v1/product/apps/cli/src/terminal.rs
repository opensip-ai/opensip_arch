use std::io;

/// Obtain an owned duplicate of the actual stdout
/// handle. Rust's convenience Stdout wrapper treats EBADF as a successful sink;
/// using File preserves the underlying write error for host outcome policy.
#[cfg(unix)]
pub(crate) fn stdout() -> io::Result<std::fs::File> {
    use std::os::fd::AsFd;
    let descriptor = io::stdout().as_fd().try_clone_to_owned()?;
    Ok(std::fs::File::from(descriptor))
}
#[cfg(not(unix))]
compile_error!("This development build selects the macOS/Linux terminal profile only");
