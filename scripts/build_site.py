import json,csv,sys,os,re
SRC=sys.argv[1]   # dir with guess/materials html, materials.json, gathering.json, recipes csv
OUT=sys.argv[2]
os.makedirs(OUT,exist_ok=True)
rd=lambda p:open(os.path.join(SRC,p),encoding='utf-8').read()
PAGES=[('index.html','체크리스트'),('guess.html','추리'),('recipes.html','레시피'),('materials.html','재료'),('gathering.html','채집물'),('gp.html','채집량'),('exchange.html','교환')]
NAVCSS='''<style>
.snav{display:flex;flex-wrap:wrap;gap:4px 14px;margin:0 0 14px;padding:0 0 8px;border-bottom:1px solid var(--line)}
.snav a{color:var(--mute);text-decoration:none;font-size:14px;padding:2px 0}
.snav a.on{color:var(--fg);font-weight:700;border-bottom:2px solid var(--fg)}
</style>'''
def nav(cur):
    return '<nav class="snav">'+''.join(f'<a href="{h}"{" class=on" if h==cur else ""}>{t}</a>' for h,t in PAGES)+'</nav>'
def inject(html,cur):
    html=re.sub(r'<p class="sub"><a href="[^"]*">[^<]*</a></p>\n?','',html)
    html=html.replace('</head>',NAVCSS+'</head>',1)
    return html.replace('<main>','<main>'+nav(cur),1)
