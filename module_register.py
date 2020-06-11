"""
服务注册中心
负责扫描 module 下的各服务，并通过反射启动服务

@author: funyoo
"""

import importlib
import os

# 服务文件列表
service_filenames = []
# 命令匹配列表   [[命令正则,(ip,port)]]
commands_list = []


def startup(dirPath="./module"):
    search_services("./module")
    load_services()


def search_services(dirPath):
    global service_filenames
    print("开始扫描服务    path:" + str(dirPath))
    if not os.path.isdir(dirPath):
        print("ERROR! 找不到" + str(dirPath) + "文件夹")
        return
    for filename in os.listdir(str(dirPath)):
        print(filename)
        if "module" not in filename:
            continue
        if os.path.isdir(dirPath + "/" + filename):
            continue
        if str(filename) in "base_module.py":
            continue
        print(filename)
        service_filenames.append(filename)


def load_services():
    global service_filenames, commands_list
    print("开始加载服务")
    for file in service_filenames:
        # 分解service
        print("加载 " + str(file) + " 中")
        # rgb_module.py -> rgb_module
        importName = file.replace(".py", "")
        m = importlib.import_module("module." + importName)
        # rgb_module -> Rgb
        class_name = importName.replace("_module", "").capitalize()
        klass = getattr(m, class_name)
        # 初始化服务类
        service = klass()
        # 获取命令信息
        commandsFunc = getattr(service, "commands")
        commands = commandsFunc()
        # 获取服务地址
        ipPortFunc = getattr(service, "ip_port")
        ip_port = ipPortFunc()
        # 登记命令和地址
        for command in commands:
            commands_list.append([command, ip_port])
        # 启动服务
        startupFunc = getattr(service, "startup")
        startupFunc()
        print("加载 " + class_name + " 成功")


if __name__ == "__main__":
    search_services("./module")
    load_services()
    print(commands_list)
