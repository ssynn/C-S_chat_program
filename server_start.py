import sys
import os
import sqlite3
from PyQt5.QtWidgets import QApplication
from src import server

if __name__ == '__main__':
    # 如若没有数据库目录则建立一个数据库目录
    if 'data' not in os.listdir('./'):
        os.mkdir('data')

    # 检查数据库
    conn = sqlite3.connect('data/data.db')
    cursor = conn.cursor()
    tables = cursor.execute("select name from sqlite_master where type='table'").fetchall()

    # 如果是第一次使用则初始化数据库,新建用户表
    if not ('users',) in tables:
        cursor.execute('''create table users (
                ID text primary key,
                PASSWORD text
                )''')
    cursor.close()
    conn.commit()
    conn.close()

    sv = server.Server()
    sv.start()