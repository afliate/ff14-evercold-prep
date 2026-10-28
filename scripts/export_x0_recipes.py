import json,sys,os,collections,csv
J=sys.argv[1];OUT=sys.argv[2]
L=lambda p:json.load(open(os.path.join(J,p),encoding='utf-8'))
rec=L('recipes.json');ip=L('item-patch.json');pn=L('patch-names.json');uc=L('ui-categories.json')
ko=L('ko/ko-items.json');kuc=L('ko/ko-item-ui-categories.json')
nm=lambda i:(ko.get(str(i)) or {}).get('ko',str(i))
ver=lambda i:(pn.get(str(ip.get(str(i)))) or {}).get('version')
JOB={8:'CRP',9:'BSM',10:'ARM',11:'GSM',12:'LTW',13:'WVR',14:'ALC',15:'CUL'}
JL=list(JOB.values())
HOUSING=set([57]+list(range(64,81))+[82])
EXP={'3.0':('창천',51),'4.0':('홍련',61),'5.0':('칠흑',71),'6.0':('효월',81),'7.0':('황금',91)}
PO={v:i for i,v in enumerate(EXP)}
rows=[];excl=collections.Counter()
for r in rec:
    v=ver(r['result'])
    if v not in EXP: continue
    if r['job'] not in JOB: excl[(v,'비제작직')]+=1;continue
    if r.get('masterbook'): excl[(v,'전승록')]+=1;continue
    u=uc.get(str(r['result']));h=u in HOUSING
    lv=r.get('lvl') or 0
    rows.append(dict(확장=EXP[v][0],패치=v,구간='신규 레벨 구간' if lv>=EXP[v][1] else '이전 레벨 구간(신규 아이템)',
      하우징=int(h),직업=JOB[r['job']],레벨=lv,별=r.get('stars',0),분류=kuc.get(str(u),{}).get('ko',u),
      결과물=nm(r['result']),재료=' | '.join(f"{nm(g['id'])}x{g['amount']}" for g in r['ingredients']),
      레시피ID=r['id'],결과ID=r['result']))
rows.sort(key=lambda r:(PO[r['패치']],r['하우징'],r['구간']!='신규 레벨 구간',JL.index(r['직업']),-r['레벨'],str(r['분류']),r['결과물']))
cols=list(rows[0].keys())
with open(os.path.join(OUT,'x0_정렬본_3.0_4.0_5.0_6.0_7.0.csv'),'w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,cols);w.writeheader();w.writerows(rows)
print('excluded',dict(excl))
for v in EXP:
    rs=[x for x in rows if x['패치']==v]
    n=[x for x in rs if not x['하우징']]
    print(v,EXP[v][0],'일반',len(n),'(신규구간',sum(x['구간']=='신규 레벨 구간' for x in n),'/ 이전구간',sum(x['구간']!='신규 레벨 구간' for x in n),') 하우징',len(rs)-len(n),dict(collections.Counter(x['직업'] for x in n)))
