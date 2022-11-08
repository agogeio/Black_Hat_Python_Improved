#FOUND ON PAGE 12 of BHP


import socket       # https://docs.python.org/3.10/library/socket.html?highlight=socket#module-socket
import threading    # https://docs.python.org/3.10/library/threading.html?highlight=threading#module-threading


IP = '0.0.0.0'
PORT = 10000

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP,PORT))
    # https://docs.python.org/3/howto/sockets.html
    # Finally, the argument to listen tells the socket library that we want it to queue 
    # up as many as 5 connect requests (the normal max) before refusing outside connections. 
    # If the rest of the code is written properly, that should be plenty.
    server.listen(5)
    print(f'[*] Listening on {IP}:{PORT}')
    
    while True:
        # https://www.w3schools.com/python/python_tuples_unpack.asp
        #? Cover unpacking
        # connection = server.accept()
        # print(connection)
        client, address = server.accept()
        print(f"{client} : {address}")
        client_handler =  threading.Thread(target=handle_client, args=(client,))
        client_handler.start()
        
def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f"[*] Recieved: {request.decode('utf-8')}")
        sock.send(b'ACK')
    
#* https://docs.python.org/3/library/__main__.html 
#* Explain how the __name__ / __main__ situation works
if __name__ == '__main__':
    main()
    
    
# use lsof -i -P -n to find the process that's listening then kill