import serial
import time
import matplotlib.pyplot as plt

# 시리얼 포트 설정
serial_port = 'COM32'  # 실제 연결된 포트로 변경
baud_rate = 115200  # STM32 보드와 일치하도록 설정

try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# 데이터 수집 리스트
pitch = []
az = []
timestamps = []

try:
    start_time = time.time()
    while True:
        # 시리얼 포트로부터 데이터 읽기
        line = ser.readline().decode('utf-8').strip()
        if line:
            print(f"Received line: {line}")
            values = line.split(',')
            if len(values) == 2:
                try:
                    current_time = time.time() - start_time
                    timestamps.append(current_time)
                    pitch.append(float(values[0]))
                    az.append(float(values[1]))
                except ValueError as e:
                    print(f"ValueError: {e}, Received values: {values}")
            else:
                print(f"Unexpected data format: {line}")
except KeyboardInterrupt:
    print("Data collection stopped by user.")
finally:
    ser.close()
    print("Serial port closed.")

# 데이터 플롯
fig, ax1 = plt.subplots()

# 왼쪽 y축: Pitch Angle
ax1.plot(timestamps, pitch, label='Pitch Angle', color='blue')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Pitch Angle')
ax1.tick_params(axis='y', labelcolor='blue')

# 오른쪽 y축: Z-axis Accel
ax2 = ax1.twinx()
ax2.plot(timestamps, az, label='Z-axis Accel', color='red')
ax2.set_ylabel('Z-axis Accel')
ax2.tick_params(axis='y', labelcolor='red')
ax2.set_ylim(0, 5)  # y축 범위 설정

plt.title('out of zone')
fig.tight_layout()  # 그래프 요소의 간격 조정
plt.show()
