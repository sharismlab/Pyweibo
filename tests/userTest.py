# userTest.py
import datetime, time

t = 600
alarm = datetime.datetime.now()+ datetime.timedelta(0,t)
print alarm

diff= alarm - datetime.datetime.now()
diff = int( round( diff.total_seconds() ) ) 
# print type(diff)
# print diff


#hits per user

users = [ ("user1",10), ("user2",10) ]

# hits = 10
page= 25
hits=0

def regainHits():
    i=0
    while i < 4:
        time.sleep(1)
        i=i+1
        print "you should wait "


# init user 1
hits = users[0][1]

index = 0

while index < len(users) and page>0:
    hits = users[index][1]
    print ("switch user!")

    if hits >0:
        while page > 0:
            if hits >0:
                print "page "+str(page)+" extracted "
                page = page -1
                hits = hits -1
            else:
                if index==len(users)-1:
                    print 'no hits anymore'
                    regainHits()
                    index=0
                    hits=10
                else:
                    index=index+1
                    break
    else:
        index = index+1

        # break
