import serial
import time
import matplotlib.pyplot as plt

# 시리얼 포트 설정
serial_port = 'COM3'  # 실제 연결된 포트로 변경
baud_rate = 9600  # STM32 보드와 일치하도록 설정

# 시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# 데이터 수집 리스트
data1 = []
data2 = []
timestamps = []

try:
    print("Reading data from serial port...")
    start_time = time.time()
    
    while True:
        # 시리얼 포트로부터 데이터 읽기
        line = ser.readline().decode('utf-8').strip()
        if line:
            # 쉼표로 구분된 데이터를 분리
            values = line.split(',')
            if len(values) == 2:
                # 현재 시간 기록
                current_time = time.time() - start_time
                timestamps.append(current_time)
                data1.append(float(values[0]))  # 첫 번째 데이터
                data2.append(float(values[1]))  # 두 번째 데이터

                # 실시간 플로팅
                plt.clf()
                plt.plot(timestamps, data1, label='Data 1')
                plt.plot(timestamps, data2, label='Data 2')
                plt.xlabel('Time (s)')
                plt.ylabel('Data')
                plt.title('Real-Time Data from STM32')
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
