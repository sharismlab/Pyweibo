# -*- coding: utf-8 -*-
import Pyweibo
pyweibo = Pyweibo.Pyweibo()

#test
posturl = 'http://e.weibo.com/1930665641/zeVxsoiyB'

#ok!
#posturl = 'http://www.weibo.com/1701401324/zeoBquVKi'

pyweibo.saveRepost2Mongo(posturl, max=10000)
# pyweibo.generateRepostMap(posturl,2, max=10000)