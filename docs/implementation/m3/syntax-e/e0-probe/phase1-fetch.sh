#!/bin/sh
# E0 phase 1: downloads and clones only. No compiler, no build, no parse.
set -eu
. "$(dirname "$0")/env.sh"
mkdir -p "$E0/dl" "$E0/toolchain" "$E0/src" "$E0/t2a/git" "$E0/t2a/files" "$E0/logs"

# 1. wasi-sdk (unpacked only; nothing in it is run in phase 1).
cd "$E0/dl"
[ -f "$WASI_SDK_ARCHIVE" ] || curl -sSL -o "$WASI_SDK_ARCHIVE" "https://github.com/WebAssembly/wasi-sdk/releases/download/$WASI_SDK_TAG/$WASI_SDK_ARCHIVE"
echo "$WASI_SDK_SHA256  $WASI_SDK_ARCHIVE" | shasum -a 256 -c -
[ -d "$WASI_SDK" ] || tar -xzf "$WASI_SDK_ARCHIVE" -C "$E0/toolchain"

# 2. tree-sitter runtime and the three grammar repositories (four code rows), by commit.
cd "$E0/src"
F="python3 $E0_PROBE/fetch_pinned.py upstream"
$F tree-sitter            "$TS_RUNTIME_URL"    "$TS_RUNTIME_COMMIT"    "$E0/src/tree-sitter"            --paths lib/ LICENSE crates/language/ crates/xtask/src/build_wasm.rs crates/xtask/src/build_wasm_stdlib.rs
$F tree-sitter-rust       "$TS_RUST_URL"       "$TS_RUST_COMMIT"       "$E0/src/tree-sitter-rust"
$F tree-sitter-typescript "$TS_TYPESCRIPT_URL" "$TS_TYPESCRIPT_COMMIT" "$E0/src/tree-sitter-typescript"
$F tree-sitter-javascript "$TS_JAVASCRIPT_URL" "$TS_JAVASCRIPT_COMMIT" "$E0/src/tree-sitter-javascript"

# 3. T2a: the 19 repositories at their pinned commits; gitTree and contentDigest verified;
#    only selector-matching blobs are materialized.
python3 "$E0_PROBE/fetch_pinned.py" t2a "$E0_CORPUS_DOCS/t2-corpus-manifest-T2a.draft.json" \
  "$E0/t2a/git" "$E0/t2a/files" "$E0/t2a/t2a-selected.tsv"
