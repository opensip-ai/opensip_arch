--- parent/crates/cargo-util/src/process_builder.rs
+++ candidate/crates/cargo-util/src/process_builder.rs
@@ -43,6 +43,48 @@
     retry_with_argfile: bool,
     /// Data to write to stdin.
     stdin: Option<Vec<u8>>,
+    experimental_query: Option<ExperimentalQuery>,
+}
+
+/// Outside-product experiment data, never a native executable capability.
+#[derive(Clone, Debug)]
+struct ExperimentalQuery {
+    program: std::path::PathBuf,
+    cwd: std::path::PathBuf,
+    allowed_arguments: Vec<Vec<OsString>>,
+    expected_sha256: String,
+    output_root: std::path::PathBuf,
+    next: std::sync::Arc<std::sync::atomic::AtomicUsize>,
+}
+
+impl ExperimentalQuery {
+    fn validate(&self, builder: &ProcessBuilder) {
+        use sha2::{Digest, Sha256};
+        assert_eq!(builder.program, self.program.as_os_str());
+        assert_eq!(builder.get_cwd(), Some(self.cwd.as_path()));
+        assert!(builder.wrappers.is_empty());
+        assert!(builder.arg0.is_none());
+        assert!(builder.jobserver.is_none());
+        assert!(!builder.retry_with_argfile);
+        assert!(builder.stdin.as_ref().is_none_or(|s| s.is_empty()));
+        assert!(builder.env.values().all(Option::is_none));
+        assert!(self.allowed_arguments.contains(&builder.args));
+        let metadata =
+            std::fs::symlink_metadata(&self.program).expect("experiment executable metadata");
+        assert!(metadata.is_file() && !metadata.file_type().is_symlink());
+        let mut file = std::fs::File::open(&self.program).expect("experiment executable read");
+        let mut hasher = Sha256::new();
+        let mut buffer = [0u8; 65536];
+        loop {
+            let count =
+                std::io::Read::read(&mut file, &mut buffer).expect("experiment executable hash");
+            if count == 0 {
+                break;
+            }
+            hasher.update(&buffer[..count]);
+        }
+        assert_eq!(hex::encode(hasher.finalize()), self.expected_sha256);
+    }
 }
 
 impl fmt::Display for ProcessBuilder {
@@ -86,7 +128,48 @@
             display_env_vars: false,
             retry_with_argfile: false,
             stdin: None,
-        }
+            experimental_query: None,
+        }
+    }
+
+    /// Explicit experiment-only exact query vectors. Supplied pins and paths
+    /// are data, not authenticated ownership or runtime closure. No cache.
+    pub fn experimental_information_queries(
+        program: &Path,
+        cwd: &Path,
+        allowed_arguments: Vec<Vec<OsString>>,
+        expected_sha256: String,
+        output_root: &Path,
+    ) -> ProcessBuilder {
+        assert!(program.is_absolute() && cwd.is_absolute() && output_root.is_absolute());
+        assert!(!allowed_arguments.is_empty());
+        let mut builder = Self::new(program);
+        builder.cwd(cwd);
+        builder.experimental_query = Some(ExperimentalQuery {
+            program: program.to_path_buf(),
+            cwd: cwd.to_path_buf(),
+            allowed_arguments,
+            expected_sha256,
+            output_root: output_root.to_path_buf(),
+            next: std::sync::Arc::new(std::sync::atomic::AtomicUsize::new(0)),
+        });
+        builder
+    }
+
+    /// Require the same experiment instance before this branch consumes a
+    /// supplied command. Equal strings or bytes from another instance do not
+    /// grant reuse of the first instance's registered query set.
+    pub fn experimental_output_for(&self, base: &ProcessBuilder) -> Result<Output> {
+        let Some(own) = &self.experimental_query else {
+            bail!("command has no experiment query association");
+        };
+        let Some(expected) = &base.experimental_query else {
+            bail!("base has no experiment query association");
+        };
+        if !std::sync::Arc::ptr_eq(&own.next, &expected.next) {
+            bail!("foreign experiment query association");
+        }
+        self.exec_with_output()
     }
 
     /// (chainable) Sets the executable for the process.
@@ -296,6 +379,49 @@
     }
 
     fn _output(&self) -> io::Result<Output> {
+        if let Some(guard) = &self.experimental_query {
+            guard.validate(self);
+            let ordinal = guard
+                .next
+                .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
+            let prefix = guard.output_root.join(format!("query-{ordinal}"));
+            let mut args_file = std::fs::OpenOptions::new()
+                .write(true)
+                .create_new(true)
+                .open(prefix.with_extension("arguments"))?;
+            for arg in &self.args {
+                #[cfg(unix)]
+                {
+                    use std::os::unix::ffi::OsStrExt;
+                    let bytes = arg.as_os_str().as_bytes();
+                    args_file.write_all(&(bytes.len() as u64).to_be_bytes())?;
+                    args_file.write_all(bytes)?;
+                }
+            }
+            let mut stdout = std::fs::OpenOptions::new()
+                .write(true)
+                .create_new(true)
+                .open(prefix.with_extension("stdout"))?;
+            let mut stderr = std::fs::OpenOptions::new()
+                .write(true)
+                .create_new(true)
+                .open(prefix.with_extension("stderr"))?;
+            let mut command = self.build_command();
+            command
+                .stdin(Stdio::null())
+                .stdout(stdout.try_clone()?)
+                .stderr(stderr.try_clone()?);
+            let status = command.status()?;
+            stdout.flush()?;
+            stderr.flush()?;
+            std::fs::write(prefix.with_extension("status"), format!("{status}\n"))?;
+            guard.validate(self);
+            return Ok(Output {
+                status,
+                stdout: std::fs::read(prefix.with_extension("stdout"))?,
+                stderr: std::fs::read(prefix.with_extension("stderr"))?,
+            });
+        }
         if !debug_force_argfile(self.retry_with_argfile) {
             let mut cmd = self.build_command();
             match piped(&mut cmd, self.stdin.is_some()).spawn() {
@@ -497,6 +623,10 @@
             cmd.args(iter);
             cmd
         };
+        if let Some(guard) = &self.experimental_query {
+            guard.validate(self);
+            command.env_clear();
+        }
         #[cfg(unix)]
         if let Some(arg0) = self.get_arg0() {
             use std::os::unix::process::CommandExt as _;
@@ -707,3 +837,106 @@
         );
     }
 }
