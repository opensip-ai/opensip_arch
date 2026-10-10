//! Conditional CRA1 actual consumer controls, not projected/config/source admission.
use super::config_merge_data::{ConfigInputData, merge_config_inputs_data};
use super::*;
use crate::core::SourceId;
use std::sync::atomic::{AtomicUsize, Ordering};
static NEXT: AtomicUsize = AtomicUsize::new(0);
fn input(path: &str, text: &str) -> ConfigInputData {
    ConfigInputData {
        bytes: text.as_bytes().to_vec(),
        definition: Definition::Path(PathBuf::from(path)),
    }
}
struct Fixture {
    ctx: GlobalContext,
    root: PathBuf,
}
impl Drop for Fixture {
    fn drop(&mut self) {
        std::fs::remove_dir_all(&self.root).unwrap();
    }
}
fn context(inputs: &[ConfigInputData]) -> Fixture {
    let merged = merge_config_inputs_data(inputs).unwrap();
    let ConfigValue::Table(values, _) = merged.value else {
        panic!("root table")
    };
    let root = std::env::temp_dir().join(format!(
        "registry-definition-data-{}-{}",
        std::process::id(),
        NEXT.fetch_add(1, Ordering::Relaxed)
    ));
    std::fs::create_dir(&root).unwrap();
    let home = root.join("home");
    std::fs::create_dir(&home).unwrap();
    std::fs::create_dir(root.join(".cargo")).unwrap();
    std::fs::write(root.join(".cargo/config.toml"), "[poisoned").unwrap();
    // Entire supplied merged map, NOT a selected semantic projection. Only
    // get_registry_index is exercised; no SourceId load/read/cache/fetch follows.
    let mut ctx =
        GlobalContext::new_with_projected_values_data(Shell::new(), root.clone(), home, values)
            .unwrap();
    ctx.set_env(HashMap::new()); // Getter isolation, not owned constructor captures.
    Fixture { ctx, root }
}
#[test]
fn registry_definition_controls_nearest_relative_file_index_keeps_original_root() {
    let inputs = [
        input(
            "/unadmitted/near/.cargo/config.toml",
            "[registries.local]\nindex='file:relative-index'\n",
        ),
        input(
            "/unadmitted/far/.cargo/config.toml",
            "[registries.local]\nindex='file:other-index'\n",
        ),
    ];
    let f = context(&inputs);
    let url = f.ctx.get_registry_index("local").unwrap();
    assert_eq!(
        url.to_file_path().unwrap(),
        PathBuf::from("/unadmitted/near/relative-index")
    );
    assert_eq!(
        f.ctx
            .get_string("registries.local.index")
            .unwrap()
            .unwrap()
            .val,
        "file:relative-index"
    );
    let sid = SourceId::for_alt_registry(&url, "local").unwrap();
    assert!(sid.is_registry());
    assert_eq!(sid.url(), &url);
}
#[test]
fn registry_definition_controls_reversed_original_order_changes_effective_root() {
    let inputs = [
        input(
            "/unadmitted/far/.cargo/config.toml",
            "[registries.local]\nindex='file:other-index'\n",
        ),
        input(
            "/unadmitted/near/.cargo/config.toml",
            "[registries.local]\nindex='file:relative-index'\n",
        ),
    ];
    let f = context(&inputs);
    assert_eq!(
        f.ctx
            .get_registry_index("local")
            .unwrap()
            .to_file_path()
            .unwrap(),
        PathBuf::from("/unadmitted/far/other-index")
    );
}
#[test]
fn registry_definition_controls_distinct_aliases_keep_per_leaf_roots() {
    let inputs = [
        input(
            "/unadmitted/a/.cargo/config.toml",
            "[registries.alpha]\nindex='file:index'\n",
        ),
        input(
            "/unadmitted/b/.cargo/config.toml",
            "[registries.beta]\nindex='file:index'\n",
        ),
    ];
    let f = context(&inputs);
    for (name, root) in [
        ("alpha", "/unadmitted/a/index"),
        ("beta", "/unadmitted/b/index"),
    ] {
        assert_eq!(
            f.ctx
                .get_registry_index(name)
                .unwrap()
                .to_file_path()
                .unwrap(),
            PathBuf::from(root)
        );
    }
}
#[test]
fn registry_definition_controls_sparse_source_interpretation_keeps_supplied_string() {
    let raw = "sparse+https://example.invalid/index/";
    let inputs = [input(
        "/unadmitted/a/.cargo/config.toml",
        &format!("[registries.test]\nindex='{raw}'\n"),
    )];
    let f = context(&inputs);
    let url = f.ctx.get_registry_index("test").unwrap();
    let sid = SourceId::for_alt_registry(&url, "test").unwrap();
    assert!(sid.is_sparse());
    assert_eq!(
        f.ctx
            .get_string("registries.test.index")
            .unwrap()
            .unwrap()
            .val,
        raw
    );
}
#[test]
fn registry_definition_controls_missing_or_invalid_name_never_defaults() {
    let inputs = [input(
        "/unadmitted/a/.cargo/config.toml",
        "[registries.'bad!']\nindex='https://example.invalid/index'\n",
    )];
    let f = context(&inputs);
    assert!(f.ctx.get_registry_index("missing").is_err());
    assert!(f.ctx.get_registry_index("bad!").is_err());
}
#[test]
fn registry_definition_controls_password_index_refuses_actual_consumer() {
    let inputs = [input(
        "/unadmitted/a/.cargo/config.toml",
        "[registries.test]\nindex='https://user:secret@example.invalid/index'\n",
    )];
    let f = context(&inputs);
    assert!(f.ctx.get_registry_index("test").is_err());
}
#[test]
fn registry_definition_controls_wrong_type_and_bare_relative_path_refuse() {
    for value in ["true", "1", "'relative-index'"] {
        let inputs = [input(
            "/unadmitted/a/.cargo/config.toml",
            &format!("[registries.test]\nindex={value}\n"),
        )];
        let f = context(&inputs);
        assert!(f.ctx.get_registry_index("test").is_err());
    }
}
#[test]
fn registry_definition_controls_full_conversion_failure_before_alias_lookup() {
    let inputs = [
        input(
            "/unadmitted/a/.cargo/config.toml",
            "[registries.test]\nindex='https://example.invalid/index'\n",
        ),
        input("/unadmitted/b/.cargo/config.toml", "[ignored]\nfloat=1.5\n"),
    ];
    let Err(error) = merge_config_inputs_data(&inputs) else {
        panic!("must refuse")
    };
    assert_eq!(error.input_index, 1);
}
