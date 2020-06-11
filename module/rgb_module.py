"""
控制树莓派rgb灯：
通过udp接收命令完成相应控制

@author: funyoo
"""

import socket
import threading
import time

from module.base_module import BaseModule
from module.rgb import rgb_operator

BUFFSIZE = 1024
COMMANDS = [".*[开,关].*[灯,彩虹,LED]", "command:.*"]
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
        SERVER.bind(IP_PORT)
        START = True
        working_thread = threading.Thread(target=self.working, args=())
        working_thread.start()
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
            command_str, client_addr = SERVER.recvfrom(BUFFSIZE)
            command_str = command_str.decode("utf-8")
            print("收到来自 " + str(client_addr) + " 的指令: " + command_str + " ", time.time())

            # 取命令编号
            data = str(command_str).split("-")
            id = int(data[1])
            if 0 < id <= COMMAND_ID:
                continue
            if COMMAND_ID is not 0:
                COMMAND_ID = id

            rgb_operator.operate(data[0])


if __name__ == "__main__":
    rgb = Rgb()
    rgb.startup()
    workingThread = threading.Thread(target=rgb.working, args=())
    workingThread.start()
    workingThread.join()
