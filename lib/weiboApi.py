# -*- coding: utf-8 -*-
#/usr/bin/env python

import sys, os, urllib, urllib2
import csv, io
import fileinput
import getpass
import pickle
import datetime
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



# class WeiboUser:

#     def __init__(self, tupleToken):
#         self.username = tupleToken[0]
#         self.token= tupleToken[1]
#         self.secret= tupleToken[2]
#         self.alarm = 0  #time to wake up
#         self.sleeping = False

#     def getToken(self):
#         return [self.token, self.secret]

#     def getSleeping(self):
#         return self.sleeping

#     def getRemaining(self):
#         diff= alarm - datetime.datetime.now()
#         diff = int( round( diff.total_seconds() ) ) 
#         return diff
#         # return self.remains

#     def toSleep(self, t):

#         print('现在 '+self.username+' 会睡眠'+str(t)+" 秒钟，直到下一个整点重新恢复运行")
#         t = t+1

#         self.alarm = datetime.datetime.now()+ datetime.timedelta(0,t)
#         self.sleeping = True


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
        file_path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "api" + os.path.sep
        self.access_token_file_path = file_path + save_access_token_file

        # print access_token_file_path
        self.client = APIClient(app_key=self.APP_KEY, app_secret=self.APP_SECRET, redirect_uri=self.CALLBACK_URL)

    def make_access_token(self,username, password):
        '''请求access token'''

        params = urllib.urlencode({'action':'submit','withOfficalFlag':'0','ticket':'','isLoginSina':'', \
            'response_type':'code', \
            'regCallback':'', \
            'redirect_uri':self.CALLBACK_URL, \
            'client_id':self.APP_KEY, \
            'state':'', \
            'from':'', \
            'userId':username, \
            'passwd':password, \
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
        self.save_access_token(username,token)

    def save_access_token(self,username,token):
        '''将access token保存到本地'''

        exists = False
        done = False
        # f = open(self.access_token_file_path, 'r+')
        # for line in f:

        for line in fileinput.input(self.access_token_file_path, inplace=1):
            if username in line:
                exists = True
                print( username+' '+token['access_token']+' ' + str(token['expires_in']) )
            else:
                continue
        # done =True

        # print exists
        # print done
        
        # if exists == False:
        #     with open(self.access_token_file_path, 'a') as f:
        #         f.write(username+' '+token['access_token']+' ' + str(token['expires_in']))
        #         f.close()

    @retry(1)
    def apply_access_token(self,username, password):
        '''从本地读取及设置access token'''
        try:
            #loop to each line
            for line in open(access_token_file_path, 'r').readlines():
                #check if the username has already been added
                if username in line:
                    token =line.split()
                    
                    if len(token) != 3: #if size problem, make new one
                        self.make_access_token(username, password)
                        return False
                    
                    # 过期验证
                    usname, access_token, expires_in = token
                    try:
                        self.client.set_access_token(access_token, expires_in)
                    except StandardError, e:
                        if hasattr(e, 'error'): 
                            if e.error == 'expired_token':
                                # token过期重新生成
                                self.make_access_token(username, password)
                        else:
                            pass
                else:
                    pass
        except:
            self.make_access_token(username, password)
        
        return False

    def create_token(self):

        print('Please input Sina Weibo credentials:')
        username = raw_input("Username (email) :")
        password = getpass.getpass("Password :")
        # print (username, password)

        self.apply_access_token(username, password)

        print "You're token is stored in "+self.access_token_file_path

        # 以下为访问微博api的应用逻辑
        # 以接口访问状态为例
        # token =
        # setToken(token)
        # status = self.client.get.account__rate_limit_status()
        # print json.dumps(status)

    def read_tokens(self):
        tokens  = [ tuple(line.split()) for line in open(self.access_token_file_path, 'r')]
        # tokens  = tuple(x) for x in tokens
        print tokens
        return tokens

    # Deal with limitations
    def remainHit(self):
        statu = self.client.account__rate_limit_status()
        # print statu
        # return 0
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

        filePath=path+os.sep+fileName+"."+format
        if os.path.exists(filePath):
            print (fileName+" already exists. 文件已经存在，请指定其他文件夹")
            return
        else:
            if format == 'csv':
            # CSV
                w = csv.writer(open(filePath, "w"))
                for key, val in JSONOBJ.items():
                    w.writerow([key, val])
            
            elif format == 'pickle':
            # Serialized
                pickle.dump(JSONOBJ, open(filePath,'w'))

            elif format == "json":
            # JSON 
                f=open(filePath,'w')
                newData = json.dumps(JSONOBJ, sort_keys=True, indent=4)
                f.write(newData)
                f.close()
            else :
                print "Unknown format. 格式不存在" 

    # Use several users to get more data 
    # def setUser(self, weiboUser):
    #     token = weiboUser.getToken()
    #     self.client.set_access_token(token[0], token[1] )

    #     return weiboUser

    def setToken(self,tokenTuple):

        self.client.set_access_token(tokenTuple[1],tokenTuple[2])

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
    def maxpage(self, command, uid, perpage):
        firstpage = self.result(command,uid,1)
        print firstpage
        total_number = firstpage['total_number']
        print total_number,' total_number'
        return (total_number/perpage) if (total_number%perpage==0) else (total_number/perpage+1)

    def mainLoop(self, command, uid, path, format ):
        maxPages = 0


        # check if the directory exist before writing
        if os.path.isdir(path) == False:

            print(path+" doesn't exist. 文件不存在")
            yn= raw_input("Do you want to create it? (y/n)")
            if yn =="y":
                os.mkdir(path)
            else:
                print("Data can't be stored, please create a directory!")

        # Import all tokens
        tokenArray= self.read_tokens()

        # weiboUsers = []
        # Create and assign users
        # for token in tokenArray:
            # weiboUsers.append(WeiboUser(token))
        
        # print weiboUsers

        # Set first user to start
        # currentUser = self.setUser(weiboUsers[0])

        # tmp set token 
        self.setToken(tokenArray[0])
        
        # get basic data about the post
        print("retrieve post info from API")
        self.getPost(uid, path, format)

        # Count maximum pages to retrieve
        maxPages = self.maxpage(command,uid, 50)# 50 items per page
        print maxPages,"pages to retrieve"
        
        index = 0

        while index < len(tokenArray) and maxPages>0: 
            
            self.setToken(tokenArray[index])
            print "New user coming!"


            if self.remainHit()>0: # check rate limit

                while maxPages > 0: # check page number

                    if self.remainHit()>0:

                        JSONOBJ = self.result(command,uid,maxPages)
                        # type(JSONOBJ)
                        print "page "+str(maxPages)+" extracted to "+command+"_"+str(maxPages)
                        maxPages = maxPages-1
                        self.toFile(JSONOBJ,command+"_"+str(maxPages), path, format)

                    else:
                        
                        if index==len(tokenArray)-1:
                            toSleep()
                            index=0
                        else:
                            index=index+1
                            break

                        # print  "len(weiboUsers)"
                        # if index==len(weiboUsers)-1:

                        #     # Put your worker in bed
                        #     currentUser.toSleep(resetTime())
                            
                        #     # Get sleepy worker index 
                        #     nextUser = weiboUsers.index(currentUser)+1

                        #     # Check if you have used all workers already
                        #     if  len(weiboUsers) >= nextUser:
                                
                        #         if weiboUsers.getSleeping == False:
                        #             currentUser = setUser(weiboUsers[nextUser])

                        #     else:

                        #         # Check if some other workers are awake already
                        #         for user in weiboUsers:
                        #             alarms = []
                                    
                        #             if(user.getSleeping== False):
                        #                 currentUser = setUser(user) # Awake! Get to work
                        #             else:

                        #                 alarms.append(user.getRemaining)
                        #                 print max(alarms)
                        #                 print('All your guys are sleeping. Now you should just rest!')
                        #                 self.toSleep()

                        #     index=0
                        # else:
                        #     index=index+1
                        #     break
            else:
                index = index+maxPages-1

    # API requests


    def result(self,command,uid, page):
        # Api requests goes there
        re = None

        if command == "coms":
            # GET comments/show
            re = self.client.comments__show(id=uid, page=page, count=50)

        elif command == "RT":
             # GET statuses/reposts
            re = self.client.statuses__repost_timeline(id=uid, page=page, count=50)

        else:
            raise Exception("This is not a valid weibo API command")

        return re

        

    # GET statuses/show
    # Get basic info on a post from API
    def getPost(self, uid, path, format):
        print uid
        re = self.client.statuses__show(id=uid)
        self.toFile(re, "statuses__show_"+uid, path, format)
        return re

    # def place__nearby_timeline(lat, lon, start, end, page, count=30, rang=2000):
    #     # start = stringTotime(STARTTIME)
    #     # end = stringTotime(ENDTIME)
    #     re = api.place__nearby_timeline(lat=lat,long=lon,starttime=start,endtime=end,page=page,count=count,range=rang)
    #     return re