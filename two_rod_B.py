from vpython import *
import numpy as np

# 設定場景
scene = canvas(title="固定夾角雙棒系統 (含x軸投影)", width=1200, height=800, background=color.white)

# 參數設定
L = 2                          # 棒子長度
alpha = 175 * np.pi/180         # 固定夾角 (175度)
rod_radius = 0.01                # 棒子粗細

# 理論旋轉半徑
theoretical_R = L * np.sqrt(2 + 2*np.cos(alpha))
"""
# 建立參考x軸 (紅色虛線)
x_axis = curve(color=color.red, radius=0.01, dash=[2,2])
x_axis.append(pos=vector(-L*1.0, 0, 0))  # 延伸2倍棒長
x_axis.append(pos=vector(L*1.0, 0, 0))
"""
# 建立棒子
rod1 = cylinder(pos=vector(0,0,0), axis=vector(L,0,0), 
              radius=rod_radius, color=color.blue)
rod2 = cylinder(pos=rod1.pos + rod1.axis, 
              axis=vector(L*np.cos(alpha), L*np.sin(alpha),0), 
              radius=rod_radius, color=color.green)

# 建立第二棒末端在x軸的投影箭頭 (紫色)
projection = arrow(pos=vector(0,0,0), axis=vector(L*(1+np.cos(alpha)),0,0),
                shaftwidth=0.02, color=color.red, opacity=0.6)

# 建立軌跡
trail = curve(color=color.orange, radius=0.01)

# 文字標籤
r_label = label(pos=vector(0,-0.5,0), 
                   text=f'第二波向量和第一波向量夾角: 175度，旋轉半徑 R = {theoretical_R:.4f}',
                   height=20, color=color.black)
projection_label = label(pos=vector(0,-0.8,0),
                       text='x軸投影長度: 計算中...',
                       height=20, color=color.purple)

# 旋轉動畫
theta = 0
dtheta = 0.005
max_R = 0

while True:
    rate(150)
    
    # 更新第一根棒子
    rod1.axis = vector(L*np.cos(theta), L*np.sin(theta), 0)
    
    # 更新第二根棒子 (固定夾角)
    rod2.pos = rod1.pos + rod1.axis
    rod2.axis = vector(L*np.cos(theta + alpha), L*np.sin(theta + alpha), 0)
    
    # 更新軌跡
    B = rod2.pos + rod2.axis  # 第二根棒子末端
    trail.append(pos=B)
    
    # 更新x軸投影 (計算第二棒末端的x座標)
    B_x = L*(np.cos(theta) + np.cos(theta + alpha))  # B.x = Lcosθ + Lcos(θ+α)
    projection.axis = vector(B_x, 0, 0)
    
    # 計算旋轉半徑
    current_R = mag(B)
    if current_R > max_R:
        max_R = current_R
    
    # 更新標籤   
    r_label.text = f'第二波向量和第一波向量夾角: 175度，旋轉半徑 R ={max_R:.4f}'
    projection_label.text = f'投影長度: {B_x:.4f}'
     
    theta += dtheta
