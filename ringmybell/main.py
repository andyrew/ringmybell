import time
# This sleep delays initializing things until after the pi finishes booting (this script is run at boot time using cron).
time.sleep(15)

import datetime
import threading
import subprocess
import sys
import os
import json
import queue
import RPi.GPIO as GPIO
from ringmybell.ringbell_reply import ringbell_reply
from ringmybell.ringbell_reply import nighttime_reply
import twython

home = os.path.expanduser("~")
auth_file = home + "/.twitterkey/auth.json"

with open(auth_file, 'r') as af:
    key = json.load(af)
    consumer_key = key["consumer_key"]
    consumer_secret = key["consumer_secret"]
    access_token = key["access_token"]
    access_token_secret = key["access_token_secret"]

# Create the queue objects
dayQ = queue.Queue()
nightQ = queue.Queue()

# On and Off hours
start=datetime.time(7,30)
end=datetime.time(20,30)

# Class to contain tweet bits
class Tweet:
   def __init__(self, username, text, tweetid):
      self.username=username
      self.text=text
      self.id=tweetid

# Class for the twitter streamer
class MyStreamer(twython.TwythonStreamer):
    def on_success(self, data):
         global dayQ,nightQ,start,end
         timestamp=datetime.datetime.now().time()
         newTweet = Tweet(data['user']['screen_name'], data['text'],str(data['id']))
         if start <= timestamp <= end :
            dayQ.put(newTweet)
         else :
            nightQ.put(newTweet)
         print("@%s: %s" % (newTweet.username, newTweet.text))

# Function for the twitter streaming thread
def streaming(*args):
   stream = MyStreamer(
       consumer_key,
       consumer_secret,
       access_token,
       access_token_secret
   )
   stream.statuses.filter(track='@ringandysbell')

# Function for ringing and replying thread
def worker(*args):
   global dayQ,nightQ,start,end
   while True:
      if start <= datetime.datetime.now().time() <= end and not dayQ.empty():
         item=dayQ.get()
         ringbell_reply(item)
      if not nightQ.empty() :
         item=nightQ.get()
         nighttime_reply(item)
         dayQ.put(item)
      time.sleep(1)

t1 = threading.Thread(target=streaming)
t2 = threading.Thread(target=worker)

def main():
   t1.start()
   t2.start()

#t1.join()
#t2.join()

if __name__ == '__main__':
    main()
