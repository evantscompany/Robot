# 🤖 Robot AI Agent System

GitHub 기반 로보틱스 코드 자동 분석 및 시뮬레이션 생성 시스템

## 🎯 시스템 개요

Robot AI Agent System은 GitHub 저장소를 검색하여 로보틱스 코드를 자동으로 분석하고, 시뮬레이션 환경을 구성해주는 지능형 파이프라인입니다.

### 🏗️ 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Client  │◄──►│  Express Server │◄──►│   GitHub API    │◄──►│  Repositories    │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   AI Agents      │
                       │ ┌─────────────┐ │
                       │ │ Collector   │ │
                       │ │ Analyst     │ │
                       │ │ Validator   │ │
                       │ │ Engineer    │ │
                       │ └─────────────┘ │
                       └─────────────────┘
```

## 🤖 AI 에이전트

### 1. Collector Agent
- **역할**: GitHub API를 통한 코드 수집 및 구조화
- **기능**:
  - 저장소 검색 및 메타데이터 수집
  - 관련 파일 필터링 (.py, .cpp, .urdf, .launch 등)
  - 원본 데이터 정제 및 JSON 변환

### 2. Analyst Agent  
- **역할**: 알고리즘 분석 및 로직 추출
- **기능**:
  - 프로젝트 타입 감지 (ROS1/ROS2, Python, C++)
  - 제어 알고리즘 식별 (PID, MPC, Adaptive 등)
  - ROS 토픽 맵핑 및 의존성 분석
  - 복잡도 평가

### 3. Validator Agent
- **역할**: 코드 검증 및 신뢰도 평가
- **기능**:
  - 정적 분석을 통한 문법 검사
  - 의존성 검증
  - 보안 취약점 스캔
  - 신뢰도 점수 계산 (0-100)

### 4. Engineer Agent
- **역할**: 시뮬레이션 환경 구성
- **기능**:
  - Gazebo 시뮬레이션 설정 생성
  - URDF 로봇 모델 구성
  - Launch 파일 자동 생성
  - Docker 컨테이너 설정

## 🚀 시작하기

### 사전 요구사항

- Node.js 16+ 
- npm 또는 yarn
- Git

### 설치 및 실행

1. **저장소 클론**
```bash
git clone <repository-url>
cd Robot_Git_collector
```

2. **의존성 설치**
```bash
npm run install-all
```

3. **환경 설정**
```bash
cp .env.example .env
# .env 파일에 필요한 설정 추가 (선택사항)
```

4. **서버 시작**
```bash
# 개발 모드 (서버 + 클라이언트 동시 실행)
npm run dev

# 또는 개별 실행
npm run server  # 서버만 실행 (포트 5000)
npm run client  # 클라이언트만 실행 (포트 3000)
```

5. **브라우저에서 접속**
```
http://localhost:3000
```

## 📁 프로젝트 구조

```
Robot_Git_collector/
├── package.json                 # 메인 패키지 설정
├── server/                      # 백엔드 서버
│   └── index.js                # Express 서버 및 AI 에이전트
├── client/                     # React 프론트엔드
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js             # 메인 애플리케이션
│   │   ├── App.css            # 스타일시트
│   │   └── index.js           # 엔트리 포인트
│   └── package.json
├── .env.example                # 환경 변수 예제
└── README.md                   # 이 파일
```

## 🎮 사용 방법

1. **검색어 입력**: 분석하고 싶은 로보틱스 프로젝트 검색어를 입력합니다.
   - 예: `ros2_diff_drive_controller`, `autonomous_navigation`, `robot_arm_kinematics`

2. **파이프라인 실행**: "Run Pipeline" 버튼을 클릭하여 AI 에이전트 파이프라인을 시작합니다.

3. **실시간 모니터링**: 각 에이전트의 작업 로그를 실시간으로 확인합니다.

4. **결과 확인**: 분석 완료 후 다음 결과물을 다운로드할 수 있습니다:
   - **Markdown Report**: 프로젝트 분석 보고서
   - **JSON Data**: 구조화된 분석 데이터
   - **Simulation Commands**: 시뮬레이션 실행 명령어

## 📊 분석 결과 예시

### 입력
```
ros2_diff_drive_controller
```

### 출력
```json
{
  "project": "ros2_diff_drive_controller",
  "engine": "ROS2",
  "components": ["controller.py", "robot.urdf", "package.xml"],
  "control_type": "Differential Drive",
  "complexity": "Intermediate",
  "reliability_score": 88
}
```

### 시뮬레이션 명령어
```bash
ros2 launch ros2_diff_drive_controller_sim simulation.launch.py
```

## 🔧 고급 설정

### GitHub 토큰 설정
높은 API 레이트 리밋을 위해 GitHub 토큰을 설정할 수 있습니다:

1. GitHub에서 Personal Access Token 생성
2. `.env` 파일에 추가: `GITHUB_TOKEN=your_token_here`

### 커스터마이징

#### 새로운 에이전트 추가
```javascript
class CustomAgent {
  constructor(socket) {
    this.socket = socket;
  }
  
  async process(data) {
    // 커스텀 로직 구현
    this.emitLog('Custom', 'Processing...');
    return result;
  }
  
  emitLog(agent, message) {
    this.socket.emit('agent-log', { agent, message });
  }
}
```

#### 분석 규칙 확장
`AnalystAgent`의 메서드를 수정하여 새로운 분석 규칙을 추가할 수 있습니다.

## 🐛 트러블슈팅

### 서버 연결 안됨
- 포트 5000이 사용 중인지 확인
- 방화벽 설정 확인
- `npm run server`로 서버만 먼저 실행

### GitHub API 오류
- API 레이트 리밋 확인
- GitHub 토큰 설정
- 인터넷 연결 상태 확인

### 분석 결과 부정확
- 더 많은 파일 수집 (코드 수정)
- 분석 규칙 개선
- 특정 도메인에 맞는 규칙 추가

## 🤝 기여하기

1. Fork 저장소
2. 기능 브랜치 생성: `git checkout -b feature/new-feature`
3. 커밋: `git commit -am 'Add new feature'`
4. 푸시: `git push origin feature/new-feature`
5. Pull Request 생성

## 📄 라이선스

MIT License - 자세한 내용은 LICENSE 파일 참조

## 🙏 감사

- GitHub API 제공
- ROS 커뮤니티
- Gazebo 시뮬레이터
- React 생태계

---

**개발팀**: Robot AI Agent Team  
**버전**: 1.0.0  
**최종 업데이트**: 2025-05-10
