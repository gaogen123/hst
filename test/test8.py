import socket
import struct
import hst_pb2

# 服务器地址和端口
HOST = '127.0.0.cust_indicator'  # 替换为实际服务器地址
PORT = 11112  # 替换为实际端口号

# 创建socket对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到服务器
try:
    client_socket.connect((HOST, PORT))
    print("Connected to server.")
    szHeaderFlag='HS'
    msgType=3
    protoFmtType=0
    protoVer=0
    serialNo=0
    bodyLen=0
    bodySHA1=0
    compressAlgorithm=0
    reserved=b'\x00' * 8
    notifymsgtype = hst_pb2.NotifyMsgType()



    # 构建TCP通讯头，这里仅作为示例，具体字段需要根据协议实现
    header = struct.pack( szHeaderFlag, msgType, protoFmtType, protoVer, serialNo, bodyLen,
                         bodySHA1, compressAlgorithm, reserved)

    # 构建完整的报文
    msg_body = struct.pack('i 8s q 4s', msg_type, notify_id, notify_time, payload)
    message = header + msg_body

    # 发送报文到服务器
    client_socket.sendall(message)
    print("Message sent to server.")

    # 接收服务器响应
    response = client_socket.recv(1024)
    print("Received from server:", response.decode())

except Exception as e:
    print("An error occurred:", e)

finally:
    # 关闭连接
    client_socket.close()
    print("Connection closed.")