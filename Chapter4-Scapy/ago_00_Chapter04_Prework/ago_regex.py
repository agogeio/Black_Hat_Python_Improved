import json
import re       #* Regular Expressions - https://docs.python.org/3.10/library/re.html?highlight=re#module-re



text_string = 'This is a nice string: we should use it some time'
text_bytes = bytes(text_string, 'utf-8')
results = dict(re.findall(r'(?P<name>.*?): (?P<value>.*?)', text_string))
print(results)
# {'This is a nice string': ''}


text_string = 'This is a nice string: we should use it some time\r\n'
text_bytes = bytes(text_string, 'utf-8')
results = dict(re.findall(r'(?P<name>.*?): (?P<value>.*?)\r\n', text_string))
print(results)
# {'This is a nice string': 'we should use it some time'}





headers = 'HTTP/1.1 200 OK\r\nServer: Werkzeug/2.2.2 Python/3.10.7\r\nDate: Thu, 24 Nov 2022 13:51:37 GMT\r\nContent-Disposition: inline; filename=Monkey.PNG\r\nContent-Type: image/png\r\nContent-Length: 119597\r\nLast-Modified: Thu, 24 Nov 2022 13:48:23 GMT\r\nCache-Control: no-cache\r\nETag: "1669297703.\r\n5241787-119597-2748457067"\r\nDate: Thu, 24 Nov 2022 13:51:37 GMT\r\nConnection: close'

bytes = bytes(headers, 'utf-8')
# print(bytes)

header = dict(re.findall(r'(?P<name>.*?): (?P<value>.*?)\r\n',bytes.decode()))

#? Regex syntax with P<name>
#* https://docs.python.org/3.10/library/re.html?highlight=re#regular-expression-syntax
#* Similar to regular parentheses, but the substring matched by the group is accessible 
#* via the symbolic group name name. Group names must be valid Python identifiers, 
#* and each group name must be defined only once within a regular expression. 
#* A symbolic group is also a numbered group, just as if the group were not named.

#? re.findall()
#* https://docs.python.org/3.10/library/re.html?highlight=re#re.findall
#* Return all non-overlapping matches of pattern in string, as a list of strings or tuples. 
#* The string is scanned left-to-right, and matches are returned in the order found. Empty matches are included in the result.



# print(json.dumps(header, sort_keys=False, indent=4))