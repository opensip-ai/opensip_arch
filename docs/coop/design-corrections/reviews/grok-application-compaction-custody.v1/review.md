# Application-review public custody across compaction — proposed successor

**Standing.** Actual Grok coauthor. Not independent design ACCEPT, not NEW blind, not application ACCEPT, not bind/assembly/activation. Independent24 grades are not reopened. Live, frozen24, and root application tooling were not edited. Blind consumer-b.v11 was not read.

**Verdict: `PROPOSED_FOR_ROOT_INTEGRATION`.** Proposed helper/retainer/checker bytes live only in this directory.

## Original failure

Independent24 completed with one CLI compaction. `chat_history.jsonl` is replaced by the post-compaction fragment. The current application retainer (`retain-application-review.successor.v1.py`) treats that named transcript as the complete public assistant/tool record.

Synthetic reproduction against the exact current retainer (`originals/`): a fixture with pre-compaction public read/tool deliveries in `updates.jsonl` and only the post-compaction fragment in `chat_history.jsonl` retains **only** the fragment. Check `original-v1-retainer-keeps-only-chat-fragment` passed as a defect demonstration, not as acceptance of that behavior.

Root already retained independent24 public evidence with `retain-grok-fresh-review-public.v2.py`. This work is the matching application-retain successor so a later application package does not silently drop pre-compaction public deliveries.

## Change

Public Grok assistant/tool deliveries are taken from authenticated session `updates.jsonl` derived from process cwd + `sessionId`. Named `chat_history.jsonl` mismatch refusal remains; the chat file is authenticated by path/existence only and is not the complete public record. There is no fallback that accepts a truncated chat as complete when `updates.jsonl` is missing.

Selection follows the root v2 public kinds (`user_message_chunk` prompt, `agent_message_chunk` text, `tool_call`, completed/failed `tool_call_update`) and is not an oracle copy of that script. Extra refusals: wrong session on an updates row, malformed JSON, duplicate prompt origin, duplicate `toolCallId`, `tool_result` without a prior call, missing launch `prompt.txt`, `--resume` in the process command. Private kinds/fields skipped: `agent_thought_chunk`, `auto_compact_completed` summaries, `rawOutput`, reasoning/thought/encrypted_content. `updates.jsonl` itself is not copied.

Claude `tool_use`/`tool_result` selection is unchanged. Bound receipts are not rewritten. Package file hashes are still verified before and after copy. Custom stdout / `response.raw.json` / `chat_history.jsonl` / other private CLI names remain excluded. Authored `review.json`/`review.md`/probes are copied unchanged.

## Tests

`check-retain-public.v2.py` **63/63**. Existing behavioral assertions **40/40** on adapted fixtures whose public stream is `updates.jsonl`. Envelope subset **20/20**. Synthetic sentinel only; no real CLI private contents; no application retain of independent24.

New discriminating checks: compaction pre+post retained while chat fragment is incomplete; thought/compaction/rawOutput/updates file excluded; wrong updates session / missing updates / missing prompt / duplicate origin / duplicate tool_call / malformed updates refuse with no dest writes; completed and failed deliveries retained; `--resume` process refused.

## Proposed files

| Path | Role |
|---|---|
| `retain_public.py` | Proposed helper (production name) |
| `retain-application-review.successor.v2.py` | Proposed retainer |
| `check-retain-public.v2.py` | Proposed checker |
| `originals/*` | Exact current root bytes |

Root integration: replace `application-successor-root.v1/retain_public.py` and `retain-application-review.successor.v1.py` with the proposed helper/retainer after root review. Do not treat this directory as an applied package.

## Limitations

- No actual application-review retention was run.
- Independent24 ACCEPT is not conferred or re-judged here.
- The live independent24 session stream was not read (private thought). Behavior is specified from the root v2 public selector plus the compaction gap.
- Named transcript still requires `chat_history.jsonl` to exist at the derived path (the post-compaction fragment does). Completeness comes from `updates.jsonl`.
- Claude retain is historical and unwidened.
- Not a product design change.
