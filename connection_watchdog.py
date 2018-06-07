#!/usr/bin/python3

import time
import socket
import wifi

import lib.rpiboard as rpi


def host_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.shutdown(2)
    except:
        return False
    else:
        return True

def isup_internet():
    if host_port('1.1.1.1', 53) == True:
        return True
    else:
        return False

def isup_gateway():
    pass

def main():
    stled = rpi.Led('status')
    stled.ledon()
    time.sleep(60)
    if isup_internet():
        stled.ledflash()
        subprocess.Popen(['nohup', '/usr/bin/python3', '/opt/pitools/phone_home.py'], stdout=subprocess.PIPE)


if __name__ == "__main__":
    main()
