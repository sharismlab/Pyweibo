import sys
import os
from pymongo.errors import ConnectionFailure
from pymongo import Connection
from ConfigParser import SafeConfigParser
#from pymongo.son_manipulator import AutoReference,NamespaceInjector
#from pymongo.code import Code

class mongoDBUtil:
    weiboDB = None

    def __init__(self):
        
        #config stuff
        config = SafeConfigParser()
        config.read( os.path.join(os.getcwd() + os.sep +  'settings.py') )
        host = str(config.get('mongo', 'host'))
        port = int(config.get('mongo', 'port'))

        
        print """ Connecting to MongoDB """

        try:
            self.connection = Connection(host=host, port=port)
            # print "Connected successfully at %s :%s on %s"(host, port,weiboDB)

        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
        
       
    #follows or fans    
    def saveData(self, data, database, collection):

        #conect database
        weiboDB = self.connection[database]
        assert weiboDB.connection == self.connection
        print "Successfully set up a database handle"
        
        # create collection
        weiboData = weiboDB[collection]
        weiboData.insert(data, safe=True)
        print "stored in Mongo db : "+ database+", collection: "+collection
        return weiboDB.bla
    
    #for now,just 2 var first
    def analyseCollection(self, collection, args, topN=5):
        list = """collection.group({
        "key":{args['key']:true},
        "initial":{"person":[]}, #consider not display person
        "reduce":function(doc, out){
            out.person.push(doc.name);
        },
        "finalize":function(out){
        out.count = out.person.length;
        },
        "condition":args['condition']
        })"""
        
        sorted_list = sorted(list, key=lambda list : list['count'], reverse=True)
        
        collection.drop() #is it necessory to remove collection?
        return sorted_list[:topN]
        
    def analyseCollection2(self, collection, topN=5):
        mapper=Code("""function () {
            this.interestTag.forEach(function(z) {
                emit(z, {count:1});
            });
        }
        """)
        reducer= Code("""
            function (key, values) {
            var total = 0;
            for (var i = 0; i < values.length; i++) {
                total += values[i].count;
            }
            
            return {count:total};
        }
        """)
        
        results = collection.mapReduce(mapper,reducer,out="resultCollection")
        for result in results.find():
            print result['_id'] , result['value']['count']
        
        resultCollection.drop()