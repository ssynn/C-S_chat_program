import socket
import threading
import time
import json
import time
from src import database


def tcplink(sock, addr, master):
    print('Accept new connection from %s:%s...' % addr)

    mySocket = addr[0]+':'+str(addr[1])
    master._socket_pool[mySocket] = sock
    try:
        while True:
            # 每次最多接受一个字节,数据格式为json
            data = sock.recv(1024).decode()
            if data == 'exit':
                break
            data = json.loads(data)

            # 发送信息操作
            if data['operation'] == 'msg':
                # 把收到的数据放入缓冲池
                master.push_msg(data, (data['source'], data['target']))
            
            # 登录操作
            if data['operation'] == 'login':
                ans = database.login(data)
                sock.send(json.dumps(ans).encode())
                break
            
            # 注册操作
            if data['operation'] == 'signup':
                message = database.signup(data)
                print(message)
                sock.send(json.dumps(message).encode())
                break
        # 断开连接
        sock.close()
        master._socket_pool.pop(f"{addr[0]}:{addr[1]}")
    except Exception as e:
        # 连接意外终止
        master._socket_pool.pop(f"{addr[0]}:{addr[1]}")
    finally:
        print('Connection from %s:%s closed.' % addr)
    

    


class Server():
    def __init__(self):
        self._msg_queue = dict()
        self._max_user = 5
        self._socket_pool = dict()

    # 把收到的消息放入消息缓冲池
    def push_msg(self, msg: dict, head: tuple):
        if head not in self._msg_queue:
            self._msg_queue[head] = [msg]
        else:
            self._msg_queue[head].append(msg)

    # 主进程处理消息池的方法
    def handle(self):
        '''
        0.1s 检查一次缓冲池，把消息发送给对应的客户端
        '''
        while True:
            time.sleep(1)
            
            print("Online: " + str(self._socket_pool.keys()))
            for head in self._msg_queue:
                if head[1] in self._socket_pool and self._msg_queue[head]!=[]:
                    try:
                        self._socket_pool[head[1]].send(json.dumps(self._msg_queue[head]).encode())
                        self._msg_queue[head] = []
                    except Exception as e:
                        print(str(time.strftime('%Y-%m-%d %H:%M:%S'))+' 发送失败')

    # 获取发到目标套接字的消息
    def get_msg(self, port: int) -> list:
        need = []
        for item in self._msg_queue:
            if item[0] == port:
                need.append(item)
        for item in need:
            if item in self._msg_queue:
                self._msg_queue.remove(item)
        return need

    # 启动服务器
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
