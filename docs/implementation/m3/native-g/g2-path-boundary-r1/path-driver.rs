#![feature(rustc_private)]
extern crate rustc_driver;
extern crate rustc_interface;
extern crate rustc_middle;
extern crate rustc_span;

#[path = "/Users/sb/code/opensip-ai/opensip/providers/rust/src/sealed_vfs.rs"]
mod sealed_vfs;
#[path = "/Users/sb/code/opensip-ai/opensip/providers/rust/src/compiler_adapter.rs"]
mod compiler_adapter;

use std::path::PathBuf;
use std::sync::Arc;
use rustc_driver::{Callbacks, Compilation};
use rustc_interface::interface::{Compiler, Config};
use rustc_middle::ty::TyCtxt;
use sealed_vfs::SealedSource;

struct Probe { loader: Option<SealedSource>, analyzed: bool }
impl Callbacks for Probe {
    fn config(&mut self, config: &mut Config) {
        config.file_loader = Some(Box::new(self.loader.take().unwrap()));
    }
    fn after_analysis<'tcx>(&mut self, _: &Compiler, _: TyCtxt<'tcx>) -> Compilation {
        self.analyzed = true;
        println!("SEALED_AFTER_ANALYSIS");
        Compilation::Stop
    }
}
fn main() {
    let args: Vec<String> = std::env::args().collect();
    let root = PathBuf::from(&args[1]);
    let sysroot = &args[2];
    let mode = &args[3];
    let external_text = root.parent().unwrap().join("external.txt");
    let entry = match mode.as_str() {
        "root-shadow" => "mod helper; pub fn value() -> u8 { helper::value() }".to_owned(),
        "absolute-text" => format!("pub const TEXT: &str = include_str!({:?});", external_text.to_str().unwrap()),
        "escape-binary" => "pub const DATA: &[u8] = include_bytes!(\"../external.bin\");".to_owned(),
        "path-module" => "#[path=\"../external.rs\"] mod external; pub fn value() -> u8 { external::value() }".to_owned(),
        "disk-symlink" => "mod alias; pub fn value() -> u8 { alias::value() }".to_owned(),
        _ => panic!("unknown owned boundary fixture"),
    };
    let entries = [
        (PathBuf::from("lib.rs"), Arc::<[u8]>::from(entry.as_bytes())),
        (PathBuf::from("helper.rs"), Arc::<[u8]>::from(&b"pub fn value() -> u8 { 7 }"[..])),
        (PathBuf::from("data.bin"), Arc::<[u8]>::from(&b"\x00\xff"[..])),
        (PathBuf::from("text.txt"), Arc::<[u8]>::from(&b"sealed"[..])),
    ];
    let mut probe = Probe { loader: Some(SealedSource::new(root.clone(), entries).unwrap()), analyzed: false };
    let compiler_args = vec![args[0].clone(), "--crate-name".into(), "owned_sealed_source".into(), "--crate-type".into(), "lib".into(), "--edition".into(), "2024".into(), "--sysroot".into(), sysroot.clone(), "--emit".into(), "metadata".into(), root.join("lib.rs").to_str().unwrap().into(), "--out-dir".into(), root.parent().unwrap().join("output").to_str().unwrap().into()];
    rustc_driver::run_compiler(&compiler_args, &mut probe);
    assert!(probe.analyzed);
}
