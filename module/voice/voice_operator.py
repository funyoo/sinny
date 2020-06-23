"""
音频操作者

负责处理音频命令 交由 voice_player 播放
"""

from module.voice import voice_player
from module.voice import sys_voice_list


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
    if sys_command == "wozai":
        voice_player.play(sys_voice_list.WO_ZAI)
    if sys_command == "hao":
        voice_player.play(sys_voice_list.HAO)
    if sys_command == "err":
        voice_player.play(sys_voice_list.ERR)


# 用户命令处理
def userCommand(command):
    # TODO more and more
    return