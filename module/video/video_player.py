"""
视频播放者 video_player
使用 omxlayer 播放视频

提供两种播放方式：循环播放 和  播放一次

@author: funyoo
"""

from omxplayer import OMXPlayer
from pathlib import Path
from time import sleep
from module.video import sys_video_list

PLAYING = False
HAVE_STOP = True
SLEEP_STEP = 0.5
NOW_PLAYING = sys_video_list.SLEEP_VIDEO


# 循环播放
def loopPlay(file, clock):
    global PLAYING, HAVE_STOP
    # 停止之前播放的视频
    PLAYING = False
    while HAVE_STOP is False:
        continue
    # 播放新视频
    PLAYING = True
    HAVE_STOP = False
    video_path = Path(file)
    clock = float(clock)
    contin = True
    while PLAYING:
        player = OMXPlayer(video_path)
        now_clock = 0
        while contin:
            sleep(SLEEP_STEP)
            now_clock += SLEEP_STEP
            if now_clock == clock:
                break
            if PLAYING is False:
                contin = False
    HAVE_STOP = True


# 播放一次
def playOnce(file, clock):
    global PLAYING, HAVE_STOP
    # 停止之前播放的视频
    PLAYING = False
    while HAVE_STOP is False:
        continue
    # 播放新视频
    PLAYING = True
    HAVE_STOP = False
    video_path = Path(file)
    clock = float(clock)
    contin = True
    player = OMXPlayer(video_path)
    now_clock = 0
    while contin:
        sleep(SLEEP_STEP)
        now_clock += SLEEP_STEP
        if now_clock == clock:
            PLAYING = False
            break
        if PLAYING is False:
            contin = False
    HAVE_STOP = True