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
import adafruit_ds3231  # still there in case you want RTC later

cwd = ("/"+__file__).rsplit('/', 1)[0]
sys.path.append(cwd)

# ------------- Inputs and Outputs Setup ------------- #
i2c_bus = busio.I2C(board.SCL, board.SDA)
ltr = adafruit_ltr390.LTR390(i2c_bus)
sensor = adafruit_lidarlite.LIDARLite(i2c_bus)

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
def numberUP(num, max_val):
    num += 1
    return num if num <= max_val else 1

# ------------- Screen Setup ------------- #
pyportal = PyPortal()
display = board.DISPLAY
display.rotation = 0

def set_backlight(val):
    val = max(0, min(1.0, val))
    board.DISPLAY.auto_brightness = False
    board.DISPLAY.brightness = val
set_backlight(0.5)

# Touchscreen setup
screen_width = 320
screen_height = 240
ts = adafruit_touchscreen.Touchscreen(board.TOUCH_XL, board.TOUCH_XR,
                                      board.TOUCH_YD, board.TOUCH_YU,
                                      calibration=((5200, 59000), (5800, 57000)),
                                      size=(320, 240))

# ------------- Display Groups ------------- #
splash = displayio.Group()
view1 = displayio.Group()
view2 = displayio.Group()
view3 = displayio.Group()

def hideLayer(h):
    try:
        splash.remove(h)
    except ValueError:
        pass

def showLayer(s):
    try:
        time.sleep(0.1)
        splash.append(s)
    except ValueError:
        pass

# ------------- Setup for Images ------------- #
pyportal.set_background('/images/loading.bmp')

bg_group = displayio.Group()
splash.append(bg_group)

icon_group = displayio.Group()
icon_group.x = 0
icon_group.y = 40
icon_group.scale = 1
view2.append(icon_group)

def set_image(group, filename):
    if group:
        group.pop()
    if not filename:
        return
    with open(filename, "rb") as f:
        img = displayio.OnDiskBitmap(f)
        try:
            tg = displayio.TileGrid(img, pixel_shader=displayio.ColorConverter())
        except TypeError:
            tg = displayio.TileGrid(img, pixel_shader=displayio.ColorConverter(),
                                    position=(0,0))
    group.append(tg)

set_image(bg_group, "/images/BGimage.bmp")

# ---------- Text Boxes ------------- #
font  = bitmap_font.load_font("/fonts/StarFleet-24.bdf")
font1 = bitmap_font.load_font("/fonts/BebasNeue-greek-Regular-26.bdf")
font2 = bitmap_font.load_font("/fonts/BebasNeue-Regular-25.bdf")
font3 = bitmap_font.load_font("/fonts/BebasNeue-Regular-19.bdf")
font4 = bitmap_font.load_font("/fonts/TrekClassic-31.bdf")
font.load_glyphs(b'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- ()')

TABS_X = 5
TABS_Y = 50

# View 1 labels (now blank until you populate it with something else)
sensors_label1 = Label(font1, text="", color=0x03AD31)
sensors_label1.x = TABS_X+100
sensors_label1.y = TABS_Y
view1.append(sensors_label1)

sensor_data1 = Label(font1, text="", color=0x03AD31)
sensor_data1.x = TABS_X+15
sensor_data1.y = 70
view1.append(sensor_data1)

# View 2 (Distance)
sensors_label2 = Label(font4, text="", color=0x03AD31)
sensors_label2.x = TABS_X+100
sensors_label2.y = TABS_Y
view2.append(sensors_label2)

sensor_data2 = Label(font4, text="", color=0x03AD31)
sensor_data2.x = TABS_X+15
sensor_data2.y = 70
view2.append(sensor_data2)

# View 3 (UV)
sensors_label = Label(font4, text="Data View", color=0x03AD31)
sensors_label.x = TABS_X+20
sensors_label.y = TABS_Y
view3.append(sensors_label)

sensor_data = Label(font4, text="Data View", color=0x03AD31)
sensor_data.x = TABS_X+15
sensor_data.y = 65
view3.append(sensor_data)

# Word‑wrapping helper
text_hight = Label(font, text="M", color=0x03AD31)
def text_box(target, top, string, max_chars):
    lines = pyportal.wrap_nicely(string, max_chars)
    new_text = "\n".join(lines)
    # force recalc of bounding box
    text_hight.text = "M\n" * len(lines)
    bb = text_hight.bounding_box
    target.text = ""
    target.y = int(bb[3]/2) + top
    target.text = new_text

# ---------- Buttons ------------- #
BUTTON_HEIGHT = 40
BUTTON_WIDTH  = 80

TAPS_HEIGHT = 40
TAPS_WIDTH  = int(screen_width/3)

BIG_BUTTON_HEIGHT = int(screen_height/3.2)
BIG_BUTTON_WIDTH  = int(screen_width/2)
BIG_BUTTON_Y      = int(screen_height - BIG_BUTTON_HEIGHT)

buttons = []

button_view1 = Button(0, 0, TAPS_WIDTH, TAPS_HEIGHT,
                      label="LOCATION", label_font=font4, label_color=0xff7e00,
                      fill_color=0x5c5b5c, outline_color=0x767676,
                      selected_fill=0x1a1a1a, selected_outline=0x2e2e2e,
                      selected_label=0x525252)
