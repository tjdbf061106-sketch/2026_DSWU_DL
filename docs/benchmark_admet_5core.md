# ADMET-AI 5코어 처리량 벤치마크

_실행일: 2026-11-18 · 목적: 전체 ChEMBL 라이브러리 처리 전에 CPU 5코어 조건의 실제 예측 시간을 측정_

---

## 📋 측정 결과

| 항목 | 실측값 |
|---|---:|
| 입력 라이브러리 행 수 | 2,897,819 |
| 벤치마크 입력 | 10,000 SMILES |
| 예측 성공 | 10,000 |
| 미예측·invalid | 0 |
| 예측 시간 | 470.95초 |
| 처리량 | 21.23 분자/초 |
| 전체 예측 단순 추정 | 37.91시간 |

## ⚙️ 실행 조건

- 모델: ADMET-AI 2.0.1 bundled pretrained ensembles
- 장치: CPU 전용
- CPU affinity: 논리 코어 5개(IDs 0–4)
- ADMET-AI DataLoader workers: 5
- PyTorch·BLAS 스레드: worker당 1개로 제한
- 물성 descriptor 별도 계산: 사용하지 않음(`include_physchem=false`)

## 📚 증거 파일

- [측정 메타데이터](../experiment/benchmark_admet_5core_metadata.json): 환경, 시간, 처리량, 추정식
- [실제 예측 결과](../experiment/benchmark_admet_5core_predictions.csv): 10,000개 분자의 ADMET-AI 예측값
- [입력 목록](../experiment/inputs_manifest.csv): 원자료 파일과 전체 행 수
- [단계 요약](../experiment/filtering_summary.csv): 이 실행은 필터링이 아닌 속도 측정임을 명시
- [실행 스크립트](../scripts/benchmark_admet_5core.py): 동일 조건 재실행용 코드

## 🎯 해석과 다음 단계

37.91시간은 10,000개 표본의 **예측 시간만** 사용한 선형 추정치입니다. PC 사용, 디스크 I/O, 분자 복잡도, 재시작과 오류 대응 시간은 포함하지 않았습니다. 따라서 전체 실행은 충분한 연속 실행 시간을 확보한 뒤 진행하고, 10,000개 단위 체크포인트와 진행 로그를 저장해야 합니다.

이 벤치마크는 최종 후보 선별 결과가 아닙니다. 타겟 활성·도킹·필터 기준이 확정된 후의 실제 screening 결과는 별도 run ID와 파일로 보존합니다.
