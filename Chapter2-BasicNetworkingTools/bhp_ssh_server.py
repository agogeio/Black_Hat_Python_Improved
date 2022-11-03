# FOUND ON PAGE 28 of BHP

import os       #* https://docs.python.org/3/library/os.html?highlight=os#module-os
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
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'Steven') and (password == 'secret'):
            return paramiko.AUTH_SUCCESSFUL


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
        print('[+] Got a connection from ',  client, address)

"""
With the above code the server will accept an SSH connection, 
but the connection will be reset because it has nothing to do 
with it
"""
