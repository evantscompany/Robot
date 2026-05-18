# Agriculture_data 폴더 요약

## 폴더 구조

- `2025_wage_labor_estimate/`
  - `(2025년)_농번기_인력_지원대책_농번기(4∼6월,_9∼10월)_농업_고용인력의_적기·적정_공급으로_‘25년_농산물의_안정적_생산·공급_지원.pdf`
  - `dashboard.html`
  - `labor_cost_estimation.ipynb`
- `survey_robotic_harvesting/`
  - `harvesting_robot_survey.py`
  - `survey_robotic harvesting_system.pdf`

---

## 2025_wage_labor_estimate

### 주요 내용
- 2025년 농번기 인력 지원 대책 관련 PDF를 기반으로 한 분석 프로젝트
- 농작물별·농작업별 월별 인력 수요를 `Long Format` 데이터로 변환하여 분석
- 작업 유형에 따라 임금 단가를 매칭하고, 예상 노동비용을 추정

### 포함 파일
- `(2025년)_농번기_인력_지원대책_..._지원.pdf`
  - 농번기 인력 수요 및 공급 대책 자료
  - 가로형 2차원 매트릭스 표 형태로 구성된 데이터를 포함
- `labor_cost_estimation.ipynb`
  - Python 분석 노트북
  - 주요 분석 내용:
    - 농작물(`crop`)과 농작업(`operation`)별 월별 수요(`monthly_demand`) 데이터를 정의
    - 데이터를 long format으로 전개하여 `DataFrame` 생성
    - 작업별로 임금 분류 및 단가 매핑
      - `전정`, `수분`, `알솎기`, `순지르기`: 전문기술직, 일당 150,000원
      - `수확`, `파종`: 일반고강도직, 일당 135,000원
      - `적과`, `봉지씌우기`, `정식`: 일반반복직, 일당 120,000원
    - 수요와 단가를 기반으로 전체 임금 예측값 계산
- `dashboard.html`
  - 분석 결과를 시각화/리포트 형식으로 보여주는 HTML 파일

### 분석 포인트
- 주요 작물: 사과, 복숭아, 마늘, 고추, 포도, 양파, 감자, 배, 배추, 무
- 각 작업의 월별 노동 수요를 정리하고, 농업 현장의 인력 부족 및 비용 구조를 평가
- 농업 로봇 도입 시 대체 가능성과 비용 절감 잠재력을 가늠하는 데 유용함

---

## survey_robotic_harvesting

### 주요 내용
- 로봇 수확 시스템 관련 PDF를 분석하고, 한국어 번역 및 요약을 자동 생성하는 Python 스크립트
- PDF에서 텍스트와 표를 추출하여 HTML 대시보드를 생성하는 흐름을 구현

### 포함 파일
- `harvesting_robot_survey.py`
  - PDF 분석 파이프라인 코드
  - 주요 기능:
    - `pdfplumber`로 PDF 텍스트 및 표 추출
    - 추출된 텍스트를 챕터 기준으로 분류
    - `deep_translator.GoogleTranslator`를 사용해 영어 텍스트를 한국어로 번역
    - 번역된 내용을 요약하고 중요 포인트를 추출
    - 결과를 보기 좋은 HTML 리포트(`pdf_analysis_result.html`)로 저장
  - 현재 코드에서 읽는 PDF 경로:
    - `C:\Users\msm03\Desktop\survey_robotic harvesting_system.pdf`
- `survey_robotic harvesting_system.pdf`
  - 수확 로봇 시스템 관련 원본 PDF 문서

### 스크립트 특징
- 한국어 번역 및 요약을 자동화함
- 추출한 표 데이터를 HTML 테이블로 표시하여 결과를 시각적으로 확인 가능
- 챕터별 요약과 주요 인사이트를 함께 제공

---

## 전체 요약

- `Agriculture_data` 폴더는 농업 인력 분석과 로봇 수확 시스템 리포트 자동화 연구를 포함
- `2025_wage_labor_estimate`는 농번기 인력 수요와 비용 예측에 집중
- `survey_robotic_harvesting`는 로봇 수확 관련 문서 분석 및 자동 요약 대시보드 생성에 집중
- 두 프로젝트 모두 농업 현장의 인력 문제와 자동화 가능성을 데이터 기반으로 검토하는 목적을 가짐
