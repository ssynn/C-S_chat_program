import socket
import threading
import time
import json
import time
from src import database


class Server():
    def __init__(self):
        self._msg_buffer = dict()
        self._max_user = 5
        self._socket_pool = dict()
        self._id_to_socket = dict()
        self._socket_to_id = dict()
        self.isAlive = True
        self.isChanged = False

    # 把收到的消息放入消息缓冲池
    def push_msg(self, msg: dict, head: tuple):
        '''
        head (userID1, userID2)
        '''
        if head not in self._msg_buffer:
            self._msg_buffer[head] = [msg]
        else:
            self._msg_buffer[head].append(msg)

    # FIXME 主进程处理消息池的方法
    def handle(self):
        '''
        0.1s 检查一次缓冲池，把消息发送给对应的客户端
        '''
        while True and self.isAlive:
            time.sleep(1)
            
            # print("Online: " + str(self._socket_pool.keys()))
            for head in self._msg_buffer:
                # 如果目标消息在socket池则把消息发送到对应的socket地址
                targetSocket = self.idToSocket(head[1])
                if targetSocket in self._socket_pool and self._msg_buffer[head]!=[]:
                    try:
                        msg = {
                            'operation':'msg',
                            'source':head[0],
                            'message':self._msg_buffer[head]
                        }
                        self._socket_pool[targetSocket].send(json.dumps(msg).encode())
                        self._msg_buffer[head] = []
                    except Exception as e:
                        print(str(time.strftime('%Y-%m-%d %H:%M:%S'))+' 发送失败')
            
            # 在线用户发生改变，需要通知客户端好友列表发生改变
            if self.isChanged:


                self.isChanged = False

    # 获取发到目标套接字的消息
    def get_info(self) -> dict:
        '''
        获取在线的用户，离线的用户，缓冲池
        ans = {
            'buffer':list,
            'online':list,
            'offline':list
        }
        '''
        ans = {
            'buffer':self._msg_buffer,
            'online':None,
            'offline':None
        }
        users_all = database.get_all_users()
        
        # 生成在线用户表
        onlineUsers = []
        for sock in self._socket_pool:
            onlineUsers.append(self.socketToId(sock))
        
        # 生成离线用户表
        offlineUsers = []
        for user in users_all:
            if user not in onlineUsers:
                offlineUsers.append(user)
        
        ans['online'] = onlineUsers
        ans['offline'] = offlineUsers

        return ans

    def socketToId(self, socket) -> str:
        '''
        把socket转换为用户ID
        '''
        return self._socket_to_id[socket]

    def idToSocket(self, _id):
        return self._id_to_socket[_id]

    def isOnline(self, userId):
        '''
        检查用户是否在线
        '''
        return userId in self._id_to_socket

    # 启动服务器
    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.s.bind(("127.0.0.1", 9999))

        # 最大连接数量
        self.s.listen(5)

        print("Waiting for connection")

        # 接受TCP连接请求
        recv = threading.Thread(target=waiting_for_connect, args=(self.s, self))
        recv.start()

        # 每秒更新消息队列里的消息
        display = threading.Thread(target=self.handle)
        display.start()

    def close(self):
        self.s.close()
        self.isAlive = False



def tcplink(sock, addr, master: Server):
    '''
    与客户端建立连接
    获取用户名
    socket变量记录用户名
    记录tcp连接
    '''
    print('Accept new connection from %s:%s...' % addr)

    mySocket = addr[0]+':'+str(addr[1])
    master._socket_pool[mySocket] = sock
    userID = None
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
                userID = data['ID']
                ans = database.login(data)
                ans['operation'] = 'ans'
                sock.send(json.dumps(ans).encode())
                master._socket_to_id[mySocket] = userID
                master._id_to_socket[userID] = mySocket
            
            # 注册操作
            if data['operation'] == 'signup':
                message = database.signup(data)
                # print(message)
                sock.send(json.dumps(message).encode())
                break

            # 查找朋友操作
            if data['operation'] == 'getFriends':
                friends = database.get_my_friends(userID)
                state = []
                for user in friends:
                    state.append(int(master.isOnline(user)))

                ans = {
                    'operation':'getFriends',
                    'friends':friends,
                    'state':state
                }
                print(ans)
                sock.send(json.dumps(ans).encode())

    except Exception as e:
        print(e)
        print(data)
    finally:
        sock.close()
        master._socket_pool.pop(f"{addr[0]}:{addr[1]}")
        if userID in master._id_to_socket:
            master._id_to_socket.pop(userID)
        if mySocket in master._socket_to_id:
            master._socket_to_id.pop(mySocket)
        master.isChanged = True
        print('Connection from %s:%s closed.' % addr)


def waiting_for_connect(s, master: Server):
    while True:
        # 接受一个新连接:
        sock, addr = s.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=tcplink, args=(sock, addr, master))
        t.start()
        master.isChanged = True


if __name__ == "__main__":
    server = Server()
    server.start()
