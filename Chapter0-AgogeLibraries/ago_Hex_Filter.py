def hex_dump(src, length=16, show=True):

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
