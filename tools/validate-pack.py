#!/usr/bin/env python3
import json,pathlib,struct,sys
code=sys.argv[1]; root=pathlib.Path("Lexicons"); errors=[]; lex=root/f"{code}.clex"; ng=root/f"{code}.cngm"
if not lex.exists(): errors.append(f"Missing {lex}")
else:
 d=lex.read_bytes()
 if len(d)<16 or d[:4]!=b"CLEX" or struct.unpack_from("<I",d,4)[0]!=1: errors.append("Invalid CLEX")
if ng.exists():
 d=ng.read_bytes()
 if len(d)<12 or d[:4]!=b"CNGM" or struct.unpack_from("<I",d,4)[0]!=1: errors.append("Invalid CNGM")
ime=root/f"{code}.cime"
if ime.exists() and not ime.read_bytes().strip(): errors.append("Empty CIME")
em=root/f"{code}.emoji.json"
if em.exists():
 try:
  j=json.loads(em.read_text(encoding="utf-8")); assert j.get("version")==1 and isinstance(j.get("aliases"),dict) and isinstance(j.get("stopwords"),list)
 except Exception as e: errors.append(f"Invalid emoji metadata: {e}")
if errors: raise SystemExit("\n".join("ERROR: "+e for e in errors))
print(f"{code}: looks ready for release.")
