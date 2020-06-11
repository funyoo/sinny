"""
声音播放

@author funyoo
"""

import os
import pygame
import threading


# 播放音频
def play(file):
    # frequency用来控制速度
    # pygame.mixer.init(frequency=16000, size=0)
    #
    # pygame.mixer.music.load(file)
    # pygame.mixer.music.play()
    # while pygame.mixer.music.get_busy():
    #     continue
    # pygame.mixer.music.stop()
    os.system("omxplayer -o local " + file)


# 异步播放音频
def playOnThread(file):
    thread = threading.Thread(target=play, args=file)
    thread.start()