#!/bin/zsh
# X3c-3, after the lead's 2026-10-04 deadlock decision: lead set 1's host
# half alone (its storage half stands: exit 0, 2131 s), then lead set 2.
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x3c3
echo "$(date -u +%FT%TZ) chain2: lead-1 host rerun after the lead's decision" >> $S/x9/waits.txt
$S/lead.sh x3c3-lead-1 host
$S/lead.sh x3c3-lead-2
echo "CHAIN2-DONE" >> $S/logs/summary.txt
