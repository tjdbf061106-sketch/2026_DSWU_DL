# 증거 연결표

실제 실행 후 아래 표의 `상태`와 `근거 파일`을 갱신합니다. 현재는 실행 전이므로 모든 항목이 미확정입니다.

| 보고서 주장 또는 요소 | 근거 파일 | 상태 |
|---|---|---|
| 타겟·PDB 선정 근거 | `configs/project.local.yaml`, 타겟 조사 기록 | 미확정 |
| 입력 화합물 수와 출처 | `experiment/inputs_manifest.csv` | 미실행 |
| ADMET-AI 5코어 처리량 | `experiment/benchmark_admet_5core_metadata.json`, `docs/benchmark_admet_5core.md` | 완료 |
| GNINA 5코어 단일 리간드 시간 | `experiment/benchmark_gnina_5core_metadata.json`, `docs/benchmark_gnina_5core.md` | 완료 |
| 활성/결합 예측 | `experiment/screening_results.csv`, `run_metadata.json` | 미실행 |
| ADMET·물성 필터 | `experiment/screening_results.csv`, `filtering_summary.csv` | 미실행 |
| 도킹 결과(선택) | `experiment/screening_results.csv`, 도킹 실행 기록 | 미실행 |
| 최종 후보와 순위 | `experiment/candidate_ranking.csv` | 미실행 |
| 보고서 그림 | `experiment/figures/` | 미실행 |

Solar Pro4는 `상태`가 미실행인 항목을 결과처럼 서술하지 않습니다.
