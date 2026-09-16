use opensip_identity::{digest_hex, raw_sha256};
use opensip_platform_asset_trial::ReleaseDirectory;
use opensip_report_asset_trial::{
    AssetSource, FixturePin, fixture_completeness, verify_fixture_assets,
};
use std::fs::{self, File};
use std::io::{self, Read};
use std::os::unix::fs::symlink;
use std::path::PathBuf;
use std::sync::atomic::{AtomicU64, Ordering};

static NEXT: AtomicU64 = AtomicU64::new(0);
struct Tree(PathBuf);
impl Tree {
    fn new() -> Self {
        let path = std::env::temp_dir().join(format!(
            "opensip-assets-{}-{}",
            std::process::id(),
            NEXT.fetch_add(1, Ordering::Relaxed)
        ));
        fs::create_dir(&path).unwrap();
        Self(fs::canonicalize(path).unwrap())
    }
    fn handle(&self) -> ReleaseDirectory {
        ReleaseDirectory::from_retained_handle(File::open(&self.0).unwrap()).unwrap()
    }
}
impl Drop for Tree {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}
struct Source(ReleaseDirectory);
impl AssetSource for Source {
    type Reader = File;
    fn open_regular(&mut self, relative: &str) -> io::Result<File> {
        self.0.open_regular(relative)
    }
}

#[test]
fn real_bundle_verifies_and_same_length_replacement_refuses() {
    let tree = Tree::new();
    fs::create_dir_all(tree.0.join("share/report")).unwrap();
    let data = b"offline bytes";
    let schema = [9; 32];
    fs::write(tree.0.join("share/report/app.js"), data).unwrap();
    let manifest = format!(
        r#"{{"schemaVersion":1,"projectionSchemaSha256s":["{}"],"assets":[{{"path":"share/report/app.js","sha256":"{}","bytes":{},"role":"script"}}]}}"#,
        digest_hex(&schema),
        digest_hex(&raw_sha256(data)),
        data.len()
    );
    fs::write(tree.0.join("share/report/manifest.json"), &manifest).unwrap();
    let pin = FixturePin {
        root: "share/report".into(),
        manifest_path: "share/report/manifest.json".into(),
        manifest_bytes: manifest.len() as u64,
        manifest_sha256: raw_sha256(manifest.as_bytes()),
    };
    let mut source = Source(tree.handle());
    let verified = verify_fixture_assets(&mut source, &pin, &schema).unwrap();
    assert_eq!(verified.assets()[0].bytes(), data);
    fixture_completeness(
        &verified,
        &[
            "share/report/app.js".into(),
            "share/report/manifest.json".into(),
        ],
    )
    .unwrap();
    fs::write(tree.0.join("share/report/app.js"), b"changed bytes").unwrap();
    assert!(verify_fixture_assets(&mut source, &pin, &schema).is_err());
    assert_eq!(verified.assets()[0].bytes(), data);
}

#[test]
fn rejects_links_nonregular_files_and_traversal_at_every_segment() {
    let tree = Tree::new();
    fs::create_dir(tree.0.join("inside")).unwrap();
    fs::write(tree.0.join("inside/file"), b"valid").unwrap();
    symlink("inside", tree.0.join("linked-parent")).unwrap();
    symlink("inside/file", tree.0.join("linked-leaf")).unwrap();
    let handle = tree.handle();
    for relative in [
        "linked-parent/file",
        "linked-leaf",
        "inside",
        "inside/../inside/file",
        "./inside/file",
        "/inside/file",
        "inside//file",
        "inside/file/",
        "inside\\file",
        "inside/\0file",
    ] {
        assert!(handle.open_regular(relative).is_err(), "{relative:?}");
    }
    let socket_path = tree.0.join("socket");
    let _socket = std::os::unix::net::UnixListener::bind(socket_path).unwrap();
    assert!(handle.open_regular("socket").is_err());
    let fifo = tree.0.join("fifo");
    assert!(
        std::process::Command::new("/usr/bin/mkfifo")
            .arg(&fifo)
            .status()
            .unwrap()
            .success()
    );
    assert!(handle.open_regular("fifo").is_err()); // O_NONBLOCK avoids waiting for a writer.
    assert!(
        ReleaseDirectory::from_retained_handle(File::open(tree.0.join("inside/file")).unwrap())
            .is_err()
    );
}

#[test]
fn retained_handles_survive_root_and_leaf_path_replacements() {
    let tree = Tree::new();
    fs::create_dir(tree.0.join("root")).unwrap();
    fs::create_dir(tree.0.join("outside")).unwrap();
    fs::write(tree.0.join("root/file"), b"pinned").unwrap();
    fs::write(tree.0.join("outside/file"), b"attacker").unwrap();
    let handle =
        ReleaseDirectory::from_retained_handle(File::open(tree.0.join("root")).unwrap()).unwrap();
    fs::rename(tree.0.join("root"), tree.0.join("retained")).unwrap();
    symlink("outside", tree.0.join("root")).unwrap();
    let mut opened = handle.open_regular("file").unwrap();
    fs::rename(tree.0.join("retained/file"), tree.0.join("retained/old")).unwrap();
    symlink("../outside/file", tree.0.join("retained/file")).unwrap();
    assert!(handle.open_regular("file").is_err());
    let mut text = String::new();
    opened.read_to_string(&mut text).unwrap();
    assert_eq!(text, "pinned");
}
