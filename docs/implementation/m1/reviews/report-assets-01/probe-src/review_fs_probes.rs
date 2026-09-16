//! Independent reviewer filesystem probes. Review copy only.
use opensip_identity::{digest_hex, raw_sha256};
use opensip_platform_asset_trial::ReleaseDirectory;
use opensip_report_asset_trial::{
    AssetError, AssetSource, FixturePin, fixture_completeness, verify_fixture_assets,
};
use std::fs::{self, File};
use std::io::{self, Read};
use std::os::unix::fs::symlink;
use std::path::PathBuf;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::{Arc, mpsc};
use std::time::{Duration, Instant};

static NEXT: AtomicU64 = AtomicU64::new(0);
struct Tree(PathBuf);
impl Tree {
    fn new() -> Self {
        let path = std::env::temp_dir().join(format!(
            "review-probe-{}-{}",
            std::process::id(),
            NEXT.fetch_add(1, Ordering::Relaxed)
        ));
        fs::create_dir(&path).unwrap();
        Self(fs::canonicalize(path).unwrap())
    }
    fn at(&self, rel: &str) -> PathBuf {
        self.0.join(rel)
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
fn read_all(mut f: File) -> Vec<u8> {
    let mut v = Vec::new();
    f.read_to_end(&mut v).unwrap();
    v
}
const SCHEMA: [u8; 32] = [9; 32];

/// Names must be supplied sorted by byte order.
fn write_bundle(tree: &Tree, files: &[(&str, &[u8])]) -> FixturePin {
    let mut rows = Vec::new();
    for (name, data) in files {
        let path = format!("share/report/{name}");
        fs::create_dir_all(tree.at(&path).parent().unwrap()).unwrap();
        fs::write(tree.at(&path), data).unwrap();
        rows.push(format!(
            r#"{{"path":"{path}","sha256":"{}","bytes":{},"role":"script"}}"#,
            digest_hex(&raw_sha256(data)),
            data.len()
        ));
    }
    write_manifest(tree, &rows.join(","))
}
fn write_manifest(tree: &Tree, rows: &str) -> FixturePin {
    let manifest = format!(
        r#"{{"schemaVersion":1,"projectionSchemaSha256s":["{}"],"assets":[{rows}]}}"#,
        digest_hex(&SCHEMA)
    );
    fs::create_dir_all(tree.at("share/report")).unwrap();
    fs::write(tree.at("share/report/manifest.json"), &manifest).unwrap();
    FixturePin {
        root: "share/report".into(),
        manifest_path: "share/report/manifest.json".into(),
        manifest_bytes: manifest.len() as u64,
        manifest_sha256: raw_sha256(manifest.as_bytes()),
    }
}

#[test]
fn probe_symlink_at_each_depth_refuses_whole_bundle() {
    let files: [(&str, &[u8]); 2] = [("app.js", b"offline bytes"), ("sub/font.woff", b"font")];
    let control = Tree::new();
    let pin = write_bundle(&control, &files);
    assert!(verify_fixture_assets(&mut Source(control.handle()), &pin, &SCHEMA).is_ok());
    for (target, link_name, link_value) in [
        ("share", "share", "share.real"),
        ("share/report", "share/report", "report.real"),
        ("share/report/sub", "share/report/sub", "sub.real"),
        ("share/report/app.js", "share/report/app.js", "app.real"),
        ("share/report/manifest.json", "share/report/manifest.json", "manifest.real"),
    ] {
        let tree = Tree::new();
        let pin = write_bundle(&tree, &files);
        let real = tree.at(target).with_file_name(link_value);
        fs::rename(tree.at(target), &real).unwrap();
        symlink(link_value, tree.at(link_name)).unwrap();
        // The same path still resolves through ordinary path APIs.
        assert!(fs::metadata(tree.at("share/report/manifest.json")).is_ok());
        assert_eq!(
            verify_fixture_assets(&mut Source(tree.handle()), &pin, &SCHEMA).unwrap_err(),
            AssetError::Io,
            "{target}"
        );
    }
}

#[test]
fn probe_dangling_loops_file_parents_long_names_and_symlinked_root_handle() {
    let tree = Tree::new();
    fs::write(tree.at("file"), b"x").unwrap();
    fs::create_dir(tree.at("dir")).unwrap();
    symlink("missing", tree.at("dangling")).unwrap();
    symlink("loop", tree.at("loop")).unwrap();
    symlink("dir", tree.at("dirlink")).unwrap();
    let h = tree.handle();
    let long = "n".repeat(300);
    for rel in [
        "dangling", "dangling/x", "loop", "loop/x", "file/x", "missing", "dir", "dirlink",
        long.as_str(),
    ] {
        assert!(h.open_regular(rel).is_err(), "{rel}");
    }
    // Host-selected root opened through a symlink is accepted: root selection is host TCB.
    assert!(ReleaseDirectory::from_retained_handle(File::open(tree.at("dirlink")).unwrap()).is_ok());
}

#[test]
fn probe_special_files_never_block_or_open_as_assets() {
    let tree = Tree::new();
    let fifo = tree.at("fifo");
    assert!(
        std::process::Command::new("/usr/bin/mkfifo")
            .arg(&fifo)
            .status()
            .unwrap()
            .success()
    );
    let h = tree.handle();
    let (tx, rx) = mpsc::channel();
    std::thread::spawn(move || {
        let results: Vec<bool> = ["fifo", "fifo/x"]
            .iter()
            .map(|p| h.open_regular(p).is_err())
            .collect();
        tx.send(results).unwrap();
    });
    let results = rx
        .recv_timeout(Duration::from_secs(5))
        .expect("FIFO open blocked");
    assert_eq!(results, [true, true]);
    let dev = ReleaseDirectory::from_retained_handle(File::open("/dev").unwrap()).unwrap();
    for name in ["null", "zero", "random", "urandom"] {
        assert!(dev.open_regular(name).is_err(), "{name}");
    }
}

#[test]
fn probe_hardlink_admitted_and_write_through_caught_by_digest() {
    let tree = Tree::new();
    let pin = write_bundle(&tree, &[("app.js", b"offline bytes")]);
    fs::hard_link(tree.at("share/report/app.js"), tree.at("alias")).unwrap();
    let mut source = Source(tree.handle());
    let verified = verify_fixture_assets(&mut source, &pin, &SCHEMA).unwrap();
    fs::write(tree.at("alias"), b"changed bytes").unwrap();
    assert_eq!(
        verify_fixture_assets(&mut source, &pin, &SCHEMA).unwrap_err(),
        AssetError::Digest
    );
    assert_eq!(verified.assets()[0].bytes(), b"offline bytes");
}

#[test]
fn probe_case_alias_is_admitted_at_load_but_refused_by_exact_completeness() {
    let tree = Tree::new();
    fs::create_dir_all(tree.at("share/report")).unwrap();
    fs::write(tree.at("share/report/app.js"), b"offline bytes").unwrap();
    let insensitive = tree.at("share/report/APP.js").exists();
    eprintln!("PROBE case-insensitive temp filesystem: {insensitive}");
    let pin = write_manifest(
        &tree,
        &format!(
            r#"{{"path":"share/report/APP.js","sha256":"{}","bytes":13,"role":"script"}}"#,
            digest_hex(&raw_sha256(b"offline bytes"))
        ),
    );
    let result = verify_fixture_assets(&mut Source(tree.handle()), &pin, &SCHEMA);
    if insensitive {
        let bundle = result.unwrap();
        assert_eq!(bundle.assets()[0].path(), "share/report/APP.js");
        let enumerated = vec![
            "share/report/app.js".to_string(),
            "share/report/manifest.json".to_string(),
        ];
        assert_eq!(
            fixture_completeness(&bundle, &enumerated),
            Err(AssetError::Unlisted)
        );
        // Pinned manifest path alias also resolves on this filesystem.
        let alias_pin = FixturePin {
            manifest_path: "share/report/MANIFEST.JSON".into(),
            ..pin.clone()
        };
        assert!(verify_fixture_assets(&mut Source(tree.handle()), &alias_pin, &SCHEMA).is_ok());
    } else {
        assert_eq!(result.unwrap_err(), AssetError::Io);
    }
}

#[test]
fn probe_retained_root_survives_real_directory_substitution() {
    let tree = Tree::new();
    fs::create_dir(tree.at("release")).unwrap();
    let inner = Tree(tree.at("release"));
    let pin = write_bundle(&inner, &[("app.js", b"offline bytes")]);
    let handle = ReleaseDirectory::from_retained_handle(File::open(tree.at("release")).unwrap()).unwrap();
    fs::rename(tree.at("release"), tree.at("release.old")).unwrap();
    std::mem::forget(inner);
    fs::create_dir(tree.at("release")).unwrap();
    let attacker = Tree(tree.at("release"));
    let _ = write_bundle(&attacker, &[("app.js", b"attacker byte")]);
    std::mem::forget(attacker);
    let bundle = verify_fixture_assets(&mut Source(handle), &pin, &SCHEMA).unwrap();
    assert_eq!(bundle.assets()[0].bytes(), b"offline bytes");
}

fn race(tree: &Tree, swap: impl Fn() + Send + 'static, rel: &'static str) -> (u64, u64, u64) {
    let stop = Arc::new(AtomicBool::new(false));
    let flag = stop.clone();
    let worker = std::thread::spawn(move || {
        while !flag.load(Ordering::Relaxed) {
            swap();
        }
    });
    let handle = tree.handle();
    let naive = tree.at(rel);
    let (mut ok, mut refused, mut naive_evil) = (0, 0, 0);
    let deadline = Instant::now() + Duration::from_millis(1500);
    while Instant::now() < deadline {
        match handle.open_regular(rel) {
            Ok(file) => {
                assert_eq!(read_all(file), b"good", "handle walk yielded outside bytes");
                ok += 1;
            }
            Err(_) => refused += 1,
        }
        if fs::read(&naive).is_ok_and(|b| b == b"evil") {
            naive_evil += 1;
        }
    }
    stop.store(true, Ordering::Relaxed);
    worker.join().unwrap();
    (ok, refused, naive_evil)
}

#[test]
fn probe_concurrent_parent_and_leaf_symlink_swaps_never_yield_outside_bytes() {
    let tree = Tree::new();
    fs::create_dir_all(tree.at("share/report")).unwrap();
    fs::create_dir_all(tree.at("evil/report")).unwrap();
    fs::write(tree.at("share/report/app.js"), b"good").unwrap();
    fs::write(tree.at("evil/report/app.js"), b"evil").unwrap();
    symlink("../evil/report", tree.at("share/report.link")).unwrap();
    symlink("../../evil/report/app.js", tree.at("share/report/app.link")).unwrap();

    let root = tree.0.clone();
    let parent = race(
        &tree,
        move || {
            let p = |s: &str| root.join(s);
            fs::rename(p("share/report"), p("share/report.hold")).unwrap();
            fs::rename(p("share/report.link"), p("share/report")).unwrap();
            fs::rename(p("share/report"), p("share/report.link")).unwrap();
            fs::rename(p("share/report.hold"), p("share/report")).unwrap();
        },
        "share/report/app.js",
    );
    let root = tree.0.clone();
    let leaf = race(
        &tree,
        move || {
            let p = |s: &str| root.join(s);
            fs::rename(p("share/report/app.js"), p("share/report/app.hold")).unwrap();
            fs::rename(p("share/report/app.link"), p("share/report/app.js")).unwrap();
            fs::rename(p("share/report/app.js"), p("share/report/app.link")).unwrap();
            fs::rename(p("share/report/app.hold"), p("share/report/app.js")).unwrap();
        },
        "share/report/app.js",
    );
    eprintln!("PROBE race parent (ok, refused, naive-path-evil) = {parent:?}; leaf = {leaf:?}");
    for (ok, refused, naive_evil) in [parent, leaf] {
        assert!(ok > 0 && refused > 0, "race window not exercised");
        assert!(naive_evil > 0, "control: naive path reads never observed the swap");
    }
}
