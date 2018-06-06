from subprocess import check_output, Popen, PIPE


def wifi_info():
    iwc = Popen(['/sbin/iwconfig'], stdout=PIPE)
    iwc_info = {}
    line = str(iwc.stdout.readline())
    if line.startswith('wlan0'):
        line = line.split()
        print(line)

wifi_info()


