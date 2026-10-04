// E0 harness build script: compiles the four pinned grammars natively (T-native leg of P3).
// The runtime itself comes from the `tree-sitter` crate, whose bundled C sources E0 checked
// byte-for-byte against the pinned tag (phase 1). Grammar sources come from E0_SRC, the
// materialized pinned commits; nothing here reads a T2a repository.
use std::{env, path::PathBuf};

fn main() {
    println!("cargo:rerun-if-env-changed=E0_SRC");
    println!("cargo:rerun-if-changed=build.rs");
    let src = PathBuf::from(env::var("E0_SRC").expect("E0_SRC must point at <e0>/src"));
    let grammars: [(&str, PathBuf); 4] = [
        ("javascript", src.join("tree-sitter-javascript/src")),
        ("rust", src.join("tree-sitter-rust/src")),
        ("tsx", src.join("tree-sitter-typescript/tsx/src")),
        ("typescript", src.join("tree-sitter-typescript/typescript/src")),
    ];
    for (name, dir) in grammars.iter() {
        let parser = dir.join("parser.c");
        let scanner = dir.join("scanner.c");
        for f in [&parser, &scanner] {
            assert!(f.is_file(), "missing {}", f.display());
            println!("cargo:rerun-if-changed={}", f.display());
        }
        cc::Build::new()
            .std("c11")
            .include(dir)
            .file(&parser)
            .file(&scanner)
            .warnings(false)
            .flag_if_supported("-Wno-unused-parameter")
            .compile(&format!("e0_grammar_{name}"));
    }
}
