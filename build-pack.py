#!/usr/bin/env python3
"""Build a basic Clink .clex dictionary from a UTF-8 word list."""
import math, pathlib, struct, sys, unicodedata
if len(sys.argv)!=3: raise SystemExit("Usage: python3 build-pack.py <language-code> <word-list.txt>")
code,source=sys.argv[1],pathlib.Path(sys.argv[2]); counts={}
for raw in source.read_text(encoding="utf-8").splitlines():
 raw=raw.strip()
 if not raw or raw.startswith("#"): continue
 fields=raw.rsplit(maxsplit=1); word,amount=(fields[0],fields[1]) if len(fields)==2 else (raw,"1")
 word=unicodedata.normalize("NFC",word.strip().lower())
 if not word or any(ch.isspace() for ch in word) or not any(ch.isalpha() for ch in word): continue
 try: count=float(amount)
 except ValueError: count=1.0
 if count>0: counts[word]=counts.get(word,0)+count
total=sum(counts.values()); entries=sorted(((w,c/total) for w,c in counts.items()),key=lambda x:x[0].encode()); letters={}
for w,p in entries:
 for ch in w: letters[ch]=letters.get(ch,0)+p
alphabet=[ch for ch,_ in sorted(letters.items(),key=lambda x:-x[1])][:48]; index={ch:i for i,ch in enumerate(alphabet)}; n=len(alphabet); rows=[[0.0]*n for _ in range(n+1)]
for w,p in entries:
 chars=list(w)
 if chars and chars[0] in index: rows[0][index[chars[0]]]+=p
 for a,b in zip(chars,chars[1:]):
  if a in index and b in index: rows[index[a]+1][index[b]]+=p
data=bytearray(b"CLEX"+struct.pack("<III",1,len(entries),n))
for ch in alphabet: data+=struct.pack("<I",ord(ch))
for row in rows:
 m=max(row,default=0); data+=bytes(round(255*v/m) if m else 0 for v in row)
offset=0
for w,_ in entries: data+=struct.pack("<I",offset); offset+=len(w.encode())
data+=struct.pack("<I",offset)
for _,p in entries: data.append(max(0,min(255,round((math.log10(p)+9)*28))))
for w,_ in entries: data.append(min(255,len(w)))
for w,_ in entries: data+=w.encode()
out=pathlib.Path("Lexicons")/f"{code}.clex"; out.parent.mkdir(exist_ok=True); out.write_bytes(data); print(f"Built {out} with {len(entries):,} words.")
