# FOUND ON PAGE 26 of BHP
"""
https://docs.paramiko.org/en/stable/
https://github.com/paramiko/paramiko/tree/main/paramiko

Paramiko is a pure-Python [1] (2.7, 3.4+) implementation of the SSHv2 protocol [2], 
providing both client and server functionality. It provides the foundation for the 
high-level SSH library Fabric, which is what we recommend you use for common client 
use-cases such as running remote shell commands or transferring files.
"""

"""
Side lesson on OpenSSH for Ubuntu
https://www.openssh.com/
https://ubuntu.com/server/docs/service-openssh
https://help.ubuntu.com/community/SSH
https://help.ubuntu.com/community/SSH/OpenSSH/ConnectingTo
"""

import getpass #* https://docs.python.org/3/library/getpass.html
import paramiko 

def ssh_command(ip, port, user, passwd, cmd):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    #* https://docs.paramiko.org/en/stable/api/client.html#paramiko.client.SSHClient.set_missing_host_key_policy (line above)
    ssh_client.connect(ip, port=port, username=user, password=passwd)

    _, stdout, stderr = ssh_client.exec_command(cmd)
    # print(type(stdout)) #* This shows that the output is a file type and that's why we're using readlines()
    # print(type(stderr)) #* This shows that the output is a file type and that's why we're using readlines()
    #* https://docs.paramiko.org/en/stable/api/client.html#paramiko.client.SSHClient.exec_command (explain the tuple returned by exec_command)
    #* https://www.w3schools.com/python/python_tuples.asp - "Tuples are used to store multiple items in a single variable."

    output = stdout.readlines() + stderr.readlines()

    if output:
        print("**** output ****")
        for line in output:
            print(line.strip())

if __name__ == '__main__':
    user = input('Username: ')
    password = getpass.getpass()
    ip = input('Enter server IP: ') or '192.168.1.100'
    port = input('Enter port or <CR>: ') or 22
    cmd = input('Enter command or <CR>: ') or 'id'
    ssh_command(ip, port, user, password, cmd)

