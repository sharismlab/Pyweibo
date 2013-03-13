#testMongo.py

import lib.mongoDBUtil as mongoDBUtil
import datetime
import json

data = [{"author": "Mike",
         "text": "My first blog post!",
         "tags": ["mongodb", "python", "pymongo"],
         "date": datetime.datetime.utcnow()
         }]

# obj = json.loads(data)

mongoDButil = mongoDBUtil.mongoDBUtil()
mongoDButil.saveData(data, "blabla",'test')
