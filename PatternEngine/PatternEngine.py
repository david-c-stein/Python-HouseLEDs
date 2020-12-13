import Global

if Global.__MULTIPROCESSING__:
    import multiprocessing

import time
import threading
import logging
import logging.config
import random
import math
import numpy
import tween
import datetime
import image_to_numpy

RUNNING = True
FORWARD = 1
REVERSE = 2


'''
class ColorByName() :
    # https://www.rapidtables.com/web/color/RGB_Color.html
    AliceBlue =0xF0F8FF
    Amethyst =0x9966CC
    AntiqueWhite =0xFAEBD7
    Aqua =0x00FFFF
    Aquamarine =0x7FFFD4
    Azure =0xF0FFFF
    Beige =0xF5F5DC
    Bisque =0xFFE4C4
    Black =0x000000
    BlanchedAlmond =0xFFEBCD
    Blue =0x0000FF
    BlueViolet =0x8A2BE2
    Brown =0xA52A2A
    BurlyWood =0xDEB887
    CadetBlue =0x5F9EA0
    Chartreuse =0x7FFF00
    Chocolate =0xD2691E
    Coral =0xFF7F50
    CornflowerBlue =0x6495ED
    Cornsilk =0xFFF8DC
    Crimson =0xDC143C
    Cyan =0x00FFFF
    DarkBlue =0x00008B
    DarkCyan =0x008B8B
    DarkGoldenrod =0xB8860B
    DarkGray =0xA9A9A9
    DarkGreen =0x006400
    DarkKhaki =0xBDB76B
    DarkMagenta =0x8B008B
    DarkOliveGreen =0x556B2F
    DarkOrange =0xFF8C00
    DarkOrchid =0x9932CC
    DarkRed =0x8B0000
    DarkSalmon =0xE9967A
    DarkSeaGreen =0x8FBC8F
    DarkSlateBlue =0x483D8B
    DarkSlateGray =0x2F4F4F
    DarkTurquoise =0x00CED1
    DarkViolet =0x9400D3
    DeepPink =0xFF1493
    DeepSkyBlue =0x00BFFF
    DimGray =0x696969
    DodgerBlue =0x1E90FF
    FairyLight =0xFFE42D
    FairyLightNCC =0xFF9D2A
    FireBrick =0xB22222
    FloralWhite =0xFFFAF0
    ForestGreen =0x228B22
    Fuchsia =0xFF00FF
    Gainsboro =0xDCDCDC
    GhostWhite =0xF8F8FF
    Gold =0xFFD700
    Goldenrod =0xDAA520
    Gray =0x808080
    Green =0x008000
    GreenYellow =0xADFF2F
    Honeydew =0xF0FFF0
    HotPink =0xFF69B4
    IndianRed =0xCD5C5C
    Indigo =0x4B0082
    Ivory =0xFFFFF0
    Khaki =0xF0E68C
    Lavender =0xE6E6FA
    LavenderBlush =0xFFF0F5
    LawnGreen =0x7CFC00
    LemonChiffon =0xFFFACD
    LightBlue =0xADD8E6
    LightCoral =0xF08080
    LightCyan =0xE0FFFF
    LightGoldenrodYellow =0xFAFAD2
    LightGreen =0x90EE90
    LightGrey =0xD3D3D3
    LightPink =0xFFB6C1
    LightSalmon =0xFFA07A
    LightSeaGreen =0x20B2AA
    LightSkyBlue =0x87CEFA
    LightSlateGray =0x778899
    LightSlateGrey =0x778899
    LightSteelBlue =0xB0C4DE
    LightYellow =0xFFFFE0
    Lime =0x00FF00
    LimeGreen =0x32CD32
    Linen =0xFAF0E6
    Magenta =0xFF00FF
    Maroon =0x800000
    MediumAquamarine =0x66CDAA
    MediumBlue =0x0000CD
    MediumOrchid =0xBA55D3
    MediumPurple =0x9370DB
    MediumSeaGreen =0x3CB371
    MediumSlateBlue =0x7B68EE
    MediumSpringGreen =0x00FA9A
    MediumTurquoise =0x48D1CC
    MediumVioletRed =0xC71585
    MidnightBlue =0x191970
    MintCream =0xF5FFFA
    MistyRose =0xFFE4E1
    Moccasin =0xFFE4B5
    NavajoWhite =0xFFDEAD
    Navy =0x000080
    OldLace =0xFDF5E6
    Olive =0x808000
    OliveDrab =0x6B8E23
    Orange =0xFFA500
    OrangeRed =0xFF4500
    Orchid =0xDA70D6
    PaleGoldenrod =0xEEE8AA
    PaleGreen =0x98FB98
    PaleTurquoise =0xAFEEEE
    PaleVioletRed =0xDB7093
    PapayaWhip =0xFFEFD5
    PeachPuff =0xFFDAB9
    Peru =0xCD853F
    Pink =0xFFC0CB
    Plaid =0xCC5533
    Plum =0xDDA0DD
    PowderBlue =0xB0E0E6
    Purple =0x800080
    Red =0xFF0000
    RosyBrown =0xBC8F8F
    RoyalBlue =0x4169E1
    SaddleBrown =0x8B4513
    Salmon =0xFA8072
    SandyBrown =0xF4A460
    SeaGreen =0x2E8B57
    Seashell =0xFFF5EE
    Sienna =0xA0522D
    Silver =0xC0C0C0
    SkyBlue =0x87CEEB
    SlateBlue =0x6A5ACD
    SlateGray =0x708090
    SlateGrey =0x708090
    Snow =0xFFFAFA
    SpringGreen =0x00FF7F
    SteelBlue =0x4682B4
    Tan =0xD2B48C
    Teal =0x008080
    Thistle =0xD8BFD8
    Tomato =0xFF6347
    Turquoise =0x40E0D0
    Violet =0xEE82EE
    Wheat =0xF5DEB3
    White =0xFFFFFF
    WhiteSmoke =0xF5F5F5
    Yellow =0xFFFF00
    YellowGreen =0x9ACD32
'''


def Color(red, green, blue):
    return [red & 0xFF, green & 0xFF, blue & 0xFF]

def getRGB(color):
    blu = color & 0xFF
    grn = (color >> 8) & 0xFF
    red = (color >> 16) & 0xFF
    return red, grn, blu

def getColor(red, blu, grn):
    return (red << 16) | (grn << 8) | blu

