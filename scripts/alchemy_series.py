import json,sys,os,collections
J=sys.argv[1]
L=lambda p:json.load(open(os.path.join(J,p),encoding='utf-8'))
rec=L('recipes.json');ip=L('item-patch.json');pn=L('patch-names.json');ko=L('ko/ko-items.json')
nm=lambda i:(ko.get(str(i)) or {}).get('ko',str(i))
ver=lambda i:(pn.get(str(ip.get(str(i)))) or {}).get('version')
def vk(v):
    a=v.split('.');return (int(a[0]),int(a[1]))
for key in ['성장 촉진제','연금용제','영험수','환혹수','환혹약','보석수','보석약','탕약','약차','약주','약액','물약','결속약']:
    rs=[r for r in rec if r['job']==14 and key in nm(r['result']) and ver(r['result'])]
    seen={}
    for r in rs:
        n=nm(r['result']); seen.setdefault(n.split(' ')[0] if key=='성장 촉진제' else n, (ver(r['result']),r['lvl']))
    items=sorted(((v,l,n) for n,(v,l) in seen.items()),key=lambda t:(vk(t[0]),t[1]))
    print(f'[{key}]',[f'{n}({v}/L{l})' for v,l,n in items][:30])
# growth catalyst full names
rs=[r for r in rec if r['job']==14 and nm(r['result']).startswith('성장 촉진제')]
print(sorted({(ver(r['result']),r['lvl'],nm(r['result'])) for r in rs},key=lambda t:(vk(t[0]),t[1])))
# aethersand names
print(sorted({nm(g['id']) for r in rec if r['job']==14 for g in r['ingredients'] if '에테르 모래' in nm(g['id'])}))
