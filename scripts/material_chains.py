import json,sys,os,collections
J=sys.argv[1]
L=lambda p:json.load(open(os.path.join(J,p),encoding='utf-8'))
rec=L('recipes.json');ip=L('item-patch.json');pn=L('patch-names.json');ko=L('ko/ko-items.json');uc=L('ui-categories.json')
nm=lambda i:(ko.get(str(i)) or {}).get('ko',str(i))
ver=lambda i:(pn.get(str(ip.get(str(i)))) or {}).get('version')
CAT={48:'석재',50:'목재',51:'옷감',52:'가죽재',53:'골재',54:'연금재'}
EXP={'3.0':'창천','4.0':'홍련','5.0':'칠흑','6.0':'효월','7.0':'황금'}
for v,n in EXP.items():
    print('=====',v,n)
    for cid,cn in CAT.items():
        sel=[r for r in rec if ver(r['result'])==v and r['job'] in range(8,16) and not r.get('masterbook') and uc.get(str(r['result']))==cid]
        seen=set();out=[]
        for r in sorted(sel,key=lambda r:r['lvl']):
            ing=tuple((nm(g['id']),g['amount'],ver(g['id'])) for g in r['ingredients'] if not 2<=g['id']<=19)
            key=(nm(r['result']),ing)
            if key in seen: continue
            seen.add(key);out.append(f"{r['lvl']} {nm(r['result'])} <- {[ (a,b,c) for a,b,c in ing]}")
        if out:
            print(f'[{cn}] {len(out)}')
            for o in out:print('   ',o)
