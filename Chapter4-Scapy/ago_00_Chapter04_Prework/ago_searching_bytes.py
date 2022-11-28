
#! Understanding bits and bytes 
#* https://web.stanford.edu/class/cs101/bits-bytes.html


message = 'Learning Black Hat Python...\r\n\r\nis fun for everyone'
#? convert string to bytes
bytes = bytes(message, 'utf-8')


#? Show the type of data we're working with and how it's displayed
print(type(bytes))
print(bytes)


#? decode the bytes 
print(bytes.decode())


#! Searching before '\r\n\r\n'
#? Demo searching through a byte string with a slice
results = bytes[:bytes.index(b'\r\n\r\n')]
print(results)


#? Demo searching through a byte string with a slice -3 bits
results = bytes[:bytes.index(b'\r\n\r\n') -3]
print(results)


#! Searching after '\r\n\r\n'
results = bytes[bytes.index(b'\r\n\r\n'):]
print(results)


results = bytes[bytes.index(b'\r\n\r\n') +4:]
print(results)


#! Printing everyother letter with ::2
results = bytes[::2]
print(results)


