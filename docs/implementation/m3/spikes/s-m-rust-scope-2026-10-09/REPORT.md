# Preliminary three-actor Rust subject-scope recipe measurements

Eleven development read sets supply the nonempty .rs file population: all seven required Rust medium entries, the prefixed serde/json overlay, and smithy-rs/rspack/deno large development entries. Development/held-out flags are checked before reading. Medium inventories come from the new typed sealing observations; large trees are read-only verified and enumerated without following symlinks. The conditional Sui workload is not measured. No held-out source is opened.

Thirty fresh child derivations per workload (330 total): host-a extracts only four exact pure recipe functions from the bound RUST3-LIM builder; host-b uses the new independent first-party encoder and reconstruction; worker-prototype independently reruns the second implementation in its own process. Every actor rebuilds the array, scope commitment, analysis-domain commitment and canonical array bytes. All three arrays/commitments/raw-CBOR lengths and SHA256 values are identical for every workload. Four controls match the exact closed synthetic vector, duplicate/empty refusals, UTF8 key ordering and uint64 width edges.

Each actor has three warmups and seven measured samples. Parent and every child priority10 readback are retained. The whole ordinary lane set uses a private 0700 Darwin TMPDIR with HOME unchanged. Timed span covers only the reconstruction/commitment/array-CBOR calculation after the inert input is parsed. Native wait4 process peak RSS is informational macOS bytes with checked identity conversion; the earlier child getrusage reading is kept separately before output serialization and may be smaller. It is not incremental algorithm heap accounting.

| Workload | Actor | Subjects | Canonical array bytes | Median ms | Max ms | Process peak RSS bytes |
|---|---|---:|---:|---:|---:|---:|
| poly-medium-napi-rs | host-a | 239 | 42133 | 2.979833 | 3.014958 | 25935872 |
| poly-medium-napi-rs | host-b | 239 | 42133 | 5.872917 | 5.908458 | 26312704 |
| poly-medium-napi-rs | worker-prototype | 239 | 42133 | 5.884083 | 5.925167 | 26312704 |
| rs-medium-aws-lambda-rust-runtime | host-a | 192 | 34990 | 2.420875 | 2.430542 | 25870336 |
| rs-medium-aws-lambda-rust-runtime | host-b | 192 | 34990 | 4.884000 | 4.908292 | 26279936 |
| rs-medium-aws-lambda-rust-runtime | worker-prototype | 192 | 34990 | 4.859417 | 4.899417 | 26279936 |
| rs-medium-axum | host-a | 301 | 54772 | 3.741459 | 3.782417 | 25968640 |
| rs-medium-axum | host-b | 301 | 54772 | 7.086375 | 7.116625 | 26312704 |
| rs-medium-axum | worker-prototype | 301 | 54772 | 7.073500 | 7.241917 | 26312704 |
| rs-medium-hyper | host-a | 98 | 15540 | 1.214167 | 1.234583 | 25591808 |
| rs-medium-hyper | host-b | 98 | 15540 | 2.893458 | 2.928209 | 25935872 |
| rs-medium-hyper | worker-prototype | 98 | 15540 | 2.907916 | 2.977125 | 25952256 |
| rs-medium-serde | host-a | 208 | 37796 | 2.595542 | 2.627542 | 25772032 |
| rs-medium-serde | host-b | 208 | 37796 | 5.178208 | 5.213417 | 26165248 |
| rs-medium-serde | worker-prototype | 208 | 37796 | 5.198083 | 5.240708 | 26198016 |
| rs-medium-serde-json | host-a | 71 | 11320 | 0.892500 | 0.902459 | 25559040 |
| rs-medium-serde-json | host-b | 71 | 11320 | 1.409917 | 1.429916 | 25886720 |
| rs-medium-serde-json | worker-prototype | 71 | 11320 | 1.407584 | 1.456333 | 25886720 |
| rs-medium-tokio | host-a | 808 | 138574 | 9.892833 | 9.955750 | 26607616 |
| rs-medium-tokio | host-b | 808 | 138574 | 17.451625 | 18.987458 | 27000832 |
| rs-medium-tokio | worker-prototype | 808 | 138574 | 17.405750 | 17.456667 | 26968064 |
| rs-large-smithy-rs | host-a | 1084 | 214098 | 13.387959 | 13.491833 | 29310976 |
| rs-large-smithy-rs | host-b | 1084 | 214098 | 22.926583 | 23.079208 | 29720576 |
| rs-large-smithy-rs | worker-prototype | 1084 | 214098 | 22.860750 | 23.062750 | 29622272 |
| poly-large-rspack | host-a | 1384 | 268029 | 17.735334 | 17.947084 | 50380800 |
| poly-large-rspack | host-b | 1384 | 268029 | 30.429875 | 30.725125 | 50806784 |
| poly-large-rspack | worker-prototype | 1384 | 268029 | 30.444666 | 30.724834 | 50823168 |
| poly-very-large-deno | host-a | 1052 | 175564 | 13.229209 | 13.333041 | 40009728 |
| poly-very-large-deno | host-b | 1052 | 175564 | 22.772333 | 22.871625 | 40452096 |
| poly-very-large-deno | worker-prototype | 1052 | 175564 | 22.893750 | 23.055541 | 40435712 |
| mr-rs-medium-serde-json | host-a | 279 | 54039 | 3.485167 | 3.545042 | 25853952 |
| mr-rs-medium-serde-json | host-b | 279 | 54039 | 6.696333 | 6.749542 | 26312704 |
| mr-rs-medium-serde-json | worker-prototype | 279 | 54039 | 6.644167 | 6.687584 | 26329088 |

