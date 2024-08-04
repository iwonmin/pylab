import serial
import time
import matplotlib.pyplot as plt

# 시리얼 포트 설정
serial_port = 'COM4'  # 실제 연결된 포트로 변경
baud_rate = 115200  # STM32 보드와 일치하도록 설정

# 시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# 데이터 수집 리스트
data = []
timestamps = []

# 플롯의 x축 범위 간격 (초)
x_range = 0.5

try:
    print("Reading data from serial port...")
    start_time = time.time()

    while True:
        # 시리얼 포트로부터 데이터 읽기
        line = ser.readline().decode('utf-8').strip()
        if line:
            # 현재 시간 기록
            current_time = time.time() - start_time
            timestamps.append(current_time)
            data.append(int(line))  # 데이터를 float으로 변환하여 저장

            # 현재 x축 범위 계산
            start = max(0, current_time - x_range)
            end = start + x_range

            # 실시간 플로팅
            plt.clf()
            plt.plot(timestamps, data, label='Data')
            plt.xlabel('Time (s)')
            plt.ylabel('Data')
            plt.title('Real-Time Data from STM32')
            plt.xlim(start, end)  # x축 범위 설정
            plt.legend()
            plt.pause(0.01)  # 짧은 시간 지연

except KeyboardInterrupt:
    print("Data collection stopped by user.")

finally:
    # 시리얼 포트 닫기
    ser.close()
    print("Serial port closed.")

# 데이터 최종 플롯
plt.show()
