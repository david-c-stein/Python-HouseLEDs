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
from functools import partial
import tween
import datetime
import image_to_numpy

RUNNING = True


FRAMES_PER_SECOND = 60


FORWARD = 1
REVERSE = 2
OneToTwo = 1
TwoToOne = 2


def Color(red, green, blue):
    return [red & 0xFF, green & 0xFF, blue & 0xFF]

class ColorByName(object):
    # https://www.rapidtables.com/web/color/RGB_Color.html
    AliceBlue = [0xF0, 0xF8, 0xFF]
    Amethyst = [0x99, 0x66, 0xCC]
    AntiqueWhite = [0xFA, 0xEB, 0xD7]
    Aqua = [0x00, 0xFF, 0xFF]
    Aquamarine = [0x7F, 0xFF, 0xD4]
    Azure = [0xF0, 0xFF, 0xFF]
    Beige = [0xF5, 0xF5, 0xDC]
    Bisque = [0xFF, 0xE4, 0xC4]
    Black = [0x00, 0x00, 0x00]
    BlanchedAlmond = [0xFF, 0xEB, 0xCD]
    Blue = [0x00, 0x00, 0xFF]
    BlueViolet = [0x8A, 0x2B, 0xE2]
    Brown = [0xA5, 0x2A, 0x2A]
    BurlyWood = [0xDE, 0xB8, 0x87]
    CadetBlue = [0x5F, 0x9E, 0xA0]
    Chartreuse = [0x7F, 0xFF, 0x00]
    Chocolate = [0xD2, 0x69, 0x1E]
    Coral = [0xFF, 0x7F, 0x50]
    CornflowerBlue = [0x64, 0x95, 0xED]
    Cornsilk = [0xFF, 0xF8, 0xDC]
    Crimson = [0xDC, 0x14, 0x3C]
    Cyan = [0x00, 0xFF, 0xFF]
    DarkBlue = [0x00, 0x00, 0x8B]
    DarkCyan = [0x00, 0x8B, 0x8B]
    DarkGoldenrod = [0xB8, 0x86, 0x0B]
    DarkGray = [0xA9, 0xA9, 0xA9]
    DarkGreen = [0x00, 0x64, 0x00]
    DarkKhaki = [0xBD, 0xB7, 0x6B]
    DarkMagenta = [0x8B, 0x00, 0x8B]
    DarkOliveGreen = [0x55, 0x6B, 0x2F]
    DarkOrange = [0xFF, 0x8C, 0x00]
    DarkOrchid = [0x99, 0x32, 0xCC]
    DarkRed = [0x8B, 0x00, 0x00]
    DarkSalmon = [0xE9, 0x96, 0x7A]
    DarkSeaGreen = [0x8F, 0xBC, 0x8F]
    DarkSlateBlue = [0x48, 0x3D, 0x8B]
    DarkSlateGray = [0x2F, 0x4F, 0x4F]
    DarkTurquoise = [0x00, 0xCE, 0xD1]
    DarkViolet = [0x94, 0x00, 0xD3]
    DeepPink = [0xFF, 0x14, 0x93]
    DeepSkyBlue = [0x00, 0xBF, 0xFF]
    DimGray = [0x69, 0x69, 0x69]
    DodgerBlue = [0x1E, 0x90, 0xFF]
    FairyLight = [0xFF, 0xE4, 0x2D]
    FairyLightNCC = [0xFF, 0x9D, 0x2A]
    FireBrick = [0xB2, 0x22, 0x22]
    FloralWhite = [0xFF, 0xFA, 0xF0]
    ForestGreen = [0x22, 0x8B, 0x22]
    Fuchsia = [0xFF, 0x00, 0xFF]
    Gainsboro = [0xDC, 0xDC, 0xDC]
    GhostWhite = [0xF8, 0xF8, 0xFF]
    Gold = [0xFF, 0xD7, 0x00]
    Goldenrod = [0xDA, 0xA5, 0x20]
    Gray = [0x80, 0x80, 0x80]
    Green = [0x00, 0x80, 0x00]
    GreenYellow = [0xAD, 0xFF, 0x2F]
    Honeydew = [0xF0, 0xFF, 0xF0]
    HotPink = [0xFF, 0x69, 0xB4]
    IndianRed = [0xCD, 0x5C, 0x5C]
    Indigo = [0x4B, 0x00, 0x82]
    Ivory = [0xFF, 0xFF, 0xF0]
    Khaki = [0xF0, 0xE6, 0x8C]
    Lavender = [0xE6, 0xE6, 0xFA]
    LavenderBlush = [0xFF, 0xF0, 0xF5]
    LawnGreen = [0x7C, 0xFC, 0x00]
    LemonChiffon = [0xFF, 0xFA, 0xCD]
    LightBlue = [0xAD, 0xD8, 0xE6]
    LightCoral = [0xF0, 0x80, 0x80]
    LightCyan = [0xE0, 0xFF, 0xFF]
    LightGoldenrodYellow = [0xFA, 0xFA, 0xD2]
    LightGreen = [0x90, 0xEE, 0x90]
    LightGrey = [0xD3, 0xD3, 0xD3]
    LightPink = [0xFF, 0xB6, 0xC1]
    LightSalmon = [0xFF, 0xA0, 0x7A]
    LightSeaGreen = [0x20, 0xB2, 0xAA]
    LightSkyBlue = [0x87, 0xCE, 0xFA]
    LightSlateGray = [0x77, 0x88, 0x99]
    LightSlateGrey = [0x77, 0x88, 0x99]
    LightSteelBlue = [0xB0, 0xC4, 0xDE]
    LightYellow = [0xFF, 0xFF, 0xE0]
    Lime = [0x00, 0xFF, 0x00]
    LimeGreen = [0x32, 0xCD, 0x32]
    Linen = [0xFA, 0xF0, 0xE6]
    Magenta = [0xFF, 0x00, 0xFF]
    Maroon = [0x80, 0x00, 0x00]
    MediumAquamarine = [0x66, 0xCD, 0xAA]
    MediumBlue = [0x00, 0x00, 0xCD]
    MediumOrchid = [0xBA, 0x55, 0xD3]
    MediumPurple = [0x93, 0x70, 0xDB]
    MediumSeaGreen = [0x3C, 0xB3, 0x71]
    MediumSlateBlue = [0x7B, 0x68, 0xEE]
    MediumSpringGreen = [0x00, 0xFA, 0x9A]
    MediumTurquoise = [0x48, 0xD1, 0xCC]
    MediumVioletRed = [0xC7, 0x15, 0x85]
    MidnightBlue = [0x19, 0x19, 0x70]
    MintCream = [0xF5, 0xFF, 0xFA]
    MistyRose = [0xFF, 0xE4, 0xE1]
    Moccasin = [0xFF, 0xE4, 0xB5]
    NavajoWhite = [0xFF, 0xDE, 0xAD]
    Navy = [0x00, 0x00, 0x80]
    OldLace = [0xFD, 0xF5, 0xE6]
    Olive = [0x80, 0x80, 0x00]
    OliveDrab = [0x6B, 0x8E, 0x23]
    Orange = [0xFF, 0xA5, 0x00]
    OrangeRed = [0xFF, 0x45, 0x00]
    Orchid = [0xDA, 0x70, 0xD6]
    PaleGoldenrod = [0xEE, 0xE8, 0xAA]
    PaleGreen = [0x98, 0xFB, 0x98]
    PaleTurquoise = [0xAF, 0xEE, 0xEE]
    PaleVioletRed = [0xDB, 0x70, 0x93]
    PapayaWhip = [0xFF, 0xEF, 0xD5]
    PeachPuff = [0xFF, 0xDA, 0xB9]
    Peru = [0xCD, 0x85, 0x3F]
    Pink = [0xFF, 0xC0, 0xCB]
    Plaid = [0xCC, 0x55, 0x33]
    Plum = [0xDD, 0xA0, 0xDD]
    PowderBlue = [0xB0, 0xE0, 0xE6]
    Purple = [0x80, 0x00, 0x80]
    Red = [0xFF, 0x00, 0x00]
    RosyBrown = [0xBC, 0x8F, 0x8F]
    RoyalBlue = [0x41, 0x69, 0xE1]
    SaddleBrown = [0x8B, 0x45, 0x13]
    Salmon = [0xFA, 0x80, 0x72]
    SandyBrown = [0xF4, 0xA4, 0x60]
    SeaGreen = [0x2E, 0x8B, 0x57]
    Seashell = [0xFF, 0xF5, 0xEE]
    Sienna = [0xA0, 0x52, 0x2D]
    Silver = [0xC0, 0xC0, 0xC0]
    SkyBlue = [0x87, 0xCE, 0xEB]
    SlateBlue = [0x6A, 0x5A, 0xCD]
    SlateGray = [0x70, 0x80, 0x90]
    SlateGrey = [0x70, 0x80, 0x90]
    Snow = [0xFF, 0xFA, 0xFA]
    SpringGreen = [0x00, 0xFF, 0x7F]
    SteelBlue = [0x46, 0x82, 0xB4]
    Tan = [0xD2, 0xB4, 0x8C]
    Teal = [0x00, 0x80, 0x80]
    Thistle = [0xD8, 0xBF, 0xD8]
    Tomato = [0xFF, 0x63, 0x47]
    Turquoise = [0x40, 0xE0, 0xD0]
    Violet = [0xEE, 0x82, 0xEE]
    Wheat = [0xF5, 0xDE, 0xB3]
    White = [0xFF, 0xFF, 0xFF]
    WhiteSmoke = [0xF5, 0xF5, 0xF5]
    Yellow = [0xFF, 0xFF, 0x00]
    YellowGreen = [0x9A, 0xCD, 0x32]

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

