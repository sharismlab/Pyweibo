# -*- coding: utf-8 -*-

import weiboCrawler
import weiboApi
import visualizationUtil
import mongoDBUtil
import ast
import os

class Pyweibo:

	weibocrawler = None
	weiboapi = None
	visualizationutil = None
	mongoDButil = None

	def __init__(self):
		print "Init Pyweibo"

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

	def getPostData(self, command, uid, path, format):
		self.weiboapi  = weiboApi.weiboApi()
		# self.weiboapi.read_tokens()
		self.weiboapi.mainLoop(command, uid, path, format)

    
	# Crawler
	def crawlRepost(self, url, level=2, max=100):
		return	self.weibocrawler.getRepost(url, level, max)

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
	def analysePerson(self, uid):
		#fill me!
		return
		
		