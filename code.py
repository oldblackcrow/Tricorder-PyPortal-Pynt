import time
import sys
import board
import microcontroller
import displayio
import busio
from analogio import AnalogIn
import neopixel
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from adafruit_button import Button
import adafruit_touchscreen
from adafruit_pyportal import PyPortal
import adafruit_lidarlite
import adafruit_ltr390
import adafruit_gps
import adafruit_ds3231

cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)
sys.path.append(cwd)

# ------------- Inputs and Outputs Setup ------------- #
i2c_bus = busio.I2C(board.SCL, board.SDA)
ltr = adafruit_ltr390.LTR390(i2c_bus, address=0x53)
gps = adafruit_gps.GPS_GtopI2C(i2c_bus, address=0x10)
rtc = adafruit_ds3231.DS3231(i2c_bus)

#RTC Clock
# Lookup table for names of days (nicer printing).
days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

# pylint: disable-msg=using-constant-test
if False:  # change to True if you want to set the time!
    # year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2022, 5, 20, 15, 42, 00, 6, -1, -1))
    # you must set year, mon, date, hour, min, sec and weekday
    rtc.datetime = t
    print()
# pylint: enable-msg=using-constant-test

# Turn on just minimum info (RMC only, location):
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b"PMTK220,20000")

# Main loop runs forever printing data as it comes in
#timestamp = time.monotonic()

# Neopixels
pixel_pin = board.D3
num_pixels = 1
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1.0, auto_write=True, pixel_order=ORDER
)

# ---------- Sound Effects ------------- #
soundDemo = '/sounds/sound.wav'
soundBeep = '/sounds/beep.wav'
soundTab = '/sounds/tab.wav'

# ------------- Other Helper Functions------------- #
# Helper for cycling through a number set of 1 to x.
def numberUP(num, max_val):
    num += 1
    if num <= max_val:
        return num
    else:
        return 1

# ------------- Screen Setup ------------- #
pyportal = PyPortal()
display = board.DISPLAY
display.rotation = 0

# Backlight function
# Value between 0 and 1 where 0 is OFF, 0.5 is 50% and 1 is 100% brightness.
def set_backlight(val):
    val = max(0, min(1.0, val))
    board.DISPLAY.auto_brightness = False
    board.DISPLAY.brightness = val

# Set the Backlight
set_backlight(0.5)

# Touchscreen setup
# ------Rotate 0:
screen_width = 320
screen_height = 240
ts = adafruit_touchscreen.Touchscreen(board.TOUCH_XL, board.TOUCH_XR,
                                      board.TOUCH_YD, board.TOUCH_YU,
                                      calibration=((5200, 59000), (5800, 57000)),
                                      size=(320, 240))


# ------------- Display Groups ------------- #
splash = displayio.Group()  # The Main Display Group
view1 = displayio.Group()  # Group for View 1 objects
view2 = displayio.Group()  # Group for View 2 objects
view3 = displayio.Group()  # Group for View 3 objects

def hideLayer(hide_target):
    try:
        splash.remove(hide_target)
    except ValueError:
        pass

def showLayer(show_target):
    try:
        time.sleep(0.1)
        splash.append(show_target)
    except ValueError:
        pass

# ------------- Setup for Images ------------- #

# Display an image until the loop starts
pyportal.set_background('/images/loading.bmp')


bg_group = displayio.Group()
splash.append(bg_group)


icon_group = displayio.Group()
icon_group.x = 0
icon_group.y = 40
icon_group.scale = 1
view2.append(icon_group)

# This will handel switching Images and Icons
def set_image(group, filename):
    """Set the image file for a given goup for display.
    This is most useful for Icons or image slideshows.
        :param group: The chosen group
        :param filename: The filename of the chosen image
    """
    print("Set image to ", filename)
    if group:
        group.pop()

    if not filename:
        return  # we're done, no icon desired

    image_file = open(filename, "rb")
    image = displayio.OnDiskBitmap(image_file)
    try:
        image_sprite = displayio.TileGrid(image, pixel_shader=displayio.ColorConverter())
    except TypeError:
        image_sprite = displayio.TileGrid(image, pixel_shader=displayio.ColorConverter(),
                                          position=(0, 0))
    group.append(image_sprite)

set_image(bg_group, "/images/BGimage.bmp")

# ---------- Text Boxes ------------- #
# Set the font and preload letters
font = bitmap_font.load_font("/fonts/StarFleet-24.bdf")
font1 = bitmap_font.load_font("/fonts/BebasNeue-greek-Regular-26.bdf")
font2 = bitmap_font.load_font("/fonts/BebasNeue-Regular-25.bdf")
font3 = bitmap_font.load_font("/fonts/BebasNeue-Regular-19.bdf")
font4 = bitmap_font.load_font("/fonts/TrekClassic-31.bdf")
font.load_glyphs(b'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- ()')

