# Operational/store chain policy follow-up 193

Private unselected successor to 191, addressing actual Claude191 W1/T1/T2. This is not host admission or cumulative implementation acceptance.

The directory-chain inspector is explicitly for retained operational/store paths after selection. It is not S3 project discovery: S3 has stopping boundaries, ancestor fallback and explicit-project owner waiver rules. The operational chain checks every component to the filesystem root and grants no owner waiver or sticky-directory exception. Supplied UID/groups still require host admission.

The actual descriptor path now invokes one private pure helper over the observed chain. The helper uses the unchanged single-component predicates and preserves the first refusal and component index. Synthetic tests cover root, middle and leaf with foreign owner, world/group writes, ACL writers, wrong file kind and symlink; they cover authorized groups/root/invoker principals and refusal ordering. Two actual macOS path tests verify invoking UID and authorized groups reach ancestor checks. The wrong-UID regression deliberately requires an unprivileged test runner. Synthetic tests grant no OS provenance. No production retry is added.

Only security/custody.rs changes; 352 input files, 351 unchanged from191 and all37 fixtures unchanged.150 security tests and strict workspace Clippy pass. Three compiled faults (skip root policy, waive owner, drop group authorization) are killed with a green baseline. Isolated host121 passes423 workspace tests and2 doctests from232 pinned sources and51 checksum-verified dependency archives, plus metadata/version/help and source immutability checks.

Sequential samples, permission changes after observation, ABA, mount qualification, Linux ACL support, actual main/WAL/SHM custody, admitted lease/exclusion through consumption and the public host routes remain separate obligations. This does not close124F1/149N4 or turn an observation into authority.191 and its actual review remain preserved unchanged.
