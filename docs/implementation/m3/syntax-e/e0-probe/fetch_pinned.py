#!/usr/bin/env python3
"""E0 pinned fetch (throwaway probe tool; never product code).

Fetches one commit of one public GitHub repository into a private bare repo,
verifies it, and materializes selected blobs. It follows FETCH-SPEC.md section 3:
no checkout, no hooks, no filters, no LFS smudge, no submodules, and nothing of
the repository is executed. Blobs are read with `git cat-file --batch` and written
as plain files (symlinks are recorded, never materialized).

Usage:
  fetch_pinned.py upstream <name> <url> <commit> <out_dir> [--paths PREFIX ...]
  fetch_pinned.py t2a <manifest.json> <git_dir_root> <files_root> <out_tsv>

Environment hygiene is the caller's (run_phase1.sh sets HOME, GIT_CONFIG_*).
"""
import hashlib, json, os, subprocess, sys

SELECTORS = [  # E1 item 3: nine owned code suffixes plus .d.ts; longest suffix wins (IDS dialect table)
    (".d.ts", "ts-declaration", "typescript"),
    (".rs", "rs", "rust"),
    (".ts", "ts", "typescript"),
    (".tsx", "tsx", "tsx"),
    (".mts", "mts", "typescript"),
    (".cts", "cts", "typescript"),
    (".js", "js", "javascript"),
    (".jsx", "jsx", "javascript"),
    (".mjs", "mjs", "javascript"),
    (".cjs", "cjs", "javascript"),
]

def select(path: bytes):
    """Byte-exact, case-sensitive longest-suffix match on the file name (E1 item 9)."""
    name = path.rsplit(b"/", 1)[-1]
    best = None
    for suf, variant, grammar in SELECTORS:
        s = suf.encode()
        # the suffix must be a proper suffix of the file name (a name that IS the suffix, e.g. ".ts", has empty stem;
        # U-4 takes the final extension from the last '.', so ".ts" still has extension ".ts")
        if name.endswith(s) and (best is None or len(s) > len(best[0])):
            best = (s, variant, grammar)
    return best

def git(gd, *args, inp=None):
    return subprocess.run(["git", "--git-dir", gd, "-c", "core.hooksPath=/dev/null", *args],
                          input=inp, check=True, capture_output=True).stdout

def fetch(gd, url, commit, tree=None):
    if not os.path.isdir(gd):
        os.makedirs(gd, mode=0o700)
        subprocess.run(["git", "init", "-q", "--bare", gd], check=True)
    have = subprocess.run(["git", "--git-dir", gd, "cat-file", "-e", commit + "^{commit}"], capture_output=True).returncode == 0
    if not have:
        git(gd, "fetch", "-q", "--depth", "1", "--no-tags", url, commit)
    got = git(gd, "rev-parse", commit + "^{commit}").decode().strip()
    if got != commit:
        raise SystemExit(f"FETCH-COMMIT-MISMATCH {url} {got} != {commit}")
    t = git(gd, "rev-parse", commit + "^{tree}").decode().strip()
    if tree is not None and t != tree:
        raise SystemExit(f"GIT-TREE-MISMATCH {url} {t} != {tree}")
    return t

def ls_tree(gd, commit):
    out = git(gd, "ls-tree", "-r", "-z", "--full-tree", commit)
    ents = []
    for rec in out.split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, typ, oid = meta.split(b" ")
        ents.append((path, mode.decode(), typ.decode(), oid.decode()))
    ents.sort(key=lambda e: e[0])
    return ents

