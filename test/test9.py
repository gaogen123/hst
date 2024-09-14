#!/usr/bin/python3
# 文件名：client.py

# 导入 socket、sys 模块
import socket
import sys

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
host = '127.0.0.cust_indicator'

# 设置端口号
port = 11112

# 连接服务，指定主机和端口
s.connect((host, port))

# 接收小于 1024 字节的数据
msg = s.recv(1024)
while msg:
    print(msg.decode('utf-8'))
    msg = s.recv(1024)

s.close()
