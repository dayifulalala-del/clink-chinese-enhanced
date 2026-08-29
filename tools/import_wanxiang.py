#!/usr/bin/env python3
"""Convert Wanxiang dictionaries into Clink zh_cn source files."""
from __future__ import annotations
import json, math, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
WANXIANG = pathlib.Path("/tmp/wanxiang/dicts")
OUT = ROOT / "source"
TONE_MAP = str.maketrans({
    "ā":"a","á":"a","ǎ":"a","à":"a","ē":"e","é":"e","ě":"e","è":"e",
    "ī":"i","í":"i","ǐ":"i","ì":"i","ō":"o","ó":"o","ǒ":"o","ò":"o",
    "ū":"u","ú":"u","ǔ":"u","ù":"u","ǖ":"v","ǘ":"v","ǚ":"v","ǜ":"v","ü":"v",
    "ń":"n","ň":"n","ǹ":"n","ḿ":"m",
})

def strip_reading(pinyin: str) -> str:
    raw = pinyin.strip().lower().translate(TONE_MAP).replace("ü","v").replace("u:","v")
    raw = re.sub(r"[\u0300-\u036f]", "", raw)
    parts = [p for p in re.split(r"[\s'\’·\-]+", raw) if p]
    return re.sub(r"[^a-z]", "", "".join(parts))

def initials(pinyin: str) -> str:
    raw = pinyin.strip().lower().translate(TONE_MAP).replace("ü","v").replace("u:","v")
    parts = [p for p in re.split(r"[\s'\’·\-]+", raw) if p]
    out=[]
    for p in parts:
        p=re.sub(r"[^a-z]","",p)
        if not p: continue
        out.append(p[:2] if p.startswith(("zh","ch","sh")) else p[0])
    return "".join(out)

def parse_dict(path: pathlib.Path):
    text=path.read_text(encoding="utf-8")
    body=text.split("\n...\n",1)[-1] if "\n...\n" in text else text
    rows=[]
    for line in body.splitlines():
        if not line.strip() or line[0] in "#-{}" or line.startswith(("name:","version:","sort:","import_tables","...")): continue
        parts=line.split("\t")
        if len(parts)<2: continue
        word,py=parts[0].strip(),parts[1].strip()
        if not word or not py: continue
        try: weight=int(float(parts[2])) if len(parts)>2 else 1
        except ValueError: weight=1
        if weight>=0: rows.append((word,py,weight))
    return rows

def add_candidates(table, reading, word, weight):
    if not reading or not word or len(reading)>28: return
    bucket=table.setdefault(reading,{})
    if weight>bucket.get(word,0): bucket[word]=weight

def ranked(bucket, limit=16):
    return [w for w,_ in sorted(bucket.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]]

_PHRASE_FILE = ROOT / "source" / "extra-phrases.json"
if not _PHRASE_FILE.exists():
    raise SystemExit(f"Missing {_PHRASE_FILE}")
EXTRA_PHRASES=[tuple(item) for item in json.loads(_PHRASE_FILE.read_text(encoding="utf-8"))]

