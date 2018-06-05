
from os import system

def init():
    system('echo none > /sys/class/leds/led0/trigger')
    system('modprobe ledtrig_heartbeat')

def status_flash():
    system('echo heartbeat > /sys/class/leds/led0/trigger')

def status_off():
    system('echo none > /sys/class/leds/led0/trigger')
    system('echo 0 > /sys/class/leds/led0/brightness')

def status_on():
    system('echo 1 > /sys/class/leds/led0/brightness')

def pwr_flash():
    system('echo heartbeat > /sys/class/leds/led1/trigger')

def pwr_off():
    system('echo none > /sys/class/leds/led1/trigger')
    system('echo 0 > /sys/class/leds/led1/brightness')

def pwr_on():
    system('echo 1 > /sys/class/leds/led1/brightness')

