from neopixel2 import Neopixel
from machine import Pin
import machine
from time import sleep
import time
import random
import sys

numpix = 294 #number of LEDs
GPIO = 28 #PIN number on RBPico
max_brightness = 10
standard_brightness = 2
#standard_brightness = 10 #Testing
stopped = False
shuffle = True
mode = 0
number_modes = 15 #incl. 0
speeds = [3.0, 1.0, 0.5, 0.1, 0.05, 0.01, 10.0, 5.0]
speed_index = 2
speed = speeds[speed_index]

#Setup
pixels = Neopixel(numpix, 0, GPIO, "GRBW")
pixels.brightness(standard_brightness) #Will be overwritten if how_bright is passed!!
#Funktionieren:
#GBRW, GBWR, GRBW, GRWB, GWRB, GWBR
#BGWR, BGRW, BWGR, BWRG, BRWG, BRGW
#WBGR, WBRG, WRGB, WRBG, WGRB, WGBR
#RWGB, RWBG, RBWG, RBGW, RGBW, RGWB
onboard_led = Pin("LED", Pin.OUT)
#Buttons
btn1 = Pin(9, Pin.IN, Pin.PULL_DOWN)
btn2 = Pin(11, Pin.IN, Pin.PULL_DOWN)
btn3 = Pin(13, Pin.IN, Pin.PULL_DOWN)
btn4 = Pin(7, Pin.IN, Pin.PULL_DOWN)
onboard_led.off()

def debounce(pin):
    prev = None
    for _ in range(32):
        current_value = pin.value()
        if prev != None and prev != current_value:
            return None
        prev = current_value
    return prev

def button1_callback(pin):
    global stopped, shuffle, number_modes, mode
    d = debounce(pin)
    if d == None:
        return
    elif not d:
        print('Button 1 pressed')
        onboard_led.value(not onboard_led.value())
        stopped = True
        shuffle = False
        if mode == number_modes:
            mode = 0
            clear()
        else:
            mode = mode +1
        print('Current mode: ' + str(mode+1))
        #modes()

def button2_callback(pin):
    global color, stopped
    d = debounce(pin)
    if d == None:
        return
    elif not d:
        print('Button 2 pressed')
        onboard_led.value(not onboard_led.value())
        #stopped = True
        if color == len(colors)-1:
            color = -1
        else:
            color = color+1
        print(f'Color: {color}')

def button3_callback(pin):
    global standard_brightness
    d = debounce(pin)
    if d == None:
        return
    elif not d:
        print('Button 3 pressed')
        onboard_led.value(not onboard_led.value())
        if standard_brightness == max_brightness:
            standard_brightness = 1
            pixels.brightness(standard_brightness)
        else:
            standard_brightness = standard_brightness+1
            pixels.brightness(standard_brightness)
        print(f'Brightness: {standard_brightness}')

def button4_callback(pin):
    global speed, speed_index
    d = debounce(pin)
    if d == None:
        return
    elif not d:
        print('Button 4 pressed')
        onboard_led.value(not onboard_led.value())
        speed = speeds[(speed_index+1)%len(speeds)]
        speed_index = speed_index+1
        print(speed)

btn1.irq(trigger=Pin.IRQ_FALLING, handler=button1_callback)
btn2.irq(trigger=Pin.IRQ_FALLING, handler=button2_callback)
btn3.irq(trigger=Pin.IRQ_FALLING, handler=button3_callback)
btn4.irq(trigger=Pin.IRQ_FALLING, handler=button4_callback)

