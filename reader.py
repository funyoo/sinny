from aip import AipSpeech

# 百度需要的参数
APP_ID = 'xxxxxx'
API_KEY = 'xxxxxxxxx'
SECRET_KEY = 'xxxxxxxxxxxxxxxxxxx'


def read():
    # 语音转成文字的内容
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    ret = client.asr(get_data("command.wav"), 'wav', 16000, {'dev_pid': 1537}, )
    print(ret)
    input_message = ret['result']
    print(input_message)
    return input_message


def get_data(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


if __name__ == '__main__':
    read()
