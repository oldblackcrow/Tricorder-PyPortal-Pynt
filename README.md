# Main-Tricorder-PyPortal-Pynt-No-IO
I've removed the AdafruitIO requirement and added new sensors. Plus, I removed the GPS due to conflicts. For the build, I just added another MCU, the GPS, and a little OLED screen that fits to the left of the Clue. Feel free to edit, improve, and/or expand this code. 
In this version, you will need the following sensors:
1. Garmin LIDAR Lite v4 - This requires separate 5v power. https://www.adafruit.com/product/4441
2. Adafruit LTR390 - Ultra Violet light sensor https://www.adafruit.com/product/4831
3. Adafruit Precision RTC - Real Time Clock https://www.adafruit.com/product/5188

MAKE SURE you create appropriate directories on your PyPortal - bmp files go in "images", bdf files in "fonts", and wav files in "sounds"
The ONLY sound and image files that go in the root directory are pyportal_startup.bmp and pyportal_startup.wav

For you physics geeks, I've included in the Fonts directory a version of BebasNeue-Regular-26.bdf with Greek letters (BebasNeue-greek-Regular-26.bdf) and just a Greek Font (Greek03-Regular-25.bdf). You can make this any font name you want within the code and use it for the main body text. The Greek03-Regular-25.bdf is big enough for the top buttons.

If you have issues with connecting to the GPS satelites (Fix Quality: 0), just use the forked version with GPS removed. On that fork, there is a bitmap file you need to add (backgraph-planet.bmp), but other than that, it's a duplicate of this repository. 