#Defining the pixel indices for each strip and the body (including)
body = []
strips_left = []
strips_right = []
body.append((0,6)) #0,6
body.append((body[-1][1]+1,body[-1][1]+12))
body.append((body[-1][1]+1,body[-1][1]+12))
body.append((body[-1][1]+1,body[-1][1]+12))
strips_left.append((body[-1][1]+1, body[-1][1]+27)) #27 richtig
strips_left.append((strips_left[-1][1]+36, strips_left[-1][1]+1)) #36 verkehrt
#strips_left.append((strips_left[-1][1]+8, strips_left[-1][1]+1)) #8 von außen nach innen verkehrt
#strips_left.append((strips_left[-1][1]+1, strips_left[-1][1]+8)) #12 von innen nach außen verkehrt
strips_left.append((strips_left[-1][0]+1, strips_left[-1][0]+20)) #20
strips_left.append((strips_left[-1][1]+21, strips_left[-1][1]+1)) #21 verkehrt
strips_left.append((strips_left[-1][0]+1, strips_left[-1][0]+18)) #18 richtig
strips_right.append((strips_left[-1][1]+18, strips_left[-1][1]+1)) #18 verkehrt
strips_right.append((strips_right[-1][0]+1, strips_right[-1][0]+21)) #21 richtig
#strips_right.append((strips_right[-1][1]+12, strips_right[-1][1]+1)) #12 verkehrt
#strips_right.append((strips_right[-1][1]+1, strips_right[-1][1]+9)) #9 richtig
strips_right.append((strips_right[-1][1]+1, strips_right[-1][1]+21)) #21
strips_right.append((strips_right[-1][1]+1, strips_right[-1][1]+36)) #36 richtig
strips_right.append((strips_right[-1][1]+27, strips_right[-1][1]+1)) #27 verkehrt

strips = []
for strip in strips_left:
    strips.append(strip)
for strip in strips_right:
    strips.append(strip)

strip_lft1_clm = list(range(43,69+1))
strip_lft2_clm = list(range(70,105+1))
strip_lft2_clm.reverse()
strip_lft3_clm = list(range(114,125+1))
temp = list(range(106,113+1))
temp.reverse()
for clm in temp:
    strip_lft3_clm.append(clm)
strip_lft4_clm = list(range(126,146+1))
strip_lft4_clm.reverse()
strip_lft5_clm = list(range(147,164+1))
strips_lft_clm = [strip_lft1_clm,strip_lft2_clm,strip_lft3_clm,strip_lft4_clm,strip_lft5_clm]

strip_rgt1_clm = list(range(261,287+1))
strip_rgt1_clm.reverse()
strip_rgt2_clm = list(range(225,260+1))
strip_rgt3_clm = list(range(204,215+1))
strip_rgt3_clm.reverse()
temp = list(range(216,224+1))
temp.reverse()
for clm in temp:
    strip_rgt3_clm.append(clm)
#strip_rgt3_clm.reverse()
strip_rgt4_clm = list(range(183,203+1))
strip_rgt5_clm = list(range(165,182+1))
strip_rgt5_clm.reverse()
strips_rgt_clm = [strip_rgt1_clm,strip_rgt2_clm,strip_rgt3_clm,strip_rgt4_clm,strip_rgt5_clm]

""" TODO delete
column_left = []
column_left.append([44,106,115,147,148])
column_left.append([45,105,116,146,149])
column_left.append([46,104,117,145,150])
column_left.append([47,103,118,144,151])
column_left.append([48,102,119,143,152])
column_left.append([49,101,120,142,153])
column_left.append([50,100,121,141,154])
column_left.append([51, 99,122,140,155])
column_left.append([52, 98,123,139,156])
column_left.append([53, 97,124,138,157])
column_left.append([54, 96,125,137,158])
column_left.append([55, 95,126,136,159])
column_left.append([56, 94,107,135,160])
column_left.append([57, 93,108,134,161])
column_left.append([58, 92,109,133,162])
column_left.append([59, 91,110,132,163])
column_left.append([60, 90,111,131,164])
column_left.append([61, 89,112,130,165])
column_left.append([62, 88,113,129])
column_left.append([63, 87,114,128])
column_left.append([64, 86,    127])
column_left.append([65, 85])
column_left.append([66, 84])
column_left.append([67, 83])
column_left.append([68, 82])
column_left.append([69, 81])
column_left.append([70, 80])
column_left.append([    79])
column_left.append([    78])
column_left.append([    77])
column_left.append([    76])
column_left.append([    75])
column_left.append([    74])
column_left.append([    73])
column_left.append([    72])
column_left.append([    71])
"""

