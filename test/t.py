def checkSocket(num: str) -> bool:
    try:
        num = num.split(':')
        ip = num[0]
        port = int(num[1])
        if port < 1024 or port > 65535:
            return False
        ip = ip.split('.')
        ip = list(map(int, ip))
        if len(ip) != 4:
            return False
        for i in ip:
            if i<0 or i>255:
                return False
        return True
    except Exception as e:
        print('套接字格式错误')
        return False

a = {1:3,3:5}

