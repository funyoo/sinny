# 通过speaker发送命令至各功能
import socket
import wave
import reader
import pyaudio
import logging

BUFFSIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "command.wav"


def command():
    global client
    # 录音
    record()
    # 解析
    msg = reader.read()[0]
    # TODO 回复指示
    # TODO 选择成员下命令
    ip_port = ('127.0.0.1', 9001)
    client.sendto(msg.encode('utf-8'), ip_port)


def record():
    logging.info("开始录音:")
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
    logging.info("录音结束")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def close():
    client.close()


if __name__ == '__main__':
    command()