#Colors
red_hsv = (int(65536/360*0), 256, 256)
orange_hsv = (int(65536/360*39), 256, 256)
yellow_hsv = (int(65536/360*60), 256, 256)
green_hsv = (int(65536/360*120), 256, 256)
cyan_hsv = (int(65536/360*180), 256, 256)
blue_hsv = (int(65536/360*240), 256, 256)
magenta_hsv = (int(65536/360*300), 256, 256)
colors_hsv = [red_hsv, orange_hsv, yellow_hsv, green_hsv, cyan_hsv, blue_hsv, magenta_hsv]

red = pixels.colorHSV(*red_hsv) + (0,)
yellow = pixels.colorHSV(*yellow_hsv) + (0,)
green = pixels.colorHSV(*green_hsv) + (0,)
cyan = pixels.colorHSV(*cyan_hsv) + (0,)
blue = pixels.colorHSV(*blue_hsv) + (0,)
magenta = pixels.colorHSV(*magenta_hsv) + (0,)
orange = pixels.colorHSV(*orange_hsv) + (0,)
colors = [red, yellow, green, cyan, blue, magenta, orange]
white = (0,0,0,256)
color = -1

#Testing
def troubleshooting():
    i = 0
    while True:
        print('Troubleshooting')
        pixels[0:numpix] = colors[i%len(colors)]
        i = i+1
        pixels.show()
        sleep(1)

#troubleshooting()

def test2():
    bright = 5
    pixels.brightness(bright)
    for i in range(len(body)):
        #print(body[i])
        pixels[body[i][0]:body[i][1]+1] = colors[i]
    for i in range(len(strips_left)):
        #print(strips_left[i])
        pixels[strips_left[i][0]:strips_left[i][1]+1] = colors[i]
    for i in range(len(strips_right)):
        #print(strips_right[i])
        pixels[strips_right[i][0]:strips_right[i][1]+1] = colors[i]
    pixels.show()
    sleep(5)

#Rainbow colors
def get_rainbow_colors(num):
    rainbow_colors = []
    for i in range(num):
        rgbw = pixels.colorHSV(int(65534/num*i), 255, 255)
        rgbw = rgbw + (0,)
        rainbow_colors.append(rgbw)
    return rainbow_colors

def rotate(l, n):
    return l[n:] + l[:n]

"""rainbow_colors = []
for i in range(numpix): #Change so a certain number of LEDs can be passed and an array with color codes be returned
    rgbw = pixels.colorHSV(int(65534/numpix*i), 255, 255) #Full brightness!!
    rgbw = rgbw + (0,)
    rainbow_colors.append(rgbw)"""

"""
#Functions from neopixel2
pixels.set_pixel()
pixels.set_pixel_line()
pixels.set_pixel_line_gradient()
pixels.rotate_left()
pixels.rotate_right()
"""

def pulse(led_start, led_end, color, pause, duration, brightness_max):
    for i in range(brightness_max+1):
        pixels.set_pixel_line(led_start,led_end,rgb_w=color,how_bright=i)
        pixels.show()
        sleep(duration/2/brightness_max)
    sleep(pause)
    for i in range(brightness_max):
        pixels.set_pixel_line(led_start,led_end,rgb_w=color,how_bright=brightness_max-i)
        pixels.show()
        sleep(duration/2/brightness_max)

def pulse_mult(leds, pause=None, duration=None, brightness_max=max_brightness, rotate=0):
    global speed
    for i in range(brightness_max+1):
        for x in leds:
            pixels.set_pixel_line(x[0],x[1],rgb_w=x[2],how_bright=i)
        pixels.rotate_right(rotate)
        pixels.show()
        #sleep(duration/2/brightness_max) #alt, funktioniert
        sleep(speed/brightness_max)
    sleep(speed/2) #hier auch?
    for i in range(brightness_max):
        for x in leds:
            pixels.set_pixel_line(x[0],x[1],rgb_w=x[2],how_bright=brightness_max-i)
        pixels.rotate_right(rotate)
        pixels.show()
        #sleep(duration/2/brightness_max) #alt, funktioniert
        sleep(speed/brightness_max)

