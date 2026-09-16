# Developer tooling

These tools are developer build and validation inputs. They are not OpenSIP
runtime configuration and do not grant evidence, execution or release authority.
Normal Rust and TypeScript consumer builds use checked-in generated sources.

## Contract generator build

`build_contracts.py` takes an explicit generator source directory, local registry
archive directory, Cargo, rustc, and a new output directory. Run it with Python
`-I -B`, without `-O`. It refuses an existing output directory, unselected source
kinds, archive checksum mismatches, unsafe tar members and ambient ancestor Cargo
configuration. It copies only its five declared generator inputs, reconstructs a
vendor directory from locked archive bytes, and builds with an empty Cargo home,
minimal environment, explicit host target and `--locked --offline --release`.

The output contains `opensip-contract-generator`, `receipt.json`, and public
compiler logs. The receipt links actual sources, builder, archives, tools,
profile and executable. It is an observed trusted-host build, not a claim of
cross-host reproducibility or complete compiler/native-library qualification.
To select a newly reviewed build, copy its receipt into
`contracts/build-receipt.json` and rebind the recipe/tool closure through review.
A drift check never builds the generator or installs dependencies.

## TypeScript tool provisioning

The generator uses only the selected TypeScript 6.0.3 package tree. Provisioning
is a separate explicit operation using the local frozen pnpm lock and already
provisioned pnpm 11.10.0. Invoke the exact pnpm `bin/pnpm.cjs` with the selected Node
binary, not the Corepack shim: a shim can download pnpm even when install has
`--offline`. The proven offline lane uses:

```
node /explicit/provisioned/pnpm/bin/pnpm.cjs install --offline --frozen-lockfile --ignore-scripts --trust-lockfile --store-dir /explicit/populated/store
```

`--trust-lockfile` is limited to this previously reviewed, exact pinned lock.
It avoids pnpm's fresh registry-metadata supply-chain check, which otherwise
runs even with `--offline`. New dependency/lock selections require separate
provisioning/policy verification and review. The lane runs with network denied,
an empty HOME, explicit empty user/global npm configs, `COREPACK_ENABLE_NETWORK=0`,
and the workspace's `ignorePnpmfile`/`ignoreScripts` settings. It then compares
all 140 materialized TypeScript files with the selected generation closure.
This establishes offline materialization, not installer filesystem confinement.

## Generation and checks

`generate_contracts.py --generator /absolute/pinned/binary --node /absolute/pinned/node`
checks all selected source, option, recipe, tool and build-receipt pins; regenerates
all eight declared files in a fresh directory; and reports exact byte drift.
`--write` explicitly publishes replacements after complete output validation and
all destination preflights. Files replace atomically one at a time; a later drift
check detects an interrupted eight-file update. The command emits one JSON summary.

Node/Rust child steps run with the pinned macOS Seatbelt development profile,
minimal environment, explicit descriptor handling and a five-minute timeout.
The system runtime remains trusted. No Linux or release qualification is implied.
The parent refuses symlinks, hard links, special/undeclared outputs and more than
128 MiB of output before reading them. Python preparation also runs confined with an exact interpreter/stdlib profile,
`-I -B -S`, and no caller environment. Its three outputs pass the same no-follow
collector before the parent constructs fresh inputs. The external design-bootstrap
join remains to select with the reviewed integration binding.

`check_dependencies.py` compares a concrete target's Cargo metadata to the pure
contracts dependency policy, including declared inactive dependencies/features.
Run it for each workspace and target in the selected build matrix. It is not an
arbitrary-native-code effect sandbox.

`verify_design.py --architecture /explicit/opensip_arch` verifies the selected
reviewed architecture bindings. The current candidate still carries the accepted
predecessor lock; new generator/source rows are not selected by that lock yet.

Python tests under `tests/` run with `python3 -I -B -m unittest discover`.
The generator execution tests use synthetic child stubs to isolate adapter
refusals; sandbox and true generator behavior have independent executed trials.