def hsvToRGB(h, s, v):
    if s == 0.0:
        v *= 255
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p, q, t = int(255 * (v * (1.0 - s))), int(255 * (v * (1.0 - s * f))), int(255 * (v * (1.0 - s * (1.0 - f))))
    v *= 255
    i %= 6
    if i == 0: return v, t, p
    if i == 1: return q, v, p
    if i == 2: return p, v, t
    if i == 3: return p, q, v
    if i == 4: return t, p, v
    if i == 5: return v, p, q

def random8(min=0, max=0xFF):
    return random.randint(min, max)

def scale8(i, scale):
    return (i * scale) >> 8

def sin8(x):
    """ fast approximation : signed int8 from -127 to 127 (-0x7F to 0x7F) """
    return math.sin((x / 127) * math.pi) * 127

def cos8(x):
    """ fast approximation : signed int8 from -127 to 127 (-0x7F to 0x7F) """
    return math.cos((x / 127) * math.pi) * 127

def bound8(x):
    if x > 0xFF: return 0xFF
    if x < 0x00: return 0x00
    return x

def random8(min=0, max=0xFF):
    return random.randint(min, max)

def bound16(x):
    if x > 0xFFFF: return 0xFFFF
    if x < 0x0000: return 0x0000
    return x

def random16(minimum=0, maximum=0xFFFF):
    return random.randint(minimum, maximum)

def scale16(i, scale):
    return (int(i * scale) & 0xFFFFFFFF) >> 16

def sin16(x):
    """ fast approximation : signed int16 from -32767 to 32767 (-0x7FFF to 0x7FFF). """
    return int(math.sin((x / 32768.0) * math.pi) * 32767.0)

def cos16(x):
    """ fast approximation : signed int16 from -32767 to 32767 (-0x7FFF to 0x7FFF). """
    return int(math.cos((x / 32768.0) * math.pi) * 32767.0)

def sbound16(x):
    if x > 0xFFFF: return 0xFFFF
    if x < 0x0000: return 0x0000
    return x

def constrain(x, minimum, maximum):
    return min(maximum, max(minimum, x))

# ====================================================

# int of millisecond time
def millisTime():
    return int((time.time() * 1000)) + int(datetime.datetime.now().microsecond / 1000)

# minute float 0-1
def minute():
    a = datetime.datetime.now()
    return round(float((float(a.second) + (float(a.microsecond) / 1000000)) / 60), 4)

# microseconds float 0-1
def micros():
    return datetime.datetime.now().microsecond

# sawtooth 0 to 1 at n bps
def beatsPerSec(bps=1):
    return (float(micros()) * bps / 1000000) % 1

# sawtooth 0 to 1 at n bpm
def beatsPerMin(bpm=60):
    return (float(minute()) * bpm) % 1

# repeating sine wave   0.0000 - 1.000
def beatSine(bpm, timeOffset=0, phaseOffset=0):
    b = beatsPerMin(bpm)
    bs = math.sin(b * math.pi + phaseOffset)
    return bs

# 16 bit repeating sawtooth wave   0x0000 - 0xFFFF
def beatSawtooth16(bpm):
    return int(beatsPerMin(bpm) * 0xFFFF) & 0xFFFF

def beat16(bpm):
    return beatSawtooth16(bpm)

# 16 bit repeating sine wave   0x0000 - 0xFFFF
def beatSine16(bpm, lowest=0x0000, highest=0xFFFF, phaseOffset=0):
    b = beatsPerMin(bpm)
    bs = math.sin(b * math.pi + phaseOffset)
    bs16 = int(bs * 65535) & 0xFFFF
    w = highest - lowest
    scaledBeat = scale16(bs16, w)
    return lowest + scaledBeat

# 8 bit repeating sawtooth wave   0x0000 - 0xFFFF
def beatSawtooth8(bpm):
    return int(beatsPerMin(bpm) * 0xFF) & 0xFF

def beat8(bpm):
    return beatSawtooth8(bpm)

# 8 bit repeating sine wave   0x00 - 0xFF
def beatSine8(bpm, lowest=0x00, highest=0xFF, phaseOffset=0):
    b = beatsPerMin(bpm)
    bs = math.sin(b * math.pi + phaseOffset)
    bs8 = int(bs * 255) & 0xFF
    w = highest - lowest
    scaledBeat = scale8(bs8, w)
    return lowest + scaledBeat

def normalDistNum(center, width):
    # approximation
    alpha = 2 * math.pi * random.random()
    return int(width / 2 * math.cos(alpha) + center)

def randomColor(minBrighness=0):
    return [random8(min=minBrighness), random8(min=minBrighness), random8(min=minBrighness)]

def rainbowWheel(pos):
    r = g = b = 0x00
    # Generate rainbow colors across 0-255 positions
    if pos < 0x55:
        r = pos * 3
        g = 0xFF - pos * 3
        b = 0
    elif pos < 0xAA:
        pos -= 0x55
        r = 0xFF - pos * 3
        g = 0
        b = pos * 3
    else:
        pos -= 0xAA
        r = 0
        g = pos * 3
        b = 0xFF - pos * 3
    return Color(r, g, b)

def stepSlice(a, step):
    return [a[i::step] for i in range(step)]

def blendColor(color1, color2, overlay):
    # blend colors across 0-255 graduations
    if overlay <= 0:
        return color1
    elif overlay >= 255:
        return color2
    else:
        keep = 255 - overlay
        r = scale8(color1[0], keep) + scale8(color2[0], overlay)
        g = scale8(color1[1], keep) + scale8(color2[1], overlay)
        b = scale8(color1[2], keep) + scale8(color2[2], overlay)
        return Color(r, g, b)

def blendColorAlpha(color1, color2):
    # combine-rgba-color.js
    alpha = 1 - (1 - color2[3]) * (1 - color1[3])
    red = bound8(int((color2[0] * color2[3] / alpha) + color1[0] * color1[3] * (1 - color1[3]) / alpha))
    grn = bound8(int((color2[1] * color2[3] / alpha) + color1[1] * color1[3] * (1 - color1[3]) / alpha))
    blu = bound8(int((color2[2] * color2[3] / alpha) + color1[2] * color1[3] * (1 - color1[3]) / alpha))
    return [red & 0xFF, grn & 0xFF, blu & 0xFF, alpha]


def fadeToColor(color1, color2, percent):
    red = bound8(int((color1[0] * float(percent) / 100)) + int((color2[0] * float(100 - percent) / 100)))
    grn = bound8(int((color1[1] * float(percent) / 100)) + int((color2[1] * float(100 - percent) / 100)))
    blu = bound8(int((color1[2] * float(percent) / 100)) + int((color2[2] * float(100 - percent) / 100)))
    return Color(red, blu, grn)