def outward_inward(outward=True,length=4):
    global color, speed
    
    if color == -1:
        rgbw = get_rainbow_colors(numpix)
    else:
        rgbw = colors[color]

    #sync
    longest = 36 #Anzahl Pixel des längsten Strips
    for i in range(longest+length):
        pixels.clear()
        if color == -1:
            rgbw = rotate(rgbw, random.randint(0,len(rgbw)))
        for strip in strips_lft_clm:
            if outward:
                index = i
            else:
                index = longest-i

            if index < len(strip) and index > 0:
                if color == -1:
                    pixels[strip[index]] = rgbw[index%len(rgbw)]
                else:
                    pixels[strip[index]] = rgbw

            #print(f'Strip: {strip}')
            #print(f'Index: {index}')

            #print(f'Index: {index}')
            for j in range(length):
                if outward:
                    index2 = index-j
                else:
                    index2 = index+j
                
                #print(f'Strip: {strip}')
                #print(f'Index2: {index2}')
                #print(f'Länge Strip: {len(strip)}')
                if index2 >= len(strip) or index2 < 0:
                    continue
                if color == -1:
                    pixels[strip[index2]] = rgbw[index2%len(rgbw)]
                else:
                    pixels[strip[index2]] = rgbw

        for strip in strips_rgt_clm:
            if outward:
                index = i
            else:
                index = longest-i

            if index < len(strip) and index > 0:
                if color == -1:
                    pixels[strip[index]] = rgbw[index%len(rgbw)]
                else:
                    pixels[strip[index]] = rgbw
                
            #print(f'Index: {index}')
            #print(strip)
            for j in range(length):
                if outward:
                    index2 = index-j
                else:
                    index2 = index+j

                if index2 >= len(strip) or index2 < 0:
                    continue
                if color == -1:
                    pixels[strip[index2]] = rgbw[index2%len(rgbw)]
                else:
                    pixels[strip[index2]] = rgbw
        pixels.show()
        sleep(speed)
    #TODO async?

def change_color(leds):
    color_froms = []
    for led in leds:
        print(led)
        color_froms.append(pixels[led[0]])
    for i in range(100):
        for j, led in enumerate(leds):
            led_from = led[0]
            led_to = led[1]
            color_from = color_froms[j]
            color_to = led[2]
            new_hue = int(65536/360*(rgb_to_hsv(color_from)[0] + int((rgb_to_hsv(color_to)[0]-rgb_to_hsv(color_from)[0])/100*i)))
            rgb_w = pixels.colorHSV(new_hue,256,256)
            pixels[led_from:led_to+1] = rgb_w
        pixels.show()
        #sleep(duration/100) #alt, funktioniert
        sleep(speed/100)

def rgb_to_hsv(rgb):
    #r, g, b = r/255.0, g/255.0, b/255.0
    r, g, b = rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return int(h), int(s/100*256), int(v/100*256)

def clear():
    pixels.clear()
    pixels.show()

def set_led(pixel, color, brightness=standard_brightness):
    if brightness > max_brightness:
        brightness = max_brightness
    pixels.set_pixel(pixel, color, brightness)

#Modi
def strips_random_order(seconds = 6000, amount = 1):
    global color, stopped, speed
    time_start = time.time()
    delta = 0

    while not stopped and not delta > seconds:
        pixels.clear()
        if color == -1:
            rgbw = get_rainbow_colors(numpix)
            rgbw = rotate(rgbw,random.randint(0,numpix))
        else:
            rgbw = colors[color]

        for i in range(amount):
            strip = random.randint(0,len(strips)-1)
            index_start = strips[strip][0]
            index_end = strips[strip][1]
            if index_start > index_end:
                temp = index_end
                index_end = index_start
                index_start = temp
            print(f'Strip: {strip}, {strips[strip][0]}:{strips[strip][1]}')
            if color == -1:
                for j in range(index_start,index_end+1):
                    pixels.set_pixel(j,rgbw[j])
            else:
                pixels[index_start:index_end+1] = rgbw
            #TODO Smooth an- und ausmachen mit pulse_mult?? Liste erstellen mit je index_start:index_end+1; Wenn, dann speed übergeben (??)
        
        if random.randint(0,2) == 1:
            for strip in body:
                pixels[strip[0]:strip[1]] = rgbw
                #TODO ggf auch pulsieren lassen und pulse_mult mit übergeben (s.o.)
    
        pixels.show()
        delta = time.time() - time_start
        sleep(speed)
    return
