"""
项目启动主程序

@author: funyoo

"""

import sys
import module_register
import wake_up
import signal

# 检查唤醒词
if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python xxx.py your.model")
    sys.exit(-1)


# 定义信号处理函数 参数：用来识别信号 进程栈状态
def signal_handle(signal, frame):
    wake_up.setInterrupt(True)
    wake_up.stop()
    while wake_up.STOP is False:
        continue
    sys.exit(-1)

# 中断信号
signal.signal(signal.SIGINT, signal_handle)

model = sys.argv[1]
module_register.startup()
wake_up.startup(model)
