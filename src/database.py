import sqlite3


# 登录
def login(user_message: dict) -> bool:
    '''
    传入以下格式的字典
    user_message{
        'ID': str,
        'PASSWORD': str
    }
    '''
    ans = None
    try:
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT ID
        FROM users
        WHERE ID=? AND PASSWORD=?
        ''', (
            user_message['ID'],
            user_message['PASSWORD']
        ))
        temp = cursor.fetchall()
        if len(temp) == 0:
            ans = {'answer': 'success'}
        else:
            ans = {'answer': 'fail'}
    except Exception as e:
        print('Login error!')
        print(e)
    finally:
        conn.close()
        return ans


# 注册
def signup(user_message: dict) -> dict:
    '''
    传入以下格式的字典
    user_message{
        'ID': str,
        'PASSWORD': str
    }
    '''
    message = dict()
    try:
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        # print(user_message)
        cursor.execute('''
            SELECT *
            FROM users
            WHERE ID = ?
            ''',[user_message['ID']]
        )
        if len(cursor.fetchall()) != 0:
            message['reason'] = '用户已存在！'
            message['answer'] = 'fail'
            raise Exception('用户已存在！')
        cursor.execute('''
        INSERT
        INTO users
        VALUES(?, ?)
        ''', [
            user_message['ID'],
            user_message['PASSWORD']
        ])
        conn.commit()
        message['answer'] = 'success'
    except Exception as e:
        print('Signup error!')
        print(e)
    finally:
        conn.close()
        return message


def makeFriend(user1: str, user2: str) -> bool:
    '''
    先检查两个人是否已经成为朋友，然后建立朋友行, 传入的两个用户不能为同一个人
    '''
    newFriends = [user1, user2]
    newFriends.sort()
    ans = None
    try:
        # 检查用户是否重复
        if user1 == user2:
            raise Exception('用户重复')

        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()

        # 先查找用户是否存在
        cursor.execute('''
        SELECT
        FROM users
        WHERE ID=? OR ID=?
        ''', newFriends)
        num = cursor.fetchall()
        if num != 2:
            raise Exception('存在无效用户！')

        # 建立新朋友行
        cursor.execute('''
            INSERT 
            INTO friends
            values(?,?)
            ''', newFriends)
        conn.commit()
        ans = {'answer': 'success'}
    except Exception as e:
        print('Make friends error!')
        print(e)
        ans = {'answer': 'fail', 'reason':str(e)}
    finally:
        conn.close()
        return ans


def get_all_users() -> list:
    users = []
    try:
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ID
            FROM users
        ''')
        users = cursor.fetchall()
        users = map(lambda x: x[0], users)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return users


if __name__ == "__main__":
    get_all_users()
    signup({
        'ID':'2',
        'PASSWORD':'1'
    })
    get_all_users()