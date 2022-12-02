import urllib.parse
import urllib.request

#? Need to know concepts
#?  What are bytes
#?  HTTP status codes

url = 'http://localhost'

#! url = 'https://www.meijer.com/' 
#! some sites will have security on them and will not allow you to access them
#! meijer will send back a 403 Forbidden

#* https://docs.python.org/3/reference/compound_stmts.html#the-with-statement 
#* https://www.geeksforgeeks.org/with-statement-in-python/
with urllib.request.urlopen(url) as response:
    # print(type(response))
    html = response.read()

print(type(html))


# response = urllib.request.urlopen(url)
# html = response.read()
# print(type(html))
#? when the urllib is read it will return a byte string
# print(html.decode())
#? Some websites will decode nicely (localhosst) others may not (google)