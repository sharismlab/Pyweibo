# -*- coding: utf-8 -*-
import Pyweibo
# from lxml import etree, html


# INFO
posturl = 'http://e.weibo.com/1930665641/zeVxsoiyB'
# posturl = 'http://www.weibo.com/1701401324/zeoBquVKi'



# Generate safe name
urlparts = posturl.split('/')
postname = 'post_%s_%s'%(urlparts[3],urlparts[4])

dotfile = "./out/repost"#+postname+".dot" # file path
gdffile = "./out/"+postname+".gdf" # file path


# init
pyweibo = Pyweibo.Pyweibo()
pyweibo.generateRepostMap(posturl, level=50, max=100000)