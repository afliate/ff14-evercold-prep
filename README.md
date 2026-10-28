# ff14-evercold-prep

FFXIV 백은의 탐구자 채집·제작 대비용 추리 자료. 3.0~7.0 확장 시작 패치(x.0)의 레시피를 Teamcraft 데이터로 분석해 패턴을 정리했습니다. 백은 정보는 없어서 전부 과거 패턴 기반 추리입니다.

- `index.html` — 신뢰도 등급별 추리 정리 (반복 확인 / 패턴 추정 / 순수 추리 / 예외)
- `materials.html` — x.0 레시피 재료 목록 (아이콘, 출시 패치, 신규/재사용 필터)
- `docs/` — 분석 상세 (밑재료 체인, 요리·연금, 확장별 구성, 칠흑 패턴)
- `data/` — CSV/JSON 원본 (x0 레시피, 재료 목록, 꾸준히 쓰인 재료)
- `scripts/` — 분석 스크립트

## 기준
- 대상: 직업 8종 레시피 중 3.0, 4.0, 5.0, 6.0, 7.0 패치에서 처음 나온 것. 전승록 제외, 하우징은 `하우징` 열로 구분.
- 확장 판정: 결과물 아이템이 처음 나온 패치.
- 데이터: [ffxiv-teamcraft](https://github.com/ffxiv-teamcraft/ffxiv-teamcraft) `libs/data/src/lib/json`.

## 스크립트 실행
```
git clone --depth 1 https://github.com/ffxiv-teamcraft/ffxiv-teamcraft
python3 -I scripts/export_x0_recipes.py <teamcraft>/libs/data/src/lib/json <출력폴더>
python3 -I scripts/export_materials.py  <teamcraft>/libs/data/src/lib/json <출력폴더>
```
백은 데이터가 Teamcraft에 올라오면 `3.0`~`7.0` 목록에 `8.0`을 추가해 다시 돌리면 됩니다.

## 한계
- 아이콘은 XIVAPI에서 불러옵니다.
- 재료 분류(채집/제작/기타)는 Teamcraft 채집 데이터 기준이라 일부 오차가 있습니다.
