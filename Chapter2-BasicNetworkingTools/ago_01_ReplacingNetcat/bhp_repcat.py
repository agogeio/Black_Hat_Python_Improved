# FOUND ON PAGE 13 of BHP
# There has been significant changes to this netcat repacement as compaired to the BHP book

import argparse     
# https://docs.python.org/3.10/library/argparse.html?highlight=argparse
import os           
# https://docs.python.org/3.10/library/os.html
import socket       
# https://docs.python.org/3.10/library/socket.html?highlight=socket#module-socket
import shlex        
# https://docs.python.org/3.10/library/shlex.html?highlight=shlex
import subprocess   
# https://docs.python.org/3.10/library/subprocess.html?highlight=subprocess
import sys          
# https://docs.python.org/3.10/library/sys.html?highlight=sys#module-sys
import textwrap     
# https://docs.python.org/3.10/library/textwrap.html?highlight=textwrap
import threading    
# https://docs.python.org/3.10/library/threading.html?highlight=threading#module-threading


class RepCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # SO_REUSEADDR = http://www.unixguide.net/network/socketfaq/4.11.shtml
        # SOL_SOCKET = https://www.gnu.org/software/libc/manual/html_node/Socket_002dLevel-Options.html
        # The SOL_SOCKET link is a good explination for both options


    #! This was a bug in the book, the book did not have the "self" argument first
    def execute(self, cmd):
        cmd = cmd.strip()
        if not cmd:
            return

        # print(shlex.split(cmd))
        is_cd = cmd.split(' ')
        cmd_to_exec = is_cd[0]

        if cmd_to_exec == 'cd':
            cd_path = is_cd[1] or '/home/'
            os.chdir(cd_path)

            
        if cmd_to_exec == 'cat':
            # https://docs.python.org/3.10/library/subprocess.html?highlight=subprocess%20run#subprocess.run (below)
            # had to use different subprocess.run settings for the cat command
            cat_result = subprocess.run(shlex.split(cmd), capture_output=True, text=True)

            if cat_result.returncode == 0:
                return cat_result.stdout + '\n'
            else:
                return cat_result.stderr


        # process_data = subprocess.Popen(shlex.split(cmd), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        # *** TESTING CONVERING EVERYTHING TO subprocess.run() *** 
        process_data = subprocess.run(shlex.split(cmd), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        # print(process_data)
        # output, error = process_data.communicate()
        
        if process_data.returncode == 0:
            return process_data.stdout
            # return output
        else:
            return process_data.stderr
            # return error
        
        #! Origional code from the book
        # output = subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT, shell=True)
        # return output.decode()


    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()


    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
            
        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096) #* https://docs.python.org/3/library/socket.html#socket.socket.recv
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    buffer = input('RepCat# > ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('User terminated the session')
            self.socket.close()
            sys.exit()


    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()


    def handle(self, client_socket):
        if self.args.execute:
            print(f'In handle {self.args.execute}')
            output = self.execute(self.args.execute)
            client_socket.send(output.encode())
            
        elif self.args.upload:
            print(f'In upload {self.args.upload}')
            file_buffer = b''
            while True:
                data = client_socket.recv(4096) #* https://docs.python.org/3/library/socket.html#socket.socket.recv
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, 'wb') as file:
                file.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())
            
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    #! Bug in the books code, had to decode the buffer 
                    prompt = 'RepCat# > '
                    prompt = prompt.encode()
                    #! The send needed to be encoded
                    client_socket.send(prompt)
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64) #* https://docs.python.org/3/library/socket.html#socket.socket.recv
                    response = self.execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    #* reset the command buffer so you don't have errors dumped back to the client forever (next line below)
                    cmd_buffer = b''
                    error = str(e)
                    client_socket.send(error.encode())
                    # self.socket.close()
                    # sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="BHP repcat", formatter_class=argparse.RawDescriptionHelpFormatter,epilog=textwrap.dedent('''Example:
        repcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
        repcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload a file
        repcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command echo 'ABC' | ./repcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
        repcat.py -t 192.168.1.108 -p 5555 # connect to the server
    '''))

parser.add_argument('-c', '--command', action='store_true', help='command shell')
parser.add_argument('-e', '--execute', help='execute specified command')
parser.add_argument('-l', '--listen', action='store_true', help='listen')
parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
parser.add_argument('-u', '--upload', help='upload file')

args = parser.parse_args()
if args.listen:
    buffer = ''
else:
    buffer = sys.stdin.read()

RepCat = RepCat(args, buffer.encode())
RepCat.run()