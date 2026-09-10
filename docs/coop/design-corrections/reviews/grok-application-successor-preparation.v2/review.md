# v2 retainer public-copy fix — coauthor preparation

Not independent design review. Not NEW blind. Frozen evaluator3 subject `652c800166a8d3f37eacfbf273c9786bb84f6fd6b5c6ead57b5a254315859a25` is not accepted here. No application binding or activation.

v1 public-envelope selftest (20) did not cover the retainer copy loop. That standing stays honest. The immutable v1 tools remain in `prepared/`. Do not run `prepared/retain-application-review.successor.v1.py`.

## Defect

`prepared/retain-application-review.successor.v1.py` wrote a sanitized `response.public.json` into the review working directory, then `src.rglob` copied **every** file, including the CLI raw envelope (`thought`) wherever stdout landed (`response.raw.json` by default, or any `launch.stdoutName`). Custody claimed private thought was not retained. That claim was false. No actual application-review retention had run.

## Fix (v2 only)

- `retain-application-review.successor.v1.py` + `retain_public.py`: whitelist Grok public envelope keys; copy authored review/probes/reports/custody; exclude CLI raw envelope by **receipt stdoutName**, `response.raw.json`, `chat_history.jsonl`, and other private CLI state names. Named Grok transcript must equal URL-quoted `Path(process cwd).resolve()` + `sessionId` under the sessions root. Public `tool_result.content` is retained, not a character count. Reasoning rows are dropped.
- Claude selector unchanged: `tool_use` / `tool_result` only.
- `launch-application-review.successor.v1.py`: Grok `--permission-mode acceptEdits` (CLI-verified), `--cwd` and process cwd are the **application-review output directory**, prompt still names the absolute frozen stage, no `--resume`.

Binder, assembler, prepare-validation, and applied runner were not edited.

## Tests

`check-retain-public.v1.py`: **39/39**. Envelope decoder subset **20/20**. Synthetic sentinel only; no real CLI private contents; no future application run.

Covered: custom and default raw envelope exclusion, transcript exclusion, public text and tool-result body retained, authored review bytes unchanged, wrong session path / cancelled / coauthor refuse with no dest writes, Claude selector not widened, launch acceptEdits + output cwd + no resume.
