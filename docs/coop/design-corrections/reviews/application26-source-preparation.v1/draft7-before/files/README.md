# OpenSIP design and architecture

Start with [docs/START-HERE.md](docs/START-HERE.md) for the curated documentation map. The architecture record preserves original custody paths so frozen references and digests remain valid.

**Current complete product design — D-372:** Read the [product contracts](docs/v2/contracts/product-v1/README.md), [current readiness](docs/v2/architecture/08-decision-and-readiness-register.md#unified-product-design-readiness), and [exact application record](docs/coop/design-corrections/application.v1.json). Implementation is not authorized; supported-platform qualification remains required.

The preview handoff below is retained as D-369 history. It is not a competing current design or the current implementation handoff.

# opensip

Greenfield next-generation OpenSIP CLI. The preview architecture is complete under D-369; implementation authorization and release qualification remain separate.

## Start here

Read the [accepted reference architecture](docs/coop/completion/reference-architecture.v2.md) and [readiness register](docs/v2/architecture/08-decision-and-readiness-register.md). The [application manifest](docs/coop/completion/architecture-application.v1.json) pins the design, evidence, reviews and row dispositions.

| Path | Purpose |
|------|---------|
| [`docs/coop/`](docs/coop/) | Architecture workspace (temporary name): design docs, binding contracts, checkers, reviews |
| [`docs/coop/ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md`](docs/coop/ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md) | Historical planning record; current implementation order is in the reference handoff |
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
