"""
reader: 读取者
提供语音识别的方法

readOffLine: 离线识别
readOnLine: 在线识别

@author: funyoo
"""

from aip import AipSpeech
import speech_recognition as sr

# 百度需要的参数
APP_ID = '20193397'
API_KEY = 'fzk019sk1FeSVgpfvz6j7C8k'
SECRET_KEY = 'UW8Hh0WzdVb6TdAG20LIPkGdlhZVPSm4'

CLIENT = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 离线识别
def readOffLine():
    r = sr.Recognizer()    #调用识别器
    test = sr.AudioFile("command.wav")   #导入语音文件
    with test as source:
        audio = r.record(source)
        type(audio)
        c = r.recognize_sphinx(audio, language='zh-cn')     #识别输出
        return c


# 在线识别
def readOnLine():
    # 语音转成文字的内容
    global CLIENT
    ret = CLIENT.asr(get_data("command.wav"), 'wav', 16000, {'dev_pid': 1537}, )
    print(ret)
    input_message = ret['result']
    return input_message[0]


def get_data(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


if __name__ == '__main__':
    readOnLine()
