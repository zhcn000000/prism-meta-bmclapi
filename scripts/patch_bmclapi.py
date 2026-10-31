#!/usr/bin/env python3
"""Rewrite PrismLauncher meta to point at BMCLAPI. Port of worker.js.

Usage: patch_bmclapi.py [ROOT]   (default ROOT = "upstream")
"""

import json
import os
import re
import sys

REPLACEMENTS = [
    # === Mojang ===
    (re.compile(r"launchermeta\.mojang\.com"), "bmclapi2.bangbang93.com"),
    (re.compile(r"piston-meta\.mojang\.com"), "bmclapi2.bangbang93.com"),
    (re.compile(r"piston-data\.mojang\.com"), "bmclapi2.bangbang93.com"),
    (re.compile(r"launcher\.mojang\.com"), "bmclapi2.bangbang93.com"),
    (re.compile(r"resources\.download\.minecraft\.net"), "bmclapi2.bangbang93.com/assets"),
    (re.compile(r"libraries\.minecraft\.net"), "bmclapi2.bangbang93.com/maven"),
    # === Fabric ===
    (re.compile(r"meta\.fabricmc\.net"), "bmclapi2.bangbang93.com/fabric-meta"),
    (re.compile(r"maven\.fabricmc\.net"), "bmclapi2.bangbang93.com/maven"),
    # === Forge ===
    (re.compile(r"maven\.minecraftforge\.net"), "bmclapi2.bangbang93.com/maven"),
    (re.compile(r"files\.minecraftforge\.net/maven"), "bmclapi2.bangbang93.com/maven"),
    # === Liteloader ===
    (
        re.compile(r"dl\.liteloader\.com/versions/versions\.json"),
        "bmclapi2.bangbang93.com/maven/com/mumfrey/liteloader/versions.json",
    ),
    (re.compile(r"dl\.liteloader\.com/versions"), "bmclapi2.bangbang93.com/maven"),
    # === Neoforge ===
    (re.compile(r"maven\.neoforged\.net/releases"), "bmclapi2.bangbang93.com/maven"),
    # === Quilt ===
    (re.compile(r"maven\.quiltmc\.org/repository/release"), "bmclapi2.bangbang93.com/maven"),
    (re.compile(r"meta\.quiltmc\.org"), "bmclapi2.bangbang93.com/quilt-meta"),
]


def strip_index_hashes(body: str) -> str:
    """Drop sha256/sha1 from index 'versions'/'packages' entries, and the
    'checksum' of Java runtime manifest entries served through BMCLAPI.

    Required: once the referenced file is rewritten its hash no longer matches,
    and Prism hard-fails online with "Checksum mismatch" when the advertised
    hash is present. Index files themselves are never hashed, so this is safe.

    BMCLAPI also re-serialises the Java runtime manifests it mirrors (same JSON,
    different bytes), so their advertised sha1 never matches the served file and
    Prism refuses to auto-install Java. Runtimes hosted elsewhere (Adoptium, ...)
    keep their checksum since those downloads are not rewritten.
    """
    try:
        data = json.loads(body)
    except ValueError:
        return body

    modified = False
    for key in ("versions", "packages"):
        entries = data.get(key)
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            for h in ("sha256", "sha1"):
                if h in entry:
                    del entry[h]
                    modified = True

    for runtime in data.get("runtimes") or []:
        if not isinstance(runtime, dict):
            continue
        if "checksum" in runtime and "bmclapi2.bangbang93.com" in runtime.get("url", ""):
            del runtime["checksum"]
            modified = True

    if not modified:
        return body
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def process(root: str) -> int:
    changed = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", ".github")]
        for name in filenames:
            if not name.endswith(".json"):
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8") as fh:
                body = fh.read()

            new = body
            for pattern, repl in REPLACEMENTS:
                new = pattern.sub(repl, new)
            new = strip_index_hashes(new)

            if new != body:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new)
                changed += 1
    return changed


def main() -> None:
    root = sys.argv[1] if len(sys.argv) > 1 else "upstream"
    if not os.path.isdir(root):
        sys.exit(f"error: '{root}' is not a directory")
    print(f"rewrote {process(root)} file(s) under {root}/")


if __name__ == "__main__":
    main()
