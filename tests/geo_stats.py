import os, fnmatch
import json

'''
Return a percentage of how much posts has geolocalized info

'''

my_path="D:\Sites\Pyweibo\out"
folder="post_3534311687371818_130123_174714"

path= my_path+os.sep+folder

files=os.listdir(path)

for f in files:
    if fnmatch.fnmatch(f, "statuses__show_*"):
        print 'non!'
    else:
        raw = open(my_path+os.sep+folder+os.sep+f)
        # print str( min(pages) )
        d = json.load(raw)
        for post in d['reposts']:
            if post["geo"]!=None:
                print "ok"
            else:
                print "None"

        # since_id=str(d['reposts'][49]['id'])
        # print since_id

