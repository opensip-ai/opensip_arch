use std::io::{self, Read};
use std::os::raw::c_int;
unsafe extern "C" { fn fcntl(fd: c_int, cmd: c_int, ...) -> c_int; }
fn main() {
    let mut input = Vec::new();
    io::stdin().read_to_end(&mut input).unwrap();
    println!("ENV_COUNT={}", std::env::vars_os().count());
    println!("CWD={}", std::env::current_dir().unwrap().display());
    println!("STDIN_BYTES={}", input.len());
    println!("ARGS={:?}", std::env::args().skip(1).collect::<Vec<_>>());
    let fd: c_int = std::env::args().find_map(|a| a.strip_prefix("--cfg=probe_fd_").and_then(|v| v.parse().ok())).unwrap_or(-1);
    println!("EXTRA_FD_RESULT={}", unsafe { fcntl(fd, 1) });
}
