#!/usr/bin/env python3
"""Self-check for patch_bmclapi.py. Run: python3 scripts/test_patch_bmclapi.py"""

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_bmclapi import process

JAVA21 = {
    "formatVersion": 1,
    "name": "Java 21",
    "runtimes": [
        {
            "checksum": {"hash": "06a3884df3d9d4072b9b6df541495d81878ad2de", "type": "sha1"},
            "downloadType": "manifest",
            "name": "java-runtime-delta",
            "runtimeOS": "linux-x64",
            "url": "https://launchermeta.mojang.com/v1/packages/06a3884df3d9d4072b9b6df541495d81878ad2de/manifest.json",
            "vendor": "mojang",
        },
        {
            "checksum": {"hash": "4a1d0bff88393d67292b2836efbb2d257df44a6a", "type": "sha1"},
            "downloadType": "archive",
            "name": "temurin21",
            "runtimeOS": "linux-arm64",
            "url": "https://github.com/adoptium/temurin21-binaries/releases/download/x.tar.gz",
            "vendor": "eclipse",
        },
    ],
}


def main() -> None:
    with tempfile.TemporaryDirectory() as root:
        path = os.path.join(root, "net.minecraft.java", "java21.json")
        os.makedirs(os.path.dirname(path))
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(JAVA21, fh)
        process(root)
        with open(path, encoding="utf-8") as fh:
            runtimes = {r["runtimeOS"]: r for r in json.load(fh)["runtimes"]}

    # rewritten -> host swapped to BMCLAPI and stale checksum dropped (Prism
    # otherwise hard-fails the Java auto-install with "Checksum mismatch")
    mojang = runtimes["linux-x64"]
    assert mojang["url"].startswith("https://bmclapi2.bangbang93.com/"), mojang["url"]
    assert "checksum" not in mojang, mojang
    # untouched upstream host -> checksum stays, it is still valid
    assert runtimes["linux-arm64"]["checksum"]["hash"] == "4a1d0bff88393d67292b2836efbb2d257df44a6a"
    print("ok")


if __name__ == "__main__":
    main()
