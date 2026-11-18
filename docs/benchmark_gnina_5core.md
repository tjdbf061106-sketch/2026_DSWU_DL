# GNINA 5코어 단일 리간드 벤치마크

_실행일: 2026-11-18 · 목적: 로컬 Docker GNINA 환경에서 CPU 5코어 기준의 단일 리간드 도킹 시간을 실측_

---

## 📋 측정 결과

| 항목 | 실측값 |
|---|---:|
| 리간드 수 | 1 |
| 벽시계 시간 | 2.67초 |
| CPU 제한 | 5 논리 코어 |
| GNINA `--cpu` | 5 |
| Exhaustiveness | 8 |
| GPU | 사용 안 함 |

이 시간은 Docker 컨테이너 실행부터 pose 파일 저장까지 포함합니다. 단일 예제 리간드의 측정값이므로, 다른 분자의 크기·회전 가능 결합 수·탐색 상자에 그대로 일반화할 수 없습니다.

## ⚙️ 재현 조건

- Docker 이미지: `gnina/gnina:v1.3.3`
- GNINA 버전: v1.3.3, master `6fe1ce2`
- 입력: 제공된 `protein.pdb`, `ligand.sdf`
- 탐색 상자: 제공 리간드 기반 `--autobox_ligand`
- 난수 시드: `20261118`
- 실행 코드: [benchmark_gnina_5core.py](../scripts/benchmark_gnina_5core.py)

## 📚 증거 파일

- [측정 메타데이터](../experiment/benchmark_gnina_5core_metadata.json)
- [GNINA 표준 출력](../experiment/benchmark_gnina_5core_stdout.log)
- [GNINA 표준 오류](../experiment/benchmark_gnina_5core_stderr.log)
- [생성된 도킹 pose](../experiment/benchmark_gnina_5core_pose.sdf)

## 🎯 다음 실행 시 주의점

전체 라이브러리에 GNINA을 적용할 때에는 상위 후보만 대상으로 삼고, 구조적 특성이 다른 리간드의 작은 배치로 다시 처리량을 재야 합니다. 이 단일 리간드 측정값만으로 전체 도킹 시간을 산정하지 않습니다.
