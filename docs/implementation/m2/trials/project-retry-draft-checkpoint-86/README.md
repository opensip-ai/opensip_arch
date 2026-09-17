# Private project lease retry86

Exact322-file85 parent;322 pins/321 unchanged, only lifecycle leases.rs changed. No dependency/inventory/fixture changes. Optional project retry composes nested five-second fence acquisition with one thirty-second overall budget using raw sleep-inclusive clock brackets and boot continuity. Busy attempts release fence and any partial leases before1/2/4/8/15-second backoff. Backoff and fence polling are capped by the remaining total budget; late acquired leases are dropped, non-busy errors are not retried.

12 lifecycle tests/strict workspace Clippy-r2 passed. Tests use actual kernel guards with scripted clocks to verify release during every backoff, partial-writer release, success after blocker release, late-guard cleanup, aggregate fence-wait budget, non-busy refusal and native awake fast path. Initial lint caught production items after the test module; source beforeimage/log retained and items reordered without behavior changes. Freshhost49 pending on final bytes.

No authenticated namespace registry, root/path custody, journal transitions, Linux qualification or hard response-time guarantee. OS scheduling/syscall stalls may delay return; no lease is returned after an observed deadline. Actual independent review and selection remain.
