# 최종 질병·타겟 선정 감사

_2026-11-18 공식 ChEMBL/RCSB 조회와 로컬 벤치마크를 바탕으로 한 재현 가능한 후보 평가_

---

## 📋 결론

이번 기말 프로젝트 권고 주제는 **알츠하이머병 — BACE1**이다. 이는 임상 효능의 확정이 아니라, 활성 데이터·리간드 결합 구조·BBB·선택성·GNINA·ADMET·REINVENT를 정직하게 연결할 수 있다는 프로젝트 구현성 판단이다.

## 📊 전체 비교표

`엄격 레코드`는 IC50/Ki/Kd, `=`, nM, 값 존재, 유효성 코멘트 없음으로 필터한 활동 **레코드 수**다. 고유 화합물 수는 아직 측정하지 않았다. `확인` 구조는 RCSB에서 리간드 존재까지 확인했다.

| 질환 | 표적 | ChEMBL ID | 엄격 레코드 | 구조 상태 | 적합성 |
|---|---|---|---:|---|---|
| 폐암·후두암 | EGFR | CHEMBL203 | 20,949 | 미감사 | 높음, 변이 분리 필요 |
| 유방암 | CDK6 | CHEMBL3974 | 1,120 | 미감사 | 보통 |
| 흑색종 | BRAF | CHEMBL5145 | 9,683 | 미감사 | 높음, V600E 분리 필요 |
| 난소암 | PARP1 | CHEMBL3105 | 5,535 | 확인: 4UND | 높음 |
| AML | FLT3 | CHEMBL1974 | 6,663 | 미감사 | 높음, 변이 분리 필요 |
| 비인두암·OSCC | EGFR/PIK3CA | 203/4005 | 20,949/9,515 | 미감사 | 이중 표적 범위 큼 |
| 원형탈모 | JAK3 | CHEMBL2148 | 10,604 | 미감사 | 높음 |
| 건선 | TYK2 | CHEMBL3553 | 10,313 | 확인: 4GIH | 최상위 |
| RA·UC | JAK1 | CHEMBL2835 | 14,601 | 미감사 | 높음, 선택성 필요 |
| SLE | IRAK4 | CHEMBL5250 | 25 | 미감사 | 낮음 |
| MS | BTK | CHEMBL5251 | 16,975 | 확인: 5P9J | 최상위 |
| 제2형 당뇨 | DPP4 | CHEMBL284 | 5,387 | 확인: 1X70 | 매우 안정적 |
| 알츠하이머 | BACE1 | CHEMBL4822 | 15,327 | 확인: 4DJW | **최우선** |
| 알츠하이머 증상 | ACHE | CHEMBL220 | 8,144 | 미감사 | 안정적, 흔함 |
| HIV 감염 | HIV-1 protease | CHEMBL2366517 | 1,592 | 미감사 | 보통 |
| MDD·OCD | SERT | CHEMBL228 | 7,074 | 미감사 | 보통, CNS 부담 |
| 조현병 | DRD2 | CHEMBL217 | 13,178 | 미감사 | 보통, 작용 방향 중요 |
| ADHD | NET | CHEMBL222 | 4,968 | 미감사 | 보통 |
| TRD·불안 | NMDA/GABA-A | 미확정 | 미검증 | 다중 소단위 | 낮음 |
| 불면 | OX2R | CHEMBL5113 | 10,215 | 미감사 | 높음 |
| 양극성 | DRD2/GSK3B | 217/262 | 13,178/5,412 | 미감사 | 위험: 이중 표적 |
| PBA | SIGMAR1 | CHEMBL287 | 4,325 | 미감사 | 위험: 질환 연결 약함 |

## 🎯 TOP 5

1. 알츠하이머 — BACE1: 데이터·구조·BBB·BACE2 선택성 축
2. 다발성 경화증 — BTK: 풍부한 데이터와 ibrutinib 구조
3. 건선 — TYK2: JAK family 선택성 분석 가능
4. 난소암 — PARP1: talazoparib 재도킹과 PARP2 선택성
5. 제2형 당뇨 — DPP4: 가장 안정적이나 독창성은 낮음

## ⚙️ 계산 기준

| 작업 | 실측 기준 | 1,000개 추정 | 10,000개 |
|---|---:|---:|---:|
| ADMET-AI | 21.23 분자/초 | 47초 | 470.95초 실측 |
| GNINA CPU | 2.67초/리간드 | 44.5분 | 7.4시간 |

전체 ChEMBL을 GNINA으로 도킹하지 말고, 50,000~100,000개 다양성 샘플의 저비용 예측 후 상위 200~500개만 도킹한다.

## ▶ 재실행

Python 3.11+ 표준 라이브러리만 필요하다. `python run_target_audit.py`를 실행하면 `results/`에 새 감사 결과를 만든다. API 실패는 0 대신 `not_measured`로 기록한다.

## 🔗 문서와 증거

- [요청 명세](PROMPT.md)
- [방법·판단 로그](METHOD.md)
- [기존 ChEMBL 감사 결과](../experiment/chembl_activity_count_audit.csv)
- [기존 RCSB 감사 결과](../experiment/rcsb_top5_structure_audit.csv)

[^1]: ChEMBL REST API. https://www.ebi.ac.uk/chembl/api/data/activity.json
[^2]: RCSB PDB Data API. https://data.rcsb.org/rest/v1/
