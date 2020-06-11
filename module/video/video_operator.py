"""
video 命令操作者
处理系统命令和用户命令，下达给video_player执行播放

@author: funyoo
"""

from module.video import sys_video_list
from module.video import video_player
import threading

# 命令编号 用于两种唤醒视频交替播放
COMMAND_ID = 0


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
    # 睡眠模式
    if sys_command == "sleep":
        video = sys_video_list.SLEEP_VIDEO
        thread = threading.Thread(target=video_player.loopPlay, args=(video[0], video[1]))
        thread.start()
    # 唤醒模式
    if sys_command == "wake_up":
        # 两种唤醒模式交替执行
        if COMMAND_ID % 2 == 0:
            video = sys_video_list.WAKE_UP_VIDEO
            thread = threading.Thread(target=video_player.playOnce, args=(video[0], video[1]))
            thread.start()
        else:
            video = sys_video_list.WAKE_UP_VIDEO_2
            thread = threading.Thread(target=video_player.playOnce, args=(video[0], video[1]))
            thread.start()
    # 忙碌模式
    if sys_command == "busy":
        video = sys_video_list.BUSY_VIDEO
        thread = threading.Thread(target=video_player.playOnce, args=(video[0], video[1]))
        thread.start()


# 用户命令处理
def userCommand(command):
    if "停止" in command:
        video = sys_video_list.SLEEP_VIDEO
        thread = threading.Thread(target=video_player.loopPlay, args=(video[0], video[1]))
        thread.start()
    # TODO more and more
