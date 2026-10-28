import json,sys,os,collections
J=sys.argv[1];OUT=sys.argv[2]
L=lambda p:json.load(open(os.path.join(J,p),encoding='utf-8'))
ko=L('ko/ko-items.json');en=L('items.json');sh=L('shops.json');uc=L('ui-categories.json');kc=L('ko/ko-item-ui-categories.json');ic=L('item-icons.json')
import re
icon=lambda i:(re.search(r'path=(ui/icon/\d+/\d+)',ic.get(str(i),'')) or [None,''])[1]
n=lambda i:(ko.get(str(i)) or {}).get('ko') or (en.get(str(i)) or {}).get('en') or str(i)
cat=lambda i:(kc.get(str(uc.get(str(i)))) or {}).get('ko') or '기타'
TOK=[(28063,'창천 거리 진흥권','이슈가르드 부흥권(구 표기)'),(13630,'하늘도적의 전리품: 놋쇠',''),(13631,'하늘도적의 전리품: 강철',''),(15858,'보이드 맨드레이크',''),(15857,'알디크 라벤더','')]
res=[]
for tid,name,alias in TOK:
    seen={};
    for s in sh:
        for t in s.get('trades',[]):
            if any(c['id']==tid for c in t['currencies']):
                cost=[c['amount'] for c in t['currencies'] if c['id']==tid][0]
                for it in t['items']:
                    seen[it['id']]=(n(it['id']),cost,it['amount'],cat(it['id']),icon(it['id']))
    if tid==28063: seen={k:v for k,v in seen.items() if k in (13630,13631)}
    else: seen={k:v for k,v in seen.items() if '크리스탈' not in v[0] and '클러스터' not in v[0]}
    rows=sorted(seen.values(),key=lambda r:(r[3],r[1],r[0]))
    res.append({'id':tid,'name':n(tid),'alias':alias,'rows':rows})
    print(n(tid),len(rows),collections.Counter(r[3] for r in rows).most_common(5))
json.dump(res,open(OUT,'w',encoding='utf-8'),ensure_ascii=False)
