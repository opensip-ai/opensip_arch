#!/usr/bin/env python3
"""p13: does the text ACTUALLY INSERTED equal the text ACTUALLY ASSESSED?

The prompt warns that no agreement about an unread version may be inferred. The coauthor record
contains three wordings: Codex's PROPOSED clarification, actual Claude's ASSESSMENT of it, and a
later CODEX-AGREED-NORMATIVE-INSERT. This compares the exact inserted paragraphs in
identity-and-evidence.md against each of those, byte-wise and paragraph-wise, so the question
"was the inserted wording the assessed wording?" is answered from bytes rather than from the
narrative in the technical review.
"""
import difflib
import hashlib
import json
import os
import re

V10 = "/tmp/opensip-design-corrections/candidate-subject.v10"
V11 = "/tmp/opensip-design-corrections/candidate-subject.v11"
DOC = "docs/v2/contracts/product-v1/identity-and-evidence.md"
AUTH = "docs/coop/design-corrections/reviews/digest-corrections-author.v9"


def read(p):
    return open(p, "r", encoding="utf-8").read()


old, new = read(os.path.join(V10, DOC)), read(os.path.join(V11, DOC))

# exact inserted lines, from a real line diff
sm = difflib.SequenceMatcher(None, old.split("\n"), new.split("\n"), autojunk=False)
inserted_blocks = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag in ("insert", "replace"):
        inserted_blocks.append({
            "tag": tag,
            "atOldLine": i1,
            "lines": new.split("\n")[j1:j2],
            "removedLines": old.split("\n")[i1:i2],
        })

inserted_text = "\n".join(l for b in inserted_blocks for l in b["lines"])
out = {
    "insertedBlockCount": len(inserted_blocks),
    "insertedLineCount": sum(len(b["lines"]) for b in inserted_blocks),
    "removedLineCount": sum(len(b["removedLines"]) for b in inserted_blocks),
    "insertedBytes": len(inserted_text.encode()),
    "docByteDelta": len(new.encode()) - len(old.encode()),
    "insertedSha256": hashlib.sha256(inserted_text.encode()).hexdigest(),
}

candidates = {}
for name in ("CODEX-PROPOSED-NORMATIVE-CLARIFICATION.md",
             "CLAUDE-ASSESSED-NORMATIVE-CLARIFICATION.md",
             "CODEX-AGREED-NORMATIVE-INSERT.md"):
    p = os.path.join(V11, AUTH, name)
    text = read(p)
    candidates[name] = {
        "bytes": len(text.encode()),
        "sha256": hashlib.sha256(text.encode()).hexdigest(),
        "containsInsertedTextVerbatim": inserted_text.strip() in text,
    }

# normalise both sides to comparable paragraph sequences (prose reflow tolerant)
def paragraphs(t):
    body = []
    for para in re.split(r"\n\s*\n", t):
        para = " ".join(para.split())
        if para and not para.startswith("#") and not para.startswith("```"):
            body.append(para)
    return body


ins_paras = paragraphs(inserted_text)
out["insertedParagraphCount"] = len(ins_paras)

for name, meta in candidates.items():
    cand_paras = paragraphs(read(os.path.join(V11, AUTH, name)))
    matched, missing = [], []
    for p in ins_paras:
        if any(p == c for c in cand_paras):
            matched.append("exact")
        elif any(p in c or c in p for c in cand_paras):
            matched.append("substring")
        else:
            best = max((difflib.SequenceMatcher(None, p, c).ratio(), c)
                       for c in cand_paras) if cand_paras else (0.0, "")
            if best[0] > 0.98:
                matched.append("near-identical")
            else:
                missing.append({"paragraph": p[:180], "bestRatio": round(best[0], 3),
                                "closest": best[1][:180]})
    meta["paragraphsMatchedExact"] = matched.count("exact")
    meta["paragraphsMatchedSubstring"] = matched.count("substring")
    meta["paragraphsNearIdentical"] = matched.count("near-identical")
    meta["paragraphsUnmatched"] = len(missing)
    meta["unmatched"] = missing
    meta["coversEveryInsertedParagraph"] = not missing

out["candidates"] = candidates
out["ASSESSED_EQUALS_INSERTED"] = candidates[
    "CLAUDE-ASSESSED-NORMATIVE-CLARIFICATION.md"]["coversEveryInsertedParagraph"]
out["AGREED_EQUALS_INSERTED"] = candidates[
    "CODEX-AGREED-NORMATIVE-INSERT.md"]["coversEveryInsertedParagraph"]
out["insertedTextPreview"] = inserted_text[:600]
print(json.dumps(out, indent=2))
