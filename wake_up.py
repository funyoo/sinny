"""
唤醒程序：通过 snowboy 唤醒
"""
import sys

sys.path.append('./snowboy/examples/Python3/')
import snowboydecoder
import signal
import logging
import commander

interrupted = False
detector = object


def startup(model):
    global detector
    # 初始化探测器 参数：唤醒词文件 灵敏度
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
    print('Listening... Press Ctrl+C to exit')
    # main loop
    start()


def interrupt_callback():
    global interrupted
    return interrupted


def setInterrupt(value):
    global interrupted
    interrupted = bool(value)


# 被唤醒回调函数
def detected():
    global detector
    snowboydecoder.play_audio_file()
    print("Now! I was waken up!")
    logging.info("Now! I was waken up!")
    # 侦听命令
    stop()
    commander.command()
    print("重新开启唤醒功能00")
    start()


def start():
    global detector
    detector.start(detected_callback=detected,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)


def stop():
    global detector
    detector.terminate()

