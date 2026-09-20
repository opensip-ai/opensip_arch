# Incomplete logical owner215 revision12

Closes paired-review T1: exact revoked-before-BEGIN restriction also prevents a below-threshold observation from interrupting RECOVERY to ordinary-enterable QUORUM-LOST. Observation stays RECOVERY, COMMIT independently needs quorum, ABORT returns REVOKED, private termination preserves REVOKED. Producers must admit BEGIN and active evidence, not invent a false Boolean from unavailable data. U1 adds missing active-evidence refusal to private-reset model. U2 explicitly leaves current Revoked record unreset while established U gets evidenced ROOT_CHANGED.

Current coordination model6272ordinary/4096genesis/1024accepted,80historycells,1protected full-sequence regression,26258profile-states1075413edges12987closed. Corpus r6:46named44distinct unsafevariants exactlabels+baselinePASS. Mixed-history two-role profile now includes revoked-source BEGIN; generic RECOVERY cells represent non-revoked source. Private reset42exact/4refusal cases;6unsafevariants exactlabels+baselinePASS. Models conditional, no authenticated BEGIN/time/custody producer claim.

222r6 prose aligns active restriction and retry capacity;203 working source fence/layout integration remains unbound. Exact schemas/creator/command/reference integration owed. No selected product or implementation approval.
