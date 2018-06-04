from configparser import ConfigParser


configfile = '/etc/remotepi.cfg'

#log = logging.getLogger(__name__)
config = ConfigParser()
config.read(configfile)

ssh_listeners = int(config.get('home', 'ports_length'))
port_start = int(config.get('home', 'starting_port'))
port_spread = int(config.get('home', 'port_spread'))

listen_ports = list(range(port_start, port_start + (ssh_listeners * port_spread), port_spread))

print('Phone Home Ports:')
print(listen_ports)
