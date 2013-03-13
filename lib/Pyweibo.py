# -*- coding: utf-8 -*-

import weiboCrawler
import weiboApi
import visualizationUtil
# import mongoDBUtil
import json
import fnmatch
import ast
import os
from ConfigParser import ConfigParser

class Pyweibo:

    weibocrawler = None
    weiboapi = None
    visualizationutil = None
    mongoDButil = None

    def __init__(self):
        print "Init Pyweibo"

        #config stuff
        config = ConfigParser()
        config.read( os.path.join(os.path.abspath(".") + os.sep +  'settings.py') )
        self.OUTPUT_PATH=config.get('files', 'path')
        # print OUTPUT_PATH

        # self.weibocrawler = weiboCrawler.weiboCrawler()
        # self.visualizationutil = visualizationUtil.visualizationUtil()
        # self.mongoDButil = mongoDBUtil.mongoDBUtil()
    
    # Crawler utils
    def getPostIdFromUrl(self, url):
        self.crawler = weiboCrawler.weiboCrawler()
        return self.crawler.getIdFromUrl(url)

    # API tasks
    def getToken(self):
        self.weiboapi  = weiboApi.weiboApi()
        self.weiboapi.create_token()
        return
    # Command can be "coms" or "RT"
    def getPostData(self, command, uid, path, format):
        self.weiboapi  = weiboApi.weiboApi()
        # self.weiboapi.read_tokens()
        self.weiboapi.mainLoop(command, uid, path, format)

    def resumePostData(self):
        self.weiboapi  = weiboApi.weiboApi()
        my_folder = self.selectFromFolder(self.OUTPUT_PATH)
        fetchInfo = self.resumeFetchData(self.OUTPUT_PATH,my_folder)
        print fetchInfo
        self.weiboapi.mainLoop(fetchInfo[0], fetchInfo[1], self.OUTPUT_PATH+os.sep+my_folder, since_page=fetchInfo[2])

    # Crawler
    def crawlRepost(self, url, level=2, max=100):
        return  self.weibocrawler.getRepost(url, level, max)

    def generateRepostMap(self, url, level=2, max=100):
        self.weibocrawler = weiboCrawler.weiboCrawler()
        self.visualizationutil = visualizationUtil.visualizationUtil()

        repost = self.weibocrawler.getRepost(url, level, max)
        
        # print repost
        urlparts = url.split('/')
        postname = 'post_%s_%s'%(urlparts[3],urlparts[4])
        
        # Write dot file
        out='./out/'+postname
        self.visualizationutil.generateDotFile(repost, out)

        # Save data to MongoDB
        # self.mongoDButil.saveData(repost, 'weibo', postname)
        

    def saveRepost2Mongo(self, url, level=2, max=100):
        repost = self.weibocrawler.getRepost(url, level, max)
        self.mongoDButil.saveData(repost, 'repost', 'post')

    #analyse the follows and fans data from weibocrawler.getFollows and weibocrawler.getFans
    #data format will be like [{uid:*, nickname:*}, ...] a dictionary list
    #follows_diff_fans:people who you follow doesn't follow you
    #fans_diff_follows:people who following you but you don't follow
    #follows_inter_fans:people who follow each other
    
    #wo can analyse some useful and funny info about follows or fans, like:
    #topN of fans(follows)'s interest(all? male? female)
    #topN of fans(follows)'s school(all? male? female)
    #topN of fans(follows)'s company(all? male? female)
    #...

    
    def analyseFollowsFansInfo(self, uid, F='follow'):
        follows = self.weibocrawler.getFollows(uid)
        fans = self.weibocrawler.getFans(uid)
        #add to do:uid to dic
        if F is 'follow':
            profiles = [self.weibocrawler.getPersonalProfile(uid) for uid in follows]
            collection = mongoDButil.saveData(profiles, 'follows', uid)
        elif F is 'fan':
            profiles = [self.weibocrawler.getPersonalProfile(uid) for uid in fans]
            collection = mongoDButil.saveData(profiles, 'fans', uid)
        
        #top5 of fans(follows)'s company in male
        #if no condition, condition will be {}
        list = mongoDButil.analyseCollection(collection, key=company, condition={'sex': 'male'}, topN=5)
        #list = mongoDButil.analyseCollection(collection, key=school, condition={'sex': 'male'}, topN=5)
        print list
        
        
        print 'extra info:\n'
        nfollows, nfans = len(follows), len(fans)
        print 'you have %d follows and %d fans\n' % (nfollows, nfans)
        follows_diff_fans = len([val for val in follows if val not in fans])
        print '%d of %d your follows have not follow you\n' % (follows_diff_fans, nfollows)
        fans_diff_follows = len([val for val in fans if val not in follows])
        print '%d of %d your fans you have not follow\n' % (fans_diff_follows, nfans)
        follows_inter_fans = len([val for val in follows if val in fans])
        print '%d people have follow each other\n' % follows_inter_fans
        
        return
    
    def getPersonalProfile(self, uid):
        self.weibocrawler.getPersonalProfile(uid)
    
    #todo
    #beside get a person's profile, we can get a lot of
    #info from it.
    # def analysePerson(self, uid):
        #fill me!
        # return

    # Interactive selection from folder elements
    def selectFromFolder(self,path):
    # def selectFromFolder(self,path):
        index=0
        sets=[]
        
        # Create index from directory
        for f in os.listdir( path ):
            if os.path.isdir( path+ os.sep+ f ) and fnmatch.fnmatch(f, "post_*"):
                sets.append(f)
                print str(index)+") "+f
                index=index+1

        # Interactive selection
        sel = raw_input( "Input the folder index (0 to "+str(len(sets)-1)+" :" ) 
        folder = sets[ int(sel) ]
        print "Will now resume fetching for" + path + os.sep+ folder
        return folder


    # Scan folder to find data and extract elements to resume data fetching
    # returns (command, uid, since_uid)
    def resumeFetchData(self, path, folder):

        # List all existing json files 
        pages=[]

        query=''
        for f in os.listdir( path+os.sep+folder ):
            # Find basic info about post
            if fnmatch.fnmatch(f, "statuses__show_*"):
                print "Original post can be found at = "+ path+os.sep+folder+os.sep+f 
            # RT
            elif fnmatch.fnmatch(f, "RT_*"):
                page = int(f[3:-5])
                pages.append(page)
                query='RT'
            # Comments
            elif fnmatch.fnmatch(f, "coms_*"):
                page = int(f[5:-5])
                pages.append(page)
                print "comments"
                query='coms'
            # Unknown
            else:
                print "directory name seems invalid"

        # Check if already pages inside folder
        if len(pages)==0 or len(pages)==1:
            print ("The folder you selected is empty. No posts fetched.")
        else:
            print str(len(pages))+" pages have already been fetched on a total of "+str(max(pages))
            # Ask for confirmation
            pursue = raw_input("Do you want to resume data extraction (y/n)?")
            
            # Go !  
            if pursue == 'y' or pursue == "Y":
                print "let s fetch it"
                
                # Find last comment
                raw = open(path+os.sep+folder+os.sep+query+'_'+str( min(pages) )+".json")
                print str( min(pages) )
                d = json.load(raw);
                since_page = min(pages)

                # Trigger extraction of  missing posts
                if query=="coms":
                    # since_id=str(d['comments'][49]['id'])
                    uid=str(d['comments'][49]['status']['id'])
                    # print 'pyWeibo '+query +" since_id "+since_id
                elif query=="RT":
                    # since_id=str(d['reposts'][49]['id'])
                    uid=str(d['reposts'][49]['retweeted_status']['id'])
                    # print 'pyWeibo '+query +" since_id "+since_id
                
                return query, uid, since_page

            else :
                print 'bye'