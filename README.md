# opensip

Greenfield next-generation OpenSIP CLI. The preview architecture is complete under D-369; implementation authorization and release qualification remain separate.

## Start here

Read the [accepted reference architecture](docs/architecture/record/completion/reference-architecture.v2.md) and [readiness register](docs/architecture/current/08-decision-and-readiness-register.md). The [application manifest](docs/architecture/record/completion/architecture-application.v1.json) pins the design, evidence, reviews and row dispositions.

| Path | Purpose |
|------|---------|
| [`docs/architecture/record/`](docs/architecture/record/) | Architecture workspace (temporary name): design docs, binding contracts, checkers, reviews |
| [`docs/architecture/record/ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md`](docs/architecture/record/ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md) | Historical planning record; current implementation order is in the reference handoff |
| [`docs/architecture/record/GORTEX-BORROW-REGISTER.md`](docs/architecture/record/GORTEX-BORROW-REGISTER.md) | Pinned Gortex design-source map: adopted, measured, parked, and rejected ideas |
| [`docs/architecture/record/TREE-ENDSTATE.md`](docs/architecture/record/TREE-ENDSTATE.md) | Post-freeze rename + layout: `docs/coop` → `docs/architecture` |
| [`docs/MAP-VS-CONTROL.md`](docs/MAP-VS-CONTROL.md) | Product planes: Control (prove) vs Map (orient); naming (`opensip` vs future Map) |

```bash
# From docs/coop — run retained architecture checkers
cd docs/coop
python3 artifacts/check-claims.py
python3 artifacts/check-completeness.py
```

After architecture freeze, rehome per `TREE-ENDSTATE.md` (do not mass-move while contracts are still in active churn).

This repository is separate from `opensip-cli` (the current shipping TypeScript monorepo).