#strips_random_order(seconds = 10, amount= 3, pause=0.1)

def strips_clock(seconds = 6000, pause = 1.0, clockwise=True, keep_on=False):
    #TODO (ganze Zeit pulse_body)
    global color, stopped, speed
    time_start = time.time()
    delta = 0
    second_round = False
    while not stopped and not delta > seconds:
        if color == -1:
            rgbw = get_rainbow_colors(numpix)
            rgbw = rotate(rgbw,random.randint(0,numpix))
        else:
            rgbw = colors[color]

        for i in range(len(strips)):
            if clockwise:
                strip = len(strips)-i-1
            else:
                strip = i
            
            index_start = strips[strip][0]
            index_end = strips[strip][1]
            if index_start > index_end:
                temp = index_end
                index_end = index_start
                index_start = temp
            #print(f'Strip: {strip}, {strips[strip][0]}:{strips[strip][1]}')
            if keep_on and second_round:
                pixels[index_start:index_end+1] = (0,0,0,0)
            elif keep_on:
                if color == -1:
                    for j in range(index_start,index_end+1):
                        pixels.set_pixel(j,rgbw[j])
                else:
                    pixels[index_start:index_end+1] = rgbw
            else:
                clear()
                if color == -1:
                    for j in range(index_start,index_end+1):
                        pixels.set_pixel(j,rgbw[j])
                else:
                    pixels[index_start:index_end+1] = rgbw
                second_round = True
            pixels.show()
            sleep(speed)
        if second_round:
            second_round = False
        else:
            second_round = True
        delta = time.time() - time_start
#strips_clock(seconds = 10, pause=0.3, clockwise=False, keep_on = False)

def strips_updown(seconds = 6000, pause = 10, up=True, opposite=False):
    global color, stopped, speed
    time_start = time.time()
    delta = 0
    while not stopped and not delta > seconds:
        if color == -1:
            rgbw = get_rainbow_colors(numpix)
            rgbw = rotate(rgbw,random.randint(0,numpix))
        else:
            rgbw = colors[color]

        for i in range(len(strips_left)):
            clear()
            if opposite:
                index_right = i
            else:
                index_right = len(strips_right)-i-1
            if up:
                index_left = len(strips_left)-i-1
                index_right = i
            else:
                index_left = i

            index_start_left = strips_left[index_left][0]
            index_start_right = strips_right[index_right][0]
            index_end_left = strips_left[index_left][1]
            index_end_right = strips_right[index_right][1]
            if index_start_left > index_end_left:
                temp = index_end_left
                index_end_left = index_start_left
                index_start_left = temp
            if index_start_right > index_end_right:
                temp = index_end_right
                index_end_right = index_start_right
                index_start_right = temp
            
            if color == -1:
                for j in range(index_start_left,index_end_left+1):
                    pixels.set_pixel(j,rgbw[j])
                for j in range(index_start_right,index_end_right+1):
                    pixels.set_pixel(j,rgbw[j])
            else:
                pixels[index_start_left:index_end_left+1] = rgbw
                pixels[index_start_right:index_end_right+1] = rgbw
            pixels.show()
            sleep(speed)
        delta = time.time() - time_start
    return
#strips_updown(seconds=10, pause=0.1, up=True, opposite=False)

def rainbow(seconds = 6000, pause = 1.0):    
    global color, stopped
    time_start = time.time()
    delta = 0
    right_rotate = True
    if random.randint(0,1) == 1:
        right_rotate = False

    rgb = get_rainbow_colors(numpix)
    for i in range(numpix):
        pixels[i] = rgb[i]
        #set_led(i, rainbow_colors[i],brightness=standard_brightness)

    pixels.show()
    while not stopped and not delta > seconds:
        delta = time.time() - time_start
        if right_rotate:
            pixels.rotate_right()
        else:
            pixels.rotate_left()

        pixels.show()
        sleep(pause)
#rainbow(pause=0.01)
    
