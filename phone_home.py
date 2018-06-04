#!/usr/bin/python3

import sys
import time
import subprocess
import socket
from configparser import ConfigParser
import lib.processlock as processlock

import paramiko

processlock.lock()

configfile = '/etc/remotepi.cfg'

#log = logging.getLogger(__name__)
config = ConfigParser()
config.read(configfile)

server_host = config.get('home', 'host')
port_start = int(config.get('home', 'starting_port'))
ports_length = int(config.get('home', 'ports_length'))
port_spread = int(config.get('home', 'port_spread'))
username = config.get('home', 'username')
password = config.get('home', 'password')
longdelay = int(config.get('home', 'longdelay'))
shortdelay = int(config.get('home', 'shortdelay'))
delaylength = int(config.get('home', 'delaylength'))

server_address = socket.gethostbyname(server_host)

server_ports = list(range(port_start, port_start + (port_spread * ports_length), port_spread))
failcount = 0
#connect to the remote ssh server and recieve commands to be #executed and send back output
def ssh_command(server_address, server_port, username, password):
    #instantiate the ssh client
    client = paramiko.SSHClient()
    #optional is using keys instead of password auth
    #client.load_host_key('/path/to/file')
    #auto add key
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #connect to ssh server
    client.connect(
        server_address,
        port=server_port,
        username=username,
        password=password
    )
    #get ssh session
    client_session = client.get_transport().open_session()
    if client_session.active and not client_session.closed:
        #wait for command, execute and send result ouput
        while True:
            #use subprocess run with timeout of 30 seconds
            try:
                command = client_session.recv(1024).decode('utf-8')
                command_output = subprocess.run(
                    command, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                    timeout=30
                )
                #send back the resulting output
                if len(command_output.stderr.decode('utf-8')):
                    client_session.send(command_output.stderr.decode('utf-8'))
                elif len(command_output.stdout.decode('utf-8')):
                    client_session.send(command_output.stdout.decode('utf-8'))
                else:
                    client_session.send('null')
            except subprocess.CalledProcessError as err:
                client_session.send(str(err))
    client_session.close()
    return

while True:
    for server_port in server_ports:
        try:
            ssh_command(server_address, server_port, username, password)
        except Exception as err:
            #print(f'ERROR: {err}')
            failcount += 1
            time.sleep(30)
        else:
            failcount = 0
    if failcount >= ports_length * delaylength:
        time.sleep(longdelay*60)
    else:
        time.sleep(shortdelay*60)





