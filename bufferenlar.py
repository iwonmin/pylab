import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import threading

# 시리얼 포트 설정
serial_port = 'COM30'  # 실제 연결된 포트로 변경
baud_rate = 115200  # STM32 보드와 일치하도록 설정

# 시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate, timeout=1)
ser.flushInput()  # 입력 버퍼 초기화

# 데이터 수집 리스트
data = deque(maxlen=500)  # 최근 500개의 데이터를 유지
timestamps = deque(maxlen=500)  # 최근 500개의 타임스탬프를 유지
falling_edges = deque(maxlen=500)  # 최근 500개의 falling edge 타임스탬프를 유지

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
    global start_time
    # 시리얼 포트로부터 데이터 읽기
    while ser.in_waiting:
        line_data = ser.readline().decode('utf-8').strip()
        if line_data:
            current_time = time.time() - start_time
            current_value = float(line_data)
            timestamps.append(current_time)
            data.append(current_value)  # 데이터를 float으로 변환하여 저장

            # falling edge 감지
            if len(data) > 1 and data[-2] == 1 and current_value == 0:
                falling_edges.append(current_time)

    # 현재 x축 범위 계산
    if timestamps:
        start = max(0, timestamps[-1] - x_range)
        end = start + x_range

        # 플롯 x축 및 y축 범위 설정
        ax.set_xlim(start, end)
        # ax.set_ylim(min(data), max(data))

        # 샘플 시간 동안의 falling edge 평균 계산
        edges_in_window = [edge for edge in falling_edges if start <= edge <= end]
        falling_edge_avg = len(edges_in_window) / x_range

        # 데이터와 falling edge 평균 업데이트
        line.set_data(timestamps, data)
        text.set_text(f'Falling Edges (avg): {falling_edge_avg:.2f} per second')

    return line, text

# PWM 값을 입력받고 보드로 전송하는 함수
def send_pwm():
    global running
    while running:
        pwm_value = input("Enter PWM value (0.0 to 1.0) or 'exit' to stop: ")
        
        if pwm_value.lower() == 'exit':
            global exit_flag
            exit_flag = True
            running = False
            break

        ser.write((pwm_value + '\n').encode())

# 실행 플래그
running = True
exit_flag = False

# PWM 입력 스레드 시작
pwm_thread = threading.Thread(target=send_pwm)
pwm_thread.start()

# 애니메이션 설정
start_time = time.time()
ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=50, cache_frame_data=False)

try:
    plt.show()
except KeyboardInterrupt:
    print("Data collection stopped by user.")
finally:
    running = False
    pwm_thread.join()  # PWM 스레드 종료 대기
    ser.close()
    print("Serial port closed.")

    # 최종 플롯 표시
    plt.show()
