import copy

def apply_overlay(base, overlay, with_workaround=False):
    applied = copy.deepcopy(base)
    for change in overlay["rowChanges"]:
        row = applied["groups"][change["group"]][change["index"]]
        assert row["id"] == change["id"]
        row["source"] = change["source"]
        for field, value in change.get("fields", {}).items():
            row[field] = value
        if "owners" in change:
            row["owners"] = change["owners"]
        if "reviewIssues" in change:
            row["reviewIssues"] = change["reviewIssues"]
        if "verificationMethod" in change:
            row["verification"]["method"] = change["verificationMethod"]
    for addition in overlay["rowAdditions"]:
        applied["groups"][addition["group"]].append(addition["row"])
    applied["reviewIssues"] = applied["reviewIssues"] + overlay["reviewIssueAdditions"]
    assert not with_workaround, "no coverage workaround after the accepted K01 unit"
    return applied
