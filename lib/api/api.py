# -*- coding:utf-8 -*-
#! /usr/local/bin/python
import weibo
import pickle
import time,os


APP_KEY = "1197702944"
APP_SECRET = "0415f4cba593ff92cbc6cad0671aef18"

# GEO-LOC 
LON =118.87800
LAT =32.02080
STARTTIME="2012-10-20 1:2:2"
ENDTIME = "2012-11-05 1:2:2"

tokenArray = [('2.009zcHyB0WnLF5354c35bbd90jxbTS',1516563232)]

api = weibo.APIClient(APP_KEY,APP_SECRET)

FILE = "test"

def toFile(JSONOBJ, fileName):
    if os.path.isdir(FILE):
        if os.path.exists(FILE+os.sep+fileName):
            print (fileName+"文件已经存在，请指定其他文件夹")
            return
        else:
            pickle.dump(JSONOBJ, open(FILE+os.sep+fileName,'w'))
    else:
        print(FILE+"已经存在")

def remainHit():
    statu = api.account__rate_limit_status()
    return statu['remaining_user_hits']

def resetTime():
    statu = api.account__rate_limit_status()
    return statu['reset_time_in_seconds']

def toSleep():
    t = resetTime()
    t = t+1
    print('现在程序会睡眠'+str(t)+" 秒钟，直到下一个整点重新恢复运行")
    time.sleep(t)

def stringTotime(strtime):#时间格式"2012-10-20 1:2:2"
    t_tuple = time.strptime(strtime,"%Y-%m-%d %H:%M:%S")
    return int(time.mktime(t_tuple))

def result(page):
    start = stringTotime(STARTTIME)
    end = stringTotime(ENDTIME)
    re = api.place__nearby_timeline(lat=LAT,long=LON,starttime=start,endtime=end,page=page,count=30,range=2000)
    return re

def maxpage():
    firstpage = result(1)
    print firstpage
    total_number = firstpage['total_number']
    print total_number,' total_number'
    return (total_number/30) if (total_number%30==0) else (total_number/30+1)

def setToken(tokenTuple):

    api.set_access_token(tokenTuple[0],tokenTuple[1])

def tokenLoop(Max):
    Max = Max
    for Token in tokenArray:
        setToken(Token)
        if remainHit()>0:
            print remainHit()
            while Max > 0:
                if remainHit()>0:
                    JSONOBJ = result(Max)
                    Max = Max -1
                    toFile(JSONOBJ,str(Max))

                else:
                    break


    return Max

def mainFunc():
    Max = 0
    token = tokenArray[0]
    setToken(token)
    Max = maxpage()
    print Max,"Max"
    index = 0
    while index < len(tokenArray) and Max>0:
        setToken(tokenArray[index])
        if remainHit()>0:
            while Max > 0:
                if remainHit()>0:
                    JSONOBJ = result(Max)
                    print Max
                    Max = Max-1
                    toFile(JSONOBJ,str(Max))
                else:
                    if index==len(tokenArray)-1:
                        toSleep()
                        index=0
                    else:
                        index=index+1
                        break
        else:
            index = index+1

mainFunc()


