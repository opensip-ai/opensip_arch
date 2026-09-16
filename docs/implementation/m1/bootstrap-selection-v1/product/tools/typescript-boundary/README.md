# TypeScript boundary checker

Run npm test after explicit provisioning with this package's independent lock. The current developer regression profile requires macOS and Node24.16.0, including real /tmp alias checks. TypeScript6.0.3/esbuild0.28.2 are trusted tools. Historical/synthetic approval fixtures are regression-only; upstream verify_design owns actual approval semantics.

The checker recognizes existing generated JavaScript only when a regular file exactly matches the selected compiler's in-memory emission from a declared TypeScript input, including an emitted byte-order mark. It maps that output back to the owned source for runtime imports and asset references. Directory names such as dist do not exempt files. Changed, linked, stale and unexpected artifacts refuse. Missing outputs still permit source analysis; a passing check is not a runnable-build or full dependency-closure guarantee.

The suite preserves 224 prior regressions and adds 10 compile/check-cycle regressions (234 total). Its disposable staging map uses stable product filenames with historical aliases only inside the test directory. No installation occurs during tests. Other platform, release and fresh blind consumer qualification remain separate.

Checker10 refuses undeclared local JavaScript runtime targets before parsing, including altered compiler outputs after failed census. The full regression suite contains 234 tests.
