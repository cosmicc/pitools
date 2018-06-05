
import os
from socket import gethostname


def is_rpi():
    uname = os.uname()
    if uname[4][:3] == 'arm':
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

def rpi_info():
    rpiinfo = {}
    uname = os.uname()
    rpiinfo.update({'hostname':gethostname(), 'system':uname[0], 'release':uname[2], 'version':uname[3], 'machine':uname[4], 'board':rpi_board()})
    return rpiinfo


def main():

    import colorama

    if is_rpi():
        model = rpi_board()
        print('This IS a Raspberry Pi')
        print('RPi Board: ',model)
    else:
        print('This is NOT a Raspberry Pi')

    uname = rpi_info()
    print('Hostname: ',uname['hostname'])
    print('Sysname: ',uname['system'])
    print('Release: ',uname['release'])
    print('Version: ',uname['version'])
    print('Machine: ',uname['machine'])

if __name__ == '__main__':
    main()





