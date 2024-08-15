import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# 시리얼 포트 설정 (STM32에 맞게 설정)
ser = serial.Serial('COM32', 115200, timeout=1) 

# 초기값 설정
x_data = []
y1_data = []
y2_data = []
string_data = ""
start_time = time.time()

# 그래프 초기 설정
fig, ax = plt.subplots()
line1, = ax.plot([], [], 'b-', label='roll')  # 첫 번째 데이터에 대한 그래프 라인 (파란색)
line2, = ax.plot([], [], 'r-', label='yaw')  # 두 번째 데이터에 대한 그래프 라인 (빨간색)
text = ax.text(0.95, 0.01, '', verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes)

# 그래프의 한계를 설정해줍니다.
ax.set_xlim(0, 10)
ax.set_ylim(-10, 10)  # y축 범위를 적절히 설정하세요
ax.legend(loc='upper left')  # 그래프의 범례를 왼쪽 위에 표시

# 데이터 업데이트 함수
def update(frame):
    global string_data
    
    # 시리얼 데이터 읽기
    try:
        line_data = ser.readline().decode('utf-8').strip()
        if line_data:
            y1, y2, string_data = line_data.split(',')
            y1 = float(y1)
            y2 = float(y2)
            current_time = time.time() - start_time  # 경과 시간 계산
            x_data.append(current_time)
            y1_data.append(y1)
            y2_data.append(y2)
            
            # 그래프 업데이트
            line1.set_data(x_data, y1_data)
            line2.set_data(x_data, y2_data)
            text.set_text(string_data)

            # x축, y축 범위를 동적으로 조정
            ax.set_xlim(min(x_data), max(x_data) + 1)
            ax.set_ylim(min(min(y1_data), min(y2_data)) - 1, max(max(y1_data), max(y2_data)) + 1)

    except Exception as e:
        print(f"Error: {e}")

    return line1, line2, text

# 애니메이션 설정
ani = animation.FuncAnimation(fig, update, blit=True, interval=100)

# 그래프 보여주기
plt.show()

# 시리얼 포트 닫기
ser.close()
