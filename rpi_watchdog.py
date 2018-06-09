#!/usr/bin/python3

from os import system
import wpa_supplicant.core
from twisted.internet.selectreactor import SelectReactor
import threading
import time
import subprocess
import logging
import argparse
from configparser import ConfigParser

import klepto
import lib.rpiboard as rpi

configfile = '/etc/remotepi.cfg'
config = ConfigParser()
config.read(configfile)

log = logging.getLogger()
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='Debug mode logging to console')
parser.add_argument('-l', '--logfile', action='store', help='Debug mode logging to file')
args = parser.parse_args()

if args.debug:
    log.setLevel(logging.DEBUG)
    console_format = logging.Formatter('%(asctime)s:[%(levelname)s]:%(name)s:%(message)s')
    log_console = logging.StreamHandler()
    log.addHandler(log_console)
    log_console.setFormatter(console_format)
    
if args.logfile:
    log_format = logging.Formatter('%(asctime)s:[%(levelname)s]:%(name)s:%(message)s')
    log.addHandler(args.logfile)
    log_fileh.setFormatter(log_format)


class WiFi(object):
    def __init__(self):
        self.wpacfg = klepto.archives.file_archive('/etc/network/.wpa_configs', serialized=True)
        self.reactor = SelectReactor()
        threading.Thread(target=self.reactor.run, kwargs={'installSignalHandlers': 0}).start()
        time.sleep(0.1)
        self.driver = wpa_supplicant.core.WpaSupplicantDriver(self.reactor)
        self.supplicant = self.driver.connect()
        try:
            self.interface = self.supplicant.create_interface('wlan0')
        except wpa_supplicant.core.InterfaceExists:
            self.interface = self.supplicant.get_interface('wlan0')
    
    def scan(self):
        return self.interface.scan(block=True)
    
    def connect_against_saved(self):
        scan_results = self.interface.scan(block=True)
        self.wpacfg.load()
        nf = False
        for bss in scan_results:
            try:
                if self.wpacfg[bss.get_ssid()]:
                    networkcfg = self.wpacfg[bss.get_ssid()]
                    configpath = self.interface.add_network(networkcfg)
                    self.interface.select_network(configpath.get_path())
                    nf = True
            except:
                pass
        if nf:
            return True
        else:
            return False
    
    def state(self):
        return self.interface.get_state()
        
    def current_stats(self):
        stats = self.interface.get_current_bss()
        return stats.to_dict()

def kill_wpasup():
    try:
        system('/usr/bin/killall wpa_supplicant')
    except:
        pass

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

def isup_gpsd():
    # FIX THIS - add check
    return True

def run_gpsd():
    subprocess.Popen(['/usr/sbin/gpsd', config.get('gps', 'port')], shell=False)

def main():
    log.DEBUG('Script is starting')
    stled = rpi.Led('status')
    stled.ledon()
    log.DEBUG('killing all wpa_supplicant processes')
    kill_wpasup()
    if config.get('gps', 'installed'):
        log.DEBUG('GPS is installed. starting gpsd')
        run_gpsd()
    else:
        log.DEBUG('GPS set to not installed in config file')
    log.DEBUG('starting WiFi instance')
    wifi = WiFi()
    while True:
        if not isup_internet():
            log.WARNING('internet DOWN detected')
            log.INFO('trying saved wireless networks')
            if wifi.connect_against_saved():
                log.INFO('saved wireless networks connection successful')
                if ifup_internet():
                    log.INFO('internet is now UP')
                    stled.ledflash()
                    log.DEBUG('sleeping...')
                    time.sleep(300)
                else:
                    time.sleep(3)
        else:
            time.sleep(60)
    if config.get('gps', 'installed'):
        if not isup_gpsd():
            log.WARNING('gpsd not running. restarting.')
            run_gpsd()

if __name__ == "__main__":
    main()



#print(wifi.current_stats())


#stats = interface.get_current_bss()
#print(stats.get_signal_dbm())
