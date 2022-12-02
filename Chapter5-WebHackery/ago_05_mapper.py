import contextlib
import os
import queue
import requests
import sys
import threading
import time

#? Need to know concepts
#?  context manager

#! Additional materal, how to hash all the files in a web directory 
#! to make sure they haven't been altered

FILTERED = ['.jgp', '.gif', '.png', '.css']
TARGET = 'http://localhost/wordpress'
THREADS = 10

answers = queue.Queue()
web_paths = queue.Queue()

#* https://docs.python.org/3/library/queue.html#queue-objects
#? Three types of queues:
#? FIFO, LIFO, Priority 
#* https://docs.python.org/3/library/queue.html#queue-objects
#? Queue.qsize()
#? Queue.empty()
#? etc...

def gather_paths():
    for dirpaths, dirnames, filenames in os.walk('.'):
        #* https://docs.python.org/3/library/os.html?highlight=os%20walk#os.walk
        #* Generate the file names in a directory tree by walking the tree either 
        #* top-down or bottom-up. For each directory in the tree rooted at directory 
        #* top (including top itself), it yields a 3-tuple (dirpath, dirnames, filenames). 
        #* in our example: root = dirpaths, _ = dirnames, files = filenames
        # print(f'{dirpaths}')
        # print(f'{dirnames}')
        # for name in dirnames:
        #     print(name)
        # print(f'{filenames}')
        #? We will get all of our subdirectory names and then map all the files in each sub directory

        for fname in filenames:
            if os.path.splitext(fname)[1] in FILTERED:
                # print(f'{fname} will be filtered')
                #? If we run this on the whole directory our PCAP png exports will be filtered
                #? This could also be used to search for things like Excel docs or Access 
                #? databases in an offensive situation
                continue
            path = os.path.join(dirpaths, fname)
            # print(path)
            #! This can be very nice to track changes to files on web servers
            #? print(type(path)) is type string
            if path.startswith('.'):
                #* https://docs.python.org/3/library/stdtypes.html?highlight=startswith#str.startswith
                #* Return True if string starts with the prefix, otherwise return False. prefix can also 
                #* be a tuple of prefixes to look for. With optional start, test string beginning at that 
                #* position. With optional end, stop comparing string at that position.
                path = path[1:] #? stripping the '.' off current directory

                #? This will remove git files
                #! if path.startswith('/.git') or path.startswith('.git'):
                #!     path = path[1:]
                #! else:
                #!     print(path)
                #!     web_paths.put(path)


@contextlib.contextmanager
def chdir(path):
    """
    On enter, change directory to the specific path
    On exit, change directory back to origional
    """

    this_dir = os.getcwd() 
    #* https://docs.python.org/3/library/os.html?highlight=os%20getcwd#os.getcwd
    #* Return a string representing the current working directory.

    os.chdir(path)
    #* https://docs.python.org/3/library/os.html?highlight=os%20chdir#os.chdir
    #* Change the current working directory to path.

    try:
        yield
        #* https://www.geeksforgeeks.org/use-yield-keyword-instead-return-keyword-python/
        #* The yield statement suspends a function’s execution and sends a value back to the caller, 
        #* but retains enough state to enable the function to resume where it left off. 
        #* When the function resumes, it continues execution immediately after the last yield run. 
        #* This allows its code to produce a series of values over time, rather than computing them 
        #* at once and sending them back like a list.
    finally:
        os.chdir(this_dir)


def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = f'{TARGET}{path}'
        print(url)
        time.sleep(5)

        response = requests.get(url=url)

        if response.status_code == 200:
            answers.put(url)
            sys.stdout.write('+')
        else:
            sys.stdout.write('x')
        sys.stdout.flush()



def run():

    pass