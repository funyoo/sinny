"""
rgb灯光操作者
控制rgb灯光的开关

这里用两个标志FLAG和CONFIRM来避免产生大量线程造成的线程泄露
@author: funyoo
"""
from module.rgb_module import rgb_color
import time
from module.rgb_module.pixels import Pixels, pixels
from module.rgb_module.alexa_led_pattern import AlexaLedPattern
from module.rgb_module.google_home_led_pattern import GoogleHomeLedPattern
import threading

pixels.pattern = GoogleHomeLedPattern(show=pixels.show)
FLAG = False  # 亮灯线程正在运行中？
THREAD_EXIT = True  # 亮灯线程已退出


def operate(msg):
    # 彩虹渐变灯命令
    if "渐变" in msg or "彩虹" in msg or "彩色" in msg:
        print("正在开启彩虹。。。")
        thread = threading.Thread(target=gradualChange, args=())
        thread.start()
    else:
        if "打" in msg:
            msg = msg.replace("打", "")
        if "开" in msg:
            msg = msg.replace("开", "")
        if "LED" in msg:
            msg = msg.replace("LED", "")
        if "灯" in msg:
            msg = msg.replace("灯", "")
        msg = msg.replace(".", "")
        msg = msg.replace("。", "")
        msg = msg.replace(" ", "")
        print("过滤结果：" + msg)
        openRgbByName(msg)


# 通过RGB开灯    参数 [255, 255, 255]
def openRgbByRGB(RGB, clock=-1):
    global FLAG, THREAD_EXIT
    if RGB is None or len(RGB) < 1:
        # 无法完成
        return
    close()
    FLAG = True
    THREAD_EXIT = False
    thread = threading.Thread(target=lightThead, args=(RGB, clock))
    thread.start()


# 通过颜色名开灯
def openRgbByName(name, clock=-1):
    print("根据 " + name + "开灯")
    rgb = rgb_color.getRGBByName(name)
    print("取得RGB " + str(rgb))
    openRgbByRGB(rgb, clock)


# 关灯
def close():
    global FLAG, THREAD_EXIT
    # 关闭灯光线程
    if FLAG is True:
        FLAG = False
        while THREAD_EXIT is False:
            continue
    pixels.off()


# 亮灯线程
def lightThead(RGB, clock=-1):
    global FLAG, THREAD_EXIT
    while FLAG:
        try:
            data = RGB * 12
            pixels.show(data)
            if clock > 0:
                time.sleep(clock)
                FLAG = False
        except InterruptedError:
            break
    THREAD_EXIT = True


# 渐变色特效
def gradualChange():
    global FLAG, THREAD_EXIT
    close()
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
    FLAG = True
    THREAD_EXIT = False
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
    THREAD_EXIT = True
