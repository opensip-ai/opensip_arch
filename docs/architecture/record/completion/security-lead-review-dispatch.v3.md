# LEAD-CORRECTION-REVIEW 3 — v8 bounded refusal repair

Subject security-freeze.v8.json SHA-256 33dad5ec1692ccbee859ead54d17d9730999a2d61012e2e48cbd1d2ad27e44ca (72 files, 864/0).
Cumulative history is three ordinary exchanges, one UPHOLD, two failed bounded confirmations, lead review 1 OBJECT (2 MUST/1 SHOULD), lead review 2 OBJECT (0 MUST/1 SHOULD). This is lead review 3, no reset or ordinary exchange. Fresh independent reviewer authored none of v8.

The sole prior finding is fixed: canonical-profile envelope rejection is caught at step 1 and returns fixed RJ-4 UNSIGNED malformed-envelope wording, while valid envelope, routing, digest and signature precedence remain unchanged. Replay check-security-unit.v8.py and inspect the exact v7->v8 diff. Retain all prior probes and controls. Write security-lead-review.v3.json/.md with numeric verdict. ACCEPT/CONSENT requires zero MUST and SHOULD. No register edit, implementation permission or qualification follows.
