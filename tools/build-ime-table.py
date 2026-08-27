#!/usr/bin/env python3
import pathlib,sys,unicodedata
if len(sys.argv)!=3: raise SystemExit("Usage: python3 tools/build-ime-table.py <code> <readings.tsv>")
code,source=sys.argv[1],pathlib.Path(sys.argv[2]); rows={}
for number,raw in enumerate(source.read_text(encoding="utf-8").splitlines(),1):
 if not raw.strip() or raw.lstrip().startswith("#"): continue
 fields=[unicodedata.normalize("NFC",p.strip()) for p in raw.split("\t")]; reading,candidates=fields[0].lower(),[v for v in fields[1:] if v]
 if not reading or not candidates: raise SystemExit(f"Line {number}: invalid")
 rows[reading]=list(dict.fromkeys(candidates))[:16]
out=pathlib.Path("Lexicons")/f"{code}.cime"; out.parent.mkdir(exist_ok=True); out.write_text("".join("\t".join([r,*rows[r]])+"\n" for r in sorted(rows)),encoding="utf-8"); print(f"Built {out} with {len(rows):,} readings.")
