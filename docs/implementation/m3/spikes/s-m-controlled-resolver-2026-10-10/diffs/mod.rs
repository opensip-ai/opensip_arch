--- parent/src/cargo/util/context/mod.rs
+++ candidate/src/cargo/util/context/mod.rs
@@ -2768,3 +2768,6 @@
         eprintln!("ACTUAL_EXPERIMENT_CONTEXT_CONTROL={}", root.display());
     }
 }
+
+#[cfg(test)]
+mod experimental_resolver_controls;
