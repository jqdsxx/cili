"""
给实拍图四边生成渐变融合，使其自然过渡到Hero背景色 #fff8d6
策略：在原图四边叠加一个由外（Hero背景色）到内（透明）的渐变alpha层
"""
from PIL import Image, ImageDraw
import numpy as np

SRC = r"C:\Users\HP\WorkBuddy\cili\images\bottle-scene2.jpg"
DST = r"C:\Users\HP\WorkBuddy\cili\images\bottle-scene-blended.png"

# Hero背景中间色，接近实拍图边缘区域最浅的部分
HERO_BG = (255, 248, 214)  # #fff8d6

img = Image.open(SRC).convert("RGBA")
w, h = img.size
data = np.array(img, dtype=np.float32)

# 四边渐变深度（像素）
fade_top    = int(h * 0.22)
fade_bottom = int(h * 0.22)
fade_left   = int(w * 0.20)
fade_right  = int(w * 0.20)

# 构建alpha遮罩（1=保留原图，0=显示背景色）
mask = np.ones((h, w), dtype=np.float32)

# 上边
for y in range(fade_top):
    mask[y, :] = np.minimum(mask[y, :], y / fade_top)
# 下边
for y in range(fade_bottom):
    mask[h - 1 - y, :] = np.minimum(mask[h - 1 - y, :], y / fade_bottom)
# 左边
for x in range(fade_left):
    mask[:, x] = np.minimum(mask[:, x], x / fade_left)
# 右边
for x in range(fade_right):
    mask[:, w - 1 - x] = np.minimum(mask[:, w - 1 - x], x / fade_right)

# 用缓动曲线让过渡更自然（ease-in: x^2）
mask = mask ** 1.8

# 合成：原图 * mask + 背景色 * (1 - mask)
bg = np.array(HERO_BG + (255,), dtype=np.float32)
result = np.zeros_like(data)
for c in range(3):
    result[:, :, c] = data[:, :, c] * mask + bg[c] * (1 - mask)
result[:, :, 3] = 255  # 完全不透明，直接显示在页面

result = np.clip(result, 0, 255).astype(np.uint8)
out = Image.fromarray(result)
out.save(DST)
print(f"OK → {DST}  ({w}x{h})")
