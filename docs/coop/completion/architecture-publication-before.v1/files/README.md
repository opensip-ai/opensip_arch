# opensip

Greenfield next-generation OpenSIP CLI (architecture and implementation).

## Start here

| Path | Purpose |
|------|---------|
| [`docs/coop/`](docs/coop/) | Architecture workspace (temporary name): design docs, binding contracts, checkers, reviews |
| [`docs/coop/ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md`](docs/coop/ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md) | Plan to finish architecture and begin implementation |
| [`docs/coop/GORTEX-BORROW-REGISTER.md`](docs/coop/GORTEX-BORROW-REGISTER.md) | Pinned Gortex design-source map: adopted, measured, parked, and rejected ideas |
| [`docs/coop/TREE-ENDSTATE.md`](docs/coop/TREE-ENDSTATE.md) | Post-freeze rename + layout: `docs/coop` → `docs/architecture` |
| [`docs/MAP-VS-CONTROL.md`](docs/MAP-VS-CONTROL.md) | Product planes: Control (prove) vs Map (orient); naming (`opensip` vs future Map) |

```bash
# From docs/coop — run retained architecture checkers
cd docs/coop
python3 artifacts/check-claims.py
python3 artifacts/check-completeness.py
```

After architecture freeze, rehome per `TREE-ENDSTATE.md` (do not mass-move while contracts are still in active churn).

This repository is separate from `opensip-cli` (the current shipping TypeScript monorepo).
