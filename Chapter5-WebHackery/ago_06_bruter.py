import queue
import requests
import sys
import threading

#! With a real long word list the, script will not provide any meaningful output
#! Recommend starting with a smaller wordlist 

AGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
EXTENSIONS = ['.php', '.bak', '.bkp', '.org', '.inc', '.tmp']
TARGET = 'http://testphp.vulnweb.com/'
THREADS = 50
WORDLIST = './Chapter5-WebHackery/ago_00_needed_lab/wordlist.txt'

def get_words(resume=None):

    def extend_words(word):
        if '.' in word:
            words.put(f'/{word}')
        else:
            words.put(f'/{word}/')

        for extension in EXTENSIONS:
            words.put(f'{word}{extension}')

    with open(WORDLIST) as file:
        raw_words = file.read()

    found_resume = False
    words = queue.Queue()

    for word in raw_words.split():
        if resume is not None:
            if found_resume:
                extend_words(word)
            elif word == resume:
                found_resume = True
                print(f'Resuming wordlist from: {resume}')
        else:
            # print(word)
            extend_words(word)

    return words


def dir_bruter(words):
    headers = {'User-Agent': AGENT}

    while not words.empty():
        url = f'{TARGET}{words.get()}'
        try:
            r = requests.get(url=url, headers=headers)
        except requests.exceptions.ConnectionError:
            sys.stderr.write('x')
            sys.stderr.flush()
            continue

    if r.status_code == 200:
        print(f'Success ({r.status_code}: {url})')
    elif r.status_code == 404:
        # print(f'Not found: ({r.status_code}: {url})')
        sys.stderr.write('.')
        sys.stderr.flush()
        pass
    else:
        print(f'Other ({r.status_code}: {url})')


if __name__ == '__main__':
    words = get_words()

    # print(f'Paths that will be brute forced are:\n')
    # for word in words.queue:
    #     print(word)

    print('Press return to continue with brute force operation')
    sys.stdin.readline()

    for _ in range(THREADS):
        thread = threading.Thread(target=dir_bruter, args=(words,))
        #? When you create a new thread you have to tell it the target function
        #? You also much use the 'args' keyword to pass argeuments to the function
        #? args expects a tupil which is why you need 'words,'
        thread.start()

#! You can show this running if you have PiHole in the PiHole 'Tools -> Tail pihole.log'