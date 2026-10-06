# Inert TOML array and integer views r1

Verdict: ACCEPT-DESIGN-UNIT. Implementation verdict: ACCEPT-UNIT.

This adds borrowed array and integer views to the existing TOML 1.0 parser and retargets the two matching local-source pins. Product HEAD is `9281b70aed0358802f59da3782780e0c4974e79f` and architecture HEAD is `4ec332798242e4f43bc07450cbb4bcd5f4dd5ec4`. Both tracked trees are clean. Inventory v166 remains 614780 bytes, sha256 `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`, and is the last selected inventory successor. The three product paths are already inventoried, and those rows do not pin content. The OpenSIP support directory is absent.

## Law and parents

Subject manifest sha256 `803d350b709cb35d32d49c6e58291d699059acd84163085de6851574bffdca36` (3159 bytes). All 14 members match. Successor `docs/implementation/m3/native-g/toml-views-r1/successor.json` is 3576 bytes, sha256 `33c92dc7afdf704008ab0a18dc24478319f9de852035ff27fef0f32da5f86649`. `passageOverrides` is empty and there is no passage supersession. The candidates are the other 13 subject members.

The two parents are already accepted, and the architecture bytes match:

| Parent | Bytes | SHA-256 |
|---|---:|---|
| `docs/implementation/m3/host-pipeline-j/j-bs-runtime-pins-r1/product/tools/identity/dependency-policy.json` | 56471 | `180a86d019b2b8885fdcce484b3651721f618447d952c30095adf44c398019ff` |
| `docs/v2/contracts/product-v1/native-evidence.md` | 329013 | `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0` |

Native-evidence §3.1 takes `name` and `version` from `Cargo.lock` `[[package]]` rows, and §3.4 names the adapter's sealed Cargo inputs. Those consumers need ordered arrays and integer fields. This record supplies inert borrowed views of an already parsed document. It adds no schema member, wire code, dependency edge, or Cargo.lock, dependency-source, feature, configuration, native-context, Plan, or provider admission.

## Three product files

`crates/identity/src/lib.rs` moves from 3231 / `271551e4d1182426744bfc4237a52e61578f2efaea3ce97606e87d1d402cffe5` to 3274 / `27e4bbf2f35612dbd696baefe28045ffffd3faf473e710134aa67d9a3c2a32cf`. The only change is the TOML export, which adds `TomlArrayView` and `TomlIntegerView` beside the existing names.

`crates/identity/src/toml.rs` moves from 6333 / `03202a1e52a7aa87420cfe325ea49c0bc327a8094597acc61127ec4c6582e339` to 13423 / `55294d354966713f4d11fd79117138e1a21f3ac849580646033681a362684c0e`. `parse_toml`, its byte, UTF-8, BOM, calendar, node, and recursion checks, and the previous test module are byte-identical through the start of the new `view_tests` module. There is no recovery path and no TOML-to-JSON conversion.

`TomlValueView::as_array` and `as_integer` return `None` for every other TOML type, including a string, float, boolean, table, nested array, or datetime where the requested view does not match. `TomlArrayView` exposes `len`, `is_empty`, `get`, and a repeatable exact-size iterator in document order. `get` returns `None` past the end, including `usize::MAX`. Duplicate entries, nested arrays, inline tables, and empty arrays stay distinct. `TomlIntegerView` exposes the parser's `from_str_radix` digits and a separate radix. The selected parser removes underscores and `0x`/`0o`/`0b` prefixes and keeps the sign on the digit string; the view does not restore the source spelling or narrow the value. A 2^128 decimal, its negative, and a wider hex literal remain a successful document whose `u128`/`i128` conversions fail. The views borrow the parsed document with the same lifetime pattern as the existing table view.

`tools/identity/dependency-policy.json` moves from 56471 / `180a86d019b2b8885fdcce484b3651721f618447d952c30095adf44c398019ff` to 56472 / `c1e2f006f51a2c5b6c85214e6963816318f6d39204d86a9ff59004942f6176a5`. Of the 20 local sources, only `src/lib.rs` and `src/toml.rs` change, and those pins match the new files. Dependencies, features, licenses, and the other local pins stay equal. `Cargo.lock` stays 13130 / `532e04105b6157d25fb52f7379e3b8ae2cd67741711e6cb15a731d9cd7c23bf1`, `crates/identity/Cargo.toml` stays 773 / `8fec4be95051c64bf8b864e79b0020bb32ada345b3e50547c2b7ff35a84aea5c`, and `schema_registry.rs` stays 26815 / `a6e34a2fd26e8db5cdb639bdd8921067683fe79653345895f868949cd617cad3`.

The accepted G2 files are already on this base and are unchanged in the candidate: `compiler_tools.rs` 10232 / `b09afe2a372b4071feb7e2b290fd7691483543b54164fda3f67b12e27bea1195` and `compiler_tools_tests.rs` 19998 / `7b1a977177314e9d7b330973211fbc94f5cface752236a954700b4f7818754c3`. The authoring tree's `design-lock.json` is the predecessor of HEAD. HEAD adds only the bound `g2-system-inputs-r1` successor. The forward product delta against HEAD is these three files.

## Evidence

The read-only checker was run as named. Its stdout matches `evidence/checks.json`, 362 bytes, sha256 `3126d4349740bd05f8cb4c5c944b656942077ce17a1937cad2c6f2910a30e140`. It compares source text and pins, executes no parser, and records no owner admission or qualification.

Supplied candidate logs, not re-executed here: identity library tests 64 passed and 0 failed, including the seven new view controls and the previous parser controls. The identity dependency closure reports eight registry tuples, `sourceFilesVerified` 305, `passed` true, and `productQualification` false. The Clippy log finishes with no warning lines. The recorded runner used `nice -n 10`, `--locked --offline`, `-D warnings`, and private `0700` `TMPDIR` `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-toml-views-sdry9qq7`. These controls are inert views. O1-a, day-0, O7, and the remaining owner gates stay open.

No required findings. Exact reviewed bytes follow assent. Product code and the design-lock bind stay separate commits, with no push.
