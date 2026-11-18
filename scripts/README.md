# 실행 스크립트

실제 모델·환경이 결정된 후 아래와 같이 단계별 스크립트를 추가합니다.

```text
01_prepare_library.py      # 구조 검증, 표준화, 중복 제거
02_predict_activity.py     # 타겟 활성 또는 결합 관련 예측
03_predict_admet.py        # 용해도, logP, ADMET 예측
04_run_docking.py          # 필요 시 GNINA 실행
05_rank_candidates.py      # 기준 적용과 후보 순위화
06_make_figures.py         # 보고서용 Matplotlib 시각화
```

각 스크립트는 설정 파일 경로를 인수로 받고, 입력·출력 경로와 실행 명령을 `experiment/run_metadata.json`에 남겨야 합니다. 스크립트가 생성한 결과만 `experiment/`의 최종 CSV로 사용합니다.
