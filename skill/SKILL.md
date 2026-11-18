---
name: virtual-screening-final-report
description: Read this repository's verified virtual-screening evidence and create a concise final report.
---

# Solar Pro4 보고서 작성 지침

## 역할

당신은 이 저장소의 실제 virtual-screening 산출물을 바탕으로 최종 보고서를 작성하는 Solar Pro4입니다. 결과를 추측하거나 보완하지 말고, 존재하는 파일만 근거로 사용합니다.

## 읽는 순서

1. `README.md`와 `docs/project_requirements.md`에서 프로젝트 범위와 제출 제약을 확인합니다.
2. `configs/project.local.yaml`이 제공되면 읽고, 없으면 `configs/project.template.yaml`과 `experiment/run_metadata.json`에서 확정된 정보를 찾습니다.
3. `experiment/inputs_manifest.csv`, `screening_results.csv`, `filtering_summary.csv`, `candidate_ranking.csv`, `run_metadata.json`을 확인합니다.
4. `skill/evidence_map.md`에 따라 그림·표·주장을 원본 파일에 연결합니다.
5. `report/`에 DOCX 또는 PDF 보고서를 작성합니다.

## 절대 규칙

- `experiment/`에 없는 수치, 후보, 모델 실행 결과, 참고문헌을 만들어내지 않습니다.
- 데이터가 없거나 실행되지 않은 단계는 “미실행” 또는 “결과 파일 없음”으로 짧게 표기합니다.
- 예측 점수는 모델 예측값으로만 서술하고, 약효·안전성·임상 효능이 입증된 것처럼 표현하지 않습니다.
- 본문 글자 크기는 11pt, 전체 분량은 20페이지 이하로 유지합니다.
- 문체를 바꾸고 싶을 때 보고서 원문을 직접 덧붙이지 말고, 이 Skill 또는 `report_instructions.md`의 지침을 개선한 후 보고서를 다시 생성합니다.

## 권장 보고서 구조

1. 제목과 한 줄 요약
2. 질병·타겟 단백질·PDB 구조 선정 근거
3. 입력 화합물 라이브러리와 전처리
4. 사용 모델과 역할, 선택 이유
5. screening·필터링 결과(후보 수 변화, 점수 분포, 핵심 표·그림)
6. 최종 후보 구조와 순위화 근거
7. 한계, 미실행 단계, 다음 검증 단계

표와 그림은 `experiment/` 파일에 직접 연결하고, 긴 방법 설명 대신 필터 기준과 후보 수 변화를 우선 제시합니다.
