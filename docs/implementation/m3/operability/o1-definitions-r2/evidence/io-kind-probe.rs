fn main() {
    let _ = std::io::ErrorKind::StorageFull;
    for (name, raw) in [("EACCES",13),("ENOSPC",28),("EIO",5)] {
        let error = std::io::Error::from_raw_os_error(raw);
        println!("{}:{}:{:?}:{}", name, raw, error.kind(), error.raw_os_error().is_some());
    }
}
