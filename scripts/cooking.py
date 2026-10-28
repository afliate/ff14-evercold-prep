import json,sys,os,collections
J=sys.argv[1]
L=lambda p:json.load(open(os.path.join(J,p),encoding='utf-8'))
rec=L('recipes.json');ip=L('item-patch.json');pn=L('patch-names.json');ko=L('ko/ko-items.json');uc=L('ui-categories.json')
nm=lambda i:(ko.get(str(i)) or {}).get('ko',str(i))
ver=lambda i:(pn.get(str(ip.get(str(i)))) or {}).get('version')
EXP={'3.0':'창천','4.0':'홍련','5.0':'칠흑','6.0':'효월','7.0':'황금'}
for v,n in EXP.items():
    rs=[r for r in rec if ver(r['result'])==v and r['job']==15 and not r.get('masterbook') and uc.get(str(r['result'])) in (46,45)]
    print('=====',v,n,'요리/식재료',len(rs))
    for r in sorted(rs,key=lambda r:(r['lvl'],nm(r['result']))):
        ing=[f"{nm(g['id'])}{g['amount']}{'' if ver(g['id'])==v else '('+str(ver(g['id']))+')'}" for g in r['ingredients'] if not 2<=g['id']<=19]
        print(f"  {r['lvl']} {'★'*r.get('stars',0)} {nm(r['result'])} x{r['yields']} <- {', '.join(ing)}")
