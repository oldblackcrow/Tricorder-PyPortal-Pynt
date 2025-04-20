# Tricorder PyPortal Pynt

In this version, you will need the following sensors:
1. Garmin LIDAR Lite v4 - This requires separate 5v power with 3v logic. https://www.adafruit.com/product/4441 You can use the Adafruit QT 3V to 5V Level Booster Breakout - STEMMA QT / Qwiic (https://www.adafruit.com/product/5649) which will kindly reduce having to solder the power separately to the sensor!

VITALLY IMPORTANT You MUST use the Garmin LIDAR Lite V4 library in this library file. There are two adafruit_lidarlite files... a .py and a .mpy. DELETE the adafruit_lidarlite.MPY! If you use the on included in CircuitPython, I believe every version, it simply won't work. I don't know why. This version was custom modified by @dastels on Adafruit back in 2021ish. Here's the report ticket on GitHub and please note the latest post by @Danh. adafruit/Adafruit_CircuitPython_LIDARLite#14 | If you are a programmer and want to contribute to convert the adafruit_lidarlite.py to adafruit_lidarlite.mpy, so it can ship with future versions. Your contributions are deeply appreciated!

2. Adafruit LTR390 - Ultra Violet light sensor https://www.adafruit.com/product/4831

MAKE SURE you create appropriate directories on your PyPortal - bmp files go in "images", bdf files in "fonts", and wav files in "sounds"
The ONLY sound and image files that go in the root directory are pyportal_startup.bmp and pyportal_startup.wav

For you physics geeks, I've included in the Fonts directory a version of BebasNeue-Regular-26.bdf with Greek letters (BebasNeue-greek-Regular-26.bdf) and just a Greek Font (Greek03-Regular-25.bdf). You can make this any font name you want within the code and use it for the main body text. The Greek03-Regular-25.bdf is big enough for the top buttons.

If you have issues with connecting to the GPS satelites (Fix Quality: 0), just use the forked version with GPS removed. On that fork, there is a bitmap file you need to add (backgraph-planet.bmp), but other than that, it's a duplicate of this repository. 
