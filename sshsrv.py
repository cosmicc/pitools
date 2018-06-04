#!/usr/bin/python3.6

from screenutils import list_screens, Screen
from configparser import ConfigParser


configfile = '/etc/remotepi.cfg'

#log = logging.getLogger(__name__)
config = ConfigParser()
config.read(configfile)

ssh_listeners = config.get('home', 'ports_length')
port_start = config.get('home', 'port_start')
port_spread = config.get('home', 'port_spread')

listen_ports = list(range(port_start, port_start + (ssh_listeners * port_spread), port_spread))
remote = []
print(f'Spawning {ssh_listeners} SSH Listeners on ports {listen_ports}')
for i in range(ssh_listeners):
    exec(f'remote{i} = Screen("remote{i}",True)')
    exec(f'remote{i}.send_commands("bash")')
    exec(f'remote{i}.enable_logs()')
    exec(f'remote{i}.send_commands(f"python3 /opt/pitools/ssh_listener.py 127.0.0.1 {listen_ports[i]} ssh sshtester!")')
list_screens()
