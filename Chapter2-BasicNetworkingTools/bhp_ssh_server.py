# FOUND ON PAGE 28 of BHP

import os           #* https://docs.python.org/3/library/os.html?highlight=os#module-os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__)) #* https://docs.python.org/3/library/os.path.html#os.path.realpath
# print(__file__)
RSA_KEY_FILE = 'id_rsa.key'
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD,RSA_KEY_FILE))

class Server (paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind ==  'session':
            return paramiko.OPEN_SUCCEEDED
            #* https://docs.paramiko.org/en/stable/api/server.html 
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED 
        #* https://docs.paramiko.org/en/stable/api/server.html 
        #* OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED is an error code

    def check_auth_password(self, username, password):
        if (username == 'user') and (password == 'secret'):
            return paramiko.AUTH_SUCCESSFUL
            #* https://docs.paramiko.org/en/stable/api/server.html


#* https://www.delftstack.com/howto/python/get-ip-address-python/
#* Cover how to get IP addressed automatically 

if __name__ == '__main__':
    server = '192.168.1.100'
    ssh_port = 2222

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind((server,ssh_port))
        sock.listen(100)
        print(f'[+] Listening for connection on {ssh_port}...')
        client, address = sock.accept()
    except Exception as e:
        print(f'[-] Listen failed: ' + str(e))
    else:
        print('[+] Got a connection from ',  address)

"""
With the above code the server will accept an SSH connection, 
but the connection will be reset because it has nothing to do 
with it
"""

bhp_ssh_session =  paramiko.Transport(client)
bhp_ssh_session.add_server_key(HOSTKEY)
server = Server()
bhp_ssh_session.start_server(server=server)

chan = bhp_ssh_session.accept(20)
if chan is None:
    print('**** No Channel ****')
    sys.exit(1)

print('[+] Authenticated!')
print(chan.recv(1024))
chan.send("Welcome to the bhp_ssh_server")

try:
    while True:
        command = input('Enter a command: ')
        if command != 'exit':
            chan.send(command)
            rcv = chan.recv(8192)
            print(rcv.decode())
        else:
            chan.send('exit')
            print('Exiting')
            bhp_ssh_session.close()
            break
except Exception as e:
    bhp_ssh_session.close()
