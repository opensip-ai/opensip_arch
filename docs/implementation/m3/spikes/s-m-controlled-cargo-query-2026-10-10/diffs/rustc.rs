--- parent/src/cargo/util/rustc.rs
+++ candidate/src/cargo/util/rustc.rs
@@ -33,6 +33,7 @@
     /// The rustc full commit hash, this comes from `verbose_version`.
     pub commit_hash: Option<String>,
     cache: Mutex<Cache>,
+    experimental_process: Option<ProcessBuilder>,
 }
 
 impl Rustc {
@@ -113,11 +114,77 @@
             host,
             commit_hash,
             cache: Mutex::new(cache),
+            experimental_process: None,
+        })
+    }
+
+    /// Outside-product explicit information-query branch. No ordinary
+    /// executable lookup, rustup fingerprint or persistent cache is entered.
+    pub(crate) fn new_experimental_information(base: ProcessBuilder) -> CargoResult<Rustc> {
+        let path = PathBuf::from(base.get_program());
+        let mut version_query = base.clone();
+        version_query.arg("-vV");
+        let verbose_version = String::from_utf8(version_query.exec_with_output()?.stdout)?;
+        let extract = |field: &str| -> CargoResult<&str> {
+            verbose_version
+                .lines()
+                .find_map(|l| l.strip_prefix(field))
+                .ok_or_else(|| {
+                    anyhow::format_err!(
+                        "`rustc -vV` didn't have a line for `{}`, got:\n{}",
+                        field.trim(),
+                        verbose_version
+                    )
+                })
+        };
+
+        let host = extract("host: ")?.into();
+        let version = semver::Version::parse(extract("release: ")?).with_context(|| {
+            format!(
+                "rustc version does not appear to be a valid semver version, from:\n{}",
+                verbose_version
+            )
+        })?;
+        let commit_hash = extract("commit-hash: ").ok().map(|hash| {
+            // Possible commit-hash values from rustc are SHA hex string and "unknown". See:
+            // * https://github.com/rust-lang/rust/blob/531cb83fc/src/bootstrap/src/utils/channel.rs#L73
+            // * https://github.com/rust-lang/rust/blob/531cb83fc/compiler/rustc_driver_impl/src/lib.rs#L911-L913
+            #[cfg(debug_assertions)]
+            if hash != "unknown" {
+                debug_assert!(
+                    hash.chars().all(|ch| ch.is_ascii_hexdigit()),
+                    "commit hash must be a hex string, got: {hash:?}"
+                );
+                debug_assert!(
+                    hash.len() == 40 || hash.len() == 64,
+                    "hex string must be generated from sha1 or sha256 (i.e., it must be 40 or 64 characters long)\ngot: {hash:?}"
+                );
+            }
+            hash.to_string()
+        });
+
+        Ok(Rustc {
+            path,
+            wrapper: None,
+            workspace_wrapper: None,
+            verbose_version,
+            version,
+            host,
+            commit_hash,
+            cache: Mutex::new(Cache {
+                cache_location: None,
+                dirty: false,
+                data: CacheData::default(),
+            }),
+            experimental_process: Some(base),
         })
     }
 
     /// Gets a process builder set up to use the found rustc version, with a wrapper if `Some`.
     pub fn process(&self) -> ProcessBuilder {
+        if let Some(base) = &self.experimental_process {
+            return base.clone();
+        }
         let mut cmd = ProcessBuilder::new(self.path.as_path()).wrapped(self.wrapper.as_ref());
         cmd.retry_with_argfile(true);
         cmd
@@ -125,6 +192,9 @@
 
     /// Gets a process builder set up to use the found rustc version, with a wrapper if `Some`.
     pub fn workspace_process(&self) -> ProcessBuilder {
+        if let Some(base) = &self.experimental_process {
+            return base.clone();
+        }
         let mut cmd = ProcessBuilder::new(self.path.as_path())
             .wrapped(self.workspace_wrapper.as_ref())
             .wrapped(self.wrapper.as_ref());
@@ -133,6 +203,9 @@
     }
 
     pub fn process_no_wrapper(&self) -> ProcessBuilder {
+        if let Some(base) = &self.experimental_process {
+            return base.clone();
+        }
         let mut cmd = ProcessBuilder::new(&self.path);
         cmd.retry_with_argfile(true);
         cmd
@@ -153,6 +226,13 @@
         cmd: &ProcessBuilder,
         extra_fingerprint: u64,
     ) -> CargoResult<(String, String)> {
+        if let Some(base) = &self.experimental_process {
+            let output = cmd.experimental_output_for(base)?;
+            return Ok((
+                String::from_utf8(output.stdout)?,
+                String::from_utf8(output.stderr)?,
+            ));
+        }
         self.cache
             .lock()
             .unwrap()
