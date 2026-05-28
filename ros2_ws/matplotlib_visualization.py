# ============================================================
# Import
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

# ============================================================
# CSV 경로
# ============================================================

CSV_PATH = r'C:\robot_motion_analysis\datasets\robot_log.csv'

# ============================================================
# Figure 생성
# ============================================================

fig, ax = plt.subplots(figsize=(8, 8))

# ============================================================
# 실시간 업데이트 함수
# ============================================================

def update(frame):

    # 이전 그래프 삭제
    ax.clear()

    try:

        # CSV 읽기
        df = pd.read_csv(CSV_PATH)

        # 데이터 없으면 종료
        if len(df) == 0:
            return

        # 좌표 추출
        x = df['pos_x'].to_numpy()
        y = df['pos_y'].to_numpy()

        # trajectory plot
        ax.plot(
            x,
            y,
            marker='o',
            label='Robot Trajectory'
        )

        # 시작점
        ax.scatter(
            x[0],
            y[0],
            s=120,
            label='Start'
        )

        # 종료점
        ax.scatter(
            x[-1],
            y[-1],
            s=120,
            label='Current Position'
        )

        # 그래프 설정
        ax.set_title('Live Robot Trajectory')

        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')

        ax.grid(True)

        ax.axis('equal')

        ax.legend()

    except Exception as e:

        print(f'CSV Read Error: {e}')

# ============================================================
# Animation 시작
# ============================================================

ani = FuncAnimation(
    fig,
    update,
    interval=500
)

plt.show()