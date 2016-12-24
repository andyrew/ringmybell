# ringmybell

Written for raspberry pi with python3
* You might need to install some packages, including twython, RPi.GPIO, picamera
* Make sure twython is 3.4.0 or newer (this is when video upload was supported and some RPi packages are older versions)
* Make sure you have your picamera enabled using raspi-config.
* Also requre arecord and ffmpeg to be installed.
* RaspberryPi does not have a sound card so you either need a USB microphone or a USB soundcard with microphone attached.
* You need a relay attached to GPIO pin 18 to switche the bell on and off. You could attach anything to the relay (not just a bell).

