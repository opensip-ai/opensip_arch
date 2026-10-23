# OpenSIP Claude bootstrap

These instructions apply only when working on OpenSIP repositories or their
linked worktrees. They control agent selection and handoff only; they do not
change product law, authority, acceptance, review independence, binding,
integration, or qualification.

Before planning, editing, testing, reviewing, or dispatching OpenSIP work:

1. Resolve the canonical architecture checkout from
   `OPENSIP_ARCHITECTURE_ROOT`, falling back to the sibling `opensip_arch`
   checkout. Read `docs/START-HERE.md` for design orientation only, then read
   `docs/implementation/m3/IMPLEMENTATION-STATUS.md` for current M3 standing.
   `START-HERE.md` does not select current implementation authority.
2. Resolve the live control directory from `OPENSIP_CONTROL_ROOT`, defaulting
   to `/Users/sb/code/.opensip-implementation-cache/control-2026-10-06`. Read
   `CURRENT-STATE.json`, the top of `ACTIVE-PLAN.md`, and the exact current
   request/continuation/handoff they name. Verify their Git pins live and treat
   older checkpoints as history. Locate the exact active plan and read
   `docs/implementation/AGENT-MODEL-ROUTING.md` in the architecture checkout.
   When live files disagree, the newest `CURRENT-STATE.json` controls over an
   older `ACTIVE-PLAN.md` checkpoint. If it does not pin one exact active plan
   and route, report `ROUTING-BLOCKED` to the current coordinator and stop;
   never choose a route from an older unit example.
3. Run the route preflight before substantive work:

   ```bash
   architecture_root="${OPENSIP_ARCHITECTURE_ROOT:-$(dirname "$(git rev-parse --show-toplevel)")/opensip_arch}"
   python3 -I -B "$architecture_root/tools/agent_model_route.py" check \
     --provider claude --plan /absolute/path/to/plan.md
   ```

   Do not modify an accepted frozen plan only to add routing metadata. Use its
   authorized handoff, or explicitly select `--route R1-BALANCED` when it has no
   route decision.
   A manually started session supplies all four values explicitly, for example:

   ```bash
   python3 -I -B "$architecture_root/tools/agent_model_route.py" check \
     --provider claude --route R1-BALANCED \
     --session-route R1-BALANCED --session-provider claude \
     --session-model claude-sonnet-5-5 --session-effort high
   ```
4. On missing session metadata or a route, model, or effort mismatch, stop
   substantive work. Use the router's `launch` command, or its `spawn` command
   with an available Herdr shell pane, to create the required Claude session.
   A running Claude session is not silently converted to another model. Record
   the transition in the current unit's named handoff/continuation artifact, or
   in the top checkpoint of `ACTIVE-PLAN.md` when that is the authorized live
   handoff.
5. New plans and substantive revisions of non-frozen active plans include the
   exact route block from the routing document. Re-run preflight whenever that
   route changes. The prior agent writes a concise handoff and stops; the
   correctly routed replacement continues from it.

The launcher passes Claude's exact `--model` and `--effort` values and sets
`OPENSIP_AGENT_ROUTE`, `OPENSIP_AGENT_PROVIDER`, `OPENSIP_AGENT_MODEL`, and
`OPENSIP_AGENT_EFFORT`. Sessions launched by another path must supply equivalent
values explicitly to `check`, which otherwise fails closed.
