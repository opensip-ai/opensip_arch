use super::*;
use crate::core::Shell;
use std::sync::atomic::{AtomicUsize, Ordering};
static NEXT: AtomicUsize = AtomicUsize::new(0);

fn fixture() -> (PathBuf, SourceId, GlobalContext) {
    let root = std::env::temp_dir().join(format!(
        "sealed-eligibility-{}-{}",
        std::process::id(),
        NEXT.fetch_add(1, Ordering::Relaxed)
    ));
    fs::create_dir(&root).unwrap();
    let source =
        SourceId::from_url("git+https://example.com/eligibility#declared-revision").unwrap();
    let gctx = GlobalContext::new(Shell::new(), root.clone(), "/Users/sb/.cargo".into());
    (root, source, gctx)
}
fn manifest(root: &Path, location: &str, name: &str, extra: &str) {
    let dir = root.join(location);
    fs::create_dir_all(&dir).unwrap();
    fs::write(dir.join("Cargo.toml"), format!("[package]\nname = \"{name}\"\nversion = \"1.0.0\"\nedition = \"2024\"\n{extra}\n[lib]\npath = \"lib.rs\"\n")).unwrap();
    fs::write(
        dir.join("lib.rs"),
        "// Parser fixture only; never built or executed.\n",
    )
    .unwrap();
}
fn required(name: &str, source: SourceId) -> PackageId {
    PackageId::new(name.into(), "1.0.0".parse().unwrap(), source)
}
#[test]
fn sealed_required_eligibility_not_loaded_is_not_missing() {
    let (root, source, gctx) = fixture();
    let tree = RecursivePathSource::new(&root, source, &gctx);
    assert!(matches!(
        tree.sealed_required_package(required("wanted", source)),
        Err(SealedEligibilityRefusal::NotLoaded)
    ));
}
#[test]
fn sealed_required_eligibility_single_retains_manifest() {
    let (root, source, gctx) = fixture();
    manifest(&root, "nested", "wanted", "");
    let mut tree = RecursivePathSource::new(&root, source, &gctx);
    tree.load().unwrap();
    assert_eq!(
        tree.sealed_required_package(required("wanted", source))
            .unwrap()
            .manifest_path(),
        root.join("nested/Cargo.toml")
    );
    assert!(tree.warned_duplicate.is_empty());
}
#[test]
fn sealed_required_eligibility_duplicate_publish_false_still_ambiguous() {
    let (root, source, gctx) = fixture();
    manifest(&root, "one", "wanted", "publish = false");
    manifest(&root, "two", "wanted", "publish = false");
    let mut tree = RecursivePathSource::new(&root, source, &gctx);
    tree.load().unwrap();
    let Err(SealedEligibilityRefusal::Ambiguous(packages)) =
        tree.sealed_required_package(required("wanted", source))
    else {
        panic!("duplicate required package must refuse")
    };
    assert_eq!(packages.len(), 2);
    let paths: HashSet<_> = packages
        .iter()
        .map(|p| p.manifest_path().to_owned())
        .collect();
    assert_eq!(
        paths,
        HashSet::from([root.join("one/Cargo.toml"), root.join("two/Cargo.toml")])
    );
    assert!(tree.warned_duplicate.is_empty());
}
#[test]
fn sealed_required_eligibility_foreign_duplicate_not_flattened() {
    let (root, source, gctx) = fixture();
    manifest(&root, "wanted", "wanted", "");
    manifest(&root, "one", "foreign", "");
    manifest(&root, "two", "foreign", "");
    let mut tree = RecursivePathSource::new(&root, source, &gctx);
    tree.load().unwrap();
    assert_eq!(
        tree.sealed_required_package(required("wanted", source))
            .unwrap()
            .name()
            .as_str(),
        "wanted"
    );
    assert_eq!(tree.packages[&required("foreign", source)].len(), 2);
    assert!(tree.warned_duplicate.is_empty());
}
#[test]
fn sealed_required_eligibility_missing_is_plain_data() {
    let (root, source, gctx) = fixture();
    manifest(&root, "foreign", "foreign", "");
    let mut tree = RecursivePathSource::new(&root, source, &gctx);
    tree.load().unwrap();
    assert!(matches!(
        tree.sealed_required_package(required("wanted", source)),
        Err(SealedEligibilityRefusal::Missing)
    ));
}
#[test]
fn sealed_required_eligibility_virtual_root_and_sibling_preserved() {
    let (root, source, gctx) = fixture();
    fs::write(root.join("Cargo.toml"),"[workspace]\nmembers = [\"member\", \"sibling\"]\nresolver = \"3\"\n[workspace.package]\nversion = \"1.0.0\"\n").unwrap();
    manifest(&root, "sibling", "sibling", "");
    fs::create_dir(root.join("member")).unwrap();
    fs::write(root.join("member/Cargo.toml"),"[package]\nname = \"wanted\"\nversion.workspace = true\nedition = \"2024\"\n[dependencies]\nsibling = { path = \"../sibling\" }\n[lib]\npath = \"lib.rs\"\n").unwrap();
    fs::write(root.join("member/lib.rs"), "// Parsed only\n").unwrap();
    let mut tree = RecursivePathSource::new(&root, source, &gctx);
    tree.load().unwrap();
    assert_eq!(tree.packages.len(), 2);
    assert_eq!(
        tree.sealed_required_package(required("wanted", source))
            .unwrap()
            .manifest_path(),
        root.join("member/Cargo.toml")
    );
    assert!(root.join("Cargo.toml").is_file() && root.join("sibling/Cargo.toml").is_file());
}
#[test]
fn sealed_required_eligibility_unrelated_malformed_remains_file() {
    let (root, source, gctx) = fixture();
    manifest(&root, "wanted", "wanted", "");
    fs::create_dir(root.join("broken")).unwrap();
    fs::write(root.join("broken/Cargo.toml"), "[broken").unwrap();
    let mut tree = RecursivePathSource::new(&root, source, &gctx);
    tree.load().unwrap();
    assert!(
        tree.sealed_required_package(required("wanted", source))
            .is_ok()
    );
    assert_eq!(
        fs::read_to_string(root.join("broken/Cargo.toml")).unwrap(),
        "[broken"
    );
}
