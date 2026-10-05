#!/bin/zsh
# X3c-3: release absence, then the two lead sets, one after the other.
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x3c3
$S/release.sh
grep -q "release-build exit=0" $S/release/summary.txt || { echo "CHAIN-STOP release" >> $S/logs/summary.txt; exit 1; }
$S/lead.sh x3c3-lead-1
$S/lead.sh x3c3-lead-2
echo "CHAIN-DONE" >> $S/logs/summary.txt