def fadeToColor(colorFrom, colorTo, percent):
    return blendColor(colorFrom, colorTo, bound8(int(percent*255)))

def fadeToBlack(color1, percent):
    return blendColor(color1, Color(0, 0, 0), bound8(int(percent*255)))

def fadeDownToColor(color1, color2, percent):

    overlay = bound8(int(percent*255))

    if overlay <= 0:
        return color1
    elif overlay >= 255:
        return color2
    else:
        if color1[0] < color2[0]:
            red = scale8(color1[0], keep) + scale8(color2[0], overlay)
            #red = bound8(int((color1[0] * float(percent) / 100)) + int((color2[0] * float(100 - percent) / 100)))
        else:
            red = color1[0]

        if color1[1] < color2[1]:
            blu = scale8(color1[1], keep) + scale8(color2[1], overlay)
            #blu = bound8(int((color1[1] * float(percent) / 100)) + int((color2[1] * float(100 - percent) / 100)))
        else:
            blu = color1[1]

        if color1[2] < color2[2]:
            grn = scale8(color1[2], keep) + scale8(color2[2], overlay)
            #grn = bound8(int((color1[2] * float(percent) / 100)) + int((color2[2] * float(100 - percent) / 100)))
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

    def __init__(self, leds, ledCnt, name, color, duration=None):
        self.ledCnt = ledCnt
        self.leds = leds
        self.name = name
        self.color = color
        self.duration = duration

    def getName(self):
        return self.name

    def step(self):
        for i in range(0, self.ledCnt):
            self.leds[i] = self.color

        if self.duration is not None:
            self.duration -= 1
            if self.duration > 0:
                return True
            else:
                return False