# Default Label styling:
TABS_X = 5
TABS_Y = 50

# Text Label Objects
sensors_label1 = Label(font1, text="", color=0x03AD31)
sensors_label1.x = TABS_X+100
sensors_label1.y = TABS_Y
view1.append(sensors_label1)

sensor_data1 = Label(font1, text="", color=0x03AD31)
sensor_data1.x = TABS_X+15
sensor_data1.y = 70
view1.append(sensor_data1)

sensors_label2 = Label(font4, text="", color=0x03AD31)
sensors_label2.x = TABS_X+100
sensors_label2.y = TABS_Y
view2.append(sensors_label2)

sensor_data2 = Label(font4, text="", color=0x03AD31)
sensor_data2.x = TABS_X+15
sensor_data2.y = 70
view2.append(sensor_data2)

sensors_label = Label(font4, text="Data View", color=0x03AD31)
sensors_label.x = TABS_X+20
sensors_label.y = TABS_Y
view3.append(sensors_label)

sensor_data = Label(font4, text="Data View", color=0x03AD31)
sensor_data.x = TABS_X+15
sensor_data.y = 65
view3.append(sensor_data)


text_hight = Label(font, text="M", color=0x03AD31)
# return a reformatted string with word wrapping using PyPortal.wrap_nicely
def text_box(target, top, string, max_chars):
    text = pyportal.wrap_nicely(string, max_chars)
    new_text = ""
    test = ""
    for w in text:
        new_text += '\n'+w
        test += 'M\n'
    text_hight.text = test  # Odd things happen without this
    glyph_box = text_hight.bounding_box
    target.text = ""  # Odd things happen without this
    target.y = int(glyph_box[3]/2)+top
    target.text = new_text

# ---------- Display Buttons ------------- #
# Default button styling:
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 80

# We want three buttons across the top of the screen
TAPS_HEIGHT = 40
TAPS_WIDTH = int(screen_width/3)
TAPS_Y = 0

# We want two big buttons at the bottom of the screen
BIG_BUTTON_HEIGHT = int(screen_height/3.2)
BIG_BUTTON_WIDTH = int(screen_width/2)
BIG_BUTTON_Y = int(screen_height-BIG_BUTTON_HEIGHT)

# This group will make it easy for us to read a button press later.
buttons = []

# Main User Interface Buttons
button_view1 = Button(x=0, y=0,
                      width=TAPS_WIDTH, height=TAPS_HEIGHT,
                      label="LOCATION", label_font=font4, label_color=0xff7e00,
                      fill_color=0x5c5b5c, outline_color=0x767676,
                      selected_fill=0x1a1a1a, selected_outline=0x2e2e2e,
                      selected_label=0x525252)
pixels.fill((0, 255, 0))
buttons.append(button_view1)  # adding this button to the buttons group

button_view2 = Button(x=TAPS_WIDTH, y=0,
                      width=TAPS_WIDTH, height=TAPS_HEIGHT,
                      label="TARGET", label_font=font4, label_color=0xff7e00,
                      fill_color=0x5c5b5c, outline_color=0x767676,
                      selected_fill=0x1a1a1a, selected_outline=0x2e2e2e,
                      selected_label=0x525252)
buttons.append(button_view2)  # adding this button to the buttons group

button_view3 = Button(x=TAPS_WIDTH*2, y=0,
                      width=TAPS_WIDTH, height=TAPS_HEIGHT,
                      label="λ", label_font=font1, label_color=0xff7e00,
                      fill_color=0x5c5b5c, outline_color=0x767676,
                      selected_fill=0x1a1a1a, selected_outline=0x2e2e2e,
                      selected_label=0x525252)
buttons.append(button_view3)  # adding this button to the buttons group

button_switch = Button(x=0, y=BIG_BUTTON_Y,
                       width=BIG_BUTTON_WIDTH, height=BIG_BUTTON_HEIGHT,
                       label="Switch", label_font=font, label_color=0xff7e00,
                       fill_color=0x5c5b5c, outline_color=0x767676,
                       selected_fill=0x1a1a1a, selected_outline=0x2e2e2e,
                       selected_label=0x525252)
#buttons.append(button_switch)  # adding this button to the buttons group

