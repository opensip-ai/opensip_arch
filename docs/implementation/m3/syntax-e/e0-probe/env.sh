# E0 environment (sourced by every E0 script). Throwaway probe; never product code.
# Scratch holds every download, clone and build output; this directory holds only sources and pin lists.
E0="${E0:-/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/e0}"
E0_PROBE="${E0_PROBE:-/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/syntax-e/e0-probe}"
E0_CORPUS_DOCS="/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/corpus"

# Private 0700 TMPDIR under the per-user temp root; private HOME; no global git or cargo config.
export TMPDIR="$(getconf DARWIN_USER_TEMP_DIR)e0-probe-tmp"
mkdir -p "$TMPDIR" && chmod 700 "$TMPDIR"
export HOME="$E0/home" XDG_CONFIG_HOME="$E0/home/.config" XDG_CACHE_HOME="$E0/home/.cache"
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 GIT_TERMINAL_PROMPT=0 GIT_LFS_SKIP_SMUDGE=1 GIT_ASKPASS=/usr/bin/false
export CARGO_HOME="$E0/cargo-home" CARGO_TARGET_DIR="$E0/target" CARGO_NET_GIT_FETCH_WITH_CLI=false
export PATH="/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export RUSTUP_TOOLCHAIN= RUSTFLAGS= CFLAGS= CXXFLAGS= LDFLAGS=
export LC_ALL=C LANG=C TZ=UTC SOURCE_DATE_EPOCH=0

# Pins (resolved 2026-10-04 by git ls-remote of the release tags; sha256 of every member is in src/*.pins.tsv).
WASI_SDK_TAG=wasi-sdk-34
WASI_SDK_ARCHIVE=wasi-sdk-34.0-arm64-macos.tar.gz
WASI_SDK_SHA256=9c59398106b417f8f14913380fdf0097a8cc0ff4af9eb3ce0065a859e88d49e9
WASI_SDK="$E0/toolchain/wasi-sdk-34.0-arm64-macos"

TS_RUNTIME_URL=https://github.com/tree-sitter/tree-sitter.git;            TS_RUNTIME_TAG=v0.27.0; TS_RUNTIME_COMMIT=6070dbfefd326bd735e5683eb128cc1b57dad0c0
TS_RUST_URL=https://github.com/tree-sitter/tree-sitter-rust.git;          TS_RUST_TAG=v0.24.2;    TS_RUST_COMMIT=77a3747266f4d621d0757825e6b11edcbf991ca5
TS_TYPESCRIPT_URL=https://github.com/tree-sitter/tree-sitter-typescript.git; TS_TYPESCRIPT_TAG=v0.23.2; TS_TYPESCRIPT_COMMIT=f975a621f4e7f532fe322e13c4f79495e0a7b2e7
TS_JAVASCRIPT_URL=https://github.com/tree-sitter/tree-sitter-javascript.git; TS_JAVASCRIPT_TAG=v0.25.0; TS_JAVASCRIPT_COMMIT=44c892e0be055ac465d5eeddae6d3e194424e7de
