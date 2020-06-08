"""
项目启动主程序
"""

import sys
import module_register
import wake_up

# 检查唤醒词
if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python xxx.py your.model")
    sys.exit(-1)
model = sys.argv[1]
module_register.startup()
wake_up.startup(model)
