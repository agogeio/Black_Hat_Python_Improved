import socket       # https://docs.python.org/3.10/library/socket.html?highlight=socket#module-socket
import threading    # https://docs.python.org/3.10/library/threading.html?highlight=threading#module-threading

IP = '0.0.0.0'
PORT = 9999
ADDRESS = (IP,PORT) 

def main():
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #? AF_INET and is ths default, means IPv4 & SOCK_STREAM means TCP (not UDP)
    #* Strongly recommend reading the socket.socket documentation
    #* https://docs.python.org/3/library/socket.html?highlight=socket%20inet#socket.socket

    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #? This option controls whether bind should permit reuse of local addresses
    #? for this socket. If you enable this option, you can actually have two sockets
    #? with the same Internet port number; but the system won’t allow you to use the two 
    #? identically-named sockets in a way that would confuse the Internet. The reason for  
    #? this option is that some higher-level Internet protocols, including FTP, require you 
    #? to keep reusing the same port number. The value has type int; a nonzero value means “yes”.

    #? Translated: If we don't have this option, and our program terminates, we have to wait until the 
    #? socket is freed by the OS instead of being able to use it again right away.

    #* SOL_SOCKET = https://www.gnu.org/software/libc/manual/html_node/Socket_002dLevel-Options.html
    #* SO_REUSEADDR = http://www.unixguide.net/network/socketfaq/4.11.shtml
    #* The SOL_SOCKET link is a good explination for both options


    tcp_server.bind(ADDRESS)
    #? the bind() method takes a tuple
    #* https://www.w3schools.com/python/python_tuples.asp

    tcp_server.listen(10)
    print(f'[+] Listening on {ADDRESS}')

    while True:
        conn, address = tcp_server.accept()
        #? Accept a connection. The socket must be bound to an address and listening for connections. 
        #? The return value is a pair ** (conn, address) ** where conn is a new socket object usable to send 
        #? and receive data on the connection, and address is the address bound to the socket on the 
        #? other end of the connection.
        #* https://docs.python.org/3/library/socket.html?highlight=socket%20inet#socket.socket.accepts

        print(f'[+] Accepted connectio from {address[0]}:{address[1]}')

        client = threading.Thread(target=client_handler, args=(conn,))
        # client = threading.Thread(target=print, args=(conn,))
        #? target is the callable object to be invoked by the run() method. 
        #? Defaults to None, meaning nothing is called. For example you 
        #? could have the Thread call the ** print ** method
        #* https://docs.python.org/3/library/threading.html?highlight=threading#threading.Thread

        client.start()


def client_handler(client_thread):
    with client_thread as client_socket:
    # print(type(client_socket))
    #? By using the print(type()) on the variable you can see 
    #? the object is a client socket
    #* https://www.geeksforgeeks.org/with-statement-in-python/
        


        while True:
    
            message = client_socket.recv(1024)
            message = message.decode()
            #? Return a string decoded from the given bytes. Default encoding is 'utf-8'.
            #? Translated - Turns bytes into a string
            #* https://docs.python.org/3/library/stdtypes.html#bytes.decode
            print(f'[+] Recived: {message}')

            response = input('Enter a response: ')
            response = response + '\n'
            response = response.encode()
            #? Return an encoded version of the string as a bytes object. Default encoding is 'utf-8'.
            #? Translated - Turns a string into bytes
            #* https://docs.python.org/3/library/stdtypes.html#str.encode
            client_socket.send(response)


if __name__ == '__main__':
    main()