#!/bin/sh
# E0 phase 2: builds, the P1-P6 runs and the analysis. Run ONLY after the lead's
# "E0 phase 2: go" (X9's timing-sensitive lead set must not overlap).
# Usage: sh phase2-run.sh 2>&1 | tee <e0>/logs/phase2.log
set -eu
. "$(dirname "$0")/env.sh"
OUT="$E0/out"
mkdir -p "$OUT" "$E0/logs" "$E0_PROBE/results"
step() { echo; echo "=== $(date -u +%H:%M:%S) $*"; }
LIST="$E0/t2a/t2a-selected.tsv"; ROOT="$E0/t2a/files"
E0BIN="$CARGO_TARGET_DIR/release/e0"

step "0 host and toolchain facts"
{ sw_vers; uname -a; sysctl -n machdep.cpu.brand_string hw.ncpu hw.memsize; xcrun clang --version | head -1
  rustc --version; cargo --version; "$WASI_SDK/bin/clang" --no-default-config --version | head -1
  cat "$WASI_SDK/VERSION"; shasum -a 256 "$E0/dl/$WASI_SDK_ARCHIVE" "$E0_PROBE/harness/Cargo.lock"; } > "$OUT/host.txt"
cat "$OUT/host.txt"

step "1 harness build (wasmi, tree-sitter runtime, four native grammars)"
( cd "$E0_PROBE/harness" && E0_SRC="$E0/src" cargo build --release --locked --offline )
( cd "$E0_PROBE/harness" && cargo tree --offline -e features -i wasmi > "$OUT/wasmi-features.txt" && cargo tree --offline --prefix none -e normal | sort -u > "$OUT/crate-closure.txt" )

step "2 P1: two clean module builds in two roots"
rm -rf "$E0/build-a" "$E0/build-b"
/usr/bin/time -p sh "$E0_PROBE/build-modules.sh" "$E0/build-a"
/usr/bin/time -p sh "$E0_PROBE/build-modules.sh" "$E0/build-b"
( cd "$E0/build-a/out" && shasum -a 256 *.wasm ) > "$OUT/p1-a.sha256"
( cd "$E0/build-b/out" && shasum -a 256 *.wasm ) > "$OUT/p1-b.sha256"
cmp "$E0/build-a/out/inputs.sha256" "$E0/build-b/out/inputs.sha256" && echo "inputs identical"
cmp "$OUT/p1-a.sha256" "$OUT/p1-b.sha256" && echo "P1 modules identical" || echo "P1 MODULES DIFFER"
cp "$E0/build-a/out/build-receipt.txt" "$OUT/build-receipt-a.txt"; cp "$E0/build-b/out/build-receipt.txt" "$OUT/build-receipt-b.txt"

