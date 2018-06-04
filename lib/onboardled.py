
import os

os.system('echo none > /sys/class/leds/led0/trigger')

os.system('modprobe ledtrig_heartbeat')

def flash():
    os.system('echo heartbeat > /sys/class/leds/led0/trigger')

def off():
    os.system('echo none > /sys/class/leds/led0/trigger')
    os.system('echo 1 > /sys/class/leds/led0/brightness')

def on():
    os.system('echo 0 > /sys/class/leds/led0/brightness')