class pattern_Rainbow(object):

    def __init__(self, leds, ledCnt, name='Rainbow', rate=10, duration=None):
        self.leds = leds
        self.ledCnt = ledCnt
        self.name = name
        self.rate = rate
        self.duration = duration

        self.idx = 0
        self.delay = self.rate

    def getName(self):
        return self.name

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

        if self.duration is not None:
            self.duration -= 1
            if self.duration > 0:
                return True
            else:
                return False


class pattern_Confetti(object):

    def __init__(self, leds, ledCnt, name='Confetti', color=None, bgcolor=None, count=10, rate=8, duration=None):
        self.leds = leds
        self.ledCnt = ledCnt
        self.name = name
        self.color = color
        self.bgcolor = bgcolor
        self.count = count
        self.rate = rate
        self.duration = duration

        if self.bgcolor is None:
            self.bgcolor = Color(0, 0, 0)

        self.delay = self.rate
        self.j = 0

    def getName(self):
        return self.name

    def step(self):
        if self.delay > self.rate:
            for i in range(0, self.count):
                pos = random16(0, self.ledCnt - 1)

                if not self.color:
                    self.leds[pos] = randomColor(180)
                elif self.color == 'rainbow':
                    self.j += 1
                    if self.j > (255 * 4):
                        self.j = 0
                    self.leds[pos] = rainbowWheel((self.j/4) & 0xFF)
                else:
                    self.leds[pos] = self.color

            for i in range(0, self.ledCnt):
                self.leds[i] = blendColor(self.leds[i], self.bgcolor, 10)   # range 0-254

            self.delay = 0
        else:
            self.delay += 1

        if self.duration is not None:
            self.duration -= 1
            if self.duration > 0:
                return True
            else:
                return False


