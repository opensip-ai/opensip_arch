# OpenSIP Codex bootstrap

These instructions apply only when working on OpenSIP repositories or their
linked worktrees. They are execution-process controls; they do not grant
implementation authority or replace plan acceptance, independent review,
binding, integration, or qualification.

Before planning, editing, testing, reviewing, or dispatching OpenSIP work:

1. Resolve the canonical architecture checkout from
   `OPENSIP_ARCHITECTURE_ROOT`, or the sibling `opensip_arch` checkout when the
   variable is unset. Read `docs/START-HERE.md` for design orientation only,
   then read `docs/implementation/m3/IMPLEMENTATION-STATUS.md` for current M3
   standing. `START-HERE.md` does not select current implementation authority.
2. Resolve the live control directory from `OPENSIP_CONTROL_ROOT`, defaulting
   to `/Users/sb/code/.opensip-implementation-cache/control-2026-10-06`. Read
   `CURRENT-STATE.json`, the top of `ACTIVE-PLAN.md`, and the exact current
   request/continuation/handoff they name. Re-check their Git pins live; older
   checkpoints are history. Locate the exact active plan. Read
   `docs/implementation/AGENT-MODEL-ROUTING.md` in the architecture checkout.
   When the live files disagree, the newest `CURRENT-STATE.json` controls over
   an older `ACTIVE-PLAN.md` checkpoint. If it does not pin one exact active
   plan and route, report `ROUTING-BLOCKED` to the current coordinator and stop;
   never select a route from an older unit example.
3. Run the route preflight before substantive work:

   ```bash
   architecture_root="${OPENSIP_ARCHITECTURE_ROOT:-$(dirname "$(git rev-parse --show-toplevel)")/opensip_arch}"
   python3 -I -B "$architecture_root/tools/agent_model_route.py" check \
     --provider codex --plan /absolute/path/to/plan.md
   ```

   If an accepted frozen plan has no route block, do not edit it merely to add
   metadata. Use its authorized execution handoff or, when none exists, the
   default route explicitly with `--route R1-BALANCED`.
   A manually started session supplies all four values explicitly, for example:

   ```bash
   python3 -I -B "$architecture_root/tools/agent_model_route.py" check \
     --provider codex --route R1-BALANCED \
     --session-route R1-BALANCED --session-provider codex \
     --session-model gpt-6.1-sol --session-effort medium
   ```
4. If preflight reports missing session metadata or any route, model, or effort
   mismatch, stop before substantive work. Start a correctly routed session
   with the tool's `launch` command, or use its `spawn` command with an
   available Herdr shell pane. Do not claim that a model was changed inside an
   already-running session. Record the transition in the current unit's named
   handoff/continuation artifact, or in the top checkpoint of `ACTIVE-PLAN.md`
   when that is the authorized live handoff.
5. Every new plan and every substantive revision of a non-frozen active plan
   must include the exact route block defined by the routing document, with
   observable escalation and de-escalation triggers. Re-run preflight after a
   route change. The old agent records a handoff and stops; the replacement
   agent continues from that handoff.

`OPENSIP_AGENT_ROUTE`, `OPENSIP_AGENT_PROVIDER`, `OPENSIP_AGENT_MODEL`, and
`OPENSIP_AGENT_EFFORT` are set by the launcher. An agent started another way
must provide the same values explicitly to `check`; otherwise preflight fails
closed.
