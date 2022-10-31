
# ASCII Character List - https://theasciicode.com.ar/
# Source - https://code.activestate.com/recipes/142812/
# Review list comprehension - https://www.w3schools.com/python/python_lists_comprehension.asp

#? What is this line doing
# HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

# print(chr(65))
# print(chr(30))

# print(repr(chr(65)))
# print(repr(chr(30)))

print(f'Just A: {ord("A")}')

print((f'A:02X: {ord("A"):02X}'))

print((f'{ord(0):02X}'))