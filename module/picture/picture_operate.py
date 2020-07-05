"""
图片控制者

@author: funyoo
"""


# 处理命令
def operate(command):
    if "command:" in command:
        # 系统命令
        sysCommand(command)
    else:
        # 用户命令
        userCommand(command)


# 系统命令处理
def sysCommand(command):
    sys_command = command.replace("command:", "")
    if sys_command == "sleep":
        # 显示睡眠图片组
        return
    if sys_command == "wozai":
        # 显示我在图片组
        return


# 用户命令处理
def userCommand(command):
    # TODO
    return