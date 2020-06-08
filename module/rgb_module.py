"""
控制树莓派rgb灯：
通过udp接收命令完成相应控制
"""

import socket
import threading
import time

from module.base_module import BaseModule
from module.rgb import rgb_operator

BUFFSIZE = 1024
COMMANDS = [".*[开,关].*[灯,彩虹,LED]"]
IP_PORT = ('127.0.0.1', 9001)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
START = False
COMMAND_ID = 0


class Rgb(BaseModule):

    def ip_port(self):
        global IP_PORT
        return IP_PORT

    def startup(self):
        global START, SERVER
        server.bind(IP_PORT)
        START = True
        workingThread = threading.Thread(target=self.working, args=())
        workingThread.start()
        print("rgb 服务已启动")

    def shutdown(self):
        global START, server
        START = False
        server.close()

    def commands(self):
        global COMMANDS
        return COMMANDS

    def working(self):
        global BUFFSIZE, START, COMMAND_ID
        while START:
            commandStr, client_addr = server.recvfrom(BUFFSIZE)
            commandStr = commandStr.decode("utf-8")
            print("收到来自 " + str(client_addr) + " 的指令: " + datastr + " ", time.time())
            # 取命令编号
            data = str(commandStr).split("-")
            id = int(data[1])
            if id <= COMMAND_ID:
                continue
            else:
                COMMAND_ID = id

            if "开" in data[0]:
                rgb_operator.operate(data[0])
                continue
            if "关" in data[0]:
                rgb_operator.close()
                continue
            if "command:" in data[0]:
                # 系统命令，非语音
                clock = data[0].replace("command:", "")
                rgb_operator.openRgbByRGB([255, 255, 255], clock)
            # 都不是TODO


if __name__ == "__main__":
    rgb = Rgb()
    rgb.startup()
    workingThread = threading.Thread(target=rgb.working, args=())
    workingThread.start()
    workingThread.join()
