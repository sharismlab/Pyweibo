# -*- coding: utf-8 -*-
#/usr/bin/env python

import sys, os, urllib, urllib2
import csv, io
import pickle
from api.weibo import APIClient # api from:http://michaelliao.github.com/sinaweibopy/
from api.http_helper import *
from api.retry import *
try:
    import json
    from ConfigParser import ConfigParser
except ImportError:
    import simplejson as json


# FILE= os.path.join(os.path.abspath(".") + os.sep +  'out')
# print(os.path.isdir(FILE))
# print FILE

# setting sys encoding to utf-8
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)



class weiboApi:

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

    def create_token(self):
        print "ok ok"
        self.apply_access_token()

        # 以下为访问微博api的应用逻辑
        # 以接口访问状态为例
        status = self.client.get.account__rate_limit_status()
        print json.dumps(status)

    def read_tokens(self):
        tokens  = [line.split() for line in open(self.access_token_file_path, 'r')]
        print tokens
        return tokens

    # Deal with limitations
    def remainHit(self):
        statu = self.client.account__rate_limit_status()
        return statu['remaining_user_hits']
    
    def resetTime(self):
        statu = self.client.account__rate_limit_status()
        return statu['reset_time_in_seconds']

    def toSleep(self):
        t = self.resetTime()
        t = t+1
        print('现在程序会睡眠'+str(t)+" 秒钟，直到下一个整点重新恢复运行")
        time.sleep(t)

    def stringTotime(self, strtime):#时间格式"2012-10-20 1:2:2"
        t_tuple = time.strptime(strtime,"%Y-%m-%d %H:%M:%S")
        return int(time.mktime(t_tuple))

    def toFile(self, JSONOBJ, fileName, path, format):

        filePath=path+os.sep+fileName
        if os.path.exists(filePath):
            print (fileName+" already exists. 文件已经存在，请指定其他文件夹")
            return
        else:
            if format == 'csv':
            # CSV
                w = csv.writer(open(filePath+os.sep+fileName, "w"))
                for key, val in JSONOBJ.items():
                    w.writerow([key, val])
            
            elif format == 'pickle':
            # Serialized
                pickle.dump(JSONOBJ, open(filePath+os.sep+fileName,'w'))

            elif format == "json":
            # JSON 
                f=open(filePath,'w')
                newData = json.dumps(JSONOBJ, sort_keys=True, indent=4)
                f.write(newData)
                f.close()
            else :
                print "Unknown format. 格式不存在" 

    # Allow several tokens from a tupple 
    def setToken(self,tokenTuple):

        self.client.set_access_token(tokenTuple[0],tokenTuple[1])

    def tokenLoop(self, maxPages):
        maxPages = maxPages
        tokenArray= self.read_tokens()

        for Token in tokenArray:
            setToken(Token)
            if self.remainHit()>0:
                print self.remainHit()
                while Max > 0:
                    if remainHit()>0:
                        JSONOBJ = result(maxPages)
                        maxPages = Max -1
                        self.toFile(JSONOBJ,str(maxPages))
                    else:
                        break

    # 
    def maxpage(self, perpage):
        firstpage = self.result(1)
        print firstpage
        total_number = firstpage['total_number']
        print total_number,' total_number'
        return (total_number/perpage) if (total_number%perpage==0) else (total_number/perpage+1)

    def mainLoop(self, path, format ):
        maxPages = 0
        tokenArray= self.read_tokens()

        # check if the directory exist before writing
        if os.path.isdir(path) == False:

            print(path+" doesn't exist. 文件不存在")
            yn= raw_input("Do you want to create it? (y/n)")
            if yn =="y":
                os.mkdir(path)
            else:
                print("Data can't be stored, please create a directory!")


        # Assign user
        token = tokenArray[0]
        self.setToken(token)
        
        # Count maximum pages to retrieve
        maxPages = self.maxpage(30) # 30 items per page
        print maxPages,"pages to retrieve"
        
        index = 0

        while index < len(tokenArray) and maxPages>0: 
            self.setToken(tokenArray[index])

            if self.remainHit()>0: # check rate limit
                while maxPages > 0: # check page number
                    if self.remainHit()>0:
                        JSONOBJ = self.result(maxPages)
                        type(JSONOBJ)
                        print maxPages
                        maxPages = maxPages-1
                        self.toFile(JSONOBJ,str(maxPages), path, format)
                    else:
                        if index==len(tokenArray)-1:
                            self.toSleep()
                            index=0
                        else:
                            index=index+1
                            break
            else:
                index = index+maxPages-1

    # API requests
    def result(self,page):
        #api request goes there
        re = self.client.comments__show(id="3537373410886268", page=page, count=30)
        return re

    # def place__nearby_timeline(lat, lon, start, end, page, count=30, rang=2000):
    #     # start = stringTotime(STARTTIME)
    #     # end = stringTotime(ENDTIME)
    #     re = api.place__nearby_timeline(lat=lat,long=lon,starttime=start,endtime=end,page=page,count=count,range=rang)
    #     return re