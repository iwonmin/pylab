import serial
import time
import threading
import matplotlib.pyplot as plt

# 시리얼 포트 설정
serial_port = 'COM32'  # 실제 연결된 포트로 변경
baud_rate = 115200  # STM32 보드와 일치하도록 설정

# 시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# 데이터 수집 리스트
roll = []
pitch = []
state = []
timestamps = []

# 데이터 수신 플래그
running = True

def read_data():
    global running
    start_time = time.time()
    
    while running:
        # 시리얼 포트로부터 데이터 읽기
        line = ser.readline().decode('utf-8').strip()
        if line:
            print(f"Received line: {line}")  # 디버깅 메시지 추가
            # 쉼표로 구분된 데이터를 분리
            values = line.split(',')
            if len(values) == 3:
                try:
                    # 현재 시간 기록
                    current_time = time.time() - start_time
                    timestamps.append(current_time)
                    roll.append(float(values[0]))
                    pitch.append(float(values[1]))
                    state.append(values[2])
                except ValueError as e:
                    print(f"ValueError: {e}, Received values: {values}")  # 디버깅 메시지 추가
            else:
                print(f"Unexpected data format: {line}")  # 디버깅 메시지 추가

# 데이터 수신 쓰레드 시작
data_thread = threading.Thread(target=read_data)
data_thread.start()

try:
    while True:
        # 사용자로부터 PWM 값 입력받기
        console = input("'exit' to stop")
        
        # 입력값이 'exit'이면 루프 종료
        if console.lower() == 'exit':
            running = False
            break

except KeyboardInterrupt:
    print("Data collection stopped by user.")
    running = False

finally:
    # 데이터 수신 쓰레드 종료 대기
    data_thread.join()
    
    # 시리얼 포트 닫기
    ser.close()
    print("Serial port closed.")

# 데이터 최종 플롯
fig, ax1 = plt.subplots()

# 왼쪽 y축에 roll과 pitch 데이터 플롯
ax1.plot(timestamps, roll, label='roll', color='b')
ax1.plot(timestamps, pitch, label='pitch', color='g')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Roll/Pitch', color='k')
ax1.tick_params(axis='y', labelcolor='k')

# 오른쪽 y축 설정 및 state 데이터 플롯
ax2 = ax1.twinx()
ax2.plot(timestamps, state, label='state', color='k', linestyle='--')
ax2.set_ylabel('State', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# 제목과 범례 설정
fig.suptitle('What happens at wiggle wiggle')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# 플롯 출력
plt.show()