button_2 = Button(x=BIG_BUTTON_WIDTH, y=BIG_BUTTON_Y,
                  width=BIG_BUTTON_WIDTH, height=BIG_BUTTON_HEIGHT,
                  label="Button", label_font=font, label_color=0xff7e00,
                  fill_color=0x5c5b5c, outline_color=0x767676,
                  selected_fill=0x1a1a1a, selected_outline=0x2e2e2e,
                  selected_label=0x525252)
#buttons.append(button_2)  # adding this button to the buttons group

# Add all of the main buttons to the splash Group
for b in buttons:
    splash.append(b)


# Make a button to change the icon image on view2
button_icon = Button(x=150, y=60,
                     width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                     label="Icon", label_font=font, label_color=0xffffff,
                     fill_color=0x8900ff, outline_color=0xbc55fd,
                     selected_fill=0x5a5a5a, selected_outline=0xff6600,
                     selected_label=0x525252, style=Button.ROUNDRECT)
#buttons.append(button_icon)  # adding this button to the buttons group

# Add this button to view2 Group
#view2.append(button_icon)

# Make a button to play a sound on view2
button_sound = Button(x=150, y=170,
                      width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      label="Sound", label_font=font, label_color=0xffffff,
                      fill_color=0x8900ff, outline_color=0xbc55fd,
                      selected_fill=0x5a5a5a, selected_outline=0xff6600,
                      selected_label=0x525252, style=Button.ROUNDRECT)
#buttons.append(button_sound)  # adding this button to the buttons group

# Add this button to view2 Group
#view3.append(button_sound)

#pylint: disable=global-statement
def switch_view(what_view):
    global view_live
    if what_view == 1:
        hideLayer(view2)
        hideLayer(view3)
        button_view1.selected = False
        button_view2.selected = True
        button_view3.selected = True
        showLayer(view1)
        view_live = 1
        print("View1 On")
    elif what_view == 2:
        # global icon
        hideLayer(view1)
        hideLayer(view3)
        button_view1.selected = True
        button_view2.selected = False
        button_view3.selected = True
        showLayer(view2)
        view_live = 2
        print("View2 On")
    else:
        hideLayer(view1)
        hideLayer(view2)
        button_view1.selected = True
        button_view2.selected = True
        button_view3.selected = False
        showLayer(view3)
        view_live = 3
        print("View3 On")
#pylint: enable=global-statement

# Set veriables and startup states
button_view1.selected = False
button_view2.selected = True
button_view3.selected = True
showLayer(view1)
hideLayer(view2)
hideLayer(view3)

view_live = 1
icon = 1
icon_name = "Ruby"
button_mode = 1
switch_state = 0
button_switch.label = "OFF"
button_switch.selected = True

#text_box(feed2_label, TABS_Y, '', 18)

text_box(sensors_label, TABS_Y-20,
         "", 28)

board.DISPLAY.show(splash)