class pattern_TheaterChase(object):

    def __init__(self, leds, ledCnt, name, color, colorBG=None, direction=FORWARD, width=6, rate=40, duration=None):
        if colorBG is None:
            colorBG = Color(0, 0, 0)
        self.leds = leds
        self.ledCnt = ledCnt
        self.name = name
        self.color = color
        self.colorBG = colorBG
        self.direction = direction
        self.width = width
        self.rate = rate
        self.duration = duration

        self.arrayColor = []

        if self.direction == FORWARD:
            cStart = 255
            cEnd = 0
        else:
            cStart = 0
            cEnd = 255

        colorList = list(tween.tween(tween.easeLinear, cStart, cEnd, self.width, True, False))

        # first check to see if this is a list of color
        if type(self.color[0]) == list:
            for c in self.color:
                for i in colorList:
                    self.arrayColor.append(blendColor(c, self.colorBG, bound8(i)))

        # or just a color
        elif type(self.color) == list:
            for i in colorList:
                self.arrayColor.append(blendColor(self.color, self.colorBG, bound8(i)))

        else:
            print("Unknown color")

        self.sliceCnt = len(self.arrayColor)

        self.delay = self.rate
        self.idx = 0

    def getName(self):
        return self.name

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

        if self.duration is not None:
            self.duration -= 1
            if self.duration > 0:
                return True
            else:
                return False


class pattern_RunningLights(object):
    def __init__(self, leds, ledCnt, name, color, rate=30, duration=None):
        self.leds = leds
        self.ledCnt = ledCnt
        self.name = name
        self.color = color
        self.duration = duration

        self.position = 0
        self.rate = rate
        self.delay = self.rate

    def getName(self):
        return self.name

    def step(self):
        if self.delay > self.rate:
            self.position += 1
            if self.position > (self.ledCnt * 2):
                self.position = 0

            for i in range(0, self.ledCnt):
                s = (((math.sin(i + self.position) * 127) + 128) / 255)
                self.leds[i] = Color(bound8(int(s * self.color[0])),
                                     bound8(int(s * self.color[1])),
                                     bound8(int(s * self.color[2])))
            self.delay = 0
        else:
            self.delay += 1

        if self.duration is not None:
            self.duration -= 1
            if self.duration > 0:
                return True
            else:
                return False


class pattern_FromImage(object):

    def __init__(self, leds, ledCnt, name, fileName, mode='RGB', rate=200, duration=None):
        self.leds = leds
        self.ledCnt = ledCnt
        self.name = name
        self.filename = fileName
        self.mode = mode
        self.rate = rate
        self.duration = duration

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

    def getName(self):
        return self.name

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

        if self.duration is not None:
            self.duration -= 1
            if self.duration > 0:
                return True
            else:
                return False