buttons.append(button_view1)

button_view2 = Button(TAPS_WIDTH, 0, TAPS_WIDTH, TAPS_HEIGHT,
                      label="TARGET", label_font=font4, label_color=0xff7e00,
                      fill_color=0x5c5b5c, outline_color=0x767676,
                      selected_fill=0x1a1a1a, selected_outline=0x2e2e2e,
                      selected_label=0x525252)
buttons.append(button_view2)

button_view3 = Button(TAPS_WIDTH*2, 0, TAPS_WIDTH, TAPS_HEIGHT,
                      label="λ", label_font=font1, label_color=0xff7e00,
                      fill_color=0x5c5b5c, outline_color=0x767676,
                      selected_fill=0x1a1a1a, selected_outline=0x2e2e2e,
                      selected_label=0x525252)
buttons.append(button_view3)

# Optional extra buttons—unchanged
button_switch = Button(0, BIG_BUTTON_Y, BIG_BUTTON_WIDTH, BIG_BUTTON_HEIGHT,
                       label="Switch", label_font=font, label_color=0xff7e00,
                       fill_color=0x5c5b5c, outline_color=0x767676,
                       selected_fill=0x1a1a1a, selected_outline=0x2e2e2e,
                       selected_label=0x525252)

button_2 = Button(BIG_BUTTON_WIDTH, BIG_BUTTON_Y, BIG_BUTTON_WIDTH, BIG_BUTTON_HEIGHT,
                  label="Button", label_font=font, label_color=0xff7e00,
                  fill_color=0x5c5b5c, outline_color=0x767676,
                  selected_fill=0x1a1a1a, selected_outline=0x2e2e2e,
                  selected_label=0x525252)

for b in buttons:
    splash.append(b)

# View‑2 extras
button_icon = Button(150, 60, BUTTON_WIDTH, BUTTON_HEIGHT,
                     label="Icon", label_font=font, label_color=0xffffff,
                     fill_color=0x8900ff, outline_color=0xbc55fd,
                     selected_fill=0x5a5a5a, selected_outline=0xff6600,
                     selected_label=0x525252, style=Button.ROUNDRECT)

# View‑3 extras
button_sound = Button(150, 170, BUTTON_WIDTH, BUTTON_HEIGHT,
                      label="Sound", label_font=font, label_color=0xffffff,
                      fill_color=0x8900ff, outline_color=0xbc55fd,
                      selected_fill=0x5a5a5a, selected_outline=0xff6600,
                      selected_label=0x525252, style=Button.ROUNDRECT)

view2.append(button_icon)
view3.append(button_sound)

def switch_view(v):
    global view_live
    if v == 1:
        hideLayer(view2); hideLayer(view3)
        button_view1.selected = False
        button_view2.selected = True
        button_view3.selected = True
        showLayer(view1)
    elif v == 2:
        hideLayer(view1); hideLayer(view3)
        button_view1.selected = True
        button_view2.selected = False
        button_view3.selected = True
        showLayer(view2)
    else:
        hideLayer(view1); hideLayer(view2)
        button_view1.selected = True
        button_view2.selected = True
        button_view3.selected = False
        showLayer(view3)
    view_live = v

# Initial state
button_view1.selected = False
button_view2.selected = True
button_view3.selected = True
showLayer(view1)
hideLayer(view2)
hideLayer(view3)
view_live = 1

board.DISPLAY.show(splash)

# ------------- Main Loop ------------- #
icon = 1
button_mode = 1
switch_state = 0

while True:
    touch = ts.touch_point

    # --- Always update your sensors ---

    if view_live == 2:
        sensor_data2.text = 'OBJ DISTANCE\n\n                   {}m'.format(sensor.distance//100)

    if view_live == 3:
        sensor_data.text = 'UV Index\n{}\n                   UV I\n                   {}'.format(
            ltr.uvi, ltr.lux
        )

    # And still let sensor_data2 update whenever LTR is present:
    if sensor is not None:
        sensor_data2.text = 'OBJ DISTANCE\n\n                   {}m'.format(sensor.distance//100)

    if ltr is not None:
        sensor_data.text = 'UV Index\n{}\n                   UV I\n                   {}'.format(
            ltr.uvi, ltr.lux
        )

    # --- Button handling (unchanged) ---
    if touch:
        for i, b in enumerate(buttons):
            if b.contains(touch):
                pyportal.play_file(soundTab)
                if i < 3 and view_live != i+1:
                    switch_view(i+1)
                    pixels.fill([(0,255,0),(255,0,0),(0,0,255)][i])
                    while ts.touch_point: pass

                elif i == 3:
                    pyportal.play_file(soundBeep)
                    # … your switch logic …

                elif i == 4:
                    pyportal.play_file(soundBeep)
                    # … your button_mode logic …

        # Extras:
        if button_icon.contains(touch) and view_live == 2:
            pyportal.play_file(soundBeep)
            # … your icon logic …

        if button_sound.contains(touch) and view_live == 3:
            pyportal.play_file(soundDemo)
            # … your sound‑demo logic …

    time.sleep(0.05)
