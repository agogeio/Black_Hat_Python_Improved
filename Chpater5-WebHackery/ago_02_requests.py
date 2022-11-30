import requests

#? Need to know concepts
#?  What are bytes
#?  HTTP status codes
#?  HTTP methods (GET. POST, PUT, DELETE)

url = 'http://localhost'

response = requests.get(url)

# print(response)
# print(response.text)


info = {'user': "Steven", 'passwd': '1234567'}
response = requests.post(url, data=info)

print(response)
print(response.content) #? byte string
print(response.text)    #? string