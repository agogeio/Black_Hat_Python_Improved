from scapy.all import TCP, rdpcap
from collections import namedtuple

import os
import re       #* Regular Expressions - https://docs.python.org/3.10/library/re.html?highlight=re#module-re
import sys
import zlib     #* gzip compatable lib - https://docs.python.org/3.10/library/zlib.html?highlight=zlib#module-zlib

OUTDIR = '/home/saiello/Pictures/agoge'
PCAPS =  '/home/saiello/Downloads/agoge'

Response = namedtuple('Response', ['header', 'payload'])


def get_header(payload):
    try:
        header_raw = payload[:payload.index(b'\r\n\r\n')+2]
        #? Figure out what this is
    except Exception as e:
        sys.stdout.write('No Headers found\n')
        sys.stdout.flush()
        return None

    header = dict(re.findall(r'(?P<name>.*?): (?P<value>.*?)\r\n',header_raw.decode()))
    #* header_raw.decode()
    #* https://docs.python.org/3.10/library/stdtypes.html?highlight=decode#bytes.decode
    #* Return a string decoded from the given bytes. Default encoding is 'utf-8'.

    if 'Content-Type' not in header:
        return None
    return header


def extract_content(Response, content_name='image'):
    content, content_type = None, None
    if content_name in Response.header['Content-Type']:
        content_type = Response.header['Content-Type'].split('/')[1]
        content = Response.payload[Response.payload.index(b'\r\n\r\n')+4:]

    if 'Content-Encoding' in Response.header:
        if Response.header['Content-Encoding'] == 'gzip':
            content = zlib.decompress(Response.payload, zlib.MAX_WBITS | 32)
        elif Response.header['Content-Encoding'] == "deflate":
            content = zlib.decompress(Response.payload)

    return content, content_type


class Recapper:
    def __init__(self, fname) -> None:
        pass

    def get_responses(self):
        pass

    def write(self, content_name):
        pass


if __name__ == '__main__':
    pfile = os.path.join(PCAPS, 'agoge.pcap')
    get_header(pfile)
    # recapper = Recapper(pfile)
    # recapper.get_responses()
    # recapper.write('image')