# ------------- Code Loop ------------- #
while True:
    touch = ts.touch_point
    gps.update()
    
    if view_live == 1:
        data = gps.read(32)
        t = rtc.datetime
        sensor = adafruit_lidarlite.LIDARLite(i2c_bus)
        sensor_data1.text = '{} {}/{}/{}  {}:{:02}:{:02}\nρθφ\nLat: {}\nLong: {}      Alt: {}'.format(days[int(t.tm_wday)], t.tm_mon, t.tm_mday, t.tm_year,t.tm_hour, t.tm_min, t.tm_sec, (gps.latitude), (gps.longitude), (gps.altitude_m))

    if data is not None:
        data_string = "".join([chr(b) for b in data])
        # '\n' is your Y axis (Enter button) and the spaces are used for the X axis.
    sensor_data.text = 'UV Index\n{}\n                   UV I\n                   {}'.format(ltr.uvi, ltr.lux)
    sensor_data2.text = 'OBJ DISTANCE\n\n                   {}m'.format(sensor.distance/100)
    
    if view_live == 2:
        data = gps.read(32)
        t = rtc.datetime
        sensor = adafruit_lidarlite.LIDARLite(i2c_bus)
        sensor_data2.text = 'OBJ DISTANCE\n\n                   {}m'.format(sensor.distance/100)

    if sensor is not None:
        data_string = "".join([chr(b) for b in data])
        # '\n' is your Y axis (Enter button) and the spaces are used for the X axis.
    sensor_data.text = 'UV Index\n{}\n                   UV I\n                   {}'.format(ltr.uvi, ltr.lux)
    sensor_data1.text = '{} {}/{}/{}  {}:{:02}:{:02}\nρθφ\nLat: {}\nLong: {}      Alt: {}'.format(days[int(t.tm_wday)], t.tm_mon, t.tm_mday, t.tm_year,t.tm_hour, t.tm_min, t.tm_sec, (gps.latitude), (gps.longitude), (gps.altitude_m))

    if view_live == 3:
        data = gps.read(32)
        t = rtc.datetime
        sensor = adafruit_lidarlite.LIDARLite(i2c_bus)
        sensor_data.text = 'UV Index\n{}\n                   UV I\n                   {}'.format(ltr.uvi, ltr.lux)

    if data is not None:
        data_string = "".join([chr(b) for b in data])
        # '\n' is your Y axis (Enter button) and the spaces are used for the X axis.
    sensor_data2.text = 'OBJ DISTANCE\n\n                   {}m'.format(sensor.distance/100)
    sensor_data1.text = '{} {}/{}/{}  {}:{:02}:{:02}\nρθφ\nLat: {}\nLong: {}      Alt: {}'.format(days[int(t.tm_wday)], t.tm_mon, t.tm_mday, t.tm_year,t.tm_hour, t.tm_min, t.tm_sec, (gps.latitude), (gps.longitude), (gps.altitude_m))


    # ------------- Handle Button Press Detection  ------------- #
    if touch:  # Only do this if the screen is touched
        # loop with buttons using enumerate() to number each button group as i
        for i, b in enumerate(buttons):
            if b.contains(touch):  # Test each button to see if it was pressed
                print('button%d pressed' % i)
                if i == 0 and view_live != 1:  # only if view1 is visable
                    pyportal.play_file(soundTab)
                    switch_view(1)
                    #sensor_data1.text = '\nρθφ\nLat: {}\nLong: {}      Alt: {}'.format((gps.latitude), (gps.longitude), (gps.altitude_m))
                    pixels.fill((0, 255, 0))
                    while ts.touch_point:
                        pass
                if i == 1 and view_live != 2:  # only if view2 is visable
                    pyportal.play_file(soundTab)
                    switch_view(2)
                    #sensor_data2.text = 'OBJ DISTANCE\n\n                   {}m'.format(LIDAR_data.distance/100)
                    pixels.fill((255, 0, 0))
                    while ts.touch_point:
                        pass
                if i == 2 and view_live != 3:  # only if view3 is visable
                    pyportal.play_file(soundTab)
                    switch_view(3)
                    #sensor_data.text = 'UV Index\n{}\n                   UV I\n                   {}'.format(ltr.uvi, ltr.lux)
                    pixels.fill((0, 0, 255))
                    while ts.touch_point:
                        pass
                if i == 3:
                    pyportal.play_file(soundBeep)
                    # Toggle switch button type
                    if switch_state == 0:
                        switch_state = 1
                        b.label = "ON"
                        b.selected = False
                        pixel.fill(BLACK)
                        print("Swich ON")
                    else:
                        switch_state = 0
                        b.label = "OFF"
                        b.selected = True
                        pixel.fill(BLACK)
                        print("Swich OFF")
                    # for debounce
                    while ts.touch_point:
                        pass
                    print("Swich Pressed")
                if i == 4:
                    pyportal.play_file(soundBeep)
                    # Momentary button type
                    b.selected = True
                    print('Button Pressed')
                    button_mode = numberUP(button_mode, 5)
                    if button_mode == 1:
                        pixel.fill(RED)
                    elif button_mode == 2:
                        pixel.fill(RED)
                    elif button_mode == 3:
                        pixel.fill(RED)
                    elif button_mode == 4:
                        pixel.fill(BLUE)
                    elif button_mode == 5:
                        pixel.fill(PURPLE)
                    switch_state = 1
                    button_switch.label = "ON"
                    button_switch.selected = False
                    # for debounce
                    while ts.touch_point:
                        pass
                    print("Button released")
                    b.selected = False
                if i == 5 and view_live == 2:  # only if view2 is visable
                    pyportal.play_file(soundBeep)
                    b.selected = True
                    while ts.touch_point:
                        pass
                    print("Icon Button Pressed")
                    icon = numberUP(icon, 3)
                    if icon == 1:
                        icon_name = "Ruby"
                    elif icon == 2:
                        icon_name = "Gus"
                    elif icon == 3:
                        icon_name = "Billie"
                    b.selected = False
                    text_box(feed2_label, TABS_Y,
                             "Every time you tap the Icon button the icon image will \
change. Say hi to {}!".format(icon_name), 18)
                    set_image(icon_group, "/images/"+icon_name+".bmp")
                if i == 6 and view_live == 3:  # only if view3 is visable
                    b.selected = True
                    while ts.touch_point:
                        pass
                    print("Sound Button Pressed")
                    pyportal.play_file(soundDemo)
                    b.selected = False
