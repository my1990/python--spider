'''
新浪登录js文件   http://login.sina.com.cn/js/sso/ssologin.js   加密算法在此文件中
用户名加密目前采用Base64加密算法   MTUyNTcxNTgyOTM=
新浪微博登录密码的加密算法没整出来。。。。
'''
import requests
import base64
import rsa
import binascii
import time
import re

def username_bs64(username):
    username_base = base64.b64encode(username.encode('utf-8')).decode()
    return username_base

def passwd_rsa(password,username):
    (pubkey,privkey) = rsa.newkeys(1024)  #生成256位长度的公私钥
    password1 = str(get_time()) + str(get_nonce(username)) + str(password)
    password_str = password1.encode('utf-8') #设置明文编码格式
    cryto1 = rsa.encrypt(password_str,pubkey) #公钥进行加密
    cryto = binascii.b2a_hex(cryto1).decode()  #将加密信息转换为16进制
    #print(cryto)
    return cryto

def get_nonce(username):
    url  = 'https://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su='
    url1 = url + str(username_bs64(username)) + 'rsakt=mod&client=ssologin.js(v1.4.15)&_=' + str(get_time())
    requests_session1 = requests.Session()
    t = requests_session1.get(url1).text
    nonce_re = re.compile(r'"nonce":"(.*?)"')
    nonce = nonce_re.findall(t)[0]
    return nonce

def get_time():
    now_time = time.time()
    now_time = round(now_time)
    return now_time

def login(username,passwd):
    login_url = 'http://login.sina.com.cn/sso/login.php'
    url = 'http://weibo.com/u/5359848915/home?wvr=5'
    headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
    post_data = {
        'entry': 'sso',
        'gateway': '1',
        'from': 'null',
        'savestate': '30',
        'useticket': '0',
        'pagerefer': 'http: // login.sina.com.cn / signup / signin.php?entry = sso',
        'vsnf': '1',
        'service': 'sso',
        'nonce': get_nonce(username),
        'pwencode': 'rsa2',
        'rsakv': '1330428213',
        'encoding': 'UTF - 8',
        'cdult': '3',
        'domain': 'sina.com.cn',
        'prelt': '586',
        'returntype': 'TEXT',
        'su':username_bs64(username),
        'sp':passwd_rsa(passwd,username),
        'servertime':get_time()
    }
    requests_session = requests.Session()
    login_url = login_url + '?client=ssologin.js(v1.4.15)&_=' + str(get_time()) + '123'
    req = requests_session.post(url=login_url,headers=headers,data=post_data)
    req.encoding = req.apparent_encoding
    print(req.json())


if __name__ == '__main__':
    login('15257158293','wo0.123')




