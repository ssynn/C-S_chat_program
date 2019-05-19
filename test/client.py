import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1',4544))
# 建立连接:
s.connect(('127.0.0.1', 9999))
# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))
msg = ''

while True:
    msg = input()
    if msg == 'exit':
        break
    # 发送数据:
    msg = json.dumps(msg.split())
    s.send(msg.encode())
    print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()