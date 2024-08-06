import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 시리얼 포트 설정
serial_port = 'COM9'  # 실제 연결된 포트로 변경
baud_rate = 115200  # STM32 보드와 일치하도록 설정

# 시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# 데이터 수집 리스트
data = []
timestamps = []
falling_edge_count = 0

# 플롯 설정
fig, ax = plt.subplots()
line, = ax.plot([], [], label='Data')
text = ax.text(0.95, 0.05, '', transform=ax.transAxes, ha='right', va='bottom', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
ax.set_xlabel('Time (s)')
ax.set_ylabel('Data')
ax.set_title('Real-Time Data from STM32')
ax.legend()

# 플롯의 x축 범위 간격 (초)
x_range = 1

# 초기화 함수
def init():
    ax.set_xlim(0, x_range)
    ax.set_ylim(-2, 2)  # y축 범위는 실제 데이터에 따라 조정
    return line, text

# 업데이트 함수
def update(frame):
    global falling_edge_count
    # 시리얼 포트로부터 데이터 읽기
    line_data = ser.readline().decode('utf-8').strip()
    if line_data:
        current_time = time.time() - start_time
        current_value = float(line_data)
        timestamps.append(current_time)
        data.append(current_value)  # 데이터를 float으로 변환하여 저장

        # falling edge 감지
        if len(data) > 1 and data[-2] == 1 and current_value == 0:
            falling_edge_count += 1

        # 현재 x축 범위 계산
        start = max(0, current_time - x_range)
        end = start + x_range

        # 플롯 x축 및 y축 범위 설정
        ax.set_xlim(start, end)
        # ax.set_ylim(min(data), max(data))

        # 데이터와 falling edge 횟수 업데이트
        line.set_data(timestamps, data)
        text.set_text(f'Falling Edges: {falling_edge_count}')

    return line, text

start_time = time.time()
ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=10, cache_frame_data=False)

try:
    plt.show()
except KeyboardInterrupt:
    print("Data collection stopped by user.")
finally:
    # 시리얼 포트 닫기
    ser.close()
    print("Serial port closed.")
