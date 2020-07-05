"""
图片操作者
"""

import threading
import time

LOOP = False
STOP = True


def playPic(file):
    print("ss")


def playPics(pics, space=0.03, loop=False):
    print(pics)
    print(space)
    print(loop)
    global LOOP, STOP
    while LOOP:
        for pic in pics:
            print("显示图片")
            time.sleep(space)
            # 显示图片
        if loop:
            continue
        else:
            break
    STOP = True


def loopPlayPics(pics):
    global LOOP
    if LOOP:
        LOOP = False
        while STOP is False:
            continue
    LOOP = True
    thread = threading.Thread(target=playPics, args=(pics, 0.03, True))
    thread.start()


if __name__ == "__main__":
    loopPlayPics("lll")