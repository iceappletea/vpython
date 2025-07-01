from vpython import *
import numpy as np

# ─────────────────────────────────────────────
# 場景設定
# ─────────────────────────────────────────────
scene = canvas(
    title="旋轉棒子系統 (含 x 軸投影)",
    width=1200,
    height=800,
    background=color.white
)

# ─────────────────────────────────────────────
# 參數設定
# ─────────────────────────────────────────────
L = 2.0                # 棒子長度
rod_radius = 0.01       # 棒子半徑

# ─────────────────────────────────────────────
# 座標與圖形元件
# ─────────────────────────────────────────────
# 參考 x 軸（黃色虛線）
x_axis = curve(color=color.yellow, radius=0.05, dash=[2, 2])
x_axis.append(pos=vector(-1.5 * L, 0, 0))
x_axis.append(pos=vector( 1.5 * L, 0, 0))

# 棒子（藍色）
rod = cylinder(
    pos=vector(0, 0, 0),
    axis=vector(L, 0, 0),
    radius=rod_radius,
    color=color.blue
)

# 棒子末端在 x 軸的投影（紅色箭頭）
projection = arrow(
    pos=vector(0, 0.1, 0),
    axis=vector(L, 0, 0),
    shaftwidth=0.1,
    color=color.red,
    opacity=0.5
)

# 末端運動軌跡（綠色）
trail = curve(color=color.green, radius=0.05)

# ─────────────────────────────────────────────
# 文字標籤
# ─────────────────────────────────────────────
r_label = label(
    pos=vector(0, -0.5, 0),
    text=f"旋轉半徑 R = {L:.4f}",
    height=20,
    color=color.black,
    border=4,
    box=False
)

projection_label = label(
    pos=vector(0, -0.8, 0),
    text="x 軸投影長度: 計算中...",
    height=20,
    color=color.purple,
    border=4,
    box=False
)

# ─────────────────────────────────────────────
# 動畫主迴圈
# ─────────────────────────────────────────────
theta  = 0.0           # 當前角度
dtheta = 0.01          # 每步增量

while True:
    rate(100)

    # 更新棒子方向
    rod.axis = vector(L * np.cos(theta), L * np.sin(theta), 0)

    # 更新投影箭頭 (僅 x 分量)
    B_x = L * np.cos(theta)                # 末端 x 座標
    projection.axis = vector(B_x, 0, 0)

    # 更新軌跡
    trail.append(pos=rod.pos + rod.axis)

    # 更新標籤文字
    r_label.text = f"旋轉半徑 R = {mag(rod.axis):.4f}"
    projection_label.text = f"投影長度: {B_x:.4f}"

    # 角度遞增
    theta += dtheta
