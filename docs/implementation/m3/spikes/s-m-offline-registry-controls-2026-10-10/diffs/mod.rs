--- parent/src/cargo/util/context/mod.rs
+++ candidate/src/cargo/util/context/mod.rs
@@ -2771,3 +2771,6 @@
 
 #[cfg(test)]
 mod experimental_resolver_controls;
+
+#[cfg(test)]
+mod experimental_registry_controls;
