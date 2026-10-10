--- parent/src/cargo/util/context/mod.rs
+++ candidate/src/cargo/util/context/mod.rs
@@ -252,6 +252,7 @@
     crates_io_source_id: OnceLock<SourceId>,
     /// If false, don't cache `rustc --version --verbose` invocations
     cache_rustc_info: bool,
+    experimental_rustc: Option<cargo_util::ProcessBuilder>,
     /// Creation time of this config, used to output the total build time
     creation_time: Instant,
     /// Target Directory via resolved Cli parameter
@@ -356,6 +357,7 @@
             easy: Default::default(),
             crates_io_source_id: Default::default(),
             cache_rustc_info,
+            experimental_rustc: None,
             creation_time: Instant::now(),
             target_dir: None,
             env,
@@ -378,6 +380,63 @@
         }
     }
 
+    /// Explicit outside-product experiment state. Supplied paths/config/query
+    /// vectors are data, not host source/profile or executable admission.
+    pub(crate) fn new_experimental_query_context(
+        shell: Shell,
+        cwd: PathBuf,
+        homedir: PathBuf,
+        values: HashMap<String, ConfigValue>,
+        query_base: cargo_util::ProcessBuilder,
+    ) -> GlobalContext {
+        let context = GlobalContext {
+            home_path: Filesystem::new(homedir),
+            shell: Mutex::new(shell),
+            cwd,
+            search_stop_path: None,
+            values: Default::default(),
+            projected_values_data: true,
+            credential_values: Default::default(),
+            cli_config: None,
+            cargo_exe: Default::default(),
+            rustdoc: Default::default(),
+            extra_verbose: false,
+            frozen: false,
+            locked: false,
+            offline: false,
+            jobserver: None,
+            unstable_flags: CliUnstable::default(),
+            unstable_flags_cli: None,
+            easy: Default::default(),
+            crates_io_source_id: Default::default(),
+            cache_rustc_info: false,
+            experimental_rustc: Some(query_base),
+            creation_time: Instant::now(),
+            target_dir: None,
+            env: Env::from_map(HashMap::new()),
+            updated_sources: Default::default(),
+            credential_cache: Default::default(),
+            registry_config: Default::default(),
+            package_cache_lock: CacheLocker::new(),
+            http_config: Default::default(),
+            future_incompat_config: Default::default(),
+            net_config: Default::default(),
+            build_config: Default::default(),
+            target_cfgs: Default::default(),
+            doc_extern_map: Default::default(),
+            progress_config: ProgressConfig::default(),
+            env_config: Default::default(),
+            nightly_features_allowed: false,
+            ws_roots: Default::default(),
+            global_cache_tracker: Default::default(),
+            deferred_global_last_use: Default::default(),
+        };
+        context
+            .set_values(values)
+            .expect("experiment values initialize once");
+        context
+    }
+
     /// Creates a new instance, with all default settings.
     ///
     /// This does only minimal initialization. In particular, it does not load
@@ -484,6 +543,9 @@
 
     /// Gets the path to the `rustc` executable.
     pub fn load_global_rustc(&self, ws: Option<&Workspace<'_>>) -> CargoResult<Rustc> {
+        if let Some(base) = &self.experimental_rustc {
+            return Rustc::new_experimental_information(base.clone());
+        }
         let cache_location =
             ws.map(|ws| ws.build_dir().join(".rustc_info.json").into_path_unlocked());
         let wrapper = self.maybe_get_tool("rustc_wrapper", &self.build_config()?.rustc_wrapper);
@@ -2622,3 +2684,87 @@
 
 #[cfg(test)]
 mod sealed_spike_metadata_tests;
+
+#[cfg(test)]
+mod experimental_query_context_tests {
+    use super::*;
+    use crate::core::compiler::build_context::TargetInfo;
+    use crate::core::compiler::{CompileKind, CompileTarget};
+    #[test]
+    fn actual_compiler_information_without_ordinary_initializers_or_cache() {
+        let root = tempfile::Builder::new()
+            .prefix("opensip-query-context-control-")
+            .tempdir()
+            .unwrap()
+            .keep();
+        let home = root.join("home");
+        let out = root.join("queries");
+        std::fs::create_dir(&home).unwrap();
+        std::fs::create_dir(&out).unwrap();
+        let head = ["-", "--crate-name", "___", "--print=file-names"];
+        let tail = [
+            "--crate-type",
+            "bin",
+            "--crate-type",
+            "rlib",
+            "--crate-type",
+            "dylib",
+            "--crate-type",
+            "cdylib",
+            "--crate-type",
+            "staticlib",
+            "--crate-type",
+            "proc-macro",
+            "--print=sysroot",
+            "--print=split-debuginfo",
+            "--print=crate-name",
+            "--print=cfg",
+            "-Wwarnings",
+        ];
+        let host_args = head
+            .iter()
+            .chain(tail.iter())
+            .map(std::ffi::OsString::from)
+            .collect();
+        let target_args = head
+            .iter()
+            .chain(["--target", "aarch64-apple-darwin"].iter())
+            .chain(tail.iter())
+            .map(std::ffi::OsString::from)
+            .collect();
+        let base = cargo_util::ProcessBuilder::experimental_information_queries(
+            Path::new(
+                "/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot/bin/rustc",
+            ),
+            &root,
+            vec![vec!["-vV".into()], host_args, target_args],
+            "b829b733131d4e1673eeebd1f34d06ae1e9ff4977b051313cf42e2a9e79ecf1c".into(),
+            &out,
+        );
+        let context = GlobalContext::new_experimental_query_context(
+            Shell::new(),
+            root.clone(),
+            home.clone(),
+            HashMap::new(),
+            base,
+        );
+        assert_eq!(context.env().count(), 0);
+        assert!(context.jobserver_from_env().is_none());
+        assert!(!context.nightly_features_allowed);
+        assert!(!context.cache_rustc_info);
+        let rustc = context.load_global_rustc(None).unwrap();
+        assert_eq!(&*rustc.host, "aarch64-apple-darwin");
+        let target =
+            CompileKind::Target(CompileTarget::new("aarch64-apple-darwin", false).unwrap());
+        let host_info = TargetInfo::new(&context, &[target], &rustc, CompileKind::Host).unwrap();
+        let target_info = TargetInfo::new(&context, &[target], &rustc, target).unwrap();
+        assert!(!host_info.cfg().is_empty());
+        assert!(!target_info.cfg().is_empty());
+        assert!(out.join("query-0.stdout").is_file());
+        assert!(out.join("query-1.stdout").is_file());
+        assert!(out.join("query-2.stdout").is_file());
+        assert!(!home.join(".rustc_info.json").exists());
+        assert_eq!(std::fs::read_dir(&home).unwrap().count(), 0);
+        eprintln!("ACTUAL_EXPERIMENT_CONTEXT_CONTROL={}", root.display());
+    }
+}
