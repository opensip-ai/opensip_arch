"""Update review.json with the completed root-inventory comparison (p15 corrects p01)."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v32'
p15 = json.load(open(os.path.join(BASE, 'receipts', 'p15-rootdelta.json')))
R = json.load(open(os.path.join(BASE, 'review.json')))
R['delta31to32']['rootInventoryLocated'] = True
R['delta31to32']['rootInventoryComparison'] = (
    'root-delta31-to32.json names 26 paths and declares 0 removals. My independently derived set is '
    'the SAME 26 paths, with the same 0 removals. My delta was derived from the two frozen manifests '
    'before consulting it, and root\'s listing is an inventory, not approval.')
R['delta31to32']['rootInventoryAgreement'] = {
    'rootDeclaredPaths': p15['rootDeclaredCount'], 'myTouchedPaths': p15['myTouchedCount'],
    'inMineNotRoot': p15['inMineNotRoot'], 'inRootNotMine': p15['inRootNotMine'],
    'agrees': p15['agrees']}
R['delta31to32']['locationCorrection'] = (
    'My p01 probe searched the reviews tree and a /tmp path and reported the inventory as not '
    'locatable. It is in my own runtime root. The earlier statement is corrected here; p01 is '
    'preserved.')
lim = [x for x in R['limitations'] if 'root-delta31-to32.json was not locatable' not in x]
lim.append('My first delta probe looked for root-delta31-to32.json in the reviews tree and /tmp and '
           'missed that it was in my own runtime root; the comparison is completed in p15 and agrees '
           'on all 26 paths.')
R['limitations'] = lim
json.dump(R, open(os.path.join(BASE, 'review.json'), 'w'), indent=1, default=str)
print('review.json updated; agreement:', p15['agrees'])
print('limitations rows:', len(R['limitations']))
