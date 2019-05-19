import socket
import threading
import time
import json


def tcplink(sock, addr, master):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(('Welcome! '+str(addr)).encode())
    
    while True:
        time.sleep(1)
        # 获取接受的消息，传给自己
        get_msg = master.get_msg(addr[1])
        print(str(addr[1])+" received:"+str(get_msg))
        sock.send(json.dumps(get_msg).encode())

        # 每次最多接受一个字节
        data = sock.recv(1024)
        
        if not data or data.decode('utf-8') == 'exit':
            break

        master.push_msg(data.decode(), addr[1])

    sock.close()
    print('Connection from %s:%s closed.' % addr)


class Server():
    def __init__(self):
        self._msg_queue = []
        self._max_user = 5

    def push_msg(self, msg: str):
        msg = json.loads(msg)
        try:
            msg[0] = int(msg[0])
            if msg[0]<1024 or msg[0] > 9999:
                raise Exception("Port Error")
            self._msg_queue.append(msg)
        except Exception as e:
            print(e)

    def handle(self):
        while True:
            time.sleep(1)
            print("Waitting:" + str(self._msg_queue))
    
    def get_msg(self, port: int) -> list:
        need = []
        for item in self._msg_queue:
            if item[0] == port:
                need.append(item)
        for item in need:
            if item in self._msg_queue:
                self._msg_queue.remove(item)
        return need

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.bind(("127.0.0.1", 9999))

        # 最大连接数量
        s.listen(5)

        print("Waiting for connection")

        # 每秒更新消息队列里的消息
        display = threading.Thread(target=self.handle)
        display.start()

        while True:
            # 接受一个新连接:
            sock, addr = s.accept()
            # 创建新线程来处理TCP连接:
            t = threading.Thread(target=tcplink, args=(sock, addr, self))
            t.start()

        




if __name__ == "__main__":
    server = Server()
    server.start()
