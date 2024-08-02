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
    
    def update(self, dx, dy, dangle):
        self.x += dx
        self.y += dy
        self.angle += dangle

# 로봇 초기 설정
robot = Robot(x=60, y=0, angle=0)
# 기하하적 원점

# 초기 위치와 각도 변화
dx, dy = 0.1, 0.05
dangle = 0.1

# 그래프 설정
fig, ax = plt.subplots()

# 배경 설정
ax.add_patch(patches.Rectangle((-120, -120), 240, 240, fill=True, color='black'))
ax.add_patch(patches.Circle((0, 0), 35, color='red'))

wedge1 = patches.Wedge(center=(-120, 120), r=70, theta1=180, theta2=90, 
                          facecolor='blue', edgecolor='none')
ax.add_patch(wedge1)
wedge2 = patches.Wedge(center=(-120, -120), r=70, theta1=0, theta2=90, 
                          facecolor='blue', edgecolor='none')
ax.add_patch(wedge2)
wedge3 = patches.Wedge(center=(120, 120), r=70, theta1=180, theta2=270, 
                          facecolor='blue', edgecolor='none')
ax.add_patch(wedge3)
wedge4 = patches.Wedge(center=(120, -120), r=70, theta1=90, theta2=180, 
                          facecolor='blue', edgecolor='none')
ax.add_patch(wedge4)

# 로봇의 화살표
arrow = patches.FancyArrowPatch((robot.x, robot.y), 
                                (robot.x + 5 * np.cos(robot.angle), robot.y + 5 * np.sin(robot.angle)), mutation_scale=50, color='white', 
                                linestyle='-', arrowstyle='-|>', connectionstyle='arc3,rad=0.2')
ax.add_patch(arrow)

# 축 설정
ax.set_xlim(-120, 120)
ax.set_ylim(-120, 120)
ax.set_aspect('equal')

def update(frame):
    # 로봇 위치와 방향 업데이트
    robot.update(dx, dy, dangle)
    
    # 화살표 업데이트
    arrow.set_positions((robot.x, robot.y),
                        (robot.x + 5 * np.cos(robot.angle), robot.y + 5 * np.sin(robot.angle)))
    arrow.set_figure(fig)  # Update figure to reflect changes
    
    return arrow,

# 애니메이션 생성
ani = FuncAnimation(fig, update, frames=100, interval=100, blit=True)

plt.show()










