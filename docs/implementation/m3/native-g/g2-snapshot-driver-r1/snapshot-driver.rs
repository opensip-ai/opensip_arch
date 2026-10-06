#![feature(rustc_private)]
extern crate rustc_driver;
extern crate rustc_interface;
extern crate rustc_middle;
extern crate rustc_span;
extern crate opensip_identity;

#[path = "/Users/sb/code/opensip-ai/opensip-g2-source-snapshot/providers/rust/src/sealed_vfs.rs"]
mod sealed_vfs;
#[path = "/Users/sb/code/opensip-ai/opensip-g2-source-snapshot/providers/rust/src/compiler_adapter.rs"]
mod compiler_adapter;
#[path = "/Users/sb/code/opensip-ai/opensip-g2-source-snapshot/providers/rust/src/source_snapshot.rs"]
mod source_snapshot;

use opensip_identity::{canonical_bytes, digest_hex, hash_canonical_value, raw_sha256, IdentityDomain, JsonInteger, JsonValue, ObjectInput, RegisteredSchemas, RetainedInputs};
use rustc_driver::{Callbacks, Compilation};
use rustc_interface::interface::{Compiler, Config};
use rustc_middle::ty::TyCtxt;
use sealed_vfs::SealedSource;
use source_snapshot::{from_snapshot, SnapshotSourceError};
use std::collections::BTreeMap;
use std::path::{Path, PathBuf};

struct Probe { source: Option<SealedSource>, analyzed: bool }
impl Callbacks for Probe {
    fn config(&mut self, config: &mut Config) {
        config.file_loader = Some(Box::new(self.source.take().unwrap()));
    }
    fn after_analysis<'tcx>(&mut self, _: &Compiler, _: TyCtxt<'tcx>) -> Compilation {
        self.analyzed = true;
        println!("VERIFIED_SNAPSHOT_AFTER_ANALYSIS");
        Compilation::Stop
    }
}
fn object(entries: impl IntoIterator<Item = (&'static str, JsonValue)>) -> JsonValue {
    JsonValue::Object(entries.into_iter().map(|(key, value)| (key.into(), value)).collect())
}
fn text(value: &str) -> JsonValue { JsonValue::String(value.into()) }
fn number(value: usize) -> JsonValue { JsonValue::Integer(JsonInteger::new(value as i128).unwrap()) }
fn main() {
    let args: Vec<_> = std::env::args().collect();
    let root = PathBuf::from(&args[1]);
    let sysroot = &args[2];
    let mode = &args[3];
    let public_sources = Path::new(&args[4]);
    let documents: Vec<_> = RegisteredSchemas::source_requirements().iter().map(|pin| std::fs::read(public_sources.join(pin.source_path())).unwrap()).collect();
    let registry = RegisteredSchemas::from_sources(&documents.iter().map(Vec::as_slice).collect::<Vec<_>>()).unwrap();
    let sources: [(&str, &[u8]); 4] = [
        ("helper.rs", b"pub fn value() -> u8 { 7 }"),
        ("lib.rs", b"mod helper; pub fn value() -> u8 { helper::value() }"),
        ("notes.md", b"retained data"),
        ("zero", b""),
    ];
    let mut rows: Vec<_> = sources.iter().map(|(path, bytes)| object([
        ("path", text(path)),
        ("sha256", text(&digest_hex(&raw_sha256(bytes)))),
        ("bytes", number(bytes.len() + usize::from(mode == "wrong-length" && *path == "helper.rs"))),
    ])).collect();
    if mode == "collision" {
        rows.insert(3, object([
            ("path", text("notes.md/child")),
            ("sha256", text(&digest_hex(&raw_sha256(sources[2].1)))),
            ("bytes", number(sources[2].1.len())),
        ]));
    }
    let mut descriptor = object([
        ("schemaVersion", number(2)),
        ("projectId", text(&format!("prj1-{}", "0".repeat(64)))),
        ("sourceInventory", JsonValue::Array(rows)),
        ("resolvedConfigDigest", text(&"a".repeat(64))),
        ("scopeDigest", text(&"b".repeat(64))),
        ("vcsDigest", text(&"c".repeat(64))),
    ]);
    let id = format!("snapshot2:{}", digest_hex(&hash_canonical_value("snapshot", &descriptor).unwrap()));
    if mode == "snapshot-mismatch" {
        let JsonValue::Object(ref mut fields) = descriptor else { unreachable!() };
        fields.insert("scopeDigest".into(), text(&"d".repeat(64)));
    }
    // The fixture owns inert identity literals; no full capture/context claim.
    let _ = canonical_bytes(&descriptor).unwrap();
    let objects = BTreeMap::from([(id.clone(), ObjectInput { domain: IdentityDomain::Snapshot, descriptor })]);
    let mut blobs: BTreeMap<_, _> = sources.iter().map(|(_, bytes)| (raw_sha256(bytes), bytes.to_vec())).collect();
    if mode == "tampered" { blobs.insert(raw_sha256(sources[0].1), b"pub fn value() -> u8 { 99 }".to_vec()); }
    if mode == "missing" { blobs.remove(&raw_sha256(sources[0].1)); }
    let source = match from_snapshot(&RetainedInputs::new(&registry, &objects, &blobs), &id, root.clone(), 10_000_000) {
        Ok(source) => { assert_eq!(mode, "positive"); source }
        Err(error) => {
            let expected = match (mode.as_str(), &error) {
                ("tampered", SnapshotSourceError::Retained(opensip_identity::RetainedInputError::BlobDigest)) |
                ("missing", SnapshotSourceError::Retained(opensip_identity::RetainedInputError::MissingBlob(_))) |
                ("wrong-length", SnapshotSourceError::Retained(opensip_identity::RetainedInputError::BlobLength)) |
                ("snapshot-mismatch", SnapshotSourceError::Retained(opensip_identity::RetainedInputError::ObjectIdentity)) => true,
                ("collision", SnapshotSourceError::Namespace(error)) => error.kind() == std::io::ErrorKind::InvalidInput,
                _ => false,
            };
            assert!(expected, "unexpected refusal: {error:?}");
            println!("REFUSED_BEFORE_COMPILER:{mode}");
            return;
        }
    };
    assert!(source.file_exists(Path::new("notes.md")) && source.file_exists(Path::new("zero")));
    assert!(!root.join("lib.rs").exists());
    let mut probe = Probe { source: Some(source), analyzed: false };
    let compiler_args = vec![args[0].clone(), "--crate-name".into(), "owned_snapshot".into(), "--crate-type".into(), "lib".into(), "--edition".into(), "2024".into(), "--sysroot".into(), sysroot.clone(), "--emit".into(), "metadata".into(), root.join("lib.rs").to_str().unwrap().into(), "--out-dir".into(), root.to_str().unwrap().into()];
    rustc_driver::run_compiler(&compiler_args, &mut probe);
    assert!(probe.analyzed);
}