# =========================================================
# Transitions

class transition_Wipe(object):

    def __init__(self, leds, ledCnt, ledArrayOne, ledArrayTwo, name='Wipe', direction=FORWARD, rate=20):
        self.leds = leds
        self.ledCnt = ledCnt
        self.arrayOne = ledArrayOne
        self.arrayTwo = ledArrayTwo
        self.name = name
        self.direction = direction
        self.rate = rate

        self.delay = self.rate
        self.idx = 0

    def getName(self):
        return self.name

    def step(self):
        if self.delay > self.rate:
            j = self.idx
            if self.direction == REVERSE:
                j = self.ledCnt - 1 - self.idx

            for i in range(0, j - 1):
                self.leds[i] = self.arrayOne[i]

            for i in range(j, self.ledCnt):
                self.leds[i] = self.arrayTwo[i]

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

    def __init__(self, leds, ledCnt, ledArrayOne, ledArrayTwo, name='Fade', transition=OneToTwo, rate=1):
        self.leds = leds
        self.ledCnt = ledCnt
        self.transition = transition
        self.name = name
        self.rate = rate

        if self.transition == TwoToOne:
            self.arrayOne = ledArrayTwo
            self.arrayTwo = ledArrayOne
        else:
            self.arrayOne = ledArrayOne
            self.arrayTwo = ledArrayTwo

        self.fade = 0
        self.delay = self.rate

    def getName(self):
        return self.name

    def step(self):

        if self.delay > self.rate:

            for i in range(0, self.ledCnt):
                self.leds[i] = blendColor(self.arrayOne[i], self.arrayTwo[i], self.fade)

            self.fade += 1
            self.delay = 0
        else:
            self.delay += 1

        if self.fade <= 254:
            return True
        else:
            return False


class transition_FadeWipe(object):

    def __init__(self, leds, ledCnt, ledArrayOne, ledArrayTwo, name='FadeWipe', transition=OneToTwo, direction=FORWARD, fadeWidth=40, rate=20):
        self.leds = leds
        self.ledCnt = ledCnt
        self.name = name
        self.transition = transition
        self.direction = direction
        self.width = fadeWidth
        self.rate = rate

        if self.transition == TwoToOne:
            self.arrayOne = ledArrayOne
            self.arrayTwo = ledArrayTwo
        else:
            self.arrayOne = ledArrayTwo
            self.arrayTwo = ledArrayOne

        self.delay = self.rate

        self.idx = 0

    def getName(self):
        return self.name

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
                    self.leds[i] = self.arrayOne[i]

            for i in range(x1, x2 - 1):
                if 0 <= i < self.ledCnt:
                    self.leds[i] = blendColor(self.arrayOne[i], self.arrayTwo[i], (255 / self.width) * (i - x1))

            for i in range(x2, x3):
                if 0 <= i < self.ledCnt:
                    self.leds[i] = self.arrayTwo[i]

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

    def __init__(self, leds, ledCnt, ledArrayOne, ledArrayTwo, name='SparkleWipe', transition=OneToTwo, direction=FORWARD, fadeWidth=40, rate=20):
        self.leds = leds
        self.ledCnt = ledCnt
        self.name = name
        self.transition = transition
        self.direction = direction
        self.width = fadeWidth
        self.rate = rate

        if self.transition == TwoToOne:
            self.arrayOne = ledArrayOne
            self.arrayTwo = ledArrayTwo
        else:
            self.arrayOne = ledArrayTwo
            self.arrayTwo = ledArrayOne

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

    def getName(self):
        return self.name

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
                    self.ledTmp1[i] = self.arrayOne[i]

            for i in range(x1, x2 - 1):
                if 0 <= i < self.ledCnt:
                    self.ledTmp1[i] = blendColor(self.arrayOne[i], self.arrayTwo[i], (255 / self.width) * (i - x1))

            for i in range(x2, x3):
                if 0 <= i < self.ledCnt:
                    self.ledTmp1[i] = self.arrayTwo[i]

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

    def __init__(self, leds, ledCnt, ledArray, name='None'):
        self.leds = leds
        self.ledCnt = ledCnt
        self.ledArray = ledArray
        self.name = name

    def getName(self):
        return self.name

    def step(self):
        self.leds[:] = self.ledArray[:]


