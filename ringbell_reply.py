import subprocess
import os
import signal
import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import tempfile
from random import randint
import twython
import string 
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
camera=PiCamera()

from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

replys=["got your ring-a-ding!",
        "good one!",
        "RING! Ha Ha!",
        "Four score and seven... RING!",
        "shhhhhhh-RING!",
        "heaRING test!",
        "MOAR RING!",
        "You get a RING, You get a RING, EVERYBIDY GETS A RING!",
        "Carol of the fire bell!",
        "Woke up like brrrrrrrring!",
        "One ring ding, two ringy dingy!",
        "Woke me right up with that one!",
        "That's some fancy ringin!",
        "Ringin' for you, ringin' for me!",
        "I ring all day, I ring all night",
        "Ring like nobody's watching!",
        "Jingle me, Jingle me, Jingle all the way!"
]

def nighttime_reply(tweet):
   twitter = twython.Twython(
      consumer_key,
      consumer_secret,
      access_token,
      access_token_secret
   )
   twitter.update_status(status="@"+tweet.username+" I'm off for the night. I'll ring your tweet at 7:30 AM (pacific).", in_reply_to_status_id=tweet.id) 

def ringbell_reply(tweet):
   tf=tempfile.NamedTemporaryFile()
   beat=0.125
   # Warning ring and five second wait
   GPIO.output(18,GPIO.HIGH)
   time.sleep(beat)
   GPIO.output(18,GPIO.LOW)  
   time.sleep(10) 
   
   # Creating a printable set for checking characters (emoji cause problems)
   printset = set(string.printable+"–"+"—")

   # A variable to see if the bell was rung during the tweet text
   unrung=True
   
   #camera.start_preview()
   # Subtitle 
   camera.annotate_text_size = 48 
   camera.resolution = (1280,720)
   subtitle = tweet.username+"\n "
   camera.annotate_text = subtitle
   
   # Start camera and audio recording
   pro = subprocess.Popen("arecord --device=hw:1,0 --format S16_LE -d 45 --rate 44100 "+tf.name+".wav", shell = True, preexec_fn=os.setsid)
   camera.start_recording(tf.name+".h264")
   
   # Dead space at begining of video and audio 
   time.sleep(1)
   
   # Loop through characters in tweet
   for c in tweet.text:
      if set(c).issubset(printset):
         if c=="–" or c=="—": c="-"
         subtitle=subtitle+c
         camera.annotate_text = subtitle
         if c=="0" or c=="O" or c=="o":
            GPIO.output(18,GPIO.HIGH)
            time.sleep(beat)
            unrung=False
         elif c=="-":
            GPIO.output(18,GPIO.LOW)
            time.sleep(beat)
   GPIO.output(18,GPIO.LOW)
   
   # Ring if the user didn't have any 0 or - in the tweet 
   if unrung:
      GPIO.output(18,GPIO.HIGH)
      time.sleep(beat*3)
      GPIO.output(18,GPIO.LOW)
      time.sleep(beat*6)
      GPIO.output(18,GPIO.HIGH)
      time.sleep(beat*3)
      GPIO.output(18,GPIO.LOW)

   # Dead space at end of recording
   time.sleep(2)
   os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
   camera.stop_recording()
   
   # Wait for file to close and such 
   time.sleep(1)
   
   # Combining video and audio into MP4
   subprocess.call("ffmpeg -y -r 30 -i "+tf.name+".h264 -i "+tf.name+".wav -c:a aac -preset medium -strict experimental "+tf.name+".mp4", shell = True)
   
   # Repling to the tweet
   twitter = twython.Twython(
      consumer_key,
      consumer_secret,
      access_token,
      access_token_secret
   )
   video=open(tf.name+".mp4", 'rb')
   response=twitter.upload_video(media=video, media_type='video/mp4')
   twitter.update_status(status=replys[randint(0,len(replys)-1)]+"\n@"+tweet.username, media_ids=[response['media_id']], in_reply_to_status_id=tweet.id)
   #camera.stop_preview()
   
   
