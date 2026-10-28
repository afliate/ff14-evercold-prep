import json,sys,os,collections
J=sys.argv[1]
L=lambda p:json.load(open(os.path.join(J,p),encoding='utf-8'))
rec=L('recipes.json');ip=L('item-patch.json');pn=L('patch-names.json');ko=L('ko/ko-items.json');ga=L('gathering-items.json')
nm=lambda i:(ko.get(str(i)) or {}).get('ko',str(i))
ver=lambda i:(pn.get(str(ip.get(str(i)))) or {}).get('version')
gath={g['itemId'] for g in ga.values()}
EXP={'3.0':'창천','4.0':'홍련','5.0':'칠흑','6.0':'효월','7.0':'황금'}
J=lambda r:r['job'] in range(8,16)
for v,n in EXP.items():
    print('=====',v,n)
    rs=[r for r in rec if ver(r['result'])==v and J(r) and not r.get('masterbook')]
    for suffix in ('덩어리','주괴'):
        sel=[r for r in rs if nm(r['result']).endswith(suffix)]
        print(f'[{suffix}] {len(sel)}개')
        for r in sorted(sel,key=lambda r:r['lvl']):
            ing=[(nm(g['id']),g['amount'],ver(g['id'])) for g in r['ingredients'] if not 2<=g['id']<=19]
            cr=[(nm(g['id']),g['amount']) for g in r['ingredients'] if 2<=g['id']<=19]
            print('  ',r['lvl'],nm(r['result']),'x',r['yields'],'<-',ing,cr)