# =============================================================================


class DisplayEngine(object):

    def __init__(self, logger, ledArray, ledCount):
        self.logger = logger
        self.ledArray = ledArray
        self.ledCount = ledCount

        size = (self.ledCount, 3)
        self.ledArrayOne = numpy.zeros(size, dtype=numpy.uint8)
        self.ledArrayTwo = numpy.zeros(size, dtype=numpy.uint8)


        '''
        self.color = [Color(255, 0, 0),
                       Color(255, 255, 0),
                       Color(0, 255, 0),
                       Color(0, 255, 255),
                       Color(0, 0, 255),
                       Color(255, 0, 255)]
        '''

        self.patternList = [
            partial(pattern_Solid, name='Red', color=ColorByName.Red, duration=1000), # duration=(FRAMES_PER_SECOND*10)),
            partial(pattern_Solid, name='OrangeRed', color=ColorByName.OrangeRed, duration=1000), # duration=(FRAMES_PER_SECOND*10)),
            partial(pattern_Solid, name='Orange', color=ColorByName.Orange, duration=1000), # duration=(FRAMES_PER_SECOND*10)),
            partial(pattern_Solid, name='Yellow', color=ColorByName.Yellow, duration=1000), # duration=(FRAMES_PER_SECOND*10)),
            partial(pattern_Solid, name='YellowGreen', color=ColorByName.YellowGreen, duration=1000), # duration=(FRAMES_PER_SECOND*10)),
            partial(pattern_Solid, name='Green', color=ColorByName.Green, duration=1000), # duration=(FRAMES_PER_SECOND*10)),
            partial(pattern_RunningLights, name='WhiteRunningLights', color=ColorByName.WhiteSmoke, rate=12, duration=2000), # duration=(FRAMES_PER_SECOND*10)),
            partial(pattern_TheaterChase, name='WhiteTheaterChase', color=ColorByName.WhiteSmoke, rate=12, duration=2000), # duration=(FRAMES_PER_SECOND*10)),
            partial(pattern_Rainbow, rate=4, duration=4000), # duration=(FRAMES_PER_SECOND*10)),
            partial(pattern_Confetti, name='RainbowConfetti', color='rainbow', count=10, rate=4, duration=4000), # duration=(FRAMES_PER_SECOND*10)),
            partial(pattern_Confetti, name='WhiteConfetti', color=ColorByName.White, bgcolor=ColorByName.Black, rate=4, duration=4000), # duration=(FRAMES_PER_SECOND*10)),
            partial(pattern_FromImage, name='ColorWaves', fileName="./Media/Images/ColorWaves.jpg", mode='RGB', rate=6, duration=6000), # duration=(FRAMES_PER_SECOND*10)),
            partial(pattern_FromImage, name='PasteleDots', fileName="./Media/Images/PasteleDots.jpg", mode='RGB', rate=6, duration=6000), # duration=(FRAMES_PER_SECOND*10)),
        ]

        self.patternLen = len(self.patternList)
        self.indexOne = random.randint(0, self.patternLen-1)
        self.indexTwo = random.randint(0, self.patternLen-1)

        self.patternOne = self.patternList[self.indexOne](self.ledArrayOne, self.ledCount)
        self.patternTwo = self.patternList[self.indexTwo](self.ledArrayTwo, self.ledCount)

        self.normalOne = transition_None(self.ledArray, self.ledCount, self.ledArrayOne)
        self.normalTwo = transition_None(self.ledArray, self.ledCount, self.ledArrayTwo)

        self.transOneToTwo = transition_FadeWipe(self.ledArray, self.ledCount, self.ledArrayOne, self.ledArrayTwo, transition=OneToTwo, direction=FORWARD, rate=1)
        self.transTwoToOne = transition_FadeWipe(self.ledArray, self.ledCount, self.ledArrayOne, self.ledArrayTwo, transition=TwoToOne, direction=FORWARD, rate=1)

        self.idx = 0
        self.state = 0
        self.prevState = -1


        self.__PATTERN_TESTING__ = False
        if self.__PATTERN_TESTING__:
            self.patternOne = self.patternList[12](self.ledArrayOne, self.ledCount)


    def tick(self):

        if self.__PATTERN_TESTING__:
            self.patternOne.step()
            self.normalOne.step()
        else:

            # Play Pattern One
            if 0 == self.state:
                if not self.patternOne.step():
                    self.state += 1
                    self.idx = -1
                self.normalOne.step()

            # Transition to Two
            elif 1 == self.state:
                self.patternOne.step()
                self.patternTwo.step()
                if not self.transOneToTwo.step():
                    self.state += 1

            # Pattern One no longer visible - change pattern
            elif 2 == self.state:
                self.indexOne = random.randint(0, self.patternLen-1)
                self.patternOne = self.patternList[self.indexOne](self.ledArrayOne, self.ledCount)
                self.logger.info(" Pattern change to " + self.patternOne.getName())
                self.state += 1

            # Play Pattern Two
            elif 3 == self.state:
                if not self.patternTwo.step():
                    self.state += 1
                    self.idx = -1
                self.normalTwo.step()

            # Transition to One
            elif 4 == self.state:
                self.patternOne.step()
                self.patternTwo.step()
                if not self.transTwoToOne.step():
                    self.state += 1

            # Pattern Two no longer visible - change pattern
            elif 5 == self.state:
                self.indexTwo = random.randint(0, self.patternLen-1)
                self.patternTwo = self.patternList[self.indexTwo](self.ledArrayTwo, self.ledCount)
                self.logger.info(" Pattern change to " + self.patternTwo.getName())
                self.state += 1

            elif 6 == self.state:
                self.state = 0
                self.idx = -1

            self.idx += 1

            if self.state != self.prevState:
                self.prevState = self.state
                self.logger.info("  >>>>> Display State: " + str(self.state))


    def getPatterns(self):
        patternNames = []
        for i in range(self.patternLen):
            self.pat = self.patternList[i](self.ledArrayOne, self.ledCount)
            patternNames.append(self.pat.getName())
        return patternNames

    def setPattern(self, name):
        self.logger.info(" <<< Set Pattern: " + name)


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

        self.msLoopDelta = round(1.0/FRAMES_PER_SECOND, 4)
        self.msPrev = 0

        # display engine
        self.engine = DisplayEngine(self.logger, self.ledArray, self.ledCount)

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

    def _frame_delay(self):
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
            self.putWeb({'addPattern': self.engine.getPatterns()})

            displayActive = False
            forceActive = False

            while self.running:
                try:
                    # check for messages from the WebService
                    if not self.getMsg.empty():
                        msg = self.getMsg.get()

                        if not Global.__MULTIPROCESSING__:
                            self.getPat.task_done()

                        if (msg != None):

                            src = msg['src']
                            data = msg['data']

                            self.logger.info("PatternEngine : " + str(msg))

                            if src == 'Web':
                                if 'selectPattern' in data:
                                    self.engine.setPattern(data['selectPattern'])

                                elif 'displayOn' in data:
                                    displayActive = data['displayOn']

                                elif 'forceOn' in data:
                                    self.logger.info("from APP : FORCEON " + str(data['forceOn']))
                                    forceActive = data['forceOn']

                            if src == 'App':
                                if 'displayOn' in data:
                                    displayActive = data['displayOn']

                            # clear display array
                            if not displayActive:
                                for i in range(self.ledCount):
                                    self.ledArray[i] = ColorByName.Black
                                        
                    if displayActive or forceActive:
                        self.engine.tick()
                        self._frame_delay()

                except Exception as e:
                    self.stop()
                    self.logger.exception(e)

        except Exception as e:
            self.logger.exception(e)

    def stop(self):
        # do cleanup
        self.running = False
        return
