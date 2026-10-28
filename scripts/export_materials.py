import json,sys,os,csv,collections
J=sys.argv[1];OUT=sys.argv[2]
L=lambda p:json.load(open(os.path.join(J,p),encoding='utf-8'))
rec=L('recipes.json');ip=L('item-patch.json');pn=L('patch-names.json');uc=L('ui-categories.json')
ko=L('ko/ko-items.json');kuc=L('ko/ko-item-ui-categories.json');icons=L('item-icons.json');ga=L('gathering-items.json')
nm=lambda i:(ko.get(str(i)) or {}).get('ko',str(i))
ver=lambda i:(pn.get(str(ip.get(str(i)))) or {}).get('version')
exof=lambda i:(pn.get(str(ip.get(str(i)))) or {}).get('ex')
EXN={0:'ARR',1:'창천',2:'홍련',3:'칠흑',4:'효월',5:'황금'}
SET={'3.0':'창천','4.0':'홍련','5.0':'칠흑','6.0':'효월','7.0':'황금'}
gath={g['itemId']:g for g in ga.values()}
made={r['result'] for r in rec}
def icon(i):
    p=icons.get(str(i))
    if not p: return ''
    return p.split('path=')[1].split('&')[0].replace('_hr1.tex','').replace('.tex','')  # ui/icon/022000/022678
rows=[]
for v,en in SET.items():
    uses=collections.Counter()
    for r in rec:
        if ver(r['result'])!=v or r['job'] not in range(8,16) or r.get('masterbook'): continue
        for g in r['ingredients']:
            if 2<=g['id']<=19: continue
            uses[g['id']]+=1
    for i,n in uses.items():
        iv=ver(i)
        src='채집' if i in gath else ('제작' if i in made else '기타(드랍·구매)')
        u=uc.get(str(i))
        gi=gath.get(i)
        rows.append(dict(set=en,setver=v,id=i,name=nm(i),patch=iv or '?',origin=EXN.get(exof(i),'?'),
            new=int(iv==v),src=src,cat=kuc.get(str(u),{}).get('ko','') if u else '',
            glv=gi['level'] if gi else '',gstar=gi['stars'] if gi else '',uses=n,icon=icon(i)))
order={k:i for i,k in enumerate(SET.values())}
rows.sort(key=lambda r:(order[r['set']],-r['new'],r['src'],r['glv'] if r['glv']!='' else 999,-r['uses'],r['name']))
print(len(rows),collections.Counter((r['set'],r['new']) for r in rows))
print('missing icon',sum(1 for r in rows if not r['icon']))
json.dump(rows,open(os.path.join(OUT,'materials.json'),'w',encoding='utf-8'),ensure_ascii=False)
with open(os.path.join(OUT,'materials_by_expansion.csv'),'w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['레시피 확장','신규/재사용','아이템','아이템ID','출시 패치','출시 확장','구분','분류','채집레벨','별','사용 레시피 수','아이콘 경로'])
    for r in rows:w.writerow([r['set'],'신규' if r['new'] else '재사용',r['name'],r['id'],r['patch'],r['origin'],r['src'],r['cat'],r['glv'],r['gstar'],r['uses'],r['icon']])
