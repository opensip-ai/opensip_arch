I’ll fix the retainer so private CLI envelopes and transcripts cannot be copied, then add disposable regressions and write v2 review/hashes only in the v2 directory.I'll fix the retainer so Grok private thought never ships with the public package, then add disposable regression controls and write only into the v2 directory.I’ll inspect Grok transcript public field names (keys only) and how session paths are derived, then implement the retainer whitelist without touching the immutable v1 copies.I’ll keep the immutable v1 copies in `prepared/` and write the fixed retainer, launch cwd/permission change, helpers, and regression tests only under v2.v1’s retainer did copy the CLI raw envelope (private thought) through `src.rglob` after writing `response.public.json`. That claim of “private thought not retained” was false. The immutable v1 copy is still in `prepared/`; **do not run it**. No application-review retention was executed.

v2 fix is only under `/tmp/opensip-design-corrections/grok-application-successor-preparation.v2/`. Binder/assembler/prepare-validation/applied runner, live tree, source23, and `prepared/` were not edited. This is not the separate independent/NEW-blind work. Frozen `652c800166a8d3f37eacfbf273c9786bb84f6fd6b5c6ead57b5a254315859a25` is **not** accepted here; no application binding.

### What changed
- **Retain:** whitelist Grok public envelope; copy authored review/probes/reports; exclude CLI raw stdout **by `launch.stdoutName`** (not only `response.raw.json`), `chat_history.jsonl`, and other private CLI state. Named transcript must match URL-quoted `resolve(process cwd)` + `sessionId`. Public `tool_result` bodies are kept. Reasoning rows are dropped. Claude `tool_use`/`tool_result` selection is unchanged.
- **Launch:** Grok `acceptEdits`, `--cwd` and process cwd = application-review **output** directory, prompt still uses the absolute frozen stage, no `--resume`.

### Checks
`check-retain-public.v1.py`: **39/39**. Envelope decoder re-run: **20/20**. v1’s 20 tests still do not cover the retainer loop. Synthetic sentinel only; no real CLI private contents.

| File | sha256 |
|---|---|
| `retain-application-review.successor.v1.py` | `a7f632e39d8aa383adef114a3cf9f0a21df819e32ec6c7a887df1d463578b2e6` |
| `retain_public.py` | `15849a91fdbf75970fb6ea610158fe0e0a91e794d463a65ba909a68ec2cf8383` |
| `launch-application-review.successor.v1.py` | `6304a751b884b0a6358ab8ff9302e170b653781bd56709ce153125c7e332edcd` |
| `review.json` | `e871c8e6dd4bc1de10a5f2979662335c8c418257b277537dba964ac0ae18e890` |
| `review.md` | `12f7060c0e36a321da188f60dce6d63d4a54bb504bd8bb7ea033d398c3ba11c8` |

Full pin list: `source-hashes.json`.
