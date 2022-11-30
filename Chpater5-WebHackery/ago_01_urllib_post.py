import urllib.parse
import urllib.request

#! This needs an webpage for a lab to show it works

#? Need to know concepts
#?  What are bytes
#?  HTTP status codes
#?  HTTP methods (GET. POST, PUT, DELETE)

url = 'http://localhost'

info = {'user': "Steven", 'passwd': '1234567'}
# print(type(info))
data = urllib.parse.urlencode(info).encode()
# print(type(data))

#? info was a dict
#? the parse.urlencode() converted it into a string
#? encode() converted it into bytes

req = urllib.request.Request(url, data)

with urllib.request.urlopen(req) as response:
    content = response.read()

print(content.decode())