def worm(seconds = 6000):
    global color, speed
    time_start = time.time()
    delta = 0
    length = random.randint(1,20)
    amount = random.randint(1,6)
    right_rotate = True

    if random.randint(0,1) == 1:
        right_rotate = False
    for i in range(amount):
        position = int(numpix/amount*i)
        if color == -1:
            rgbw = colors[random.randint(0,len(colors)-1)]
        else:
            rgbw = colors[color]
        
        print(f'position: {position}, length: {length}')

        pixels[position:position+length] = rgbw
        pixels.show()
    
    pixels.rotate_right(80)

    while not stopped and not delta > seconds:
        if right_rotate:
            pixels.rotate_right()
        else:
            pixels.rotate_left()
        pixels.show()
        delta = time.time() - time_start
        sleep(speed)
    #self.pixels = self.pixels[num_of_pixels:] + self.pixels[:num_of_pixels]
    return
#worm(pause=0.01)

def pulse_body(seconds=6000, pause=2.0, duration=3.0, brightness_max=10, once=False):
    global color, stopped, speed
    time_start = time.time()
    delta = 0
    while not stopped and not delta > seconds:
        delta = time.time() - time_start
        lst = []
        if color == -1:
            rgbw = get_rainbow_colors(body[3][1]-body[0][0])
            for i in range(body[0][0],body[3][1]):
                lst.append((i,i+1,rgbw[i]))
        else:
            lst.append((body[0][0], body[3][1], colors[color]))
        #print(f'Seconds: {seconds}')
        pulse_mult(lst, pause, duration, brightness_max)
        if once:
            break

        """Alt, funktioniert
        rand1 = random.randint(body[0],body[1])
        rand2 = random.randint(rand1,body[1])
        rand3 = random.randint(rand2,body[1])
        lst = [(0, rand1,colors[random.randint(0,len(colors)-1)]), (rand1,rand2,colors[random.randint(0,len(colors)-1)]), (rand2,rand3,colors[random.randint(0,len(colors)-1)]), (rand3,30,colors[random.randint(0,len(colors)-1)])]
        pulse_mult(lst, pause, duration, 50)"""
#pulse_body()

def pulse_all(seconds = 6000, pause=2.0, brightness_max=10):
    global color, stopped, speed
    time_start = time.time()
    delta = 0
    
    lst = []
    
    while not stopped and not delta > seconds:
        if color == -1:
            rgbw = get_rainbow_colors(numpix)
            rgbw = rotate(rgbw,random.randint(0,numpix))
        else:
            rgbw = colors[color]

        if color == -1:
            for i in range(numpix):
                lst.append((i,i+1,rgbw[i]))
        else:
            lst.append((0,numpix,colors[color]))
        #pulse_mult(lst, pause, speed, brightness_max,rotate=random.randint(0,numpix))
        pulse_mult(lst, brightness_max,rotate=random.randint(0,numpix))
        delta = time.time() - time_start
        sleep(speed)
#pulse_all()

def firefly(seconds=6000, duration=10):
    #TODO löschen
    global color, stopped
    time_start = time.time()
    delta = 0
    while not stopped and not delta > seconds:
        delta = time.time() - time_start
        sleep(1)
    #body random die farben wechseln lassen mit change_color(body))
    return
    
def firefly_rainbow(seconds=6000, duration=10):
    #TODO löschen
    global color, stopped
    time_start = time.time()
    delta = 0
    while not stopped and not delta > seconds:
        delta = time.time() - time_start
    #noch eine function zum Wechseln der Farben des bodies und jedes Strips
    return

def explode(seconds=6000, pulses=5, pulse_random=True):
    global stopped, speed
    time_start = time.time()
    delta = 0
    while not stopped and not delta > seconds:
        if pulse_random:
            pulses = random.randint(0,10)
        for _ in range(pulses):
            pulse_body(seconds=20,once=True)
        print('Here')
        outward_inward(length=random.randint(1,10))
        #outward_inward(length=10)
        delta = time.time() - time_start
        sleep(speed)

