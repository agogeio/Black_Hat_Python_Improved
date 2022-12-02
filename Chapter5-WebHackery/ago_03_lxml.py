
from io import BytesIO
from lxml import etree
#* etree - https://lxml.de/parsing.html
#? etree stands for element tree

import requests

#? Need to know concepts
#?  What are bytes
#?  HTTP status codes
#?  HTTP methods (GET. POST, PUT, DELETE)
#?  bytes - https://docs.python.org/3/library/stdtypes.html?highlight=bytes#bytes-objects

url = 'http://localhost'
#! The URL https://nostarch.com/ doesn't seem to work

resp = requests.get(url=url)
html_bytes = resp.content
parser = etree.HTMLParser()
content = etree.parse(BytesIO(html_bytes), parser=parser)

#* https://lxml.de/parsing.html#parsing-html
#* The following examples also use StringIO or BytesIO to show 
#* how to parse from files and file-like objects. Both are available in the io module:

print(type(html_bytes))
print(type(BytesIO(html_bytes)))


for link in content.findall('//a'):
    print(f"{link.get('href')} -> {link.text}")