The manifests are exact synthetic snapshot-equivalent descriptors over prepared source observations, not accepted SnapshotManifest transport or custody witnesses. The requested key is the bound vector illustrative shape with the actual derived scope commitment substituted; the vector expressly says this is not a validated C-2 value. No production stage/coverage-key selection or native worker executes. The worker-prototype label denotes a throwaway process role only. The encoders exercise the JSON-shaped subset of native CBOR and are not general native payload decoders/admission codecs. All actually selected Rust paths were separately checked NFC; no normalization was performed.

The scope algorithm preserves exact file-kind selection, case-sensitive .rs suffix, nonempty bytes, UTF8 path ordering, duplicate/empty refusals and contiguous ordinals. It does not impose the historical inline256 cap on this by-reference recipe. Actual admission/negotiation/token-needed rules, native source/profile/manifest custody, independently selected Plan inputs and complete worker checks remain future owners work. SM12FigureComplete=false, SM12PlaceholderFilled=false, SM14FigureComplete=false, SMComplete=false, LG1Met=false, effectiveL=false, productQualification=false. No selected stage budget or F/T/qualification assertion. All earlier accepted scopes remain closed.

## Actual private Rust helper measurements

A separate optimized bare-rustc image imports the exact unmodified candidate RSD-1 helper and links the actual release identity/JSON libraries. Eleven prepared input sets supply 110 additional fresh children, three warmups/seven measured per workload. Every complete array, scope/domain commitment and canonical array byte-length/raw-SHA matches both independent Python implementations. Parent and every direct child priority10 readbacks, owned ordinary lane, private0700TMPDIR/HOME unchanged, source/runtime pins and all raw outputs/statistics are retained. Initial unobserved build-priority evidence is historical; the measured image was rebuilt under observed parent priority10.

The timed span covers rebuild and domain_commitment after inert JSON/LogicalPath/key conversion. It includes the actual helper NFC checks and its native CBOR work; final output framing, serialization and raw-CBOR SHA are outside timing. This is a helper-only image, not an operational native worker. It supplies no accepted manifest, C-2 key derivation, negotiation or independent operational-host reconstruction. Process RSS is final wait4 macOS bytes including process/runtime/input/output work, not incremental algorithm memory. No cross-implementation speed ratio is asserted because internal checking and framing work differ.

| Workload | Subjects | Median ms | Max ms | Process peak RSS bytes |
|---|---:|---:|---:|---:|
| poly-medium-napi-rs | 239 | 1.679167 | 2.020459 | 4440064 |
| rs-medium-aws-lambda-rust-runtime | 192 | 1.076583 | 1.166250 | 4276224 |
| rs-medium-axum | 301 | 1.562084 | 1.583458 | 4325376 |
| rs-medium-hyper | 98 | 0.519458 | 0.542125 | 3260416 |
| rs-medium-serde | 208 | 1.124291 | 1.150083 | 3997696 |
| rs-medium-serde-json | 71 | 0.391208 | 0.400417 | 3047424 |
| rs-medium-tokio | 808 | 3.784083 | 3.940292 | 5996544 |
| rs-large-smithy-rs | 1084 | 5.284708 | 5.381000 | 10289152 |
| poly-large-rspack | 1384 | 6.668209 | 7.274666 | 38764544 |
| poly-very-large-deno | 1052 | 5.111917 | 5.382958 | 24870912 |
| mr-rs-medium-serde-json | 279 | 1.518167 | 1.536375 | 4292608 |

Combined record: 330 Python recipe children plus 110 exact Rust helper children, 440 total. Full SM12/SM14, native worker, actual transport/source/key admission, LG1, effective L and product qualification remain false.
