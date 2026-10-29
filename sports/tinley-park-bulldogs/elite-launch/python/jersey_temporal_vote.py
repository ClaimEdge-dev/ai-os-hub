from collections import defaultdict

def choose_jersey(observations, roster_numbers=None, min_total_weight=1.0, min_margin=0.15):
    scores=defaultdict(float)
    evidence=defaultdict(list)
    allowed={str(x) for x in roster_numbers} if roster_numbers else None
    for o in observations:
        txt="".join(ch for ch in str(o.get("text","")) if ch.isdigit())
        if not txt or (allowed is not None and txt not in allowed):
            continue
        weight=max(0.0,float(o.get("ocr_conf",0))) * max(0.0,float(o.get("quality",0)))
        if not weight: continue
        scores[txt]+=weight
        evidence[txt].append(o)
    if not scores:
        return {"status":"ABSTAIN","reason":"no_valid_votes","candidate":None}
    ranked=sorted(scores.items(),key=lambda kv:kv[1],reverse=True)
    best,best_score=ranked[0]
    second=ranked[1][1] if len(ranked)>1 else 0.0
    if best_score < min_total_weight:
        return {"status":"ABSTAIN","reason":"insufficient_weight","candidate":best}
    margin=(best_score-second)/best_score if best_score else 0.0
    if margin < min_margin:
        return {"status":"ABSTAIN","reason":"ambiguous_vote","candidate":best,"margin":margin}
    return {"status":"CANDIDATE","candidate":best,"score":best_score,"margin":margin,"evidence":evidence[best]}