step "3 P2 and module shape (two witnesses)"
"$E0BIN" inspect "$E0"/build-a/out/*.wasm > "$OUT/p2-inspect.tsv"; cat "$OUT/p2-inspect.tsv"

step "4 admission chain cost and SymbolTableV1 join (3 repetitions)"
for i in 1 2 3; do "$E0BIN" admit --modules "$E0/build-a/out" --dump "$OUT/symtab" > "$OUT/admit-$i.tsv"; done
cp "$OUT/admit-3.tsv" "$OUT/admit.tsv"; cat "$OUT/admit.tsv"

R="$E0BIN run --list $LIST --root $ROOT"
step "5 run A: P3 (wasm and native), P4 base, P6 data"
$R --modules "$E0/build-a/out" --mode both --order sorted --threads 1 --dump "$OUT/mismatch" --out "$OUT/run-a.tsv"
step "6 P4 runs B, C, D"
$R --modules "$E0/build-a/out" --mode wasm --order shuffle:1 --threads 1 --out "$OUT/run-b.tsv"
$R --modules "$E0/build-a/out" --mode wasm --order shuffle:2 --threads 8 --out "$OUT/run-c.tsv"
$R --modules "$E0/build-b/out" --mode wasm --order reverse --threads 4 --out "$OUT/run-d.tsv"
step "7 P4 discrimination controls (lazy translation; instance reuse)"
$R --modules "$E0/build-a/out" --mode wasm --order shuffle:1 --threads 1 --compilation lazy --out "$OUT/run-lazy.tsv"
$R --modules "$E0/build-a/out" --mode wasm --order sorted --threads 1 --reuse-instance --out "$OUT/run-reuse.tsv"
# Added in phase 2: lazy under a second order, to show the translation fuel moves between files.
$R --modules "$E0/build-a/out" --mode wasm --order sorted --threads 1 --compilation lazy --out "$OUT/run-lazy2.tsv"

step "8 P5 timing: warm-up (every 10th file), then the timing run"
$R --modules "$E0/build-a/out" --mode wasm --order sorted --threads 1 --sample 10 --out "$OUT/run-warmup.tsv"
$R --modules "$E0/build-a/out" --mode wasm --order sorted --threads 1 --out "$OUT/run-t.tsv"

step "9 P6: derive constants, verify them, boundary controls (every 10th file)"
python3 "$E0_PROBE/analyze.py" "$OUT" > /dev/null
eval "$(python3 -c "import json;c=json.load(open('$OUT/summary.json'))['P6']['constants'];print(f\"FB={c['fuelBase']} FK={c['fuelPerByte']} MP={c['maxMemoryPages']}\")")"
echo "fuelBase=$FB fuelPerByte=$FK maxMemoryPages=$MP"
$R --modules "$E0/build-a/out" --mode wasm --threads 4 --fuel-base "$FB" --fuel-per-byte "$FK" --max-pages "$MP" --out "$OUT/run-limits.tsv"
B="--budget-from $OUT/run-a.tsv --sample 10 --mode wasm --threads 4 --modules $E0/build-a/out"
$R $B --fuel-delta 0  --pages-delta 0  --out "$OUT/run-exact.tsv"
$R $B --fuel-delta -1 --pages-delta 0  --out "$OUT/run-fuel-minus1.tsv"
$R $B --fuel-delta 0  --pages-delta -1 --out "$OUT/run-pages-minus1.tsv"

step "9b diagnostic, not gated: root-only serialization (OSG_DIAG_ROOT_ONLY), added in phase 2"
D="$E0/build-diag"; rm -rf "$D"; cp -R "$E0/build-a" "$D"; cp "$E0_PROBE/shim/osg_shim.c" "$D/in/shim/"
( cd "$D" && T="--no-default-config --target=wasm32-unknown-unknown -mcpu=mvp -mbulk-memory -msign-ext"
  for g in javascript rust tsx typescript; do
    "$WASI_SDK/bin/clang" $T -nostdlibinc -std=c11 -O2 -fvisibility=hidden -ffunction-sections -fdata-sections -fno-ident -w \
      -Iin/runtime/src -Iin/runtime/include -Iin/language/include -DOSG_DIAG_ROOT_ONLY -DOSG_LANGUAGE_FN=tree_sitter_$g \
      -c in/shim/osg_shim.c -o obj/$g.shim.o
    "$WASI_SDK/bin/clang" $T -nostdlib -Wl,--no-entry -Wl,--stack-first -Wl,-z,stack-size=1048576 -Wl,--gc-sections \
      -o out/$g.wasm obj/runtime.o obj/libc.o obj/stdio.o obj/$g.parser.o obj/$g.scanner.o obj/$g.shim.o
  done )
$R --modules "$D/out" --mode wasm --order sorted --threads 1 --out "$OUT/run-diag-rootonly.tsv"

step "10 analysis"
python3 "$E0_PROBE/analyze.py" "$OUT"
# Small records only into the probe directory; the per-file TSVs stay in scratch, pinned here by digest.
cp "$OUT/p2-inspect.tsv" "$OUT/admit.tsv" "$OUT/summary.json" "$OUT/host.txt" "$OUT/wasmi-features.txt" \
   "$OUT/crate-closure.txt" "$OUT/build-receipt-a.txt" "$OUT/p1-a.sha256" "$OUT/p1-b.sha256" "$E0_PROBE/results/"
( cd "$OUT" && shasum -a 256 run-*.tsv ) > "$E0_PROBE/results/run-tsv.sha256"
echo "done; the report is written from $OUT/summary.json"
