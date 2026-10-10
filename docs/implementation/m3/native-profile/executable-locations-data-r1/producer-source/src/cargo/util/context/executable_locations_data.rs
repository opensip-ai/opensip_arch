//! Required two-getter executable LOCATION DATA, not closure/Tool admission.
use super::explicit_context_data::{InitialStateData, new_with_initial_state_data};
use super::*;
pub(super) struct ExecutableLocationsData {
    pub(super) cargo: PathBuf,
    pub(super) rustdoc: PathBuf,
}
impl GlobalContext {
    pub(super) fn install_executable_locations_data(
        &mut self,
        data: ExecutableLocationsData,
    ) -> CargoResult<()> {
        if !self.projected_values_data {
            bail!("initialized configuration data required");
        }
        // Absolute syntax only: no existence/signature/tree/permission proof.
        if !data.cargo.is_absolute() || !data.rustdoc.is_absolute() {
            bail!("absolute executable location data required");
        }
        // Both checks precede either write. &mut excludes concurrent safe aliases.
        if self.cargo_exe.get().is_some() || self.rustdoc.get().is_some() {
            bail!("executable location data already queried or installed");
        }
        self.cargo_exe
            .set(data.cargo)
            .map_err(|_| anyhow!("cargo location data already set"))?;
        self.rustdoc
            .set(data.rustdoc)
            .map_err(|_| anyhow!("rustdoc location data already set"))?;
        Ok(())
    }
}
pub(super) fn new_with_executable_locations_data(
    shell: Shell,
    cwd: PathBuf,
    home: PathBuf,
    values: HashMap<String, ConfigValue>,
    initial: InitialStateData,
    locations: ExecutableLocationsData,
) -> CargoResult<GlobalContext> {
    if !locations.cargo.is_absolute() || !locations.rustdoc.is_absolute() {
        bail!("absolute executable location data required");
    }
    let mut context = new_with_initial_state_data(shell, cwd, home, values, initial)?;
    context.install_executable_locations_data(locations)?;
    Ok(context)
}
#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static NEXT: AtomicUsize = AtomicUsize::new(0);
    fn roots() -> (PathBuf, PathBuf) {
        let root = std::env::temp_dir().join(format!(
            "executable-location-data-{}-{}",
            std::process::id(),
            NEXT.fetch_add(1, Ordering::Relaxed)
        ));
        std::fs::create_dir(&root).unwrap();
        let home = root.join("home");
        std::fs::create_dir(&home).unwrap();
        (root, home)
    }
    fn initial(environment: HashMap<String, String>) -> InitialStateData {
        InitialStateData {
            environment,
            jobserver: None,
            nightly_features_allowed: false,
        }
    }
    fn locations() -> ExecutableLocationsData {
        ExecutableLocationsData {
            cargo: PathBuf::from("/unadmitted/operational/cargo-data"),
            rustdoc: PathBuf::from("/unadmitted/operational/rustdoc-data"),
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
    fn fixture(env: HashMap<String, String>, values: HashMap<String, ConfigValue>) -> Fixture {
        let (root, home) = roots();
        let ctx = new_with_executable_locations_data(
            Shell::new(),
            root.clone(),
            home,
            values,
            initial(env),
            locations(),
        )
        .unwrap();
        Fixture { ctx, root }
    }
    #[test]
    fn executable_locations_data_actual_getters_prefilled_before_escape_repeat_exact() {
        let f = fixture(HashMap::new(), HashMap::new());
        assert!(f.ctx.cargo_exe.get().is_some() && f.ctx.rustdoc.get().is_some());
        for _ in 0..2 {
            assert_eq!(
                f.ctx.cargo_exe().unwrap(),
                Path::new("/unadmitted/operational/cargo-data")
            );
            assert_eq!(
                f.ctx.rustdoc().unwrap(),
                Path::new("/unadmitted/operational/rustdoc-data")
            );
        }
    }
    #[test]
    fn executable_locations_data_hostile_supplied_env_does_not_select_getter_paths() {
        let f = fixture(
            HashMap::from([
                ("CARGO".into(), "/unadmitted/hostile/cargo".into()),
                ("RUSTDOC".into(), "/unadmitted/hostile/rustdoc".into()),
                ("PATH".into(), "/unadmitted/hostile/search".into()),
            ]),
            HashMap::new(),
        );
        assert_eq!(
            f.ctx.cargo_exe().unwrap(),
            Path::new("/unadmitted/operational/cargo-data")
        );
        assert_eq!(
            f.ctx.rustdoc().unwrap(),
            Path::new("/unadmitted/operational/rustdoc-data")
        );
    }
    #[test]
    fn executable_locations_data_poisoned_build_rustdoc_not_lazily_interpreted() {
        let values = HashMap::from([(
            "build".into(),
            ConfigValue::Table(
                HashMap::from([(
                    "rustdoc".into(),
                    ConfigValue::Boolean(true, Definition::BuiltIn),
                )]),
                Definition::BuiltIn,
            ),
        )]);
        let f = fixture(HashMap::new(), values);
        assert_eq!(
            f.ctx.rustdoc().unwrap(),
            Path::new("/unadmitted/operational/rustdoc-data")
        );
        assert!(!f.ctx.build_config.filled());
    }
    #[test]
    fn executable_locations_data_relative_or_empty_inputs_refuse_before_constructor() {
        for (cargo, rustdoc) in [
            ("", "/unadmitted/rustdoc"),
            ("relative-cargo", "/unadmitted/rustdoc"),
            ("/unadmitted/cargo", "relative-rustdoc"),
        ] {
            let (root, home) = roots();
            let result = new_with_executable_locations_data(
                Shell::new(),
                root.clone(),
                home,
                HashMap::new(),
                initial(HashMap::new()),
                ExecutableLocationsData {
                    cargo: cargo.into(),
                    rustdoc: rustdoc.into(),
                },
            );
            assert!(result.is_err());
            std::fs::remove_dir_all(root).unwrap();
        }
    }
    #[test]
    fn executable_locations_data_reinstall_refuses_preserves_both_cells() {
        let mut f = fixture(HashMap::new(), HashMap::new());
        assert!(
            f.ctx
                .install_executable_locations_data(ExecutableLocationsData {
                    cargo: "/unadmitted/new/cargo".into(),
                    rustdoc: "/unadmitted/new/rustdoc".into()
                })
                .is_err()
        );
        assert_eq!(
            f.ctx.cargo_exe().unwrap(),
            Path::new("/unadmitted/operational/cargo-data")
        );
        assert_eq!(
            f.ctx.rustdoc().unwrap(),
            Path::new("/unadmitted/operational/rustdoc-data")
        );
    }
    #[test]
    fn executable_locations_data_one_filled_cell_refuses_without_partial_second_write() {
        let (root, home) = roots();
        let mut ctx = new_with_initial_state_data(
            Shell::new(),
            root.clone(),
            home,
            HashMap::new(),
            initial(HashMap::new()),
        )
        .unwrap();
        ctx.cargo_exe
            .set(PathBuf::from("/unadmitted/already/cargo"))
            .unwrap();
        assert!(ctx.install_executable_locations_data(locations()).is_err());
        assert_eq!(
            ctx.cargo_exe.get().unwrap(),
            Path::new("/unadmitted/already/cargo")
        );
        assert!(ctx.rustdoc.get().is_none());
        drop(ctx);
        std::fs::remove_dir_all(root).unwrap();
    }
}