def simply_on(seconds=6000):
    global color, speed
    time_start = time.time()
    delta = 0
    rainbow_colors = get_rainbow_colors(numpix)
    if color == -1:
        rgbw = rainbow_colors[random.randint(0,numpix)]
        pixels.set_pixel_line(0,numpix,rgbw)
    else:
        pixels.set_pixel_line(0,numpix,colors[color])

    while not stopped and not delta > seconds:
        if color == -1:
            rgbw = rainbow_colors[random.randint(0,numpix)]
            change_color([(0,numpix,rgbw)])
        else:
            rgbw = colors[color]
            pixels.set_pixel_line(0,numpix,rgbw)

        pixels.show()
        delta = time.time() - time_start
        sleep(speed)

def modes():
    global mode, shuffle, color, stopped, number_modes
    first_round = False
    while True:
        if mode > number_modes:
            mode = 0
        
        if shuffle and not first_round:
            mode = random.randint(0,number_modes) #TODO Testing
            seconds = random.randint(15*60,25*60)
        else:
            seconds = 60*60

        #mode = 9 #Testing
        #seconds = 10 #TODO Testing

        #Hier landen wir, wenn btn1 gedrückt wurde ODER der Modus nach timeout beendet wurde.
        #Nach jedem Pressen von btn1 direkt den nächsten mode anzeigen lassen?
        time_start = time.time()
        delta = 0
        if stopped:
            while delta < 10:
                pixels[strips_left[-1][0]:strips_left[-1][0]+mode+1] = red
                pixels.show()
                delta = time.time() - time_start
                sleep(0.1)
        clear()
        stopped = False

        #mode = mode_test

        if mode == 0:
            print(f'Mode{mode}')
            simply_on(seconds)
        elif mode == 1:
            print(f'Mode{mode}')
            rainbow(seconds)
        elif mode == 2:
            print(f'Mode{mode}')
            strips_updown(seconds,up=False)
        elif mode == 3:
            print(f'Mode{mode}')
            strips_updown(seconds,up=True)
        elif mode == 4:
            print('Mode4')
            strips_updown(seconds,up=False,opposite=True)
        elif mode == 5:
            print(f'Mode{mode}')
            pulse_body(seconds, duration=0.2, pause=0.2)
        elif mode == 6:
            print(f'Mode{mode}')
            pulse_all(seconds, pause=0.2)
        elif mode == 7:
            print(f'Mode{mode}')
            explode(seconds,pulse_random=True)
        elif mode == 8:
            print(f'Mode{mode}')
            explode(seconds,pulse_random=False)
        elif mode == 9:
            print(f'Mode{mode}')
            time_start = time.time()
            delta = 0
            while not stopped and not delta > seconds:
                outward_inward(outward=False)
                delta = time.time() - time_start
        elif mode == 10:
            print(f'Mode{mode}')
            worm(seconds)
        elif mode == 11:
            print(f'Mode{mode}')
        elif mode == 12:
            print(f'Mode{mode}')
            clockwise = True
            if random.randint(0,1) == 1:
                clockwise = False
            strips_clock(seconds,clockwise=clockwise)
        elif mode == 13:
            print(f'Mode{mode}')
            strips_random_order(seconds)
            
        first_round = False
        mode = mode + 1
        clear()

modes()

#Löschen?
def test():
    global stopped
    #pixels.set_pixel_line(0,10,rgb_w=yellow)
    #pixels.set_pixel_line(11,20,rgb_w=blue)
    #pixels[21:31] = red
    pixels.show()
    sleep(0.5)
    #change_color([(0,10,blue),(11,20,yellow),(21,30,green)], 10)
    while not stopped:
        line = []
        for i in range(3):
            line.append((10*i,10*i+10,colors[random.randint(0,len(colors)-1)]))
        print(line)
        #change_color([(0,10,colors[random.randint(0,len(colors)-1)])],10)
        change_color(line)
    #change_color([(0,10,blue)],10)
    stopped = False
    pixels[0:31] = white
    pixels.show()
    sleep(1)
    pixels[0:31] = yellow
    pixels.show()

    while True:
        pulse(0,10,colors[random.randint(0,len(colors)-1)],2,3,20)
        pulse(10,20,colors[random.randint(0,len(colors)-1)],2,3,20)
        pulse(20,30,colors[random.randint(0,len(colors)-1)],2,3,20)
        break

    test()

#test()