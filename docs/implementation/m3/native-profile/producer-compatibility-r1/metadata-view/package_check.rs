mod core { pub use cargo::core::SourceId; }
#[path = "../native-source-join-kernel-2026-10-09/source_join.rs"] mod comparison;
use cargo::core::{SourceId, Shell};
use cargo::util::GlobalContext;
fn main() {
    let mode = std::env::args().nth(1).unwrap();
    let root = std::env::current_dir().unwrap().join("fixture");
    std::fs::create_dir(&root).unwrap();
    let manifest = root.join("Cargo.toml");
    std::fs::write(&manifest, "[package]\nname = \"source_view_fixture\"\nversion = \"1.0.0\"\nedition = \"2024\"\n[lib]\npath = \"lib.rs\"\n").unwrap();
    std::fs::write(root.join("lib.rs"), "// Fixture content is parsed only; never built or executed.\n").unwrap();
    let gctx = GlobalContext::new(Shell::new(), root.clone(), "/Users/sb/.cargo".into());
    let cases = [
        "registry+https://example.com/index",
        "sparse+https://example.com/index/",
        "git+https://example.com/repo#arbitrary-precise",
        "git+https://example.com/repo?branch=topic%2Ffoo%2Bbar#same",
        "git+https://example.com/repo?branch=topic+foo#same",
        "git+https://example.com/repo?branch=topic%26foo%3Dbar#same",
        "git+https://example.com/repo?branch=%E9%9B%AA#same",
        "git+https://example.com/repo?tag=v%2B1#same",
        "git+https://example.com/repo?rev=a%2Bb#same",
        "git+https://github.com/Example/Repo.git?branch=a%2Bb#same",
    ];
    for raw in cases {
        let source = SourceId::from_url(raw).unwrap();
        let package = cargo::ops::read_package(&manifest, source, &gctx).unwrap();
        let serialized = serde_json::to_value(package.serialized(gctx.cli_unstable(), package.manifest().unstable_features())).unwrap();
        let metadata_source = serialized["source"].as_str().unwrap();
        let matches = comparison::compare_nonpath(raw, Some(metadata_source)).is_ok();
        if mode == "candidate" { assert!(matches, "{raw} => {metadata_source}"); }
        println!("{}", serde_json::json!({"originalLockSource":raw,"metadataSource":metadata_source,"comparison":matches,"name":serialized["name"],"version":serialized["version"]}));
    }
    let source = SourceId::for_path(&root).unwrap();
    let package = cargo::ops::read_package(&manifest, source, &gctx).unwrap();
    let serialized = serde_json::to_value(package.serialized(gctx.cli_unstable(), package.manifest().unstable_features())).unwrap();
    assert!(serialized["source"].is_null());
    println!("11 actual Package serialization controls completed: {mode}");
}
