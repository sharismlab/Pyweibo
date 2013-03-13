# userTest.py
import datetime, time, sys
import threading

t = 600
alarm = datetime.datetime.now()+ datetime.timedelta(0,t)
print alarm

diff= alarm - datetime.datetime.now()
diff = int( round( diff.total_seconds() ) ) 
# print type(diff)
# print diff


# users = [ 
#     ("user1",10, None), 
#     ("user2",10, None),
#     ("user3",10, None)
#     ]

# Users
#####
# string name
# int hits
# datetime asleep
# int token
# int secret
class WeiboUser():

    def __init__(self, name, hits, token, secret, asleep):
        self.name = name
        self.hits = hits
        self.token = token
        self.secret = secret
        self.asleep=None


    def wakeUp(self):
        self.asleep= None # "I am not sleeping anymore"
        self.hits=10
        print self.name+" just woke up!"

    def gotoBed(self,t):
        alarm = datetime.datetime.now()+ datetime.timedelta(0,t)

        # Store when the guy will wake up
        self.asleep = alarm
        print user.name+" is going to bed and will wake up at "+ str(self.asleep)

    def getSleep(self):
        # Time difference in seconds
        
        if(self.asleep == None):
            return 0
        
        diff= user.asleep - datetime.datetime.now()
        diff = int( round( diff.total_seconds() ) ) #find time diff in sec

        if(diff>1):
            return diff
        else:
            self.wakeUp()
            return 0

    def returnHits(self):
        return self.hits

user1 =  WeiboUser("user1",10, "token", 'secret', None) 
user2 =  WeiboUser("user2",10, "token", 'secret', None)
user3 =  WeiboUser("user3",10, "token", 'secret', None)

users = [user1,user2,user3] 
print users

def systemSleep(t):
    i=0
    
    # t = 600 #wait 500 sec
    alarm = datetime.datetime.now()+ datetime.timedelta(0,t)
    print 'the system will be in pause until ' +str(alarm)

    for x in range(t): 
        time.sleep(1)
        diff= alarm - datetime.datetime.now()
        print '\r%s'%(diff), 
        sys.stdout.flush()

# hits = 10
page= 35

print users
# init user 1
user = users[0]
hits = 0

while page>0:
    

    if user.returnHits() >0: #hits 
        print "page "+str(page)+" extracted by "+ user.name
        page = page -1
        user.hits = user.hits -1
        # print "hits :"+ str(hits)
    else:
        # No hits anymore
        print 'No hits anymore'
        print '-----------------------------'
        
        # Go to sleep
        t=10
        user.gotoBed(t)

        # Check if there is other tokens available
        alarms=[]
        found=False
        for u in users:
            # u=list(u)
            # u=us[0]
            # print type(u)
            # print type(u)
            my_asleep= u.getSleep()
            # print str(my_asleep)

            if( my_asleep ==0 ): # Check if a user is available
                print "new user!"
                user=u # assign user
                found=True
                break # continue extraction
                # continue
            else:
                alarms.append(my_asleep)
                
                # Nobody is left, look for the user with closest awaken time
                # user=u
        if(found == False):
            # find the user with minimum waiting time
            i= alarms.index(min(alarms))
            user= users[i]

            # print user

            # then go to sleep
            systemSleep(user.getSleep())

            # reset
            user.wakeUp()
            

        # break

