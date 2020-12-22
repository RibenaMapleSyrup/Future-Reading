import json
import time
import requests 
from datetime import datetime 
import os 
import dateparser 
from bs4 import BeautifulSoup
from urllib import request
import numpy as np
import sys, getopt

PUSHSHIFT_REDDIT_URL = "http://api.pushshift.io/reddit"

def date_to_utc(date):
    utc = datetime.timestamp(datetime(int(str(date)[0:4]),int(str(date)[5:6]),int(str(date)[7:8])))
    return int(utc)

def progress_bar(current, total, barLength = 20):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))
    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')

def fetch_objects(**kwargs):
    # Default params values
    params = {
        "sort_type": "created_utc",
        "sort": "asc", 
        "size": 300
    }
    for key, value in kwargs.items():
        params[key] = value
    type = "comment"
    if 'type' in kwargs and kwargs['type'].lower() == "submission":
        type = "submission"        
    r = requests.get(PUSHSHIFT_REDDIT_URL + "/" + type + "/search/", params=params, timeout=30)
    time.sleep(1)
    if r.status_code == 200:
        response = json.loads(r.text)
        data = response['data']
        sorted_data_by_id = sorted(data, key=lambda x: int(x['id'], 36))
        return sorted_data_by_id
    else: print("error code: " + str(r.status_code))

def process(max_created_utc, min_created_utc, filename, subreddit):
    full = min_created_utc-max_created_utc
    max_id = 0
    start = max_created_utc
    file = open(filename, "a")
    while 1:
        nothing_processed = True
        objects = fetch_objects(subreddit=subreddit, type="submission", after=max_created_utc, before=min_created_utc)
        for object in objects:
            id = int(object['id'], 36)
            # Check if post was created after min_created_utc:
            if id > max_id:
                nothing_processed = False
                created_utc = object['created_utc']
                max_id = id
                if created_utc > max_created_utc: 
                    max_created_utc = created_utc
                    progress_bar((max_created_utc-start),full)
                print(json.dumps(object, sort_keys=True, ensure_ascii=True), file=file)
        if nothing_processed: 
            return
        max_created_utc -= 1
        time.sleep(.5)

def params(argv):
    start_time = ''
    end_time = ''
    filename = ''
    subreddit = ''
    try: 
        opts, args = getopt.getopt(argv, "hs:e:f:r:", ["start=", "end=", "filename=", "subreddit="])
    except getopt.GetoptError:
        print('python3 test_scrape.py -s <YYYYMMDD> -e <YYYYMMDD> -f <filename> -s <subreddit>')
        sys.exit(2)
    for opt, arg in opts: 
        if opt == '-h':
            print('python3 test_scrape.py -s <YYYYMMDD> -e <YYYYMMDD> -f <filename> -s <subreddit>')
            sys.exit()
        elif opt in ("-s", "--start"):
            start_time = arg
        elif opt in ("-e", "--end"):
            end_time = arg
        elif opt in ("-f", "--filename"):
            filename = arg
        elif opt in ("-r", "--subreddit"):
            subreddit = arg
    return start_time, end_time, filename, subreddit

start_time, end_time, filename, subreddit = params(sys.argv[1:])

process(date_to_utc(start_time), date_to_utc(end_time), str(filename) + ".json", str(subreddit))

