"""Build-side complete asset enumeration. No network, package manager or signing.

Accepts a trusted retained directory descriptor and explicit build role map.
Returns manifest bytes and a candidate HostAssetPin data record; publication and
compiling that pin into the host are separate build-assembly responsibilities.
"""
import hashlib
import json
import os
import re
import stat


MANIFEST_LIMIT = 4 * 1024 * 1024
MEMBER_LIMIT = 16 * 1024 * 1024
BUNDLE_LIMIT = 32 * 1024 * 1024
FILE_LIMIT = 4096
PROJECTION_LIMIT = 16
DEPTH_LIMIT = 16
PATH_LIMIT = 4096
ROLES = frozenset(("script", "style", "font", "image", "notice"))


class AssemblyRefusal(ValueError):
    """Build diagnostic only; never a new runtime/public DomainDetailCode."""


def need(ok, code):
    if not ok:
        raise AssemblyRefusal(code)


def portable_path(path):
    # Build outputs use this deliberately narrower ASCII-lowercase namespace.
    # It avoids casefold/NFC aliases without changing public LogicalPath laws.
    need(isinstance(path, str) and 0 < len(path) <= PATH_LIMIT, "ASSET_PATH")
    parts = path.split("/")
    need(len(parts) <= DEPTH_LIMIT, "ASSET_DEPTH")
    need(all(re.fullmatch(r"[a-z0-9][a-z0-9._-]*", p, flags=re.ASCII)
             and len(p) <= 255 and p[-1] not in ". " for p in parts), "ASSET_PORTABLE_NAME")
    return parts


def digest_hex(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value, flags=re.ASCII) is not None


def stable_file_bytes(fd, limit):
    """Bounded streamed hashing; no size-proportional allocation."""
    before = os.fstat(fd)
    need(stat.S_ISREG(before.st_mode), "ASSET_NONREGULAR")
    need(before.st_size <= limit, "ASSET_MEMBER_LIMIT")
    digest = hashlib.sha256()
    count = 0
    while True:
        try:
            data = os.read(fd, min(64 * 1024, limit + 1 - count))
        except InterruptedError:
            continue
        if not data:
            break
        count += len(data)
        need(count <= limit, "ASSET_MEMBER_LIMIT")
        digest.update(data)
    after = os.fstat(fd)
    need(count == before.st_size == after.st_size
         and before.st_dev == after.st_dev and before.st_ino == after.st_ino
         and before.st_mtime_ns == after.st_mtime_ns
         and before.st_ctime_ns == after.st_ctime_ns, "ASSET_CHANGED")
    return count, digest.hexdigest()


