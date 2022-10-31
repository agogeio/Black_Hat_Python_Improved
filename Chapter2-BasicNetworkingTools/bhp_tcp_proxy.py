# FOUND ON PAGE 19 of BHP

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


hex_dump("This is informtion that we will convert to HEX A")