import requests
import json
import time
from datetime import datetime 
from dateutil.relativedelta import relativedelta

PUSHSHIFT_REDDIT_URL = "http://api.pushshift.io/reddit"

def fetchObjects(**kwargs):
    # Default params values
    
    params = {
        "sort_type": "created_utc",
        "sort": "asc", 
        "size": 300
    }
    
    for key, value in kwargs.items():
        params[key] = value
    #print(params)
    type = "comment"
    if 'type' in kwargs and kwargs['type'].lower() == "submission":
        type = "submission"
        
    #print(PUSHSHIFT_REDDIT_URL + "/" + type + "/search/", params=params, timeout=30)
    r = requests.get(PUSHSHIFT_REDDIT_URL + "/" + type + "/search/", params=params, timeout=30)
    #print(r.url)
    #r = requests.get("https://api.pushshift.io/reddit/search/submission/?subreddit=futurology&sort=asc&sort_type=created_utc&size=12&after=%201323709535&before=%201323820800")
    time.sleep(1)
    if r.status_code == 200:
        response = json.loads(r.text)
        data = response['data']
        #print(data)
        sorted_data_by_id = sorted(data, key=lambda x: int(x['id'], 36))
        return sorted_data_by_id
    else: print("error code: " + str(r.status_code))


def process(max_created_utc, min_created_utc):
    full = min_created_utc-max_created_utc
    # max_created_utc = 1356998400  # 01/01/2013 @ 12:00am (UTC)
    #min_created_utc = 1323820800
    #max_created_utc = 1323709535  # Update epoch time here if script crashes
    # If script crashes, use tail <filename> to find last created_utc timestamp
    
    max_id = 0
    # file = open("submissions.json","a")  # For submissions
    file = open("infini.json", "a")  # For comments
    while 1:
        nothing_processed = True
        # objects = fetchObjects(**kwargs, after=max_created_utc)
        # objects is it hitting the url 
        objects = fetchObjects(subreddit="futurology", type="submission", after=max_created_utc, before=min_created_utc)
        for object in objects:
            id = int(object['id'], 36)
            
            #here we check if the post was created after min_created_utc
            if id > max_id:
                nothing_processed = False
                created_utc = object['created_utc']
                max_id = id
                if created_utc > max_created_utc: 
                    max_created_utc = created_utc
                    print(100*min_created_utc-max_created_utc/full)
                print(json.dumps(object, sort_keys=True, ensure_ascii=True), file=file)
                
        # add one month to both... 
        # might be worth getting rid of this... 
        # return
              
        if nothing_processed: 
            print("nothing")
            return
        max_created_utc -= 1
        time.sleep(.5)


# Convert date to unix

#from dateutil.relativedelta import relativedelta
#x = datetime.now() + relativedelta(months=+2)
#x = datetime(2020,2,10)
#y = datetime(2020,3,10)
#print(datetime.now() + relativedelta(months=+2))
#print(datetime.timestamp(x))
#print(datetime.timestamp(y))

# Convert unix to date
x = 1583798400
datetime.fromtimestamp(x)


process(1581292800,1583798400)
