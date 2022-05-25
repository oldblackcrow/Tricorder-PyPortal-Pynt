# Main-Tricorder-PyPortal-Pynt-No-IO
I've removed the AdafruitIO requirement and added new sensors. Feel free to edit, improve, and/or expand this code. 
In this version, you will need the following sensors:
1. Garmin LIDAR Lite v4 - This requires separate 5v power. https://www.adafruit.com/product/4441
2. Adafruit Mini GPS - https://www.adafruit.com/product/4415
3. Adafruit LTR390 - Ultra Violet light sensor https://www.adafruit.com/product/4831
4. Adafruit Precision RTC - Real Time Clock https://www.adafruit.com/product/5188
5. TEA5767 - FM Radio https://www.amazon.com/dp/B074TC3VLN?ref_=cm_sw_r_cp_ud_dp_2F7FR8FH3EB7TBVA6B5K

MAKE SURE you put create appropriate directories on your PyPortal - bmp files go in "images", bdf files in "fonts", and wav files in "sounds"
The ONLY sound and image files that go in the root directory are pyportal_startup.bmp and pyportal_startup.wav

For you physics geeks, I've included in the Fonts directory a version of BebasNeue-Regular-26.bdf with Greek letters (BebasNeue-greek-Regular-26.bdf) and just a Greek Font (Greek03-Regular-25.bdf). You can make this any font name you want within the code and use it for the main body text. The Greek03-Regular-25.bdf is big enough for the top buttons.
