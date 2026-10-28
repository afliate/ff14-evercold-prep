import json,sys,os,collections,csv
J=sys.argv[1];OUT=sys.argv[2]
L=lambda p:json.load(open(os.path.join(J,p),encoding='utf-8'))
nodes=L('nodes.json');ga=L('gathering-items.json');ip=L('item-patch.json');pn=L('patch-names.json');ko=L('ko/ko-items.json')
rec=L('recipes.json');kp=L('ko/ko-places.json');icons=L('item-icons.json')
nm=lambda i:(ko.get(str(i)) or {}).get('ko',str(i))
ver=lambda i:(pn.get(str(ip.get(str(i)))) or {}).get('version')
TYPE={0:'광업',1:'채석',2:'벌목',3:'원예'}
SET={'3.0':'창천','4.0':'홍련','5.0':'칠흑','6.0':'효월','7.0':'황금'}
def icon(i):
    p=icons.get(str(i));return p.split('path=')[1].split('&')[0].replace('_hr1.tex','') if p else ''
item2nodes=collections.defaultdict(list)
for nid,n in nodes.items():
    if n.get('type') not in TYPE: continue
    for i in n.get('items',[]): item2nodes[i].append((n,False))
    for i in n.get('hiddenItems',[]): item2nodes[i].append((n,True))
uses=collections.defaultdict(collections.Counter)
for r in rec:
    v=ver(r['result'])
    if v in SET and r['job'] in range(8,16) and not r.get('masterbook'):
        for g in r['ingredients']: uses[v][g['id']]+=1
rows=[]
for g in ga.values():
    i=g['itemId'];v=ver(i)
    if v not in SET: continue
    ns=item2nodes.get(i,[])
    cls=sorted({TYPE[n['type']] for n,_ in ns})
    zones=collections.Counter(kp.get(str(n.get('zoneid')),{}).get('ko','?') for n,_ in ns)
    rows.append(dict(set=SET[v],patch=v,id=i,name=nm(i),lvl=g['level'],stars=g['stars'],hidden=int(bool(g['hidden'])),perc=g['perceptionReq'],
      cls='/'.join(cls),nodes=len(ns),timed=int(any(n.get('limited') for n,_ in ns)),eph=int(any(n.get('ephemeral') for n,_ in ns)),
      leg=int(any(n.get('legendary') for n,_ in ns)),zones=', '.join(z for z,_ in zones.most_common(3)),
      special_only=int(bool(ns) and all(n.get('limited') or n.get('ephemeral') or n.get('legendary') for n,_ in ns)),used=uses[v].get(i,0),usedany=sum(uses[x].get(i,0) for x in SET),icon=icon(i)))
order={k:j for j,k in enumerate(SET.values())}
rows.sort(key=lambda r:(order[r['set']],r['stars']>0,r['lvl'],r['cls'],r['name']))
json.dump(rows,open(os.path.join(OUT,'gathering.json'),'w',encoding='utf-8'),ensure_ascii=False)
with open(os.path.join(OUT,'gathering_x0.csv'),'w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['확장','출시패치','아이템','ID','채집Lv','별','히든','채집력요구','채집직','노드수','시간제','돌발','전설','한정노드 전용','주요지역','x.0레시피 사용','전체 x.0 사용','아이콘'])
    for r in rows:w.writerow([r['set'],r['patch'],r['name'],r['id'],r['lvl'],r['stars'],r['hidden'],r['perc'],r['cls'],r['nodes'],r['timed'],r['eph'],r['leg'],r['special_only'],r['zones'],r['used'],r['usedany'],r['icon']])
# summary
for s in SET.values():
    rs=[r for r in rows if r['set']==s]
    n=[r for r in rs if r['nodes']]
    print('==',s,'items',len(rs),'(no-node',len(rs)-len(n),')','stars',dict(collections.Counter(r['stars'] for r in rs)),'hidden',sum(r['hidden'] for r in rs),'timed',sum(r['timed'] for r in rs),'eph',sum(r['eph'] for r in rs),'leg',sum(r['leg'] for r in rs))
    print('  class',dict(collections.Counter(r['cls'] for r in rs)))
    print('  used in x.0 recipes',sum(1 for r in rs if r['used']),'/ unused',sum(1 for r in rs if not r['used']))
    lv=collections.Counter(r['lvl'] for r in rs);print('  lvl',dict(sorted(lv.items())))
    print('  zones',collections.Counter(z for r in rs for z in r['zones'].split(', ') if z).most_common(8))
    print('  unused sample',[r['name'] for r in rs if not r['used']][:12])
