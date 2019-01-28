"""

  NeoPixel status led functions

"""

import time
from neopixel import *
import threading

LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


class statusLed():
    black = Color(0, 0, 0)
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    blue = Color(0, 0, 255)
    white = Color(255, 255, 255)
    def __init__(self, led_pin, brightness):
        self.brightness = brightness
        strip = Adafruit_NeoPixel(1, led_pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, brightness, LED_CHANNEL)
        self.blinking = False
        self.strip = strip
        self.strip.begin()
        self.strip.setPixelColor(0, statusLed.black)
        self.strip.setBrightness(20)
        self.strip.show()
        self.strip.setPixelColor(0, statusLed.white)
        self.strip.show()
        time.sleep(.2)
        self.strip.setPixelColor(0, statusLed.black)
        self.strip.setBrightness(self.brightness)
        self.strip.show()
    def color(self, color, chgbright=-1):
        self.blinking = False
        self.strip.setPixelColor(0, color)
        if chgbright != -1:
            self.strip.setBrightness(chgbright)
        self.strip.show()
    def off(self):
        self.blinking = False
        self.strip.setPixelColor(0, statusLed.black)
        self.strip.show()
    def resetbrightness(self):
        self.strip.setBrightness(self.brightness)
        self.strip.show()
    def setbrightness(self, chgbright):
        self.strip.setBrightness(chgbright)
        self.strip.show()
    def stopblink(self):
        self.blinking = False
        self.strip.setPixelColor(0, statusLed.black)
        self.strip.show()
    def blink(self, color, fast=False):
        self.blinking = True
        if fast:
            self.blinkrate = 0
        else:
            self.blinkrate = .5
        def blinkthread(self, color):
            self.strip.setPixelColor(0, color)
            def blinkit(self, bright):
                self.strip.setBrightness(bright)
                self.strip.show()
                time.sleep(.1)
            while self.blinking:
                blinkit(self, self.brightness)
                blinkit(self, int(self.brightness/2))
                #blinkit(self, int(self.brightness/4))
                blinkit(self, 0)
                time.sleep(self.blinkrate)
                #blinkit(self, int(self.brightness/4))
                blinkit(self, int(self.brightness/2))
            self.strip.setPixelColor(0, statusLed.black)
            self.strip.setBrightness(self.brightness)
            self.strip.show()

        bthread = threading.Thread(target=blinkthread, args=(self, color))
        bthread.start()