def load_table():
    table={}; word_freq={}; syllables=set()
    def ingest(rows, min_weight=0, max_chars=8, into_dict=True):
        kept=0
        for word,py,weight in rows:
            if weight<min_weight or len(word)>max_chars: continue
            reading=strip_reading(py)
            if not reading: continue
            add_candidates(table, reading, word, weight)
            if into_dict: word_freq[word]=max(word_freq.get(word,0), weight)
            kept+=1
        return kept
    zi=parse_dict(WANXIANG/"zi.dict.yaml")
    print("zi", ingest(zi,0,1,True))
    for word,py,weight in zi:
        reading=strip_reading(py)
        if reading: syllables.add(reading)
    print("jichu>=1500", ingest(parse_dict(WANXIANG/"jichu.dict.yaml"),1500,4,True))
    print("duoyin>=400", ingest(parse_dict(WANXIANG/"duoyin.dict.yaml"),400,6,True))
    print("cuoyin", ingest(parse_dict(WANXIANG/"cuoyin.dict.yaml"),0,8,False))
    print("diming>=200", ingest(parse_dict(WANXIANG/"diming.dict.yaml"),200,6,True))
    print("renming>=400", ingest(parse_dict(WANXIANG/"renming.dict.yaml"),400,3,True))
    print("mingren>=200", ingest(parse_dict(WANXIANG/"mingren.dict.yaml"),200,6,True))
    print("yiren>=200", ingest(parse_dict(WANXIANG/"yiren.dict.yaml"),200,6,True))
    print("lianxiang>=80", ingest(parse_dict(WANXIANG/"lianxiang.dict.yaml"),80,8,True))
    for word,py,weight in EXTRA_PHRASES:
        reading=strip_reading(py)
        add_candidates(table, reading, word, weight)
        word_freq[word]=max(word_freq.get(word,0), weight)
    high=[(w,py,wt) for w,py,wt in parse_dict(WANXIANG/"jichu.dict.yaml") if wt>=30000 and 2<=len(w)<=4]
    high += [(w,py,wt) for w,py,wt in EXTRA_PHRASES if 2<=len(w)<=4]
    added_jp=0
    for word,py,weight in high:
        reading=strip_reading(py)
        variants={initials(py), initials(py).replace("zh","z").replace("ch","c").replace("sh","s")}
        for jp in variants:
            if not jp or jp==reading or jp in syllables or len(jp)<2: continue
            add_candidates(table, jp, word, max(1, weight//4)); added_jp+=1
    print("jianpin mappings", added_jp)
    firsts={"yi":"一","er":"二","san":"三","si":"四","wu":"五","wo":"我","ni":"你","ta":"他","de":"的","le":"了","shi":"是","bu":"不","you":"有","zai":"在","he":"和","lv":"绿","lve":"略","nv":"女","nve":"虐","hao":"好","zhong":"中","guo":"国","ren":"人","da":"大","xiao":"小","shang":"上","xia":"下","tian":"天","di":"地","men":"们","ge":"个","zg":"中国","zhg":"中国","bj":"北京","wx":"微信","nh":"你好"}
    for reading,word in firsts.items():
        bucket=table.setdefault(reading,{}); bucket[word]=max(bucket.values(), default=1)+1
    return table, word_freq, syllables

CHAT_FRAMES=[["我","想"],["我","要"],["我","在"],["你","在"],["你","想"],["我们","一起"],["今天","我"],["明天","我"],["现在","想"],["等一下"],["先"],["待会"],["晚上"],["早上"]]
CHAT_TAILS=["吃饭","睡觉","回家","上班","下班","工作","学习","休息","出去","出门","买东西","看电影","看视频","玩游戏","聊天","打电话","发消息","洗澡","做饭","开车","坐车","开会","加班","请假","到家","看看","处理","回复"]

def write_sentences(word_freq, path):
    lines=[]
    def keep(*tokens):
        if all(t in word_freq for t in tokens): lines.append(" ".join(tokens))
    for s in ["你 好","你 好 吗","在 吗","好 的","没 问题","不 知道","晚上 一起 吃饭","我 想 你","谢谢 你","对 不 起","没 关系","我 在 路上","快 到 了","先 这样","外卖 到 了","晚安","早安","加油","打开 微信","语言 包"]:
        lines.append(s)
    for head in CHAT_FRAMES:
        for tail in CHAT_TAILS: keep(*head, tail)
    top=[w for w,_ in sorted(word_freq.items(), key=lambda kv:-kv[1]) if 1<=len(w)<=3][:800]
    function=[w for w in ("的","了","在","和","是","我","你","他","她","我们","很","也","都","就","还","不","没","有","要","想","能","会","可以") if w in word_freq]
    for a in function:
        for b in top[:120]:
            if a!=b: keep(a,b)
    uniq=list(dict.fromkeys(lines))
    path.write_text("\n".join(uniq)+"\n", encoding="utf-8")
    return len(uniq)

def write_emoji(path):
    data={"version":1,"aliases":{},"stopwords":["的","了","和","是","在","有","我","你","他","这"]}
    for candidate in (pathlib.Path("/tmp/zh.emoji.json"), path):
        if candidate.exists():
            data=json.loads(candidate.read_text(encoding="utf-8")); break
    extras={"⌨️":["键盘","输入法"],"🇨🇳":["中国","中文"],"🍚":["吃饭","米饭"],"📱":["手机","微信"],"🔥":["火","厉害","热门"],"👍":["赞","可以","好的"],"🙏":["谢谢","拜托","感谢"]}
    for glyph, aliases in extras.items():
        cur=data.setdefault("aliases",{}).setdefault(glyph,[])
        for a in aliases:
            if a not in cur: cur.append(a)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return len(data.get("aliases",{})), len(data.get("stopwords",[]))

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    table, word_freq, syllables = load_table()
    ime_path = OUT / "zh_cn-ime.tsv"
    with ime_path.open("w", encoding="utf-8") as fh:
        for reading in sorted(table):
            cands=ranked(table[reading],16)
            if cands: fh.write(reading+"\t"+"\t".join(cands)+"\n")
    dict_words=dict(word_freq)
    for bucket in table.values():
        for word,weight in bucket.items(): dict_words[word]=max(dict_words.get(word,0), weight)
    items=[]
    for word,weight in dict_words.items():
        if len(word)==1 and weight<200: continue
        items.append((word, max(1, int(round(1000*math.log10(weight+1))))))
    items.sort(key=lambda x: (-x[1], x[0]))
    (OUT/"zh_cn.txt").write_text("".join(f"{w}\t{s}\n" for w,s in items), encoding="utf-8")
    sent_n=write_sentences(dict_words, OUT/"zh_cn.sentences.txt")
    emoji_n, stop_n=write_emoji(ROOT/"Lexicons"/"zh_cn.emoji.json")
    stats={"languageCode":"zh_cn","version":"v0.4.0","source":"amzxyz/rime-wanxiang (CC BY 4.0) + community phrases","ime_readings":sum(1 for _ in ime_path.open(encoding="utf-8")),"clex_entries":len(items),"sentence_lines":sent_n,"emoji_aliases":emoji_n,"emoji_stopwords":stop_n,"syllables":len(syllables)}
    (ROOT/"BUILD-STATS.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=2))

if __name__=="__main__":
    main()