def assemble(directory_fd, *, asset_root, manifest_path, projection_digests, roles, build_channel):
    """Read a quiescent build tree; do not write or follow any symlinks.

    directory_fd already names asset_root; discovery/custody is the caller's.
    roles maps release-relative file paths to explicit roles. It is exact: an
    extra or missing file refuses. The manifest path is the only exclusion.
    External concurrent mutation is outside build custody, but observed changes
    are refused. Load-time verification remains independently mandatory.
    """
    portable_path(asset_root)
    portable_path(manifest_path)
    need(manifest_path.startswith(asset_root + "/"), "ASSET_MANIFEST_ROOT")
    relative_manifest = manifest_path[len(asset_root) + 1:]
    need("/" not in relative_manifest, "ASSET_MANIFEST_LOCATION")
    need(build_channel in ("development", "release"), "ASSET_BUILD_CHANNEL")
    need(isinstance(projection_digests, list) and 0 < len(projection_digests) <= PROJECTION_LIMIT
         and all(digest_hex(d) for d in projection_digests)
         and projection_digests == sorted(set(projection_digests)), "ASSET_PROJECTIONS")
    need(isinstance(roles, dict) and 0 < len(roles) <= FILE_LIMIT, "ASSET_ROLES")
    for path, role in roles.items():
        portable_path(path)
        need(path.startswith(asset_root + "/") and path != manifest_path, "ASSET_ROLE_PATH")
        need(isinstance(role, str) and role in ROLES, "ASSET_ROLE")
    need(stat.S_ISDIR(os.fstat(directory_fd).st_mode), "ASSET_ROOT_NOT_DIRECTORY")
    flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_NONBLOCK
    rows = []
    count_bytes = 0
    visited_directories = 0

    def visit(fd, relative, depth):
        nonlocal count_bytes, visited_directories
        need(depth <= DEPTH_LIMIT, "ASSET_DEPTH")
        visited_directories += 1
        need(visited_directories <= FILE_LIMIT, "ASSET_DIRECTORY_LIMIT")
        before = os.fstat(fd)
        names = os.listdir(fd)
        # No hidden-name, extension or role filter may silently omit an entry.
        need(len(names) <= FILE_LIMIT + 1, "ASSET_DIRECTORY_LIMIT")
        for name in sorted(names):
            child = relative + "/" + name if relative else name
            release_path = asset_root + "/" + child
            portable_path(release_path)
            entry = os.stat(name, dir_fd=fd, follow_symlinks=False)
            need(stat.S_ISREG(entry.st_mode) or stat.S_ISDIR(entry.st_mode), "ASSET_NONREGULAR")
            if stat.S_ISDIR(entry.st_mode):
                need(release_path != manifest_path, "ASSET_MANIFEST_NONREGULAR")
                child_fd = os.open(name, flags | os.O_DIRECTORY, dir_fd=fd)
                try:
                    actual = os.fstat(child_fd)
                    need((actual.st_dev, actual.st_ino) == (entry.st_dev, entry.st_ino), "ASSET_CHANGED")
                    visit(child_fd, child, depth + 1)
                finally:
                    os.close(child_fd)
                continue
            child_fd = os.open(name, flags, dir_fd=fd)
            try:
                actual = os.fstat(child_fd)
                need(stat.S_ISREG(actual.st_mode), "ASSET_NONREGULAR")
                need((actual.st_dev, actual.st_ino) == (entry.st_dev, entry.st_ino), "ASSET_CHANGED")
                if release_path == manifest_path:
                    # Prior manifest bytes never enter their own new digest.
                    # Its type and exact spelling still must be admitted.
                    continue
                need(release_path in roles, "ASSET_UNDECLARED_FILE")
                need(len(rows) < FILE_LIMIT, "ASSET_FILE_LIMIT")
                size, digest = stable_file_bytes(child_fd, MEMBER_LIMIT)
                count_bytes += size
                need(count_bytes <= BUNDLE_LIMIT, "ASSET_BUNDLE_LIMIT")
                rows.append({"path": release_path, "sha256": digest, "bytes": size, "role": roles[release_path]})
            finally:
                os.close(child_fd)
        after = os.fstat(fd)
        need((before.st_mtime_ns, before.st_ctime_ns) == (after.st_mtime_ns, after.st_ctime_ns), "ASSET_DIRECTORY_CHANGED")

    visit(directory_fd, "", 1)
    rows.sort(key=lambda row: row["path"].encode("ascii"))
    need([row["path"] for row in rows] == sorted(roles), "ASSET_MISSING_FILE")
    body = {"schemaVersion": 1, "projectionSchemaSha256s": projection_digests, "assets": rows}
    # Only bounded ASCII strings and exact nonnegative integers enter this
    # private canonical JSON projection; no float/Unicode ordering ambiguity.
    manifest = json.dumps(body, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")
    need(0 < len(manifest) <= MANIFEST_LIMIT, "ASSET_MANIFEST_LIMIT")
    need(count_bytes + len(manifest) <= BUNDLE_LIMIT, "ASSET_BUNDLE_LIMIT")
    pin = {"schemaVersion": 1, "assetRoot": asset_root, "assetManifestPath": manifest_path,
           "assetManifestSha256": hashlib.sha256(manifest).hexdigest(),
           "assetManifestBytes": len(manifest), "buildChannel": build_channel}
    return manifest, pin
