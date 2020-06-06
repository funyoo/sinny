# 引入snowboy资源
import sys
sys.path.append('./snowboy/examples/Python3/')
import snowboydecoder
import signal
import logging

interrupted = False

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python xxx.py your.model")
    sys.exit(-1)

model = sys.argv[1]
# 初始化探测器 参数：唤醒词文件 灵敏度
detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

# 定义信号处理函数 参数：用来识别信号 进程栈状态
def signal_handle(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

# 被唤醒回调函数
def detected():
    global detector
    logging.info("Now! I was waken up!");
    # TODO 侦听命令

def start():
    global detector
    detector.start(detected_callback=detected,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

# 中断信号
signal.signal(signal.SIGINT, signal_handle)

print('Listening... Press Ctrl+C to exit')

# main loop
start();

detector.terminate()