def fadeToBlack(color1, percent):
    return fadeToColor(Color(0, 0, 0), color1, percent)

def fadeDownToColor(color1, color2, percent):
    if color1[0] < color2[0]:
        red = bound8(int((color1[0] * float(percent) / 100)) + int((color2[0] * float(100 - percent) / 100)))
    else:
        red = color1[0]

    if color1[1] < color2[1]:
        blu = bound8(int((color1[1] * float(percent) / 100)) + int((color2[1] * float(100 - percent) / 100)))
    else:
        blu = color1[1]

    if color1[2] < color2[2]:
        grn = bound8(int((color1[2] * float(percent) / 100)) + int((color2[2] * float(100 - percent) / 100)))
    else:
        grn = color1[2]

    return Color(red, blu, grn)

def adjBrightness(color, brightness):
    r = bound8(int(color[0] * float(brightness) / 100))
    g = bound8(int(color[1] * float(brightness) / 100))
    b = bound8(int(color[2] * float(brightness) / 100))
    return Color(r, g, b)


# =========================================================
# Patterns

class pattern_Solid(object):
    def __init__(self, leds, ledCnt, color):
        self.ledCnt = ledCnt
        self.leds = None
        self._olor = color
        self.delay = 0

    @property
    def color(self):
        return self.color

    @color.setter
    def color(self, c):
        self.color = c

    def step(self):
        for i in range(self.ledCnt):
            self.leds[i] = self.color


class pattern_Juggle(object):

    def __init__(self, leds, ledCnt, dotCnt=8, color=None, rate=0):
        if color is None:
            color = Color(200, 200, 200)
        self.leds = leds
        self.ledCnt = ledCnt
        self.rate = rate
        self.dotCnt = dotCnt
        self.color = color

        self.idx = 0
        self.delay = self.rate

    def step(self):
        if self.delay > self.rate:

            for i in range(0, self.ledCnt):
                self.leds[i] = fadeToBlack(self.leds[i], 1)

            for i in range(0, self.dotCnt):
                # self.leds[ beatSine16((i + self.dotCnt-1), lowest=0, highest=(self.ledCnt)) ] = self.color
                self.leds[beatSine16(3, lowest=0, highest=(self.ledCnt))] = self.color

            self.delay = 0
        else:
            self.delay += 1


'''
Waveform Functions

time(interval)
A sawtooth waveform between 0.0 and 1.0 that loops about every 65.536*interval seconds. e.g. use .015 for an aproximately 1 second.

wave(v)
Converts a sawtooth waveform v between 0.0 and 1.0 to a sinusoidal waveform between 0.0 to 1.0. Same as (1+sin(v*PI2))/2 but faster. v "wraps" between 0.0 and 1.0.

square(v, duty)
Converts a sawtooth waveform v to a square wave using the provided duty cycle where duty is a number between 0.0 and 1.0. v "wraps" between 0.0 and 1.0.

triangle(v)
Converts a sawtooth waveform v between 0.0 and 1.0 to a triangle waveform between 0.0 to 1.0. v "wraps" between 0.0 and 1.0.
Pixel / Color Functions

hsv(hue, saturation, value)
Sets the current pixel by calculating the RGB values based on the HSV color space. Hue "wraps" between 0.0 and 1.0. Nevative values wrap backwards.

rgb(red, green, blue)
Sets the current pixel to the RGB value provided. Values range between 0.0 and 1.0.
'''


def wave(v):
    return float((1.0 + math.sin(v * math.pi)) / 2.0) % 1


def triangle(v):
    return float(v * v) % 1


'''
regenbogendrogen
https://electromage.com/patterns/

hl = pixelCount/2

export function beforeRender(delta) {
  t1 = time(.2)
}

export function render(index) {
  c = 0.1-abs(index - hl)/hl
  c = wave(c)
  c = wave(c + t1)
  hsv(c,1,1)
}
'''


class pattern_RegenbogenDrogen(object):

    def __init__(self, leds, ledCnt, rate=5):
        self.leds = leds
        self.ledCnt = ledCnt
        self.rate = rate

        self.h1 = float(self.ledCnt / 2)

        self.delay = self.rate

    def step(self):
        if self.delay > self.rate:

            t1 = beatsPerMin(15)

            for i in range(0, self.ledCnt):
                c = 0.1 - float(abs(i - self.h1) / self.h1)
                c1 = wave(c)
                c2 = wave(c1 + t1)
                self.leds[i] = hsvToRGB(c2, 1, 1)

            self.delay = 0
        else:
            self.delay += 1


'''
fastpulse
https://electromage.com/patterns/
'''


class pattern_fastpulse(object):

    def __init__(self, leds, ledCnt, rate=0):
        self.leds = leds
        self.ledCnt = ledCnt
        self.rate = rate

        self.delay = self.rate

    def step(self):
        if self.delay > self.rate:
            t1 = beatsPerMin(30)

            for i in range(0, self.ledCnt):
                v = triangle((2 * wave(t1) + i / self.ledCnt) % 1)
                v = v * v * v * v * v
                s = v < .9
                self.leds[i] = hsvToRGB(t1, s, v)

            self.delay = 0
        else:
            self.delay += 1


'''
-------------------------
export function beforeRender(delta) {
  t1 = time(.1)
  r1 = sin(time(.1)*PI2)
  r2 = sin(time(.05)*PI2)
  r3 = sin(time(.07)*PI2)
}

export function render(index) {
  v = triangle((2*wave(t1) + index/pixelCount) %1)
  v = v*v*v*v*v
  s = v < .9
  hsvToRGB(t1,s,v)
}

export function render2D(index, x, y) {
  render3D(index, x, y, 0)
}

export function render3D(index, x, y, z) {
  v = triangle((3*wave(t1) + x*r1 + y*r2 + z*r3) %1)
  v = v*v*v*v*v
  s = v < .8
  hsvToRGB(t1,s,v)
}
'''


class pattern_Rainbow(object):

    def __init__(self, leds, ledCnt, rate=10):
        self.leds = leds
        self.ledCnt = ledCnt
        self.rate = rate

        self.idx = 0
        self.delay = self.rate

    def setRate(self, rate):
        self.rate = rate

    def getRate(self):
        return self.rate

    def step(self):
        if self.delay > self.rate:
            for i in range(0, int(self.ledCnt)):
                self.leds[i] = rainbowWheel((i + self.idx) & 0xFF)
            self.idx += 1
            if self.idx >= 256:
                self.idx = 0

            self.delay = 0
        else:
            self.delay += 1