BASE_CSS='''<style>
:root{--bg:#f2f7fa;--fg:#222b40;--mute:#5f6b80;--card:#fbfdff;--line:#cfdde6;--acc:#3f6ea6;--new:#1d7a46}
@media (prefers-color-scheme:dark){:root{--bg:#0d1521;--fg:#e6edf5;--mute:#8d9bb0;--card:#141f2e;--line:#27384d;--acc:#86bfd0;--new:#58c58a}}
*{box-sizing:border-box}body::before{content:"";display:block;height:4px;background:linear-gradient(90deg,#4a76ad,#8cc7c9,#d9a76a)}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,-apple-system,"Noto Sans KR",sans-serif}
main{max-width:980px;margin:0 auto;padding:20px 16px 56px}h1{font-size:20px;margin:0 0 4px}h2{font-size:16px;margin:24px 0 8px;padding-bottom:4px;border-bottom:1px solid var(--line)}
.sub{color:var(--mute);font-size:13px;margin:0 0 14px}.m{color:var(--mute);font-size:12px}
.ctl{display:flex;flex-wrap:wrap;gap:8px;position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:2;border-bottom:1px solid var(--line)}
select,input,button{font:inherit;padding:5px 8px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg)}input[type=text],input:not([type]){flex:1;min-width:140px}
.cnt{color:var(--mute);font-size:12px;align-self:center}
table{width:100%;border-collapse:collapse;margin-top:8px}th,td{text-align:left;padding:5px 6px;border-bottom:1px solid var(--line);vertical-align:middle}
th{font-size:12px;color:var(--mute);font-weight:600}td.i{width:40px}img{width:32px;height:32px;display:block;border-radius:4px;background:var(--line)}
.n{font-weight:600}.tag{font-size:11px;font-weight:700}.new{color:var(--new)}.old{color:var(--acc)}
.num{text-align:right;font-variant-numeric:tabular-nums}
.tw{overflow-x:auto}
@media (max-width:640px){.hm{display:none}}
</style>'''
def page(title,cur,body,script,css=''):
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>{BASE_CSS}{NAVCSS}{css}</head><body><main>{nav(cur)}{body}</main><script>{script}</script></body></html>'''

# --- existing pages
open(os.path.join(OUT,'guess.html'),'w',encoding='utf-8').write(inject(rd('guess_src.html'),'guess.html'))
open(os.path.join(OUT,'materials.html'),'w',encoding='utf-8').write(inject(rd('materials_src.html'),'materials.html'))

# --- gathering
G=json.load(open(os.path.join(SRC,'gathering.json'),encoding='utf-8'))
GP='''<h2>채집량 늘리기 (GP 운용)</h2>
<p class="sub">개인 연구 시트(GP 저레벨 운용표) 정리. 강장제를 포함해 장기 수확량을 최대화하는 운용 기준입니다. 막대한 = 막대한 수익 II(100GP), 광1·광2 = 광맥의 선물 I(50GP)·II(100GP), 날달 = 날달의 복음(200GP), 석공 = 석공의 이론/농부의 지혜(300GP), 왕2 = 왕의 수익 II/축복받은 수확 II(500GP).</p>
<h3>시작 로테이션 (900GP에서 첫 강장제 쿨 돌리기)</h3>
<div class="tw"><table><thead><tr><th>노드 상태</th><th class="num">소비 GP</th><th>추천 조합</th><th>비고</th></tr></thead><tbody>
<tr><td>보너스 없음</td><td class="num">450</td><td>막대한×4 + 광1</td><td class="m">4회 노드·여유 26GP. 광1로 60→70%, 강장제 손실 없이 쿨 돌리는 후보</td></tr>
<tr><td>획득 +1</td><td class="num">450</td><td>막대한×4 + 광1</td><td class="m">4회 노드·여유 26GP. 노드 자체 +1이라 같은 GP라도 가치 높음</td></tr>
<tr><td>획득 +3</td><td class="num">450</td><td>막대한×4 + 광1</td><td class="m">4회 노드·여유 26GP. 노드 +3이 커서 GP 태우는 가치 높음</td></tr>
<tr><td>발생률 100%</td><td class="num">500</td><td>날달 + 막대한×3</td><td class="m">4회 노드·여유 76GP. 광맥 불필요, 100% 보너스를 날달에 활용</td></tr>
<tr><td>내구도 +2</td><td class="num">500</td><td>막대한×5</td><td class="m">6회 노드·여유 64GP. 막대한 5회가 자연스러움</td></tr>
</tbody></table></div>
<p class="m">424/436GP는 이론적 최소선이고, 실제 스킬 비용 단위에 맞춰 450/500을 현실적 후보로 씁니다.</p>
<h3>노드 상태별 우선순위</h3>
<div class="tw"><table><thead><tr><th>노드 상태</th><th>우선 사용</th></tr></thead><tbody>
<tr><td>보너스 없음</td><td>막대한 우선 (900GP는 왕2 검토)</td></tr>
<tr><td>획득 +1</td><td>막대한 우선 (900GP는 왕2 검토)</td></tr>
<tr><td>획득 +3</td><td>석공 우선</td></tr>
<tr><td>발생률 100%</td><td>날달 우선 (900GP는 왕2 검토)</td></tr>
<tr><td>내구도 +2</td><td>막대한 확장 우선 (900GP는 광2 + 날달)</td></tr>
</tbody></table></div>
<p class="m">공통 원칙: 막대한을 그 노드 최대치까지 먼저 채우고, 그다음 노드 상태에 맞는 지속형 스킬을 고릅니다. 발생률 100% 노드에서는 광맥이 낭비입니다. 700GP 발생률 100%는 100GP, 800GP 보너스 없음·획득 +1은 각 50GP를 다음 노드로 이월합니다.</p>
<h3>가용 GP별 기대 수확 (개)</h3>
<div class="tw"><table><thead><tr><th>가용 GP</th><th class="num">보너스 없음</th><th class="num">획득 +1</th><th class="num">획득 +3</th><th class="num">발생률 100%</th><th class="num">내구도 +2</th></tr></thead><tbody>
<tr><td>0</td><td class="num">6.4</td><td class="num">10.4</td><td class="num">18.4</td><td class="num">8.0</td><td class="num">9.6</td></tr>
<tr><td>100</td><td class="num">9.4</td><td class="num">13.4</td><td class="num">21.4</td><td class="num">11.0</td><td class="num">12.6</td></tr>
<tr><td>200</td><td class="num">12.4</td><td class="num">16.4</td><td class="num">24.4</td><td class="num">14.0</td><td class="num">15.6</td></tr>
<tr><td>300</td><td class="num">15.4</td><td class="num">19.4</td><td class="num">27.4</td><td class="num">17.0</td><td class="num">18.6</td></tr>
<tr><td>400</td><td class="num">18.4</td><td class="num">22.4</td><td class="num">30.4</td><td class="num">20.0</td><td class="num">21.6</td></tr>
<tr><td>500</td><td class="num">19.6</td><td class="num">23.6</td><td class="num">31.6</td><td class="num">21.0</td><td class="num">24.6</td></tr>
<tr><td>600</td><td class="num">20.8</td><td class="num">24.8</td><td class="num">32.8</td><td class="num">24.0</td><td class="num">27.6</td></tr>
<tr><td>700</td><td class="num">23.2</td><td class="num">27.2</td><td class="num">35.2</td><td class="num">24.0</td><td class="num">29.4</td></tr>
<tr><td>800</td><td class="num">24.0</td><td class="num">28.0</td><td class="num">38.0</td><td class="num">25.0</td><td class="num">31.8</td></tr>
<tr><td>900</td><td class="num">26.4</td><td class="num">30.4</td><td class="num">39.5</td><td class="num">28.0</td><td class="num">34.8</td></tr>
</tbody></table></div>
<p class="m">4노드 한 바퀴(고정 2 + 랜덤 2) 시뮬레이션: 900GP 시작, 고정 획득 +1 → 고정 발생률 +40% → 랜덤 꽝 → 랜덤 획득 +3 순서에서 8개 노드 합계 기대 수확 116.0개 (1바퀴 75.6 + 2바퀴 40.4). 노드 순서에 따라 한 바퀴 합계가 75.6~80.8개로 달라집니다.</p>
'''
gbody='''<h1>채집물 (3.0~7.0 x.0)</h1>
<p class="sub">각 확장 x.0에서 처음 나온 채집물. 채집직은 광부(광물·암석)와 원예(나무·풀)로 나눕니다. 한정 노드 전용 = 상시 노드에는 없고 시간제·돌발·전설 노드에서만 나오는 아이템 (Teamcraft 노드 플래그 기준). 소장용 = 수집품용.</p>
<div class="tw"><table><thead><tr><th>확장</th><th class="num">종류</th><th class="num">광부</th><th class="num">원예</th><th class="num">만렙 Lv</th><th class="num">별 1+</th><th class="num">한정 전용</th><th class="num">소장용</th><th class="num">레시피 사용</th></tr></thead><tbody id="sum"></tbody></table></div>
@@GP@@<h2>목록</h2>
<div class="ctl"><select id="fs"><option value="">확장 전체</option><option>창천</option><option>홍련</option><option>칠흑</option><option>효월</option><option>황금</option></select>
<select id="fc"><option value="">채집직 전체</option><option>광부</option><option>원예</option></select>
<select id="fk"><option value="">전체</option><option value="u">레시피 사용</option><option value="n">레시피 미사용</option><option value="sp">한정 노드 전용</option><option value="st">별 1+</option></select>
<input id="q" placeholder="이름 검색"><span class="cnt" id="cnt"></span></div>
<div class="tw"><table><thead><tr><th></th><th>이름</th><th>패치</th><th>채집직</th><th class="num">Lv</th><th class="hm">지역</th><th class="num">사용</th></tr></thead><tbody id="tb"></tbody></table></div>'''
gscript='''const D=__DATA__;const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const job=x=>x.cls.split('/').map(k=>k==='광업'||k==='채석'?'광부':'원예').filter((v,i,a)=>a.indexOf(v)===i).join('/');
const CAP={'창천':60,'홍련':70,'칠흑':80,'효월':90,'황금':100};
function url(p){return 'https://beta.xivapi.com/api/1/asset?path='+p+'_hr1.tex&format=png'}
function alt(p){const m=p.match(/icon\\/(\\d+)\\/(\\d+)/);return m?'https://xivapi.com/i/'+m[1]+'/'+m[2]+'.png':''}
window.fb=function(img){if(!img.dataset.t){img.dataset.t=1;img.src=img.dataset.alt}else img.removeAttribute('src')}
$('sum').innerHTML=Object.keys(CAP).map(s=>{const r=D.filter(x=>x.set===s);
 return `<tr><td>${s}</td><td class="num">${r.length}</td><td class="num">${r.filter(x=>job(x).includes('광부')).length}</td><td class="num">${r.filter(x=>job(x).includes('원예')).length}</td><td class="num">${r.filter(x=>x.lvl===CAP[s]).length}</td><td class="num">${r.filter(x=>x.stars>0).length}</td><td class="num">${r.filter(x=>x.special_only).length}</td><td class="num">${r.filter(x=>x.name.includes('소장용')).length}</td><td class="num">${r.filter(x=>x.used>0).length}</td></tr>`}).join('');
