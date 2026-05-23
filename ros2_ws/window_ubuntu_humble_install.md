1단계: WSL2 및 Ubuntu 22.04 설치 (Windows 터미널)
윈도우 시작 버튼 우클릭 ➔ Terminal(PowerShell)을 관리자 권한으로 실행한 뒤 아래 명령어를 입력합니다.

PowerShell
# 1. Ubuntu 22.04 버전으로 WSL2 설치
wsl --install -d Ubuntu-22.04
설치가 완료되면 컴퓨터를 한 번 재부팅하라는 안내가 뜰 수 있습니다.

재부팅 후 자동으로 리눅스 콘솔 창이 열리며 Username과 Password를 설정하라고 나옵니다. 기억하기 쉬운 비밀번호로 세팅해 주세요.

2단계: WSL2 내부 환경 업데이트 (Ubuntu 터미널)
새로 열린 Ubuntu 22.04 리눅스 터미널 창에서 패키지 매니저를 최신 상태로 업데이트합니다.

Bash
sudo apt update && sudo apt upgrade -y
3단계: ROS 2 Humble 공식 설치 툴킷 가동
공식 레포지토리를 등록하고 ROS 2 Humble을 설치하는 과정입니다. 명령어 양이 좀 되니 한 줄씩 복사해서 붙여넣어 주세요.

① 로케일(Locale) 설정 (언어 및 문자 인코딩 설정)
Bash
sudo apt update && sudo apt install locales -y
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
② ROS 2 Apt 레포지토리 등록
Bash
sudo apt install software-properties-common -y
sudo add-apt-repository universe -y

sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/sqlite3 /etc/apt/sources.list.get /etc/apt/sources.list.d/ros2.list > /dev/null
③ ROS 2 Humble 데스크톱 버전 설치
Bash
sudo apt update
sudo apt install ros-humble-desktop -y
(설치에 몇 분 정도 소요됩니다. 차분히 커피 한 잔 하셔도 좋습니다.)

④ 빌드 도구 및 파이썬 의존성 패키지 설치
Bash
sudo apt install python3-colcon-common-extensions python3-rosdep python3-argcomplete -y
4단계: 🌟 [가장 중요] WSL2로 아두이노 시리얼 포트 넘겨주기
WSL2는 독립된 가상화 환경이기 때문에, 노트북에 꽂은 아두이노(COM5 등)를 인식하지 못합니다. 윈도우의 USB 장치를 WSL2 리눅스 쪽으로 강제 이식해 주는 usbipd 도구를 세팅해야 합니다.

① 윈도우(PowerShell) 작업
다시 윈도우 PowerShell(관리자 권한)을 열고 usbipd 프로그램을 설치합니다.

PowerShell
# 1. usbipd 설치 (설치 후 파워쉘 창을 껐다 다시 켜야 적용됩니다)
winget install pywin32
winget install usbipd-win

# 2. 노트북에 아두이노를 꽂은 상태에서 리스트 확인
usbipd list
리스트를 보면 COM5나 Arduino Uno 옆에 BUSID (예: 2-3)가 보일 겁니다. 기억해 두세요.

PowerShell
# 3. 해당 USB 장치를 WSL2로 바인딩 (BUSID가 2-3이라고 가정)
usbipd attach --wsl --busid 2-3
② 리눅스(Ubuntu) 작업
이제 Ubuntu 터미널로 돌아와서 아두이노가 잡혔는지 확인합니다.

Bash
ls /dev/ttyACM* /dev/ttyUSB*
포트 이름(예: /dev/ttyACM0)이 정상적으로 뜨면 성공입니다! 통신 권한을 열어줍니다.

Bash
sudo chmod 666 /dev/ttyACM0
5단계: ROS 2 Humble 구동 테스트
이제 모든 인프라가 갖춰졌습니다. 터미널을 열고 환경 변수를 로드한 뒤 이전에 설계했던 워크스페이스를 빌드하러 가면 됩니다!

Bash
# ROS 2 환경 로드
source /opt/ros/humble/setup.bash

# 터미널을 켤 때마다 자동으로 로드되도록 .bashrc에 등록해두면 편합니다.
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
이제 이 Ubuntu 환경 안에서 mkdir -p ~/ros2_ws/src 하시고 아까 짜놓은 robot_serial_bridge 패키지를 그대로 가져가서 colcon build 돌려주시면 됩니다.