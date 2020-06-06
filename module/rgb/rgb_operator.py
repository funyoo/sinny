"""
rgb灯光操作者
控制rgb灯光的开关

这里用两个标志FLAG和CONFIRM来避免产生大量线程造成的线程泄露
@author: funyoo
"""
from module.rgb import rgb_color
import time
from module.rgb.pixels import Pixels, pixels
from module.rgb.alexa_led_pattern import AlexaLedPattern
from module.rgb.google_home_led_pattern import GoogleHomeLedPattern
import _thread

pixels.pattern = GoogleHomeLedPattern(show=pixels.show)
FLAG = False  # 亮灯线程正在运行中？
CONFIRM = False  # 亮灯线程已退出


def operate(msg):
    if "渐变" in msg or "彩虹" in msg or "彩色" in msg:
        gradualChange()
        return
    if "打开" in msg:
        msg = msg.replace("打开", "")
    if "LED" in msg:
        msg = msg.replace("LED", "")
    if "灯" in msg:
        msg = msg.replace("灯", "")
    openRgbByName(msg)


# 通过RGB开灯    参数 [255, 255, 255]
def openRgbByRGB(RGB):
    global FLAG, CONFIRM
    if RGB is None or len(RGB) < 1:
        # 无法完成
        return
    if FLAG is True:
        FLAG = False
        while CONFIRM is not False:
            continue
    FLAG = True
    CONFIRM = False
    _thread.start_new_thread(openRgbByRGB(), (RGB,))


# 通过颜色名开灯
def openRgbByName(name):
    rgb = rgb_color.getRGBByName(name)
    openRgbByRGB(rgb)


# 关灯
def close():
    global FLAG
    FLAG = False
    pixels.off()


# 亮灯线程
def lightThead(RGB):
    global FLAG, CONFIRM
    while FLAG:
        try:
            data = RGB * 12
            pixels.show(data)
        except InterruptedError:
            break
    CONFIRM = True


# 渐变色特效
def gradualChange():
    global FLAG, CONFIRM
    r = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
         240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240]
    g = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240,
         255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
         255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
    b = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240,
         255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
         255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
         240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = 0  # 当前渐变下标
    direction = 0  # 方向：从小到大
    length = len(r)
    while FLAG:
        try:
            data = [r[index], g[index], b[index]] * 12
            pixels.show(data)
            time.sleep(0.05)
            # 上升方向
            if direction == 0:
                index += 1
                if index == length:
                    direction = 1
                    index -= 1
            else:
                index -= 1
                if index == -1:
                    direction = 0
                    index += 1
        except InterruptedError:
            break
    CONFIRM = True