class pattern_Confetti(object):

    def __init__(self, leds, ledCnt, color=None, bgcolor=None, count=None, rate=None):
        self.leds = leds
        self.ledCnt = ledCnt
        self.color = color
        self.bgcolor = bgcolor
        self.count = count
        self.rate = rate

        if self.bgcolor is None:
            self.bgcolor = Color(0, 0, 0)

        if self.count is None:
            self.count = 5

        self.delay = self.rate
        self.j = 0

    def setRate(self, rate):
        self.rate = rate

    def getRate(self):
        return self.rate

    def step(self):
        if self.delay > self.rate:
            for i in range(0, self.count):
                pos = random16(0, self.ledCnt - 1)

                if not self.color:
                    self.leds[pos] = randomColor(180)
                elif self.color == 'rainbow':
                    self.j += 1
                    if self.j > 0xFF:
                        self.j = 0
                    self.leds[pos] = rainbowWheel(self.j & 0xFF)
                else:
                    self.leds[pos] = self.color

            for i in range(0, self.ledCnt):
                self.leds[i] = fadeToColor(self.leds[i], self.bgcolor, 95)

            self.delay = 0
        else:
            self.delay += 1


class pattern_TheaterChase(object):

    def __init__(self, leds, ledCnt, colors, colorBG=None, direction=FORWARD, width=5, rate=40):
        if colorBG is None:
            colorBG = Color(0, 0, 0)
        self.leds = leds
        self.ledCnt = ledCnt
        self.colors = colors
        self.colorBG = colorBG
        self.direction = direction
        self.width = width
        self.rate = rate
        self.arrayColor = []

        if self.direction == FORWARD:
            cStart = 255
            cEnd = 0
        else:
            cStart = 0
            cEnd = 255

        colorList = list(tween.tween(tween.easeInOutCirc, cStart, cEnd, self.width, True, False))

        # first check to see if this is a list of colors
        if type(self.colors[0]) == list:
            for c in self.colors:
                for i in colorList:
                    self.arrayColor.append(blendColor(c, self.colorBG, bound8(i)))

        # or just a color
        elif type(self.colors) == list:
            for i in colorList:
                self.arrayColor.append(blendColor(self.colors, self.colorBG, bound8(i)))

        else:
            print("Unknown colors")

        self.sliceCnt = len(self.arrayColor)

        self.delay = self.rate
        self.idx = 0

    def step(self):

        if self.delay > self.rate:

            for i in range(0, self.sliceCnt):
                self.leds[(i + self.idx)::self.sliceCnt] = self.arrayColor[i]

            # need to fix idx for Reverse
            if self.idx < self.sliceCnt - 1:
                self.idx += 1
            else:
                self.idx = 0

            self.delay = 0
        else:
            self.delay += 1


class pattern_RunningLights(object):
    def __init__(self, leds, ledCnt, color, rate=30):
        self.leds = leds
        self.ledCnt = ledCnt
        self.color = color

        self.position = 0

        self.rate = rate
        self.delay = self.rate

    def step(self):
        if self.delay > self.rate:

            self.position += 1
            if self.position > (self.ledCnt * 2):
                self.position = 0

            for i in range(0, self.ledCnt):
                s = ((math.sin(i + self.position) * 127 + 128) / 255)
                self.leds[i] = Color(bound8(int(s * self.color[0])), bound8(int(s * self.color[1])),
                                     bound8(int(s * self.color[2])))

            self.delay = 0
        else:
            self.delay += 1


# pattern_Fire(55,120,15)
class pattern_Fire(object):
    def __init__(self, leds, ledCnt, cooling, sparking, rate=30):
        self.leds = leds
        self.ledCnt = ledCnt
        self.cooling = cooling
        self.sparking = sparking
        self.rate = rate
        self.heat = [0] * self.ledCnt
        self.delay = self.rate

    def step(self):
        if self.delay > self.rate:

            # Step 1.  Cool down every cell a little
            for i in range(0, self.ledCnt - 1):
                self.heat[i] = bound8(self.heat[i] - random8(0, ((self.cooling * 10) / self.ledCnt) + 2))

            # Step 2.  Heat from each cell drifts 'up' and diffuses a little
            for k in range(self.ledCnt - 1, 2, -1):
                self.heat[k] = (self.heat[k - 1] + self.heat[k - 2] + self.heat[k - 2]) / 3

            # Step 3.  Randomly ignite new 'sparks' near the bottom
            if random8(0, 254) < self.sparking:
                y = random8(0, 7)
                self.heat[y] = bound8(self.heat[y] + random8(160, 254))

            # Step 4.  Convert heat to LED colors
            for j in range(0, self.ledCnt - 1):

                # Scale 'heat' down from 0-255 to 0-191
                t192 = (bound8(int((self.heat[j] / 255.0) * 191)))

                # calculate ramp up from
                heatramp = t192 & 0x3F  # 0..63
                heatramp <<= 2  # scale up to 0..252

                # figure out which third of the spectrum we're in:
                # reverse the effect by switching the commented out lines in all 3 places.

                if t192 > 0x80:  # hottest
                    # self.leds[self.ledCnt - j - 1] = Color(255, 255, heatramp)
                    self.leds[j] = Color(255, 255, heatramp)
                elif t192 > 0x40:  # middle
                    # self.leds[self.ledCnt - j - 1] = Color(255, heatramp, 0)
                    self.leds[j] = Color(255, heatramp, 0)
                else:  # coolest
                    # self.leds[self.ledCnt - j - 1] = Color(heatramp, 0, 0)
                    self.leds[j] = Color(heatramp, 0, 0)

            self.delay = 0
        else:
            self.delay += 1


