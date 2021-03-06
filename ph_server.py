#!/usr/bin/python3.6

from screenutils import list_screens, Screen
from configparser import ConfigParser


configfile = '/etc/remotepi.cfg'

#log = logging.getLogger(__name__)
config = ConfigParser()
config.read(configfile)

ssh_listeners = int(config.get('home', 'ports_length'))
port_start = int(config.get('home', 'starting_port'))
port_spread = int(config.get('home', 'port_spread'))
username = config.get('home', 'username')
password = config.get('home', 'password')

listen_ports = list(range(port_start, port_start + (ssh_listeners * port_spread), port_spread))
remote = []
print(f'Spawning {ssh_listeners} SSH Listeners on ports {listen_ports}')
for i in range(ssh_listeners):
    exec(f'remote{i} = Screen("remote{i}",True)')
    exec(f'remote{i}.send_commands("bash")')
    exec(f'remote{i}.disable_logs()')
    exec(f'remote{i}.send_commands(f"python3 /opt/pitools/ph_listener.py 172.25.1.30 {listen_ports[i]} {username} {password}")')
list_screens()
