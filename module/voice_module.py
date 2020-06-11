"""
控制树莓派rgb灯：
通过udp接收命令完成相应控制

@author: funyoo
"""

import socket
import threading
import time

from module.base_module import BaseModule
from module.voice import voice_operator

BUFFSIZE = 1024
COMMANDS = ["command:.*", ".*播放音.*"]
ip_port = ('127.0.0.1', 9003)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
START = False
COMMAND_ID = 0


class Voice(BaseModule):

    def ip_port(self):
        global ip_port
        return ip_port

    def startup(self):
        global START, server
        server.bind(ip_port)
        START = True
        working_thread = threading.Thread(target=self.working, args=())
        working_thread.start()
        print("voice 服务已启动")

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
            command, client_addr = server.recvfrom(BUFFSIZE)
            command_str = command.decode("utf-8")
            print("收到来自 " + str(client_addr) + " 的指令: " + command_str + " ", time.time())

            # 取命令编号 记录并判断 防止重复执行同一命令 系统命令编号 0
            data = str(command_str).split("-")
            id = int(data[1])
            if COMMAND_ID >= id > 0:
                continue
            if id is not 0:
                COMMAND_ID = id

            voice_operator.operate(data[0])

