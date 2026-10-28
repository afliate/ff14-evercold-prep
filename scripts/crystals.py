import json,sys,os,collections,functools,statistics
sys.setrecursionlimit(10000)
J=sys.argv[1]
L=lambda p:json.load(open(os.path.join(J,p),encoding='utf-8'))
rec=L('recipes.json');ip=L('item-patch.json');pn=L('patch-names.json');uc=L('ui-categories.json');kuc=L('ko/ko-item-ui-categories.json');ko=L('ko/ko-items.json')
ver=lambda i:(pn.get(str(ip.get(str(i)))) or {}).get('version')
nm=lambda i:(ko.get(str(i)) or {}).get('ko',str(i))
KIND=lambda i:'샤드' if 2<=i<=7 else '크리스탈' if 8<=i<=13 else '클러스터'
ELEM={2:'불',3:'얼음',4:'바람',5:'땅',6:'번개',7:'물'}
def el(i): return ELEM[(i-2)%6+2]
byres=collections.defaultdict(list)
for r in rec:
    if r['job'] in range(8,16) and not r.get('masterbook'): byres[r['result']].append(r)
def best(i):
    c=byres.get(i)
    return min(c,key=lambda r:str(r['id'])) if c else None
@functools.lru_cache(None)
def tree(i,depth=0):
    # returns Counter of crystal id -> amount per 1 item
    r=best(i)
    c=collections.Counter()
    if not r or depth>8: return c
    for g in r['ingredients']:
        if 2<=g['id']<=19: c[g['id']]+=g['amount']
        else:
            sub=tree(g['id'],depth+1)
            for k,v in sub.items(): c[k]+=v*g['amount']/max(1,(best(g['id']) or {'yields':1}).get('yields',1))
    y=max(1,r.get('yields',1))
    return collections.Counter({k:v/y for k,v in c.items()})
def direct(r):
    c=collections.Counter()
    for g in r['ingredients']:
        if 2<=g['id']<=19: c[g['id']]+=g['amount']
    return c
HOUSING=set([57]+list(range(64,81))+[82])
CAT=lambda i:kuc.get(str(uc.get(str(i))),{}).get('ko')
for v,cap in (('3.0',60),('4.0',70),('5.0',80),('6.0',90),('7.0',100)):
    rs=[r for r in rec if ver(r['result'])==v and r['job'] in range(8,16) and not r.get('masterbook') and uc.get(str(r['result'])) not in HOUSING]
    # direct
    d=[sum(direct(r).values()) for r in rs]
    dk=collections.Counter()
    for r in rs:
        for i,a in direct(r).items(): dk[KIND(i)]+=a
    # tree for equipment (ui in 방어구/장신구/무기) at levels >= cap-4
    eq=[r for r in rs if (r['lvl'] or 0)>=cap-4 and CAT(r['result']) and any(k in CAT(r['result']) for k in ('방어구','목걸이','귀걸이','팔찌','반지'))]
    t=[sum(tree(r['result']).values()) for r in eq]
    print('==',v,'recipes',len(rs),'direct total',sum(d),'direct avg',round(statistics.mean(d),1),'median',statistics.median(d),'max',max(d),'by kind',dict(dk))
    print('   top-level gear lv>=%d:'%(cap-4),len(eq),'tree avg',round(statistics.mean(t),1) if t else None,'median',statistics.median(t) if t else None,'max',round(max(t),1) if t else None)
    # by category avg direct at cap levels
    capr=[r for r in rs if (r['lvl'] or 0)>=cap-4]
    cc=collections.defaultdict(list)
    for r in capr: cc[CAT(r['result'])].append(sum(direct(r).values()))
    print('   cap-band direct avg by cat',{k:round(statistics.mean(x),1) for k,x in sorted(cc.items(),key=lambda kv:-len(kv[1]))[:10]})
    # by element total direct
    ec=collections.Counter()
    for r in rs:
        for i,a in direct(r).items(): ec[el(i)]+=a
    print('   elements',dict(ec))
    # distribution of direct per recipe at cap band
    print('   cap-band direct dist',sorted(collections.Counter(sum(direct(r).values()) for r in capr).items()))
