import wpa_supplicant.core
from twisted.internet.selectreactor import SelectReactor
import threading
import time

import klepto
import lib.rpiboard as rpi


class WiFi(object):
    def __init__(self):
        self.wpacfg = klepto.archives.file_archive('.wpa_configs', serialized=True)
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


stled = rpi.Led('status')
stled.ledon()

wifi = WiFi()

if wifi.connect_against_saved():
    #check if connected to internet
    stled.ledflash()

print(wifi.current_stats())


#stats = interface.get_current_bss()
#print(stats.get_signal_dbm())
