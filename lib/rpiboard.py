from os import uname
from socket import gethostname
from subprocess import check_output, Popen, PIPE

def is_rpi():
    uname = os.uname()
    if uname[4][:3] == 'arm':
        return True
    else:
        return False

def is_zero():
    if 'Zero' in rpi_board():
        return True
    else:
        return False

def rpi_board():
    try:
        file = open('/sys/firmware/devicetree/base/model', 'r')
        model = file.read()
        file.close()
    except:
        return None
    else:
        return model.rstrip('\x00')

def enable_hdmi():
    try:
        check_output(['/usr/bin/tvservice', '-p'], shell=False)
    except:
        return False
    else:
        return True

def disable_hdmi():
    try:
        check_output(['/usr/bin/tvservice', '-o'], shell=False)
    except:
        return False
    else:
        return True

def get_freemem():
    fm = Popen(['/usr/bin/free', '-h'], stdout=PIPE)
    i = 0
    freemem = {}
    while True:
        i += 1
        line = str(fm.stdout.readline())
        if i == 2:
            line = line.split()
            freemem.update({'total':line[1], 'used':line[2], 'free':line[3], 'available':line[6].strip("\\n'")})
        if i == 3:
            line = line.split()
            freemem.update({'swap':line[2]})
            return freemem

def get_diskspace():
    ds = Popen(['/bin/df', '-h', '/'], stdout=PIPE)
    i = 0
    diskspace = {}
    while True:
        i += 1
        line = str(ds.stdout.readline())
        if i == 2:
            line = line.split()
            diskspace.update({'size':line[1], 'available':line[3], 'used':line[2], 'used_percent':line[4]})
            return diskspace

def rpi_info():
    rpiinfo = {}
    runame = uname()
    cores = 0
    rpiinfo.update({'hostname':gethostname(), 'system':runame[0], 'release':runame[2], 'version':runame[3], 'machine':runame[4], 'board':rpi_board()})
    cpuinfofile = open('/proc/cpuinfo')
    for line in cpuinfofile:
        line = line.split(':')
        if line[0].startswith('Serial'):
            rpiinfo.update({'serial':line[1].strip('\n').strip()})
        elif line[0].startswith('Hardware'):
            rpiinfo.update({'hardware':line[1].strip('\n').strip()})
        elif line[0].startswith('processor'):
            cores += 1

    cpuinfofile.close()
    rpiinfo.update({'cores':cores})
    return rpiinfo



class Led(type):
    def __init__():
        check_output(['echo', 'none', '>', '/sys/class/leds/led0/trigger'], shell=False)
        check_output(['modprobe', 'ledtrig_heartbeat'], shell=False)

    def on():
        check_output(['echo', '1', '>', '/sys/class/leds/led0/brightness'], shell=False)



def status_flash():
    check_output(['echo', 'heartbeat', '>', '/sys/class/leds/led0/trigger'], shell=False)

def status_off():
    check_output(['echo', 'none', '>', '/sys/class/leds/led0/trigger'], shell=False)
    check_output(['echo', '0', '>', '/sys/class/leds/led0/brightness'], shell=False)

def status_on():
    check_output(['echo', '1', '>', '/sys/class/leds/led0/brightness'], shell=False)

def pwr_flash():
    check_output(['echo', 'heartbeat', '>', '/sys/class/leds/led1/trigger'], shell=False)

def pwr_off():
    check_output(['echo', 'none', '>', '/sys/class/leds/led1/trigger'], shell=False)
    check_output(['echo', '0', '>', '/sys/class/leds/led1/brightness'], shell=False)

def pwr_on():
    check_output(['echo', '1', '>', '/sys/class/leds/led1/brightness'], shell=False)

def cpu_temp():
    tempu = check_output(['cat', '/sys/class/thermal/thermal_zone0/temp'], shell=False)
    cel = float(tempu)/1000
    feri = cel * 1.8 + 32
    return feri // 0.1 / 10

print(is_zero())
