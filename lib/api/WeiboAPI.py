# -*- coding: utf-8 -*-
#/usr/bin/env python

from weibo import APIClient
# api from:http://michaelliao.github.com/sinaweibopy/

import sys, os, urllib, urllib2
from http_helper import *
from retry import *
try:
    import json
    from ConfigParser import ConfigParser
except ImportError:
    import simplejson as json

# setting sys encoding to utf-8
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class WeiboAPI:

    def __init__(self):
        print "Init Pyweibo API"

        #config stuff
        config = ConfigParser()
        config.read( os.path.join(os.path.abspath(".") + os.sep +  'settings.py') )

        # weibo api访问配置
        self.APP_KEY = config.get('api', 'key')
        self.APP_SECRET = config.get('api', 'secret')
        self.CALLBACK_URL = config.get('api', 'callback')

        #user info
        self.USERID = config.get('login', 'username')       # 微博用户名                     
        self.USERPASSWD = config.get('login', 'password')   # 用户密码

        # token file path
        save_access_token_file  = 'access_token.txt'
        file_path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep
        self.access_token_file_path = file_path + save_access_token_file

        # print access_token_file_path
        self.client = APIClient(app_key=self.APP_KEY, app_secret=self.APP_SECRET, redirect_uri=self.CALLBACK_URL)

    def make_access_token(self):
        '''请求access token'''
        params = urllib.urlencode({'action':'submit','withOfficalFlag':'0','ticket':'','isLoginSina':'', \
            'response_type':'code', \
            'regCallback':'', \
            'redirect_uri':self.CALLBACK_URL, \
            'client_id':self.APP_KEY, \
            'state':'', \
            'from':'', \
            'userId':self.USERID, \
            'passwd':self.USERPASSWD, \
            })

        login_url = 'https://api.weibo.com/oauth2/authorize'

        url = self.client.get_authorize_url()
        content = urllib2.urlopen(url)
        if content:
            headers = { 'Referer' : url }
            request = urllib2.Request(login_url, params, headers)
            opener = get_opener(False)
            urllib2.install_opener(opener)
            try:
                f = opener.open(request)
                print f.headers.headers
                return_callback_url = f.geturl
                print f.read()
            except urllib2.HTTPError, e:
                return_callback_url = e.geturl()
            # 取到返回的code
            code = return_callback_url.split('=')[1]
        #得到token
        token = self.client.request_access_token(code)
        self.save_access_token(token)

    def save_access_token(self,token):
        '''将access token保存到本地'''
        f = open(self.access_token_file_path, 'w')
        f.write(token['access_token']+' ' + str(token['expires_in']))
        f.close()

    @retry(1)
    def apply_access_token(self):
        '''从本地读取及设置access token'''
        try:
            token = open(access_token_file_path, 'r').read().split()
            if len(token) != 2:
                self.make_access_token()
                return False
            # 过期验证
            access_token, expires_in = token
            try:
                self.client.set_access_token(access_token, expires_in)
            except StandardError, e:
                if hasattr(e, 'error'): 
                    if e.error == 'expired_token':
                        # token过期重新生成
                        self.make_access_token()
                else:
                    pass
        except:
            self.make_access_token()
        
        return False

    def token(self):
        print "ok ok"
        self.apply_access_token()

        # 以下为访问微博api的应用逻辑
        # 以接口访问状态为例
        status = self.client.get.account__rate_limit_status()
        print json.dumps(status)