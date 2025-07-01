from vpython import *
import numpy as np

# ── 場景設定 ────────────────────────────────────────────────
scene = canvas(
    title="三棒連桿系統 (旋轉半徑計算)",
    width=1200,
    height=800,
    background=color.white
)

# ── 系統參數 ────────────────────────────────────────────────
L = 2                                   # 每根棒子長度
alpha = np.radians(120)                 # 第一、二棒夾角 (120°)
beta  = np.radians(115)                 # 第二、三棒夾角 (115°)
rod_radius = 0.01                       # 棒子半徑

# ── 建立三根棒子 ────────────────────────────────────────────
rod1 = cylinder(
    pos=vector(0, 0, 0),
    axis=vector(L, 0, 0),
    radius=rod_radius,
    color=color.blue
)
rod2 = cylinder(
    pos=rod1.pos + rod1.axis,
    axis=vector(L * np.cos(alpha), L * np.sin(alpha), 0),
    radius=rod_radius,
    color=color.green
)
rod3 = cylinder(
    pos=rod2.pos + rod2.axis,
    axis=vector(L * np.cos(alpha + beta), L * np.sin(alpha + beta), 0),
    radius=rod_radius,
    color=color.red
)

# ── x 軸投影箭頭與末端軌跡 ──────────────────────────────────
projection = arrow(
    pos=vector(0, 0, 0),
    axis=vector(0, 0, 0),                # 初始無長度，稍後更新
    shaftwidth=0.02,
    color=color.red,
    opacity=0.6
)
trail = curve(color=color.purple, radius=0.01)     # 第三棒末端軌跡

# ── 文字標籤 (放於畫面下方，與雙棒範例一致) ─────────────────
angle_label = label(
    pos=vector(0, -0.5, 0),
    text=f'第二棒向量與第一棒向量夾角: {np.degrees(alpha):.0f}°，'
         f'第三棒向量與第二棒向量夾角: {np.degrees(beta):.0f}°',
    height=20,
    color=color.black
)

status_label = label(
    pos=vector(0, -0.8, 0),
    text='旋轉半徑 R = 計算中…，x 軸投影長度 = 計算中…',
    height=20,
    color=color.purple
)

# ── 旋轉動畫初始化 ───────────────────────────────────────────
theta = 0.0
dtheta = 0.005
max_R = 0                               # 記錄歷史最大旋轉半徑

# ── 主迴圈 ──────────────────────────────────────────────────
while True:
    rate(150)

    # 更新三根棒子的位置與方向
    rod1.axis = vector(L * np.cos(theta), L * np.sin(theta), 0)

    rod2.pos = rod1.pos + rod1.axis
    rod2.axis = vector(L * np.cos(theta + alpha),
                       L * np.sin(theta + alpha), 0)

    rod3.pos = rod2.pos + rod2.axis
    rod3.axis = vector(L * np.cos(theta + alpha + beta),
                       L * np.sin(theta + alpha + beta), 0)

    # 第三棒末端座標 C 及其 x 投影
    C = rod3.pos + rod3.axis
    C_x = C.x                              # = L∑cos(θ+偏移)

    # 更新軌跡與 x 軸投影箭頭
    trail.append(pos=C)
    projection.axis = vector(C_x, 0, 0)

    # 計算旋轉半徑並更新歷史最大值
    current_R = mag(C)
    if current_R > max_R:
        max_R = current_R

    # 更新動態標籤文字
    status_label.text = (f'旋轉半徑 R = {max_R:.4f}，'
                         f'x 軸投影長度 = {C_x:.4f}')

    # 增量角度
    theta += dtheta
