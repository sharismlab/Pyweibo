'''
Test write / read on mongoDB
'''

import lib.mongoDBUtil as mongoDBUtil
import datetime
import json

data = [{"author": "Mike",
         "text": "My first blog post!",
         "tags": ["mongodb", "python", "pymongo"],
         "date": datetime.datetime.utcnow()
         }]


mongoDButil = mongoDBUtil.mongoDBUtil()

mongoDButil.saveData(data, "blabla",'test')
