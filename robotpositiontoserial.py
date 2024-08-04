import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.animation import FuncAnimation
import serial

# 로봇 클래스 정의
class Robot:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
    
    def update(self, x, y, angle):
        self.x += x
        self.y += y
        self.angle += angle

# (절대 좌표에서 로봇 위치)
robot = Robot(x=60, y=0, angle=90)

# 시리얼 포트 설정 (포트와 보드레이트를 실제 사용하는 값으로 바꿔야 함)
ser = serial.Serial('COM4', 115200, timeout=1)  # Windows의 경우 'COMx', Linux/Mac은 '/dev/ttyUSBx'

# 그래프 설정
fig, ax = plt.subplots()

# 배경 설정
ax.add_patch(patches.Rectangle((-120, -120), 240, 240, fill=True, color='black'))
ax.add_patch(patches.Circle((0, 0), 35, color='red'))

# 부채꼴 추가
wedge1 = patches.Wedge(center=(-120, 120), r=70, theta1=180, theta2=90, facecolor='blue', edgecolor='none')
ax.add_patch(wedge1)
wedge2 = patches.Wedge(center=(-120, -120), r=70, theta1=0, theta2=90, facecolor='blue', edgecolor='none')
ax.add_patch(wedge2)
wedge3 = patches.Wedge(center=(120, 120), r=70, theta1=180, theta2=270, facecolor='blue', edgecolor='none')
ax.add_patch(wedge3)
wedge4 = patches.Wedge(center=(120, -120), r=70, theta1=90, theta2=180, facecolor='blue', edgecolor='none')
ax.add_patch(wedge4)

# 로봇의 화살표(로봇 초기 위치)
arrow = patches.FancyArrowPatch((robot.x, robot.y), 
                                (robot.x + 5 * np.cos(np.deg2rad(robot.angle)), robot.y + 5 * np.sin(np.deg2rad(robot.angle))), 
                                mutation_scale=50, color='white', 
                                linestyle='-', arrowstyle='-|>', connectionstyle='arc3,rad=0.2')
ax.add_patch(arrow)

# 축 설정
ax.set_xlim(-120, 120)
ax.set_ylim(-120, 120)
ax.set_aspect('equal')

def update(frame):
    # 시리얼 포트에서 데이터 읽기
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        try:
            # 데이터 파싱: "x,y,angle" 형식으로 들어온다고 가정
            x_str, y_str, angle_str = line.split(',')
            x = float(x_str)
            y = float(y_str)
            angle = float(angle_str)
            robot.update(x, y, angle)
            
            # 화살표 업데이트(로봇 초기위치에서 로봇의 상대좌표만큼 increment)
            arrow.set_positions((robot.x, robot.y),
                                (robot.x + 5 * np.cos(np.deg2rad(robot.angle)), robot.y + 5 * np.sin(np.deg2rad(robot.angle))))
            arrow.set_figure(fig)  # Update figure to reflect changes
        except ValueError:
            print("Received data in unexpected format.")
    
    return arrow,

# 애니메이션 생성
ani = FuncAnimation(fig, update, frames=100, interval=100, blit=False)

plt.show()
