#!/usr/bin/python3

import socket
import paramiko
import threading
import sys

#script args
server_address = sys.argv[1]
server_port = int(sys.argv[2])
server_username = sys.argv[3]
server_password = sys.argv[4]
server_host_key = paramiko.RSAKey(filename="/home/ip/.ssh/id_rsa")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#ssh server parameters defined in the class
class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
    def check_auth_password(self, username, password):
        if username == server_username and password == server_password:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

#ssh client handler
def client_handler(client_socket,addr):
    try:
        #bind client socket to ssh server session and add rsa key
        ssh_session = paramiko.Transport(client_socket)
        ssh_session.add_server_key(server_host_key)
        server = Server()
#start the ssh server and negotiate ssh params
        try:
            ssh_session.start_server(server=server)
        except SSHException as err:
            print("[!] SSH Parameters Negotiation Failed")
        else:
            print("[*] SSH Parameters Negotiation Succeeded")
#authenticate the client
        print("[*] Authenticating")
        ssh_channel = ssh_session.accept(20)
        if ssh_channel == None or not ssh_channel.active:
            print("[*] SSH Client Authentication Failure")
            ssh_session.close()
        else:
            print("[*] SSH Client Authenticated")
#ssh channel is established. We can start the shell
            #and send commands from input
            ssh_channel.send('hostname')
            remhostname = ssh_channel.recv(1024).decode('utf-8').rstrip('\n\r ')
        while not ssh_channel.closed:
            command = input(f"<{remhostname}:{addr}>:$ ").rstrip()
            if len(command):
                if command != "exit":
                    ssh_channel.send(command)
                    print(ssh_channel.recv(1024).decode('utf-8') + '\n')
                else:
                    print("[*] Exiting")
                    try:
                        ssh_session.close()
                    except:
                        print("[!] Error closing SSH session")
                    else:
                        print("[*] SSH session closed")
    except Exception as err:
        print("[*] Caught Exception: ", str(err))
        print("[*] Exiting Script")
        try:
            ssh_session.close()
        except:
            print("[!] Error closing SSH session")
        else:
            print("[*] SSH session closed")

#ssh server bind and listen
def main():
    while True:
        try:
            server_socket.bind((server_address, server_port))
        except:
            print(f"[!] Bind Error for SSH Server using {server_address}:{server_socket.getsockname()[1]}")
            sys.exit(1)
        print(f"[*] Bind Success for SSH Server using {server_address}:{server_socket.getsockname()[1]}")
        server_socket.listen(100)
        print("[*] Listening")
#Keep ssh server active and accept incoming tcp connections
        while True:
            client_socket, addr = server_socket.accept()
            print(f"[*] Incoming TCP Connection from {addr[0]}:{addr[1]}")
            client_handler(client_socket,addr[0])

if __name__ == '__main__':
    main()
