#!/bin/zsh
# Record D-294 after dual CONSENT at turn $1: append entry, freeze reviews, commit, push. Usage: record-D294.sh <turn>
set -e
cd /Users/sb/code/opensip-ai/opensip
S=/private/tmp/claude-501/-Users-sb-code-opensip-ai-opensip/dcbad0ae-7fad-4c78-89e7-e93d989f5501/scratchpad
T=${1:?turn}
A=docs/coop/artifacts
TS=$([ "$T" = 1 ] && echo "" || echo ".turn$T")
chmod 0444 $A/coordinator-decisions.D-294.review-adversarial.claude2$TS.json $A/coordinator-decisions.D-294.review-adversarial.codex$TS.json
TURN=$T python3 $S/make-D294-entry.py --apply
FILES=$(grep -v '^$' $S/commit-files.D-294.txt)
echo "$FILES" | grep -q '_dispatch' && { echo "refusing: dispatch text in commit list"; exit 1; }
git add $(echo "$FILES")
git status --short | grep -v '^?? ' | head -20
git commit -q -F - <<'MSG'
D-294: adopt the cross-lineage leftover-join citation convention

RULE-GOVERNED entry recorded at dual CONSENT (0 MUST-FIX, 0 SHOULD-FIX):
cross-lineage leftover-join citations are custody at recording, not
standing currency claims; a successor is required only when a cited
occupancy is superseded, a projected value the citing join relies on
changes, or the join's own lineage is superseded. Authorized by D-293
(A4). No file-08 edit; nothing marked SATISFIED; readiness effect zero.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018sTJXXiBverccbDPM2xGF8
MSG
git log -1 --format='committed %h %s'
git fetch -q origin && git merge-base --is-ancestor origin/main HEAD && git push origin main 2>&1 | tail -1
git status -sb | head -1
