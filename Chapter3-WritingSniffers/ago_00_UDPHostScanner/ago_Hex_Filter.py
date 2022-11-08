def hex_dump(src, length=16, show=True):

    print(type(src))

    HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)]) # SRC - https://code.activestate.com/recipes/142812/

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



hex_dump(b'E \x00T\x00\x00\x00\x006\x01\xb8\x1e\x8e\xfa{d\xc0\xa8\x01d\x00\x00C.!\xe6\x00\x03\xb1^jc\x00\x00\x00\x00\xb4S\x0c\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567')