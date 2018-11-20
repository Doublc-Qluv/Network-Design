import hashlib
import sys,os
# from PIL import Image, ImageFont, ImageDraw, ImageFilter
# import random




def store(user, secret, db):
    md5 = hashlib.md5()
    md5.update(secret.encode('utf-8'))
    result = md5.hexdigest()
    db[user] = result



def verify(db):
    while True:
        username = input('输入你的用户名\n')
        secret = input('输入你的密码:\n')
        md5 = hashlib.md5()
        md5.update(secret.encode('utf-8'))
        result = md5.hexdigest()
        if username not in db:
            print('用户名不存在')
        elif db[username] == result:
            print('验证通过，欢迎光临')
            break
        else:
            print('密码不正确,请重新输入')


def register(db):
    while True:
        username = input('输入你的用户名\n')
        if username in db.keys():
            print('用户名已存在，请重新输入')
            continue
        secret = input('输入你的密码:\n')
        dicta = {'number': 0, 'lower': 0, 'upper': 0, 'other': 0}
        for item in secret:
            if item.isdigit():
                dicta['number'] += 1
            elif item.islower():
                dicta['lower'] += 1
            elif item.isupper():
                dicta['upper'] += 1
            else:
                dicta['other'] += 1
        if dicta['lower'] < 1: # or dicta['upper'] < 1 or dicta['number'] < 1 or dicta['other'] < 1:
            print('密码必须有大、小写字母，数字，和特殊字符四部分组成,请重新输入')
        else:
            print('验证通过，欢迎光临')
            break
    return username, secret


if __name__ == '__main__':
    while True:
        database = {'sam': '67ae79674e56657bb652bd02f7251474'}
        receive = input('欢迎光临，输入您的身份,新用户（1），老客户（2）\n')
        if receive == '1':
            user, password = register(database)
            store(user, password, database)
            print(database)
        elif receive == '2':
            verify(database)