class Batch:
    def __init__(self, gd):
        self.p = subprocess.Popen(["git", "--git-dir", gd, "cat-file", "--batch"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    def get(self, oid):
        self.p.stdin.write(oid.encode() + b"\n"); self.p.stdin.flush()
        hdr = self.p.stdout.readline().split()
        if len(hdr) != 3 or hdr[1] != b"blob":
            raise SystemExit(f"bad cat-file header {hdr}")
        n = int(hdr[2]); data = self.p.stdout.read(n); self.p.stdout.read(1)
        return data
    def close(self):
        self.p.stdin.close(); self.p.wait()

def content_digest(gd, commit, ents, batch):
    """opensip-t2-content-sha256/1-draft (T2a manifest contentDigestAlgorithm)."""
    h = hashlib.sha256()
    for path, mode, typ, oid in ents:
        hx = oid if typ == "commit" else hashlib.sha256(batch.get(oid)).hexdigest()
        h.update(f"{mode} {typ} {hx} ".encode() + path + b"\0")
    return h.hexdigest()

def write_file(root, path: bytes, data: bytes):
    rel = path.decode("utf-8")
    if rel.startswith("/") or ".." in rel.split("/"):
        raise SystemExit(f"unsafe path {rel!r}")
    dst = os.path.join(root, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.lexists(dst):
        if not os.path.islink(dst) and open(dst, "rb").read() == data:
            return
        os.unlink(dst)
    with open(dst, "wb") as f:
        f.write(data)
    os.chmod(dst, 0o444)

def cmd_upstream(name, url, commit, out_dir, prefixes):
    gd = os.path.join(os.path.dirname(out_dir.rstrip("/")), name + ".git")
    tree = fetch(gd, url, commit)
    ents = ls_tree(gd, commit)
    b = Batch(gd)
    rows = []
    for path, mode, typ, oid in ents:
        if typ != "blob" or mode == "120000":
            continue
        if prefixes and not any(path.startswith(p.encode()) for p in prefixes):
            continue
        data = b.get(oid)
        write_file(out_dir, path, data)
        rows.append((path.decode(), hashlib.sha256(data).hexdigest(), len(data), oid))
    b.close()
    with open(os.path.join(os.path.dirname(out_dir.rstrip("/")), name + ".pins.tsv"), "w") as f:
        f.write(f"# {name} {url} commit={commit} tree={tree}\n# path\tsha256\tbytes\tgit-blob\n")
        for r in rows:
            f.write("\t".join(map(str, r)) + "\n")
    print(f"{name}: commit={commit} tree={tree} files={len(rows)} bytes={sum(r[2] for r in rows)}")

def cmd_t2a(manifest, git_root, files_root, out_tsv):
    raw = open(manifest, "rb").read()
    m = json.loads(raw)
    print("manifest sha256", hashlib.sha256(raw).hexdigest())
    rows = []
    for r in m["repositories"]:
        if r["tranche"] != "T2a":
            continue
        rid = r["id"]
        gd = os.path.join(git_root, rid + ".git")
        fetch(gd, r["url"], r["commit"], r["gitTree"])
        ents = ls_tree(gd, r["commit"])
        b = Batch(gd)
        cd = content_digest(gd, r["commit"], ents, b)
        if cd != r["contentDigest"]["value"] or len(ents) != r["contentDigest"]["treeEntries"]:
            raise SystemExit(f"CONTENT-DIGEST-MISMATCH {rid} {cd}")
        n = 0
        for path, mode, typ, oid in ents:
            if typ != "blob":
                continue
            sel = select(path)
            if sel is None:
                continue
            if mode == "120000":   # a symlink is not a regular file; recorded, never parsed
                rows.append((rid, path.decode("utf-8"), sel[1], sel[2], "symlink", 0, "-", oid))
                continue
            data = b.get(oid)
            write_file(os.path.join(files_root, rid), path, data)
            rows.append((rid, path.decode("utf-8"), sel[1], sel[2], mode, len(data), hashlib.sha256(data).hexdigest(), oid))
            n += 1
        b.close()
        print(f"{rid}: commit={r['commit']} tree ok, contentDigest ok, selected={n}")
    rows.sort(key=lambda x: (x[0].encode(), x[1].encode()))
    with open(out_tsv, "w") as f:
        f.write("# repoId\tpath\tvariant\tgrammarId\tmode\tbytes\tsha256\tgit-blob\n")
        for x in rows:
            f.write("\t".join(map(str, x)) + "\n")
    print(f"total selected rows={len(rows)} bytes={sum(x[5] for x in rows)}")

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "upstream":
        pre = a[6:] if len(a) > 6 and a[5] == "--paths" else []
        cmd_upstream(a[1], a[2], a[3], a[4], pre)
    elif a and a[0] == "t2a":
        cmd_t2a(*a[1:5])
    else:
        raise SystemExit(__doc__)
