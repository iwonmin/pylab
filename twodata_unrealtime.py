import serial
import time
import threading
import matplotlib.pyplot as plt

# 시리얼 포트 설정
serial_port = 'COM30'  # 실제 연결된 포트로 변경
baud_rate = 115200  # STM32 보드와 일치하도록 설정

# 시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# 데이터 수집 리스트
total_pulse = []
raw_data = []
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
            if len(values) == 2:
                try:
                    # 현재 시간 기록
                    current_time = time.time() - start_time
                    timestamps.append(current_time)
                    total_pulse.append(float(values[0]))  # Total Pulse 데이터
                    raw_data.append(float(values[1]))  # Raw Data 데이터
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
        pwm_value = input("Enter PWM value (0.0 to 1.0) or 'exit' to stop: ")
        
        # 입력값이 'exit'이면 루프 종료
        if pwm_value.lower() == 'exit':
            running = False
            break

        # 입력값을 보드로 전송
        ser.write((pwm_value + '\n').encode())

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
plt.plot(timestamps, total_pulse, label='Total Pulse')
plt.plot(timestamps, raw_data, label='Raw Data')
plt.xlabel('Time (s)')
plt.ylabel('Data')
plt.title('PWM == 1.0')
plt.legend()
plt.show()
