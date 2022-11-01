# FOUND ON PAGE 19 of BHP

from ast import arg
import sys
import socket
import threading

HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)]) # SRC - https://code.activestate.com/recipes/142812/

def hex_dump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()


    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i+length])

        #* str.translate() - https://www.w3schools.com/python/ref_string_translate.asp 
        printable = word.translate(HEX_FILTER)
        #* ord() - https://www.w3schools.com/python/ref_func_ord.asp
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length*3
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
    
    if show:
        for line in results:
            print(line)
        else:
            return results


def recieve_from(connection):
    buffer = b""
    connection.settimeout(10)

    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        print(f"{e}")

    return buffer


def request_handler(buffer):
    return buffer


def response_handler(buffer):
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, recieve_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if recieve_first:
        remote_buffer = recieve_from(remote_socket)
        hex_dump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        #? Why is this not an f string?
        print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
        client_socket.send(remote_buffer)

    while True:
        local_buffer = recieve_from(client_socket)
        if len(local_buffer):
            #? Why is this not an f string?
            line = "[==>] Recieved %d bytes to localhost." % len(local_buffer)
            print(line)
            hex_dump(local_buffer)

        local_buffer = request_handler(local_buffer)
        remote_socket.send(local_buffer)
        print("[==>] Sent to remote")

        remote_buffer = recieve_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Recieved %d bytes to remote." % len(remote_buffer))
            hex_dump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data, closing connections")
            break

            
def server_loop(local_host, local_port, remote_host, remote_port, recieve_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print(f"Problem on bing {str(e)}")
        print(f"[!!] Failed to listen on {local_host} on port {local_port}")
        print(f"[!!] Check for other listening sickets or correct permissions")
        sys.exit(0)

    print(f"Listening on {local_host} on port {local_port}")
    server.listen(10)
    while True:
        client_socket, addr = server.accept()
        print(f"Recieved incoming connection from {local_host} on port {local_port}")

        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, recieve_first))
        proxy_thread.start()


def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./bhp_tcp_proxy.py localhost localport", end='')
        print("remotehost remoteport recieve_first")
        print("Example: ./bhp_tcp_proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    recieve_first = sys.argv[5]

    if "True" in recieve_first:
        recieve_first = True
    else:
        recieve_first = False

    server_loop(local_host, local_port, remote_host, remote_port, recieve_first)

if __name__ == '__main__':
    main()

# hex_dump("This is informtion that we will convert to HEX A")