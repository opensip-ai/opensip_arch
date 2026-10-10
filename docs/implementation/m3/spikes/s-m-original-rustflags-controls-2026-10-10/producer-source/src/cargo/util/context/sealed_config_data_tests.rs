use super::*;
use std::sync::atomic::{AtomicUsize, Ordering};
static NEXT: AtomicUsize = AtomicUsize::new(0);
fn inputs() -> (PathBuf, PathBuf, HashMap<String, ConfigValue>) {
    let root = std::env::temp_dir().join(format!(
        "projected-config-data-{}-{}",
        std::process::id(),
        NEXT.fetch_add(1, Ordering::Relaxed)
    ));
    std::fs::create_dir(&root).unwrap();
    std::fs::create_dir(root.join(".cargo")).unwrap();
    std::fs::write(root.join(".cargo/config.toml"), "[poisoned").unwrap();
    let home = root.join("private-home");
    std::fs::create_dir(&home).unwrap();
    std::fs::write(home.join("credentials.toml"), "[poisoned").unwrap();
    let leaf = ConfigValue::String("allow".into(), Definition::BuiltIn);
    let values = HashMap::from([(
        "resolver".into(),
        ConfigValue::Table(
            HashMap::from([("incompatible-rust-versions".into(), leaf)]),
            Definition::BuiltIn,
        ),
    )]);
    (root, home, values)
}
fn context() -> GlobalContext {
    let (root, home, values) = inputs();
    let mut gctx =
        GlobalContext::new_with_projected_values_data(Shell::new(), root, home, values).unwrap();
    // Debug replacement isolates typed config controls only; it is not host env admission
    // and does not undo the ordinary constructor's original captures.
    gctx.set_env(HashMap::new());
    gctx
}
#[test]
fn sealed_config_data_values_consumed_without_poisoned_disk() {
    let gctx = context();
    assert_eq!(
        gctx.get::<String>("resolver.incompatible-rust-versions")
            .unwrap(),
        "allow"
    );
    assert!(gctx.values().unwrap().contains_key("resolver"));
}
#[test]
fn sealed_config_data_second_install_refuses() {
    let gctx = context();
    assert!(gctx.set_values(HashMap::new()).is_err());
    assert!(gctx.values().unwrap().contains_key("resolver"));
}
#[test]
fn sealed_config_data_mutation_refuses() {
    let mut gctx = context();
    assert!(gctx.values_mut().is_err());
    assert_eq!(
        gctx.get::<String>("resolver.incompatible-rust-versions")
            .unwrap(),
        "allow"
    );
}
#[test]
fn sealed_config_data_reload_preserves_context_and_values() {
    let mut gctx = context();
    let cwd = gctx.cwd.clone();
    let home = gctx.home_path.clone().into_path_unlocked();
    assert!(gctx.reload_cwd().is_err());
    assert!(gctx.reload_rooted_at(cwd.join("absent")).is_err());
    assert_eq!(gctx.cwd, cwd);
    assert_eq!(gctx.home_path.clone().into_path_unlocked(), home);
    assert_eq!(
        gctx.get::<String>("resolver.incompatible-rust-versions")
            .unwrap(),
        "allow"
    );
}
#[test]
fn sealed_config_data_disk_and_include_readers_refuse_before_parse() {
    let gctx = context();
    assert!(
        gctx.load_values()
            .unwrap_err()
            .to_string()
            .contains("forbids disk")
    );
    assert!(gctx.load_values_unmerged().is_err());
    let mut seen = HashSet::new();
    assert!(
        gctx._load_file(
            &gctx.cwd.join(".cargo/config.toml"),
            &mut seen,
            true,
            WhyLoad::FileDiscovery
        )
        .is_err()
    );
    assert!(seen.is_empty());
}
#[test]
fn sealed_config_data_credentials_refuse_before_loading() {
    let gctx = context();
    assert!(gctx.load_credentials().is_err());
    assert!(!gctx.credential_values.filled());
}
#[test]
fn sealed_config_data_cli_none_noop_some_refuses() {
    let mut gctx = context();
    gctx.merge_cli_args().unwrap();
    gctx.cli_config = Some(vec![
        "resolver.incompatible-rust-versions='fallback'".into(),
    ]);
    assert!(gctx.merge_cli_args().is_err());
    assert_eq!(
        gctx.get::<String>("resolver.incompatible-rust-versions")
            .unwrap(),
        "allow"
    );
}
#[test]
fn sealed_config_data_environment_not_claimed_owned_or_frozen() {
    let mut gctx = context();
    gctx.set_env(HashMap::from([(
        "CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS".into(),
        "fallback".into(),
    )]));
    assert_eq!(
        gctx.get::<String>("resolver.incompatible-rust-versions")
            .unwrap(),
        "fallback"
    );
}
