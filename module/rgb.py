"""
控制树莓派rgb灯：
通过udp接收命令完成相应控制
"""

import socket
import _thread

from module.base_module import BaseModule
from module.rgb import rgb_operator

BUFFSIZE = 1024
COMMANDS = ["灯", "LED"]
ip_port = ('127.0.0.1', 9001)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
START = False


class Rgb(BaseModule):

    def ip_port(self):
        global ip_port
        return ip_port

    def startup(self):
        global START, server
        server.bind(ip_port)
        START = True
        _thread.start_new_thread(working, ())

    def shutdown(self):
        global START, server
        START = False
        server.close()

    def commands(self):
        global COMMANDS
        return COMMANDS


def working():
    global BUFFSIZE, START
    while START:
        data, client_addr = server.recvfrom(BUFFSIZE)
        datastr = data.decode("utf-8")
        if "开" in datastr:
            rgb_operator.operate(datastr)
            continue
        if "关" in datastr:
            rgb_operator.close()
            continue
        # 都不是TODO