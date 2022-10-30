#FOUND ON PAGE 10 of BHP

import socket                   # https://docs.python.org/3.10/library/socket.html?highlight=socket#module-socket
from urllib import response     # https://docs.python.org/3.10/howto/urllib2.html?highlight=urllib

target_host = "localhost"
target_port = 10000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host,target_port))

#! https://www.rfc-editor.org/rfc/rfc9110.html
#? Explained what's being sent in the byte array
# client.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
msg = input("Enter the message you would like to send: ")

#! https://docs.python.org/3/howto/unicode.html
#? Explains what the encode() function is doing
print(type(msg))
print(type(msg.encode()))
client.send(msg.encode())
# client.send(b"This is my message")
client.send(b"")

#? Note an error with the recv() method, it will only recieve
#? the buffer size assigned even if the response is larger
#? the rest of the message will be lost
response = client.recv(4096)

print(response.decode())

client.close()