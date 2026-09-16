# Initial generator compatibility probes

These retained probes select two exact definitions from the accepted schemas,
with projection and source hashes. They do not exercise the full source closure
or eight generated outputs, compile every generated carrier, establish a hermetic
generator closure, or select the final tools.

- Typify0.8.0 emits a Rust `u64` carrier for the selected U64 and a checked string
  using `regress` for ClosureId's ECMAScript lookahead. An earlier assumption that
  this version necessarily uses Rust regex/lookaround refusal was incorrect.
  The generated string uses `std::sync::LazyLock`; pure-layer suitability and
  full-schema constraint coverage remain to be reviewed.
- json-schema-to-typescript16.0.0 emits `U64 = number`. That default declaration
  cannot represent the full admitted domain and is not selected as-is.
- Ajv8.20.0 draft2020 standalone compilation succeeds on both definitions and
  rejects a trailing newline in ClosureId. Native JSON parsing rounds both U64's
  maximum and its one-past-maximum to the same JS value; the latter is accepted.
  Built-in integer validation rejects `bigint`, including small values. Neither
  path satisfies exact admission. Lexical/schema parsing and generated numeric
  predicates need a lossless adapter or a different validator, with new trials.

The setup used Cargo's locked trial dependency graph and pnpm11.10.0 with
`--ignore-scripts`, Node24.16.0. Initial tool acquisition used the registries;
these are development trials, not sealed/offline release evidence. No installed
`node_modules`, build cache or private agent log is retained here.
