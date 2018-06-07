import klepto


ssid = 'Galaxy'
psk = 'shakedownstreet'
key_mgmt = 'WPA-PSK'

networkcfg = {'psk':psk, 'ssid':ssid, 'key_mgmt':key_mgmt}


wpacfg = klepto.archives.file_archive('.wpa_configs', serialized=True)
wpacfg[ssid] = networkcfg
wpacfg.dump()
