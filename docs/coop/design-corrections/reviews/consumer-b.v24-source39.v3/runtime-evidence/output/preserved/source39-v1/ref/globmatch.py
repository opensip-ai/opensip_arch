"""Portable glob matching v1 (docs/coop/design-corrections/foundation/glob-pattern-contract.v1.md)."""


def _segment_match(pat, cand):
    # '*' zero or more scalars within a segment, '?' exactly one scalar; everything else literal.
    p, c = list(pat), list(cand)
    memo = {}

    def m(i, j):
        key = (i, j)
        if key in memo:
            return memo[key]
        if i == len(p):
            r = j == len(c)
        elif p[i] == '*':
            r = m(i + 1, j) or (j < len(c) and m(i, j + 1))
        elif p[i] == '?':
            r = j < len(c) and m(i + 1, j + 1)
        else:
            r = j < len(c) and p[i] == c[j] and m(i + 1, j + 1)
        memo[key] = r
        return r

    return m(0, 0)


def glob_match(pattern, candidate):
    P = pattern.split('/')
    S = candidate.split('/')
    memo = {}

    def m(i, j):
        key = (i, j)
        if key in memo:
            return memo[key]
        if i == len(P):
            r = j == len(S)
        elif P[i] == '**':
            r = any(m(i + 1, k) for k in range(j, len(S) + 1))
        else:
            r = j < len(S) and _segment_match(P[i], S[j]) and m(i + 1, j + 1)
        memo[key] = r
        return r

    return m(0, 0)


def scope_document_selects(scope_doc, path):
    """ScopeDocumentV1: at least one include matches and no exclude matches (exclusion wins)."""
    if not any(glob_match(p, path) for p in scope_doc['include']):
        return False
    return not any(glob_match(p, path) for p in scope_doc.get('exclude', []))


def rule_enumeration_selects(include, exclude, path):
    """Composition section 2: include absent or [] means all paths; exclusion wins."""
    inc = include or []
    if inc and not any(glob_match(p, path) for p in inc):
        return False
    return not any(glob_match(p, path) for p in (exclude or []))