function render(){const s=$('fs').value,c=$('fc').value,k=$('fk').value,q=$('q').value.trim();
 const rows=D.filter(x=>(!s||x.set===s)&&(!c||job(x).includes(c))&&(!k||(k==='u'?x.used>0:k==='n'?x.used===0:k==='sp'?x.special_only:x.stars>0))&&(!q||x.name.includes(q)));
 $('cnt').textContent=rows.length+'개';
 $('tb').innerHTML=rows.map(x=>`<tr><td class="i"><img loading="lazy" src="${esc(url(x.icon))}" data-alt="${esc(alt(x.icon))}" onerror="fb(this)" alt=""></td><td><span class="n">${esc(x.name)}</span>${x.stars?' <span class="tag old">★'+x.stars+'</span>':''}${x.special_only?' <span class="tag new">한정</span>':''}<div class="m">#${x.id}</div></td><td>${esc(x.patch)}<div class="m">${esc(x.set)}</div></td><td>${esc(job(x))}</td><td class="num">${x.lvl}</td><td class="hm m">${esc(x.zones)}</td><td class="num">${x.used}</td></tr>`).join('')}
['fs','fc','fk'].forEach(i=>$(i).onchange=render);$('q').oninput=render;render();'''
open(os.path.join(OUT,'gathering.html'),'w',encoding='utf-8').write(page('채집 구성 3.0~7.0','gathering.html',gbody.replace('@@GP@@',''),gscript.replace('__DATA__',json.dumps(G,ensure_ascii=False,separators=(',',':')))))

# --- recipes
rows=list(csv.DictReader(open(os.path.join(SRC,'x0_recipes.csv'),encoding='utf-8-sig')))
ICO=json.load(open(os.path.join(SRC,'recipe_icons.json')))
R=[[r['확장'],r['패치'],r['구간'].replace(' 레벨 구간','').replace('(신규 아이템)','').strip(),int(r['하우징']),r['직업'],int(r['레벨']),int(r['별'] or 0),r['분류'],r['결과물'],r['재료'],ICO.get(r['결과ID'],'')] for r in rows]
rbody='''<h1>레시피 (3.0~7.0 x.0)</h1>
<p class="sub">각 확장 x.0에서 처음 나온 직업 8종 레시피. 전승록 제외. 신규 = 그 확장의 새 레벨 구간, 이전 = 이전 레벨 구간이지만 새로 추가된 아이템. 재료의 크리스탈은 제외.</p>
<div class="ctl"><select id="fs"><option value="">확장 전체</option><option>창천</option><option>홍련</option><option>칠흑</option><option>효월</option><option>황금</option></select>
<select id="fj"><option value="">직업 전체</option><option>CRP</option><option>BSM</option><option>ARM</option><option>GSM</option><option>LTW</option><option>WVR</option><option>ALC</option><option>CUL</option></select>
<select id="fc"><option value="">분류 전체</option></select>
<select id="fg"><option value="">구간 전체</option><option>신규</option><option>이전</option></select>
<select id="fh"><option value="0">하우징 제외</option><option value="">하우징 포함</option><option value="1">하우징만</option></select>
<input id="q" placeholder="결과물·재료 검색"><span class="cnt" id="cnt"></span></div>
<div class="tw"><table><thead><tr><th></th><th>확장</th><th>직업</th><th class="num">Lv</th><th>결과물</th><th class="hm">분류</th><th class="hm">재료</th></tr></thead><tbody id="tb"></tbody></table></div>
<p><button id="more">더 보기</button></p>'''
rscript='''const R=__DATA__;const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
[...new Set(R.map(r=>r[7]))].sort().forEach(c=>{const o=document.createElement('option');o.textContent=c;$('fc').appendChild(o)});
function url(p){return 'https://beta.xivapi.com/api/1/asset?path='+p+'_hr1.tex&format=png'}
function alt(p){const m=p.match(/icon\\/(\\d+)\\/(\\d+)/);return m?'https://xivapi.com/i/'+m[1]+'/'+m[2]+'.png':''}
window.fb=function(img){if(!img.dataset.t){img.dataset.t=1;img.src=img.dataset.alt}else img.removeAttribute('src')}
let N=300,rows=[];
function render(){const s=$('fs').value,j=$('fj').value,c=$('fc').value,g=$('fg').value,h=$('fh').value,q=$('q').value.trim();
 rows=R.filter(r=>(!s||r[0]===s)&&(!j||r[4]===j)&&(!c||r[7]===c)&&(!g||r[2]===g)&&(h===''||String(r[3])===h)&&(!q||r[8].includes(q)||r[9].includes(q)));
 $('cnt').textContent=rows.length+'개';draw()}
