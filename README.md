# ringmybell

Written for raspberry pi with python3
* You might need to install some packages, including twython, RPi.GPIO, picamera
* Make sure twython is 3.4.0 or newer (this is when video upload was supported and some RPi packages are older versions)
* Make sure you have your picamera enabled using raspi-config.
* Also requre arecord and ffmpeg to be installed.
* RaspberryPi does not have a sound card so you either need a USB microphone or a USB soundcard with microphone attached.
* You need a relay attached to GPIO pin 18 to switche the bell on and off. You could attach anything to the relay (not just a bell).
* You need to create a twitter app here: https://apps.twitter.com/ Then use auth_template.py to create a file named auth.py with your app's key info (the key info is generated when you create the twitter app)

##Running the program
To run the program: 
~~~~
python3 stream_queue.py
~~~~
   
##Using the cron scheduler to start on boot
I use cron to start the program at startup. To edit your crontab file
~~~~
chron -e
~~~
then add:
~~~~
@reboot /usr/bin/python3 /home/pi/ringmybell/stream_queue.py > /home/pi/ringmybell/cron.log 2>&1 &
~~~~
Make sure your pi is set to autologin the user pi.
