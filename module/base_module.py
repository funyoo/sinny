"""
为所有module提供基类

所有功能模块都要实现以下方法：
ip_port：获取功能模块地址
startup: 开启服务
shutdown：关闭
commands: 服务识别关键信息
"""

import abc


class BaseModule(object):

    @abc.abstractmethod
    def ip_port(self):
        pass

    @abc.abstractmethod
    def startup(self):
        pass

    @abc.abstractmethod
    def shutdown(self):
        pass

    @abc.abstractmethod
    def commands(self):
        pass
