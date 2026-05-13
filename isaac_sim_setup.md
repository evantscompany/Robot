1. 사전 준비 (환경 점검)
아이작 심 실행을 위해 Docker와 GPU 드라이버가 준비되어 있어야 합니다.

Docker Desktop 설정: Settings > General > Use the WSL 2 based engine 체크 확인.

GPU 인식 확인: CMD에서 아래 명령어를 입력해 표가 나오면 성공입니다.

DOS
docker run --rm --runtime=nvidia --gpus all nvidia/cuda:12.6.3-base-ubuntu22.04 nvidia-smi
2. 아이작 심 설치 (CMD 명령어)
① 이미지 다운로드 (약 9GB)
DOS
docker pull nvcr.io/nvidia/isaac-sim:6.0.0-dev2
② 내 PC에 저장용 폴더 생성
설정 파일과 데이터를 보존하기 위해 윈도우 사용자 폴더(C:\Users\사용자명\docker\...)에 미리 공간을 만듭니다.

DOS
mkdir %USERPROFILE%\docker\isaac-sim\cache\main
mkdir %USERPROFILE%\docker\isaac-sim\cache\computecache
mkdir %USERPROFILE%\docker\isaac-sim\config
mkdir %USERPROFILE%\docker\isaac-sim\data
mkdir %USERPROFILE%\docker\isaac-sim\logs
mkdir %USERPROFILE%\docker\isaac-sim\pkg
3. 아이작 심 실행 (실행 명령어)
① 컨테이너 구동 (긴 명령어)
아래 내용을 한 번에 복사해서 CMD에 붙여넣으세요. (윈도우용 ^ 기호 포함)

DOS
docker run --name isaac-sim --entrypoint bash -it --runtime=nvidia --gpus all -e "ACCEPT_EULA=Y" --rm --network=host ^
     -e "PRIVACY_CONSENT=Y" ^
     -v %USERPROFILE%\docker\isaac-sim\cache\main:/isaac-sim/.cache:rw ^
     -v %USERPROFILE%\docker\isaac-sim\cache\computecache:/isaac-sim/.nv/ComputeCache:rw ^
     -v %USERPROFILE%\docker\isaac-sim\logs:/isaac-sim/.nvidia-omniverse/logs:rw ^
     -v %USERPROFILE%\docker\isaac-sim\config:/isaac-sim/.nvidia-omniverse/config:rw ^
     -v %USERPROFILE%\docker\isaac-sim\data:/isaac-sim/.local/share/ov/data:rw ^
     -v %USERPROFILE%\docker\isaac-sim\pkg:/isaac-sim/.local/share/ov/pkg:rw ^
     nvcr.io/nvidia/isaac-sim:6.0.0-dev2
② 내부 시뮬레이터 시작 (Bash)
컨테이너 안에 접속된 상태에서 아래 명령어를 칩니다.

Bash
./runheadless.sh -v
또는 화면 스트리밍이 잘 안 될 때 권장되는 명령어:

Bash
./isaac-sim.headless.native.sh --allow-root
4. 시뮬레이션 화면 보기 (브라우저)
로딩이 완료된 후(로그에 frame ...이 올라가면), 크롬이나 엣지 브라우저에서 아래 주소로 접속합니다.

주소: http://localhost:8210

💡 주요 문제 해결(Troubleshooting) 요약
Waiting for viewport handle...: 셰이더를 굽는 중입니다. RTX 5060이라도 첫 실행 시 2~5분 정도 기다려야 합니다.

화면이 안 뜰 때: 브라우저를 새로고침하거나, 실행 시 ./isaac-sim.headless.native.sh 명령어를 사용해 보세요.

권한 에러: 만약 sudo 권한 문제가 생기면 sudo chown -R 1234:1234 ~/docker/isaac-sim (WSL 내부용) 명령을 통해 폴더 소유권을 조정해야 합니다.