+
+#[cfg(test)]
+mod experimental_information_tests {
+    use super::*;
+    fn prepared(root: &Path) -> ProcessBuilder {
+        ProcessBuilder::experimental_information_queries(
+            Path::new("/tmp/opensip-implementation/sm-compiler-query-kernel-2026-10-10/probe"),
+            root,
+            vec![vec![OsString::from("-vV")]],
+            "1e177c008a0cfb448d942062de33c080b1248dd8d8d763fe51f3f848690b5436".to_owned(),
+            root,
+        )
+    }
+    #[test]
+    fn actual_empty_environment_eof_cwd_and_retained_output() {
+        let root = tempfile::Builder::new()
+            .prefix("opensip-query-process-control-")
+            .tempdir()
+            .unwrap()
+            .keep();
+        let mut builder = prepared(&root);
+        builder.arg("-vV");
+        let output = builder.exec_with_output().unwrap();
+        let text = String::from_utf8(output.stdout.clone()).unwrap();
+        assert!(text.contains("ENV_COUNT=0\n"));
+        assert!(text.contains("STDIN_BYTES=0\n"));
+        assert!(text.contains("ARGS=[\"-vV\"]\n"));
+        let observed = text.lines().find_map(|l| l.strip_prefix("CWD=")).unwrap();
+        assert!(same_file::is_same_file(observed, root.as_path()).unwrap());
+        assert_eq!(
+            std::fs::read(root.as_path().join("query-0.stdout")).unwrap(),
+            output.stdout
+        );
+        assert!(root.as_path().join("query-0.arguments").is_file());
+        assert!(root.as_path().join("query-0.status").is_file());
+        let again = builder.exec_with_output().unwrap();
+        assert!(again.status.success());
+        assert!(root.as_path().join("query-1.stdout").is_file());
+        // Retain the actual controls outside the ephemeral TempDir owner.
+        let retained = root;
+        eprintln!("ACTUAL_EXPERIMENT_QUERY_CONTROL={}", retained.display());
+    }
+    #[test]
+    fn unregistered_arguments_refused_before_any_output() {
+        let root = tempfile::tempdir().unwrap();
+        let mut builder = prepared(root.path());
+        builder.arg("--print=target-spec-json");
+        assert!(
+            std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| builder.output())).is_err()
+        );
+        assert_eq!(std::fs::read_dir(root.path()).unwrap().count(), 0);
+    }
+    #[test]
+    fn executable_override_wrapper_environment_and_argfile_refused() {
+        let root = tempfile::tempdir().unwrap();
+        for variant in 0..4 {
+            let mut builder = prepared(root.path());
+            builder.arg("-vV");
+            match variant {
+                0 => {
+                    builder.program("/usr/bin/false");
+                }
+                1 => {
+                    builder = builder.wrapped(Some(Path::new("/usr/bin/env")));
+                }
+                2 => {
+                    builder.env("TMPDIR", root.path());
+                }
+                _ => {
+                    builder.retry_with_argfile(true);
+                }
+            }
+            assert!(
+                std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| builder.output()))
+                    .is_err()
+            );
+        }
+        assert_eq!(std::fs::read_dir(root.path()).unwrap().count(), 0);
+    }
+    #[test]
+    fn foreign_equal_and_ordinary_commands_refused_before_output() {
+        let root = tempfile::tempdir().unwrap();
+        let base = prepared(root.path());
+        let mut equal = prepared(root.path());
+        equal.arg("-vV");
+        assert!(equal.experimental_output_for(&base).is_err());
+        let mut ordinary = ProcessBuilder::new(base.get_program());
+        ordinary.arg("-vV").cwd(root.path());
+        assert!(ordinary.experimental_output_for(&base).is_err());
+        assert_eq!(std::fs::read_dir(root.path()).unwrap().count(), 0);
+    }
+    #[test]
+    fn mismatched_pin_refused_before_any_output() {
+        let root = tempfile::tempdir().unwrap();
+        let mut builder = prepared(root.path());
+        builder.experimental_query.as_mut().unwrap().expected_sha256 = "0".repeat(64);
+        builder.arg("-vV");
+        assert!(
+            std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| builder.output())).is_err()
+        );
+        assert_eq!(std::fs::read_dir(root.path()).unwrap().count(), 0);
+    }
+}
