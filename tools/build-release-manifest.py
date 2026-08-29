#!/usr/bin/env python3
import hashlib
import json
import pathlib
import shutil
import sys

LANGUAGE_CODE = "zh_cn"
ASSET_SUFFIXES = (".cime", ".clex", ".cngm", ".emoji.json")

if len(sys.argv) != 4:
    raise SystemExit("usage: build-release-manifest.py VERSION OWNER/REPO OUT")

version, repo, out = sys.argv[1:]
root = pathlib.Path(__file__).resolve().parents[1]
lex = root / "Lexicons"
output = pathlib.Path(out)
assets = output / "assets"

if assets.exists():
    shutil.rmtree(assets)
assets.mkdir(parents=True, exist_ok=True)

entries = []
for suffix in ASSET_SUFFIXES:
    path = lex / f"{LANGUAGE_CODE}{suffix}"
    if not path.is_file():
        raise SystemExit(f"Missing release asset: {path}")
    rel = path.relative_to(lex).as_posix()
    name = f"{LANGUAGE_CODE}--{rel.replace('/', '--')}"
    target = assets / name
    shutil.copy2(path, target)
    data = target.read_bytes()
    entries.append(
        {
            "path": rel,
            "url": f"https://github.com/{repo}/releases/download/{version}/{name}",
            "sha256": hashlib.sha256(data).hexdigest(),
            "byteCount": len(data),
        }
    )

manifest = {
    "version": version,
    "packs": [{"code": LANGUAGE_CODE, "version": version, "assets": entries}],
}
(output / "manifest.json").write_text(
    json.dumps(manifest, separators=(",", ":")), encoding="utf-8"
)
