# Resources 폴더

이 폴더에는 PR4 프로젝트의 시각적 자료들이 포함되어 있습니다.

## 이미지 파일 목록

- **real-time_Eng_temp_monitoring_sys.png**: 웹 기반 ECU 대시보드 스크린샷
  - 터미널 스타일의 녹색 텍스트 인터페이스
  - 실시간 RPM, 온도, 속도 모니터링
  - 액셀 페달 슬라이더 및 제어 버튼

- **ECU_Auto_Cooling_HW.png**: Wokwi 시뮬레이터 환경
  - ESP32 보드와 주변 하드웨어 구성
  - 가변저항(액셀)과 RGB LED 연결
  - 실시간 시뮬레이션 실행 화면

- **tractor_dignostics_temp_servo_valve_control.png**: 시스템 아키텍처 다이어그램
  - 전체 시스템 구조와 데이터 흐름
  - 웹-서버-ESP32 간의 통신 프로토콜
  - 엔진 물리 연산 모듈 구성

## 이미지 사용법

README.md에서 이미지를 참조할 때:
```markdown
![설명 텍스트](resources/파일명.png)
```

예시:
```markdown
![웹 대시보드](resources/dashboard.png)
```

## 이미지 추가 방법

1. 스크린샷 캡처 (PNG 권장)
2. 이 resources 폴더에 저장
3. README.md에 이미지 링크 추가
4. Git에 함께 커밋

## 권장 이미지 사양

- **형식**: PNG 또는 JPG
- **크기**: 너비 800-1200px 권장
- **용량**: 파일당 2MB 이하 권장
- **이름**: 영문 소문자, 언더스코어 사용
