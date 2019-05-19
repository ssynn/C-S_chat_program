# 设计

## 客户端
### 界面
1. 登录界面
2. 注册界面
3. 好友选择界面
4. 聊天界面

### 功能
1. 登录
2. 注册
3. 登出
4. 添加好友
5. 删除好友
6. 聊天


## 服务器
### 功能
1. 与客户端建立连接
2. 管理在线用户
   1. 剔除不在线的客户端
   2. 定时与客户端确认连接
3. 用户管理
   1. 建立新用户
   2. 登出
   3. 登录（扫描未发消息队列）
4. 聊天
   1. 缓存聊天信息
   2. 当目标用户在线则把信息发给目标，否则进入缓存数据库