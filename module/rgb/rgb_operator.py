"""
rgb操作者
过滤命令，再委托给 rgb_worker执行

@author: funyoo
"""
from module.rgb import rgb_worker
import threading


# 操作入口
def operate(msg):
    if "command:" in msg:
        sysCommand(msg)
    else:
        userCommand(msg)


# 用户命令
def userCommand(msg):
    if "开" in msg:
        # 彩虹渐变灯命令
        if "渐变" in msg or "彩虹" in msg or "彩色" in msg:
            print("正在开启彩虹。。。")
            thread = threading.Thread(target=rgb_worker.gradualChange, args=())
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
            rgb_worker.openRgbByName(msg)
    if "关" in msg:
        rgb_worker.close()


# 系统命令
def sysCommand(command):
    clock = command.replace("command:", "")
    rgb_worker.openRgbByRGB([255, 255, 255], clock)



