#!/bin/sh
# E0: build the four code modules (rust, javascript, typescript, tsx) with the pinned wasi-sdk.
# PHASE 2 ONLY (compiles C). Usage: sh build-modules.sh <build-root>
#
# P1 runs this twice into two different roots; each root gets its own fresh copy of every
# input, so no byte of one build can reach the other, and the modules must be byte-identical.
# Every path the compiler sees is relative to the build root (cwd), and -ffile-prefix-map
# maps the root to "." as a second guard.
set -eu
. "$(dirname "$0")/env.sh"
ROOT="$1"
[ ! -e "$ROOT" ] || { echo "build root exists: $ROOT (P1 needs clean builds)"; exit 1; }
mkdir -p "$ROOT"
ROOT="$(cd "$ROOT" && pwd -P)"

# Fresh copies of the pinned inputs (the closure's source/** members, as E1 item 4 lays them out).
mkdir -p "$ROOT/in/runtime" "$ROOT/in/language" "$ROOT/in/shim" "$ROOT/obj" "$ROOT/out"
cp -R "$E0/src/tree-sitter/lib/src" "$E0/src/tree-sitter/lib/include" "$ROOT/in/runtime/"
cp -R "$E0/src/tree-sitter/crates/language/wasm/include" "$ROOT/in/language/"
cp -R "$E0/src/tree-sitter-rust/src" "$ROOT/in/rust"
cp -R "$E0/src/tree-sitter-javascript/src" "$ROOT/in/javascript"
mkdir -p "$ROOT/in/typescript-repo"
cp -R "$E0/src/tree-sitter-typescript/common" "$E0/src/tree-sitter-typescript/typescript" "$E0/src/tree-sitter-typescript/tsx" "$ROOT/in/typescript-repo/"
cp "$E0_PROBE/shim/osg_shim.c" "$ROOT/in/shim/"
chmod -R u+w "$ROOT/in"
cd "$ROOT"

CC="$WASI_SDK/bin/clang"
# Target features are listed explicitly; LLVM's generic defaults are never inherited (E1 item 6).
TARGET="--no-default-config --target=wasm32-unknown-unknown -mcpu=mvp -mbulk-memory -msign-ext"
CFLAGS="$TARGET -nostdlibinc -std=c11 -O2 -fvisibility=hidden -ffunction-sections -fdata-sections \
 -fno-ident -ffile-prefix-map=$ROOT=. -w"
INC="-Iin/runtime/src -Iin/runtime/include -Iin/language/include"
# TREE_SITTER_WASM_STDLIB is deliberately NOT defined: with it, the stdlib headers attach
# export_name to every libc function, which would break A10's closed export set.
LDFLAGS="$TARGET -nostdlib -Wl,--no-entry -Wl,--stack-first -Wl,-z,stack-size=1048576 -Wl,--gc-sections"

RECEIPT="out/build-receipt.txt"
{
  echo "toolchain $WASI_SDK_TAG archive=$WASI_SDK_ARCHIVE sha256=$WASI_SDK_SHA256"
  "$CC" --no-default-config --version | head -1
  echo "cc=$CC"; echo "CFLAGS=$CFLAGS"; echo "INC=$INC"; echo "LDFLAGS=$LDFLAGS"
} > "$RECEIPT.tmp"
sed "s|$ROOT|<root>|g; s|$E0|<e0>|g" "$RECEIPT.tmp" > "$RECEIPT"; rm "$RECEIPT.tmp"

run() { echo "+ $*" | sed "s|$ROOT|<root>|g; s|$E0|<e0>|g" >> "$RECEIPT"; "$@"; }

# Shared units (compiled once per build root; every module links the same objects).
run $CC $CFLAGS $INC -c in/runtime/src/lib.c -o obj/runtime.o
run $CC $CFLAGS $INC -c in/runtime/src/wasm-stdlib/libc.c -o obj/libc.o
run $CC $CFLAGS $INC -c in/runtime/src/wasm-stdlib/stdio.c -o obj/stdio.o

build_one() {  # $1 grammarId  $2 grammar src dir  $3 language function
  g="$1"; src="$2"; fn="$3"
  run $CC $CFLAGS $INC -I"$src" -c "$src/parser.c" -o "obj/$g.parser.o"
  run $CC $CFLAGS $INC -I"$src" -c "$src/scanner.c" -o "obj/$g.scanner.o"
  run $CC $CFLAGS $INC -DOSG_LANGUAGE_FN="$fn" -c in/shim/osg_shim.c -o "obj/$g.shim.o"
  run $CC $LDFLAGS -o "out/$g.wasm" obj/runtime.o obj/libc.o obj/stdio.o \
      "obj/$g.parser.o" "obj/$g.scanner.o" "obj/$g.shim.o"
}
build_one javascript in/javascript tree_sitter_javascript
build_one rust in/rust tree_sitter_rust
build_one tsx in/typescript-repo/tsx/src tree_sitter_tsx
build_one typescript in/typescript-repo/typescript/src tree_sitter_typescript

( cd out && shasum -a 256 javascript.wasm rust.wasm tsx.wasm typescript.wasm && ls -l *.wasm ) | tee -a "$RECEIPT"
# The input tree's digest, so the receipt also proves both roots compiled the same bytes.
( cd in && find . -type f | LC_ALL=C sort | xargs shasum -a 256 ) > out/inputs.sha256
echo "inputs-digest $(shasum -a 256 < out/inputs.sha256 | cut -c1-64)" | tee -a "$RECEIPT"