function draw(){$('tb').innerHTML=rows.slice(0,N).map(r=>`<tr><td class="i">${r[10]?`<img loading="lazy" src="${esc(url(r[10]))}" data-alt="${esc(alt(r[10]))}" onerror="fb(this)" alt="">`:''}</td><td>${esc(r[0])}<div class="m">${esc(r[1])}</div></td><td>${esc(r[4])}</td><td class="num">${r[5]}${r[6]?' ★'+r[6]:''}</td><td><span class="n">${esc(r[8])}</span>${r[2]==='이전'?' <span class="tag old">이전</span>':''}${r[3]?' <span class="tag">하우징</span>':''}</td><td class="hm m">${esc(r[7])}</td><td class="hm m">${esc(r[9])}</td></tr>`).join('');$('more').style.display=rows.length>N?'':'none'}
$('more').onclick=()=>{N+=300;draw()};
['fs','fj','fc','fg','fh'].forEach(i=>$(i).onchange=()=>{N=300;render()});$('q').oninput=()=>{N=300;render()};render();'''
open(os.path.join(OUT,'recipes.html'),'w',encoding='utf-8').write(page('레시피 3.0~7.0','recipes.html',rbody,rscript.replace('__DATA__',json.dumps(R,ensure_ascii=False,separators=(',',':')))))

# --- checklist (home)
CL=[
('확장 전 기본 준비 (한도·수량)',[
 ('crys','크리스탈은 충분하나요?','황금은 7/8, 8/8개씩 소모. 백은 추측: 9/8개 이상 (추리)'),
 ('scrip','자화·등화 제작·채집 화폐 한도까지 모아두기','백화·자색은 과거 확장 화폐. 한도는 제작·채집 각각 4000개'),
 ('leve','수주권 100개 채우기','업데이트 날짜에 맞춰 미리. 약 16일이면 100개가 참'),
 ('bi','두 빛깔 보석 토큰 1500개 (한계까지)','가죽·재봉·연금 재료로 많이 나감'),
 ('cust','단골손님 소장용 미리 준비','리셋은 화요일인데 패치일은 아직 모름. 글로벌 얼리 액세스는 목요일 업데이트였음 → 목요일 업데이트면 리셋 직전에 소진하지 말고 아껴 두기. 한섭 요일은 공개 후 판단'),
]),
('납품·소모품·정리',[
 ('gc','총사령부 납품 제작·채집 준비','템은 자기 레벨 -2까지 나옴. 제작은 HQ, 채집은 NQ도 충분'),
 ('food','강장제 충분하나요?','먼바다 낚시 수급이 빠름'),
 ('tok','교환용 토큰 챙기기: 이슈가르드 부흥권, 하늘도적의 전리품(놋쇠·강철), 보이드 맨드레이크, 알디크 라벤더','이전엔 은 광석·에테르석 재료 수급에 사용. 무엇으로 교환되는지는 교환 탭 참고'),
 ('art','제작술·채집술 상용술/개정판 대비','새 제작·채집술이 추가될 수도, 안 될 수도 있음. 대비해 두면 좋음. 황금 때는 제작 상용술 45·개정판 40, 채집 상용술 25·개정판 20 정도 사용'),
 ('inv','인벤 비우기 · 옷장 정리 · 염료 모으기','신규 재료가 확장마다 약 120~185종 추가됨 (재료 페이지)')]),
('필수는 아님 (챙겨도 안 챙겨도 무관)',[
 ('bt','집사 템·레벨 맞춰 두기 (자화/전투템)','채집은 획득력만 맞추면 됨'),
 ('gs','채집 소장용 모아뒀나요?',''),
 ('bond','결속도 관련템 챙기기','결속약·결속도 음식·부대버프 또는 스크롤. +6 이상은 효과 없음'),
 ('tele','텔레포 티켓·귀환 아이템, 길 / 에테르석 / 전송망 이용권','')]),
('공개 정보 나오면 확인',[
 ('pll','마지막 프로듀서 레터 라이브(PLL) 확인','전승록·신규 장비 시기 확인용'),
 ('fan','팬 페스티벌 공개 지역·신규 직업·신규 기믹','신규 직업이 있으면 무기 레시피가 x.0에 추가됨 (추리 페이지)'),
 ('lv','레벨 캡·신규 레벨 구간 확인','구간 번호가 맞아야 레시피 목록과 대조 가능'),
 ('rcp','공개된 레시피와 추리 대조','추리 페이지 항목의 등급 갱신')]),
('재료 추리 (추리 페이지 기준, 확정 아님)',[
 ('ore','과거 광석 후보 확보: 몰리브덴·경금·휘취은 광석/모래, 경철·은 광석, 마그네시아 가루','주괴 1개당 과거 광석 1개 패턴'),
 ('herb','5능력 허브 확보: 바람 파슬리·코자말루 캐모마일·바람 월계수잎·유칼립투스·진주풀 (+ 대성수·도끼부리 날개)','5.0 허브는 2확장(5.0~6.x) 사용, 7.0에서 교체됨. 백은이 7.0 허브를 이어 쓸 수 있어 넉넉히 (추리). 전승록 보석약도 같은 허브'),
 ('leath','7.0 가죽 부자재 확인: 아까시나무 껍질 등','하위 가죽 2~3종에서 직전 부자재 재사용 패턴'),
 ('cook','요리 재료 재고: 꼬마레몬·고지대 밀가루·프란토이오 기름·크림버섯·피토마토·발효 버터','과거 요리 재료 비중 증가 추세')])]
CRYS=''
cbody='<h1>백은의 탐구자 채작 대비</h1><p class="sub">체크 상태는 이 브라우저에 저장됩니다. 백은 정보는 아직 없어서 재료 항목은 과거 패턴 기반 추리입니다.</p><div id="cl"></div><p><button id="reset">전체 해제</button> <span class="cnt" id="prog"></span></p>'+CRYS
cscript='''const CL=__DATA__;
const $=id=>document.getElementById(id);const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const KEY='evercold-checklist-v1';let st={};
try{st=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){st={}}
function save(){try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
function render(){let tot=0,done=0;
 $('cl').innerHTML=CL.map(([t,items])=>`<section class="sec"><h2>${esc(t)}</h2>`+items.map(([id,name,note])=>{tot++;if(st[id])done++;
  return `<label class="ck"><input type="checkbox" data-id="${id}"${st[id]?' checked':''}><span><span class="n">${esc(name)}</span>${note?`<div class="m">${esc(note)}</div>`:''}</span></label>`}).join('')+'</section>').join('');
 $('prog').textContent=done+' / '+tot;
 document.querySelectorAll('.ck input').forEach(i=>i.onchange=()=>{st[i.dataset.id]=i.checked;save();render()})}
$('reset').onclick=()=>{st={};save();render()};render();'''
ccss='<style>main{max-width:1000px}#cl{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:0 18px;align-items:start}.sec{padding-bottom:6px}.sec h2{margin-top:0!important;padding-top:6px}.sec h2{margin-top:6px}.ck{padding:6px 9px!important;margin:5px 0!important}.ck{display:flex;gap:10px;align-items:flex-start;padding:8px 10px;margin:6px 0;background:var(--card);border:1px solid var(--line);border-radius:6px;cursor:pointer}.ck input{margin-top:4px;width:16px;height:16px;padding:0}</style>'
open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(page('백은의 탐구자 채작 대비','index.html',cbody,cscript.replace('__DATA__',json.dumps(CL,ensure_ascii=False)),ccss))
print('ok')

gpbody='<h1>채집량 늘리기</h1>'+GP.replace('<h2>채집량 늘리기 (GP 운용)</h2>','',1)
open(os.path.join(OUT,'gp.html'),'w',encoding='utf-8').write(page('채집량 늘리기','gp.html',gpbody,''))

EXC=json.load(open(os.path.join(SRC,'exchange.json'),encoding='utf-8'))
ebody='<h1>교환용 토큰</h1><p class="sub">이전 확장 때 챙겨 두던 교환용 토큰이 무엇으로 교환되는지 (Teamcraft 상점 데이터 기준). 비용은 교환물 1개당 필요한 토큰 수.</p>'
for t in EXC:
    ebody+='<details open><summary><b>'+t['name']+'</b>'+(' <span class="m">'+t['alias']+'</span>' if t['alias'] else '')+' <span class="m">· '+str(len(t['rows']))+'종</span></summary><div class="tw"><table><thead><tr><th>분류</th><th>교환물</th><th class="num">비용</th></tr></thead><tbody>'
    last=None
    for nm,cost,amt,cat in t['rows']:
        ebody+='<tr><td class="m">'+(cat if cat!=last else '')+'</td><td>'+nm+(' ×'+str(amt) if amt>1 else '')+'</td><td class="num">'+str(cost)+'</td></tr>';last=cat
    ebody+='</tbody></table></div></details>'
ecss='<style>details{margin:14px 0}summary{cursor:pointer;font-size:15px;padding:4px 0;border-bottom:1px solid var(--line)}main{max-width:760px}</style>'
open(os.path.join(OUT,'exchange.html'),'w',encoding='utf-8').write(page('교환용 토큰','exchange.html',ebody,'',ecss))