# meteorRain(color,10, 64, true, 30);
class pattern_MeteorRain(object):
    def __init__(self, leds, ledCnt, color, meteorSize, meteorTrailDecay, meteorRandomDecay, rate=20):
        self.leds = leds
        self.ledCnt = ledCnt
        self.color = color
        self.meteorSize = meteorSize
        self.meteorTrailDecay = meteorTrailDecay
        self.meteorRandomDecay = meteorRandomDecay
        self.meteorSize = meteorSize
        self.rate = rate
        self.delay = self.rate
        self.idx = 0

        self.tmpLed = []
        for i in range(self.ledCnt):
            self.tmpLed.append([0, 0, 0])

    def step(self):
        if self.delay > self.rate:

            # Fade leds
            for j in range(0, self.ledCnt):
                if (not self.meteorRandomDecay) or (random8(0, 10) > 5):
                    self.tmpLed[j] = fadeToBlack(self.tmpLed[j], self.meteorTrailDecay)

            # Draw meteor
            for j in range(0, self.meteorSize):
                k = self.idx - j
                if (k < self.ledCnt) and (k >= 0):
                    self.tmpLed[k] = self.color

            # Write to leds
            self.leds[:] = self.tmpLed[:]

            self.idx += 1
            if self.idx > (self.ledCnt + self.meteorTrailDecay + self.meteorSize):
                self.idx = 0

            self.delay = 0
        else:
            self.delay += 1


# bouncingBalls(color, 6)
class pattern_BouncingBalls(object):
    def __init__(self, leds, ledCnt, color, ballCnt, rate=20):
        self.leds = leds
        self.ledCnt = ledCnt
        self.color = color
        self.ballCnt = ballCnt
        self.rate = rate

        self.gravity = -9.81
        self.startHeight = 1

        self.height = [float(0.0)] * ballCnt
        self.impactVelocityStart = float(math.sqrt(-2 * self.gravity * self.startHeight))
        self.impactVelocity = [float(0.0)] * ballCnt
        self.timeSinceLastBounce = [float(0.0)] * ballCnt
        self.position = [0] * ballCnt
        self.clockTimeSinceLastBounce = [0] * ballCnt
        self.dampening = [float(0.0)] * ballCnt

        for i in range(0, self.ballCnt):
            self.clockTimeSinceLastBounce[i] = millisTime()
            self.height[i] = self.startHeight
            self.position[i] = 0
            self.impactVelocity[i] = self.impactVelocityStart
            self.timeSinceLastBounce[i] = 0
            self.dampening[i] = 0.90 - float(i) / (ballCnt * 2)

        self.delay = self.rate

    def step(self):
        if self.delay > self.rate:

            for i in range(0, self.ledCnt):
                self.leds[i] = fadeToBlack(self.leds[i], 5)

            for i in range(0, self.ballCnt):
                self.timeSinceLastBounce[i] = millisTime() - self.clockTimeSinceLastBounce[i]
                self.height[i] = 0.5 * self.gravity * (self.timeSinceLastBounce[i] / 1000 * 2.0) + self.impactVelocity[
                    i] * self.timeSinceLastBounce[i] / 1000

                if self.height[i] < 0:
                    self.height[i] = 0
                    self.impactVelocity[i] = self.dampening[i] * self.impactVelocity[i]
                    self.clockTimeSinceLastBounce[i] = millisTime()

                    if self.impactVelocity[i] < 0.01:
                        self.impactVelocity[i] = self.impactVelocityStart

                self.position[i] = int(round(self.height[i] * (self.ledCnt - 1) / self.startHeight))

                self.leds[self.position[i]] = self.color

            self.delay = 0
        else:
            self.delay += 1


