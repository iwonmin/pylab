import serial
import time
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

try:
    print("Reading data from serial port...")
    start_time = time.time()
    
    while True:
        # 사용자로부터 PWM 값 입력받기
        pwm_value = input("Enter PWM value (0.0 to 1.0): ")
        
        # 입력값이 'exit'이면 루프 종료
        if pwm_value.lower() == 'exit':
            break

        # 입력값을 보드로 전송
        ser.write((pwm_value + '\n').encode())

        # 시리얼 포트로부터 데이터 읽기
        line = ser.readline().decode('utf-8').strip()
        if line:
            # 쉼표로 구분된 데이터를 분리
            values = line.split(',')
            if len(values) == 2:
                # 현재 시간 기록
                current_time = time.time() - start_time
                timestamps.append(current_time)
                total_pulse.append(float(values[0]))  # Total Pulse 데이터
                raw_data.append(float(values[1]))  # Raw Data 데이터

                # 실시간 플로팅
                plt.clf()
                plt.plot(timestamps, total_pulse, label='Total Pulse')
                plt.plot(timestamps, raw_data, label='Raw Data')
                plt.xlabel('Time (s)')
                plt.ylabel('Data')
                plt.title('Real-Time Data from STM32')
                plt.legend()
                plt.pause(0.02)  # 짧은 시간 지연

except KeyboardInterrupt:
    print("Data collection stopped by user.")

finally:
    # 시리얼 포트 닫기
    ser.close()
    print("Serial port closed.")

# 데이터 최종 플롯
plt.show()
