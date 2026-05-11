# 🛠️ 환경 설정 가이드

## 📋 .env 파일 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 아래 내용을 설정하세요.

```bash
cp .env.example .env
```

## 🔧 필수 환경 변수

### 1. 기본 서버 설정
```env
# 서버 포트 (기본값: 5000)
PORT=5000

# 클라이언트 API URL
REACT_APP_API_URL=http://localhost:5000
```

### 2. GitHub API 설정 (권장)
```env
# GitHub Personal Access Token
# 생성 방법: GitHub > Settings > Developer settings > Personal access tokens
GITHUB_TOKEN=ghp_your_github_token_here

# GitHub API 엔드포인트 (기본값)
GITHUB_API_BASE=https://api.github.com
```

## 🚀 GitHub 토큰 생성 방법

### 1. GitHub Personal Access Token 생성
1. GitHub 로그인
2. Settings > Developer settings > Personal access tokens > Tokens (classic)
3. "Generate new token" 클릭
4. 권한 설정:
   - ✅ `public_repo` (공개 저장소 접근)
   - ✅ `repo` (모든 저장소 접근 - 선택사항)
   - ✅ `read:org` (조직 저장소 접근 - 선택사항)
5. 토큰 복사하여 `.env` 파일에 붙여넣기

### 2. 토큰 권한 설명
- **필수**: `public_repo` - 공개 저장소 검색 및 접근
- **선택**: `repo` - 개인 저장소 포함 모든 저장소 접근
- **선택**: `read:org` - 특정 조직의 저장소 접근

## 📊 API 레이트 리밋

| 인증 방식 | 시간당 요청 | 제한 |
|-----------|------------|------|
| 인증 안함 | 60 requests | IP당 |
| 토큰 인증 | 5,000 requests | 사용자당 |

**권장**: 반드시 GitHub 토큰을 설정하여 높은 레이트 리밋을 확보하세요.

## 🔍 테스트 방법

### 1. 서버 상태 확인
```bash
curl http://localhost:5000/api/health
```

### 2. GitHub API 연결 테스트
```bash
# 토큰 없이
curl https://api.github.com/search/repositories?q=ros2

# 토큰으로
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/search/repositories?q=ros2
```

## ⚠️ 보안 주의사항

### 1. 토큰 관리
- ✅ `.env` 파일은 `.gitignore`에 포함됨
- ✅ 절대 토큰을 코드에 직접 작성하지 마세요
- ✅ 주기적으로 토큰을 갱신하세요
- ❌ 토큰을 공개 저장소에 커밋하지 마세요

### 2. 권한 최소화
- 필요한 최소 권한만 부여하세요
- 토큰 사용 후 즉시 삭제 가능
- 만료 기간 설정 권장

## 🐛 문제 해결

### 1. "API rate limit exceeded" 오류
```env
GITHUB_TOKEN=your_actual_token_here
```
- GitHub 토큰을 설정하세요

### 2. "Bad credentials" 오류
- 토큰이 올바른지 확인
- 토큰 권한이 만료되지 않았는지 확인
- 토큰에 공백이 없는지 확인

### 3. "Connection refused" 오류
- 서버가 실행 중인지 확인: `npm run server`
- 포트 5000이 사용 중인지 확인

### 4. "Socket connection failed" 오류
- 클라이언트와 서버가 모두 실행 중인지 확인
- 방화벽 설정 확인
- CORS 설정 확인

## 🌐 네트워크 설정

### 프록시 설정 (필요시)
```env
# HTTP 프록시
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=https://proxy.company.com:8080

# 또는 .npmrc 파일 설정
proxy=http://proxy.company.com:8080
https-proxy=https://proxy.company.com:8080
```

### 로컬 개발 환경
```env
# 개발 환경 설정
NODE_ENV=development
```

## 📱 환경별 설정

### 개발 환경 (development)
```env
NODE_ENV=development
PORT=5000
REACT_APP_API_URL=http://localhost:5000
```

### 프로덕션 환경 (production)
```env
NODE_ENV=production
PORT=80
REACT_APP_API_URL=https://your-domain.com
```

## 🔍 디버깅

### 환경 변수 확인
```bash
# 서버 환경 변수 확인
node -e "console.log(process.env)"

# 클라이언트 환경 변수 확인 (브라우저 콘솔)
console.log(process.env)
```

### 로그 확인
```bash
# 서버 로그 확인
npm run server

# 클라이언트 로그 확인
npm run client
```

---

**📝 중요**: `.env` 파일은 절대 Git에 커밋하지 마세요!  
**🔐 보안**: 토큰은 주기적으로 갱신하고 안전하게 관리하세요.  
**🚀 성능**: 토큰 설정 시 API 호출 속도가 80배 향상됩니다.
