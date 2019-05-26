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
            ans = {'answer':'success'}
        else:
            ans = {'answer':'fail'}
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
        print(user_message)
        cursor.execute('''
            SELECT *
            FROM users
            WHERE ID = ?
            ''', 
            [user_message['ID']]
        )
        print(233)
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