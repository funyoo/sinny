"""
commander 即指挥者，指令处理中心
负责处理和发送指令

@author: funyoo
"""
import socket
import wave
import reader
import pyaudio
import time
import re
import module_register

BUFFSIZE = 1024

# 命令发送客户端
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "command.wav"

# 命令列表
COMMANDS_LIST = module_register.commands_list
# 命令标号，避免一条命令被同一个服务多次执行
COMMAND_ID = 0


def command():
    global CLIENT, COMMAND_ID
    beforeRecord()
    # 录音
    record()
    # 解析
    msg = reader.readOnLine()
    print("解析到语音命令：" + msg + " ", time.time())
    COMMAND_ID += 1
    msg = msg + "-" + str(COMMAND_ID)
    # 选择成员下命令
    has = False
    for soldier in COMMANDS_LIST:
        if match(soldier[0], msg):
            has = True
            CLIENT.sendto(msg.encode("utf-8"), soldier[1])
    if has:
        CLIENT.sendto("command:hao-0".encode("utf-8"), ("127.0.0.1", 9003))
    else:
        CLIENT.sendto("command:err-0".encode("utf-8"), ("127.0.0.1", 9003))


def record():
    global CLIENT
    print("开始录音:", time.time())
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("录音已生成文件 ", time.time())


def close():
    global CLIENT
    CLIENT.close()


# 正则表达式匹配
def match(pattern, strs):
    pattern = re.compile(r'(' + pattern + ')')
    m = pattern.match(strs)
    return m


# 录音前
def beforeRecord():
    CLIENT.sendto("command:3-0".encode("utf-8"), ("127.0.0.1", 9001))
    #CLIENT.sendto("command:wake_up-0".encode("utf-8"), ("127.0.0.1", 9002))
    CLIENT.sendto("command:wozai-0".encode("utf-8"), ("127.0.0.1", 9003))


if __name__ == '__main__':
    module_register.startup()
    command()
