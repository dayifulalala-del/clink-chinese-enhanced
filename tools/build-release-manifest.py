#!/usr/bin/env python3
import hashlib,json,pathlib,shutil,sys
if len(sys.argv)!=4: raise SystemExit("usage: build-release-manifest.py VERSION OWNER/REPO OUT")
version,repo,out=sys.argv[1:]; root=pathlib.Path(__file__).resolve().parents[1]; lex=root/"Lexicons"; output=pathlib.Path(out); assets=output/"assets"; assets.mkdir(parents=True,exist_ok=True); packs=[]
for clex in sorted(lex.glob("*.clex")):
 code=clex.stem; entries=[]
 for path in sorted(lex.glob(code+".*")):
  files=list(path.rglob("*")) if path.is_dir() else [path]
  for f in files:
   if not f.is_file(): continue
   rel=f.relative_to(lex).as_posix(); name=code+"--"+rel.replace("/","--"); target=assets/name; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(f,target); data=target.read_bytes(); entries.append({"path":rel,"url":f"https://github.com/{repo}/releases/download/{version}/{name}","sha256":hashlib.sha256(data).hexdigest(),"byteCount":len(data)})
 packs.append({"code":code,"version":version,"assets":entries})
(output/"manifest.json").write_text(json.dumps({"version":version,"packs":packs},separators=(",",":")),encoding="utf-8")