class pattern_Water(object):
    """
    https://www.instructables.com/id/4000-Pixel-Animated-LED-Mural-Cheap-and-Simple/
    """

    def __init__(self, leds, ledCnt):
        self.leds = leds
        self.ledCnt = ledCnt

        self.positions = [0.25] * self.ledCnt
        self.velocities = [0] * self.ledCnt

        self.counter = 0
        self.RAND_MAX = 0xFFFFFFFF

        '''
        ORIGINAL VALUES
        self.m = 0.005                  # mass of each bead on the string
        self.T = 55.0                   # tension in the strings
        self.a = 5.0                    # distance between masses on the string
        self.gamm = 0.0185              # damping constant
        self.error = 0.0                # allows the termination to be imperfect
        self.omega = 5.0                # angular freq of driving force
        self.AMin = -self.a / 100.0
        self.AMax = self.a / 100.0
        self.A =  self.AMax / 2.0       # amplitude of driving force
        self.brightnessMax = 1000.0     # out of 1000

        self.waterStepIncrement = .0015
        '''

        self.m = 0.0075  # mass of each bead on the string
        self.T = 40.0  # tension in the strings
        self.a = 2.0  # distance between masses on the string
        self.gamm = 0.0185  # damping constant
        self.error = 0.1  # allows the termination to be imperfect
        self.omega = 5.0  # angular freq of driving force
        self.AMin = -self.a / 100.0
        self.AMax = self.a / 100.0
        self.A = self.AMax / 1.1  # amplitude of driving force
        self.brightnessMax = 1000.0  # out of 1000

        self.waterStepIncrement = .001

        self.bgColor = Color(0, 0, 250)
        self.bgDark = Color(0, 0, 175)

        # build out list of background colors
        self.cLen = 1000
        self.bgPallet = list(tween.colorTween(tween.easeLinear, self.bgDark, self.bgColor, self.cLen, True, False))
        self.gradLen = len(self.bgPallet)

        self.maxCounter = 2000
        self.counter = self.maxCounter

    def mapl(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def mapf(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def waterStep(self, tstep):
        # calculate the positions and velocities using forward euler's method

        for i in range(0, self.ledCnt):
            # calculate the force on this element based on its and its neighbors positions

            # use this to keep track of the forces contributed by tensions (i.e. the position dependent component)
            positionTerm = 0.00

            if i > 0:
                positionTerm += self.positions[i] - self.positions[i - 1]

            if i < (self.ledCnt - 1):
                positionTerm += self.positions[i] - self.positions[i + 1]

            if self.positions[i] > self.AMax:
                self.positions[i] = self.AMax

            if self.positions[i] < self.AMin:
                self.positions[i] = self.AMin

            # force as the sum of the z-component of the tensions minus the damping (gamma*v)
            force = -(self.T / self.a) * positionTerm - self.gamm * self.velocities[i]

            # update the positions and velocities

            # get new position via second order taylor expansion about current point
            self.positions[i] = self.positions[i] + (self.velocities[i] * tstep) + (
                    0.5 * (force / self.m) * tstep * tstep)

            # get new velocity via first order taylor expansion about current point
            self.velocities[i] = self.velocities[i] + ((force / self.m) * tstep)

            # assign colors according to position and motion
            j = int(self.mapf(self.positions[i], self.AMin, self.AMax, 0.0, float(self.gradLen - 1)))

            if j < 0:
                j = 0
            if j >= self.gradLen:
                j = self.gradLen - 1

            color = self.bgPallet[j]
            brightness = pow((self.mapf(math.fabs(self.positions[i]), 0, self.AMax, 0.0, self.gradLen) / self.gradLen),
                             1)

            r = bound8(int(brightness * self.bgPallet[j][0]))
            g = bound8(int(brightness * self.bgPallet[j][1]))
            b = bound8(int(brightness * self.bgPallet[j][2]))

            self.leds[i] = Color(r, g, b)

    def step(self):

        if self.counter >= self.maxCounter:
            self.counter = 0

            # perturb the water
            self.positions[random.randint(0, self.ledCnt - 1)] = self.mapf(random.random(), 0.0, 0.1, self.AMin,
                                                                           self.AMax)
            k = random.randint(0, self.ledCnt - 1)
            self.positions[k] = self.mapf(random.random(), 0.0, 0.1, self.AMin, self.AMax)

        else:
            self.counter += 1

        self.waterStep(self.waterStepIncrement)


class pattern_FromImage(object):

    def __init__(self, leds, ledCnt, fileName, mode='RGB', rate=200):
        self.leds = leds
        self.ledCnt = ledCnt
        self.filename = fileName
        self.mode = mode
        self.rate = rate

        self.image = image_to_numpy.load_image_file(self.filename, mode=self.mode)

        ''' Lets see the image '''
        # import matplotlib.pyplot as plt
        # plt.imshow(image)
        # plt.show()

        self.width, self.length, self.dim = numpy.shape(self.image)
        if self.width != self.ledCnt:
            raise Exception("Image size error")
        if self.dim == 4:
            self.transparency = [0] * self.ledCnt

        self.delay = self.rate
        self.idx = 0

    def step(self):

        if self.delay > self.rate:
            if self.idx < self.length:
                # copy image columns into led array
                for i in range(self.ledCnt):
                    self.leds[i][0] = self.image[i][self.idx][0]
                    self.leds[i][1] = self.image[i][self.idx][1]
                    self.leds[i][2] = self.image[i][self.idx][2]
                    if self.dim == 4:
                        self.transparency[i] = self.image[i][self.idx][3]

                self.idx += 1
            else:
                self.idx = 0

            self.delay = 0
        else:
            self.delay += 1


# =========================================================
# Transitions

class transition_Wipe(object):

    def __init__(self, leds, ledCnt, ledsOne, ledsTwo, direction=FORWARD, rate=20):
        self.leds = leds
        self.ledCnt = ledCnt
        self.ledsOne = ledsOne
        self.ledsTwo = ledsTwo
        self.direction = direction
        self.rate = rate

        self.delay = self.rate
        self.idx = 0

    def step(self):
        if self.delay > self.rate:
            j = self.idx
            if self.direction == REVERSE:
                j = self.ledCnt - 1 - self.idx

            for i in range(0, j - 1):
                self.leds[i] = self.ledsOne[i]

            for i in range(j, self.ledCnt):
                self.leds[i] = self.ledsTwo[i]

            self.idx += 1
            self.delay = 0
        else:
            self.delay += 1

        if self.idx < self.ledCnt:
            return True
        else:
            self.idx = 0
            return False


class transition_Fade(object):

    def __init__(self, leds, ledCnt, ledsOne, ledsTwo, direction=FORWARD, rate=15):
        self.leds = leds
        self.ledCnt = ledCnt
        self.ledsOne = ledsOne
        self.ledsTwo = ledsTwo
        self.direction = direction
        self.rate = rate

        self.fade = 0
        self.delay = self.rate

    def step(self):

        if self.delay > self.rate:

            for i in range(0, self.ledCnt):
                j = i
                if self.direction == FORWARD:
                    j = self.ledCnt - 1 - i

                    self.leds[j] = blendColor(self.ledsOne[j], self.ledsTwo[j], self.fade)

            self.fade += 1
            if self.fade >= 255:
                self.fade = 0

            self.delay = 0
        else:
            self.delay += 1

        if self.fade < 255:
            return True
        else:
            return False


class transition_FadeWipe(object):

    def __init__(self, leds, ledCnt, ledsOne, ledsTwo, direction=FORWARD, fadeWidth=40, rate=20):
        self.leds = leds
        self.ledCnt = ledCnt
        self.ledsOne = ledsOne
        self.ledsTwo = ledsTwo
        self.direction = direction
        self.width = fadeWidth
        self.rate = rate

        self.delay = self.rate

        self.idx = 0

    def step(self):

        if self.delay > self.rate:

            # |>---------->|===========================================|
            #              |..........|>---------->|===================|
            #              |...........................................|>---------->|
            # x0           0          x1   width   x2               ledCnt         x3

            # start with width off the left side
            # and finish with width off the right side

            # start with width off the side
            x0 = -self.width
            x1 = self.idx - self.width
            x2 = self.idx
            x3 = self.ledCnt + self.width

            for i in range(x0, x1 - 1):
                if 0 <= i < self.ledCnt:
                    self.leds[i] = self.ledsOne[i]

            for i in range(x1, x2 - 1):
                if 0 <= i < self.ledCnt:
                    self.leds[i] = blendColor(self.ledsOne[i], self.ledsTwo[i], (255 / self.width) * (i - x1))

            for i in range(x2, x3):
                if 0 <= i < self.ledCnt:
                    self.leds[i] = self.ledsTwo[i]

            self.idx += 1

            if x1 > x3:
                # transition complete
                self.idx = 0
                return False

            self.delay = 0
        else:
            self.delay += 1

        # transition still running
        return True


class transition_SparkleWipe(object):

    def __init__(self, leds, ledCnt, ledsOne, ledsTwo, direction=FORWARD, fadeWidth=40, rate=20):
        self.leds = leds
        self.ledCnt = ledCnt
        self.ledsOne = ledsOne
        self.ledsTwo = ledsTwo
        self.direction = direction
        self.width = fadeWidth
        self.rate = rate

        self.sparkleWidth = int(self.width * 1.5)
        self.sparkleCnt = int(self.width / 4)

        self.ledTmp1 = []
        for i in range(self.ledCnt):
            self.ledTmp1.append([0, 0, 0])

        self.ledTmp2 = []
        for i in range(self.ledCnt):
            self.ledTmp2.append([0, 0, 0])

        self.delay = self.rate

        self.idx = -self.width

    def step(self):

        if self.delay > self.rate:

            # |>---------->|===========================================|
            #              |..........|>---------->|===================|
            #              |...........................................|>---------->|
            # x0           0          x1   width   x2               ledCnt         x3

            # start with width off the left side
            # and finish with width off the right side

            x0 = -self.width
            x1 = self.idx - self.width
            x2 = self.idx
            x3 = self.ledCnt + self.width

            for i in range(x0, x1 - 1):
                if 0 <= i < self.ledCnt:
                    self.ledTmp1[i] = self.ledsOne[i]

            for i in range(x1, x2 - 1):
                if 0 <= i < self.ledCnt:
                    self.ledTmp1[i] = blendColor(self.ledsOne[i], self.ledsTwo[i], (255 / self.width) * (i - x1))

            for i in range(x2, x3):
                if 0 <= i < self.ledCnt:
                    self.ledTmp1[i] = self.ledsTwo[i]

            # add the sparkle
            for i in range(self.sparkleCnt):
                sparkle = normalDistNum(self.idx - int(self.sparkleWidth / 2), self.sparkleWidth)
                if 0 < sparkle < self.ledCnt:
                    self.ledTmp2[sparkle] = Color(0xFF, 0xFF, 0xFF)

            for i in range(0, self.ledCnt):
                self.leds[i] = self.ledTmp1[i]
                self.leds[i] = fadeDownToColor(self.leds[i], self.ledTmp2[i], 5)
                self.ledTmp2[i] = fadeToBlack(self.ledTmp2[i], 5)

            self.idx += 1

            if x1 > x3:
                # transition complete
                self.idx = 0
                return False

            self.delay = 0
        else:
            self.delay += 1

        # transition still running
        return True


class transition_None(object):

    def __init__(self, leds, ledCnt, ledsOne):
        self.leds = leds
        self.ledCnt = ledCnt
        self.ledsOne = ledsOne

    def step(self):
        self.leds[:] = self.ledsOne[:]


# =============================================================================


class pattern_Halloween(object):

    def __init__(self, leds, ledCnt, density=10, rate=10):
        self.leds = leds
        self.ledCnt = ledCnt
        self.density = density
        self.rate = rate

        self.bgColor = Color(0xFF, 0x8C, 0x00)  # dark orange    # Color(80, 0, 160)  # dark purple
        self.bgDark = adjBrightness(self.bgColor, 5)

        # build out list of background colors
        self.cLen = 100
        self.bgPallet = list(tween.colorTween(tween.easeLoop, self.bgDark, self.bgColor, self.cLen, True, False))
        self.lenBgPal = len(self.bgPallet)

        # background color index list
        self.bgMap = [0] * self.ledCnt

        # index tween to overlay
        self.p1 = list(tween.tween(tween.easeInCirc, 0, self.cLen, 100, True, False))
        self.lenP1 = len(self.p1)

        self.posStart = 300
        self.posEnd = 340

        self.delay = self.rate
        self.j = 0

    def setRate(self, rate):
        self.rate = rate

    def getRate(self):
        return self.rate

    def step(self):
        if self.delay > self.rate:

            # background
            for i in range(0, self.lenP1 - 1):
                self.bgMap[(i + self.j) % self.ledCnt] = self.p1[i]

                self.bgMap[((i + self.j) * 2) % self.ledCnt] = self.p1[i]
                self.bgMap[((i + self.j) * 2 - 1) % self.ledCnt] = self.p1[i]

                x = self.ledCnt - ((i + self.j) % self.ledCnt) - 1
                self.bgMap[x] = self.p1[i]

                x1 = self.ledCnt - (((i + self.j) * 2) % self.ledCnt) - 1
                self.bgMap[x1] = self.p1[i]
                self.bgMap[(x1 + 1) % self.ledCnt] = self.p1[i]
                self.bgMap[(x1 + 2) % self.ledCnt] = self.p1[i]
                self.bgMap[(x1 + 3) % self.ledCnt] = self.p1[i]

            for i in range(0, self.ledCnt):
                if (i < self.posStart) or (i > self.posEnd):
                    self.leds[i] = self.bgPallet[self.bgMap[i]]
                    self.leds[i] = fadeDownToColor(self.bgDark, self.leds[i], 10)

            if self.j < self.ledCnt:
                self.j += 1
            else:
                self.j = 0

            self.delay = 0
        else:
            self.delay += 1


class DisplayEngine(object):

    def __init__(self, ledArray, ledCount):
        self.ledArray = ledArray
        self.ledCount = ledCount

        size = (self.ledCount, 3)
        self.ledArrayOne = numpy.zeros(size, dtype=numpy.uint8)
        self.ledArrayTwo = numpy.zeros(size, dtype=numpy.uint8)

        self.patternOne = None
        self.patternTwo = None
        self.transition = None

        '''
        self.pRainbow = pattern_Rainbow(self.ledArray, self.ledCount, rate=2)

    def tick(self):
        self.pRainbow.step()
        '''




        #self.colors = [Color(255, 0, 0),
        #               Color(255, 255, 0),
        #               Color(0, 255, 0),
        #               Color(0, 255, 255),
        #               Color(0, 0, 255),
        #               Color(255, 0, 255)]

        # pattern list
        #self.patternOne = pattern_Solid(self.ledCount)
        #self.patternOne.leds = self.ledArrayOne
        #self.patternOne.color = Color(255, 0, 0)

        # self.patternTwo = pattern_Solid(self.ledCount)
        # self.patternTwo.leds = self.ledArrayTwo
        # self.patternTwo.color = Color(0, 255, 0)

        # self.patternOne = pattern_BouncingBalls(self.ledArrayOne, self.ledCount, Color(0xFF,0x00, 0x00), ballCnt=1, rate=20)

        # self.patternOne = pattern_TheaterChase(self.ledArrayOne, self.ledCount, Color(250, 250, 250), rate=4)


        # ---patters from images
        self.fromImage = pattern_FromImage(self.ledArray, self.ledCount, "./Media/Images/Image09.jpg", mode='RGB', rate=4)
        #self.fromImage = pattern_FromImage(self.ledArray, self.ledCount, "./Media/Images/Image02.png", mode='RGBA', rate=4)


        #self.patternOne = pattern_FromImage(self.ledArrayOne, self.ledCount, "./Media/Images/Image02.png", mode='RGBA', rate=4)
        #self.patternTwo = pattern_Rainbow(self.ledArrayTwo, self.ledCount)

        # self.pJuggle = pattern_Juggle(self.ledArray, self.ledCount)
        # self.pDrogen = pattern_RegenbogenDrogen(self.ledArray, self.ledCount)
        # self.pFastPulse = pattern_fastpulse(self.ledArray, self.ledCount)
        # self.pRainbow = pattern_Rainbow(self.ledArray, self.ledCount, rate=2)

        # self.pConfetti = pattern_Confetti(self.ledArrayTwo, self.ledCount, 'rainbow')
        # self.pConfetti = pattern_Confetti(self.ledArray, self.ledCount, Color(255,255,255), Color(100,100,100), rate=3)
        # self.pConfetti = pattern_Confetti(self.ledArray, self.ledCount, Color(180,79,2), Color(160,73,0), rate=8)

        # self.patternTwo = pattern_TheaterChase(self.ledArrayTwo, self.ledCount, Color(250,250,250)) #self.colors)
        # self.pTheater = pattern_TheaterChase(self.ledArray, self.ledCount, Color(250,250,250))

        # self.pFire = pattern_Fire(self.ledArray, self.ledCount, 55, 120, 15)
        # self.patternTwo = pattern_Water(self.ledArrayTwo, self.ledCount)
        # self.pMeteor = pattern_MeteorRain(self.ledArray, self.ledCount, Color(255,240,250), 10, 5, True, 15)
        # self.pRunningLights = pattern_RunningLights(self.ledArray, self.ledCount, Color(200,200,200))

        # self.Halloween = pattern_Halloween(self.ledArray, self.ledCount)

        # transitions
        #self.normalOne = transition_None(self.ledArray, self.ledCount, self.ledArrayOne)
        #self.normalTwo = transition_None(self.ledArray, self.ledCount, self.ledArrayTwo)
        # self.transition = transition_Wipe(self.ledArray, self.ledCount, self.+ledArrayTwo, self.ledArrayOne)
        # self.transition = transition_Fade(self.ledArray, self.ledCount, self.ledArrayOne, self.ledArrayTwo)
        # self.transition = transition_FadeWipe(self.ledArray, self.ledCount, self.ledArrayOne, self.ledArrayTwo, rate=40)
        #self.transitionOne = transition_SparkleWipe(self.ledArray, self.ledCount, self.ledArrayOne, self.ledArrayTwo, rate=2)
        #self.transitionTwo = transition_SparkleWipe(self.ledArray, self.ledCount, self.ledArrayTwo, self.ledArrayOne, rate=2)

        # self.pSolid = pattern_Solid(self.ledArrayOne, self.ledCount, Color(200, 200, 20))
        # self.pRainbow = pattern_Rainbow(self.ledArrayTwo, self.ledCount)
        # self.tFadeWipe = transition_FadeWipe(self.ledArray, self.ledCount, self.ledArrayOne, self.ledArrayTwo)
        # self.tSparkleWipe = transition_SparkleWipe(self.ledArray, self.ledCount, self.ledArrayOne, self.ledArrayTwo)


        self.pattern = 0

        self.idx = 0
        self.state = 0

    def tick(self):
        # self.pRainbow.step()

        self.fromImage.step()
        #self.Halloween.step()

        # self.patternOne.step()
        # self.normalOne.step()

        '''
        if 0 == self.state:
            if self.idx >= 200000:
                self.state += 1
                self.idx = 0
            self.patternOne.step()
            self.normalOne.step()

        elif 1 == self.state:
            self.patternOne.step()
            self.patternTwo.step()
            if not self.transitionOne.step():
                self.state += 1

        elif 2 == self.state:
            if self.idx >= 2000:
                self.state += 1
                self.idx = 0
            self.patternTwo.step()
            self.normalTwo.step()

        elif 3 == self.state:
            self.patternOne.step()
            self.patternTwo.step()
            if not self.transitionTwo.step():
                self.state += 1

        elif 4 == self.state:
            self.state = 0
            self.idx = 0

        self.idx += 1
        '''


class PatternEngine(multiprocessing.Process if Global.__MULTIPROCESSING__ else threading.Thread):

    def __init__(self, qApp, qAud, qWeb, qPat, config, sharedArrayBase, ledCount):
        if Global.__MULTIPROCESSING__:
            # -- multiprocessing
            multiprocessing.Process.__init__(self)
        else:
            # -- threading
            super(PatternEngine, self).__init__()

        self.config = config

        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing " + __file__)

        self.ledCount = ledCount
        sharedArray = numpy.ctypeslib.as_array(sharedArrayBase)
        self.ledArray = sharedArray.reshape((self.ledCount, 3))

        # message queues
        self.getMsg = qPat
        self.putMsgApp = qApp.put
        self.putMsgAud = qAud.put
        self.putMsgWeb = qWeb.put

        self.FRAMES_PER_SECOND = 60
        self.msLoopDelta = round(1.0/self.FRAMES_PER_SECOND, 4)
        self.msPrev = 0

        # display engine
        self.engine = DisplayEngine(self.ledArray, self.ledCount)

        self.running = True

    def putApp(self, data):
        # send data to app
        self.putMsgApp({'src': 'Pat', 'data': data})

    def putAud(self, data):
        # send data to audio
        self.putMsgAud({'src': 'Pat', 'data': data})

    def putWeb(self, data):
        # send data to web
        self.putMsgWeb({'src': 'Pat', 'data': data})

    def putAll(self, data):
        # send data back to audio and web
        self.putMsgApp({'src': 'Pat', 'data': data})
        self.putMsgAud({'src': 'Pat', 'data': data})
        self.putMsgWeb({'src': 'Pat', 'data': data})

    def _delay(self):
        msCurr = time.time()
        msDelta = msCurr - self.msPrev
        if 0 < msDelta < self.msLoopDelta:
            time.sleep(self.msLoopDelta - msDelta)
        self.msPrev = msCurr

    def run(self):

        # called on start() signal
        try:
            self.logger.info("Running PatternEngine process")





            # send over the list of patterns
            # ----hardcoded during development of web interface > replace with real list next  :)
            self.putWeb({'addPattern': ['Derp', 'Random', 'Rainbow', 'Theatre Chase', 'Candy Cane', 'Bounce']})






            while self.running:
                try:
                    # check for messages from the WebService
                    if not self.getMsg.empty():
                        msg = self.getMsg.get()

                        if not Global.__MULTIPROCESSING__:
                            self.getPat.task_done()

                        if (msg != None):

                            event = msg['src']
                            data = msg['data']

                            self.logger.info("Print : " + str(msg))


                    self.engine.tick()
                    self._delay()

                except Exception as e:
                    self.stop()
                    self.logger.exception(e)

        except Exception as e:
            self.logger.exception(e)

    def stop(self):
        # do cleanup
        self.running = False
        return
