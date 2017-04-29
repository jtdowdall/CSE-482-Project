import tweepy
from tweepy import OAuthHandler
from tweepy import API
import time
import json
from tweepy.streaming import StreamListener
from tweepy import Stream
from afinn import Afinn
import requests
import sys

C_KEY = "TQbAsSoi0iwzv76iEVFNkCN1p"
C_SECRET = "eKYicCDpprdLvCxr1TFxCFzQMGB98Wk6AJovTPdkr6w0NYUSyR"
A_TOKEN_KEY = "174046629-KF7Try8Qt6MLdn2BKx1Mwq3ybhOXNel0UByogAXg"
A_TOKEN_SECRET = "y1lFV6qMO2E6hvCZp3FzjO15IvpD1yK5oIKzvBo9Xp0bw"
afinn = Afinn(emoticons=True)
if len(sys.argv) < 2:
    print("Please enter keyword as commandline argument.")
    exit()
KEYWORD = sys.argv[1]
positive = 0.0
negative = 0.0

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN_KEY, A_TOKEN_SECRET)
api = tweepy.API(auth)

def sentiment(text):
    r = requests.post("http://text-processing.com/api/sentiment/", data={"text":text})
    prob = json.loads(r.text)["probability"]
    return int(prob['neg'] < ['pos'])

def sentiment2(text):
    return int(afinn.score(text) > 0)

class MyListener(StreamListener):
    def __init__(self, time_limit=-1):
        self.start_time = time.time()
        self.limit = time_limit
        super(MyListener, self).__init__()

    def on_data(self, data):
        global red, blue
        if self.limit == -1 or (time.time() - self.start_time) < self.limit:
            data = json.loads(data)
            text = data['text'].encode('utf-8', errors = 'ignore')
            split = text.find('https://t.co')
            if split != -1:
                text = text[:split-1]
            split = text.find(':')
            if split != -1:
                text = text[split+2:]
            text = text.replace('#', '')
            api = sentiment(text)
            afinn = sentiment2(text)
            print('''

**************TWEET**************
{}
************Sentiment************
API: {}
Afinn: {}
*********************************
            '''.format(text,api,afinn))
            # negative += neg
            # positive += pos
            return True
        else:
            self.outFile.close()
            return False

    def on_error(self, status):
        print(status)

myStream = Stream(auth, MyListener())
myStream.filter(track=[KEYWORD])
