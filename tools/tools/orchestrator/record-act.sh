#!/bin/zsh
# Record an act after dual CONSENT: freeze reviews, append entry via its builder, commit (listed files only), push.
# Usage: record-act.sh <D-NNN> <turn> <entry-builder.py> <commit-subject> [<commit-body-file>]
set -e
cd /Users/sb/code/opensip-ai/opensip
S=/private/tmp/claude-501/-Users-sb-code-opensip-ai-opensip/dcbad0ae-7fad-4c78-89e7-e93d989f5501/scratchpad
NEW=${1:?D-NNN}; T=${2:?turn}; BUILDER=${3:?builder}; SUBJECT=${4:?commit subject}; BODY=${5:-}
A=docs/coop/artifacts
TS=$([ "$T" = 1 ] && echo "" || echo ".turn$T")
chmod 0444 $A/coordinator-decisions.$NEW.review-adversarial.*.json
TURN=$T python3 $BUILDER entry --apply
FILES=$(grep -v '^$' $S/commit-files.$NEW.txt)
echo "$FILES" | grep -q '_dispatch' && { echo "refusing: dispatch text in commit list"; exit 1; }
git add $(echo "$FILES")
git status --short | grep -v '^?? ' | head -30
{ echo "$SUBJECT"; echo; [ -n "$BODY" ] && cat "$BODY" && echo; echo "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"; echo "Claude-Session: https://claude.ai/code/session_018sTJXXiBverccbDPM2xGF8"; } | git commit -q -F -
git log -1 --format='committed %h %s'
git fetch -q origin && git merge-base --is-ancestor origin/main HEAD && git push origin main 2>&1 | tail -1
git status -sb | head -1
