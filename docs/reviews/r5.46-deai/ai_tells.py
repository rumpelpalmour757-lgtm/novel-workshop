"""Count common Chinese AI-prose tells per category (independent of the workshop's own lint)."""
import json, re, sys

CATS = {
 "C01 情绪氛围直述": r"涌起一股|说不清的情绪|五味杂陈|百感交集|空气(?:仿佛|好像|似乎)?[^，。]{0,6}凝固|一片死寂|死一般的|气氛[^，。]{0,4}(?:紧张|凝重|压抑)|莫名的(?:情绪|感觉|不安)|心中一暖|暖流",
 "C02 现成身体反应": r"嘴角[^，。]{0,3}(?:勾起|扬起|上扬|噙着)|指节[^，。]{0,6}(?:发白|泛白)|瞳孔[^，。]{0,3}(?:骤缩|一缩|猛缩|收缩)|深吸(?:了)?一口气|喉结[^，。]{0,3}(?:滚动|上下)|倒吸[^，。]{0,2}(?:凉气|冷气)|心跳[^，。]{0,3}(?:加速|漏了一拍)|呼吸[^，。]{0,2}一滞|心(?:中|里|头)?[^，。]{0,2}一(?:紧|沉|凛|颤)|手心[^，。]{0,3}(?:冷汗|出汗|汗)|青筋暴|咬紧(?:了)?牙关|攥紧(?:了)?拳头|后背[^，。]{0,3}(?:发凉|发冷|一凉)|头皮发麻|鼻(?:子|头)一酸|眼眶[^，。]{0,3}(?:一热|发热|泛红|红了)",
 "C03 神态套话": r"(?:眼中|眼里|眸中|眼底)[^，。]{0,2}(?:闪过|划过|掠过)|意味深长|一丝(?:坚定|寒芒|冷意|笑意|不易察觉)|寒芒|精光",
 "C04 内心宣告": r"(?:他|她|我)(?:知道|明白|意识到|清楚)[，,：:]|这意味着|(?:他|她)终于(?:明白|懂)",
 "C05 不是而是": r"不是[^。！？]{1,20}而是|与其说[^。！？]{1,20}不如说",
 "C06 点题升华": r"这一刻|终于明白|真正的[^，。]{1,8}(?:是|不是)|一旦失去|再也(?:找|回)不(?:来|去)|往后的每一个|温暖[^，。]{0,4}每一个|永远(?:不会|都会)|那些爱",
 "C07 排比三连": r"是[^，。]{1,10}的[^，。]{1,4}，是[^，。]{1,10}的[^，。]{1,4}，是|一[个只张把条][^，。]{1,12}，一[个只张把条][^，。]{1,12}，一[个只张把条]",
 "C08 套路比喻夸饰": r"如墨|如江河|仿佛要撕裂|撕裂空气|镀上(?:了)?一层|洒(?:进来|在)[^，。]{0,6}(?:金色|光)|化作一道|宛如|犹如|仿佛(?:永远|整个)",
 "C09 一股抽象名词": r"一股(?:前所未有|磅礴|莫名|强大|难以言喻|说不清)[^，。]{0,6}|前所未有的",
 "C10 时间转折套语": r"下一秒|就在这时|与此同时|紧接着|就在此时|刹那间|一瞬间|电光火石",
 "C13 虚化副词": r"缓缓|微微|轻轻|淡淡|死死|狠狠|静静",
 "C16 固定形容搭配": r"森冷的|猩红的|锈迹斑斑|阴冷的|冰冷的|刺骨的|凌厉的|磅礴的",
 "C18 段尾否定刹车": None,  # computed separately
}
COMPILED = {k: re.compile(v) for k, v in CATS.items() if v}

def paragraphs(t):
    return [p.strip() for p in re.split(r"\n\s*\n|\n", t) if p.strip()]

def analyze(text):
    out = {}
    for k, rx in COMPILED.items():
        hits = [m.group(0) for m in rx.finditer(text)]
        out[k] = {"n": len(hits), "hits": hits}
    paras = paragraphs(text)
    neg = [p[-14:] for p in paras if re.search(r"没(?:有|再)[^，。！？]{0,10}[。！？]?$", p) and not p.endswith("”")]
    out["C18 段尾否定刹车"] = {"n": len(neg), "hits": neg}
    han = len(re.findall(r"[一-鿿]", text))
    short = [p for p in paras if len(re.findall(r"[一-鿿]", p)) <= 12 and not p.startswith("“")]
    sents = [s for s in re.split(r"[。！？!?]", text) if re.search(r"[一-鿿]", s)]
    lens = [len(re.findall(r"[一-鿿]", s)) for s in sents]
    total = sum(v["n"] for v in out.values())
    return {"han": han, "paras": len(paras), "short_narr_paras(<=12字)": len(short),
            "sent_count": len(sents), "avg_sent_len": round(sum(lens)/len(lens), 1) if lens else 0,
            "max_sent_len": max(lens) if lens else 0,
            "tells_total": total, "tells_per_1k": round(total * 1000 / han, 1) if han else 0, "cats": out}

if __name__ == "__main__":
    res = {p: analyze(open(p, encoding="utf-8").read()) for p in sys.argv[1:]}
    if "--json" in sys.argv: print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        for p, r in res.items():
            print(f"== {p}: 汉字{r['han']} 段{r['paras']} 短叙述段{r['short_narr_paras(<=12字)']} 句均{r['avg_sent_len']} 最长句{r['max_sent_len']} | 套话{r['tells_total']}（每千字{r['tells_per_1k']}）")
            for k, v in r["cats"].items():
                if v["n"]: print(f"   {k}: {v['n']}  {'、'.join(v['hits'][:8])}")
