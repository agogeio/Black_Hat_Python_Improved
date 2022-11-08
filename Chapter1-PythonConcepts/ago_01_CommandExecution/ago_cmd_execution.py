import subprocess

def execute_cmd(cmd):
    cmd = input('cmd:' )
    cmd = cmd.strip()

    try:
        results = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        #? The recommended approach to invoking subprocesses is to use the run() function for all use cases it can handle. 
        #*
        #* https://docs.python.org/3/library/subprocess.html#subprocess.run
        #* 'shell = True' will take a literal string and pass it to the command line, this can lead to shell injection
        #* 'text = True' converts the default byte stream into strings
        #* 'capture_output' allows stdout, stderr, return code, etc to be returned from the command
        #! subprocess.run() is NOT an effective way to change directories within a script when you need to maintain state
        #*
        if results.returncode == 127:
            return('Command not found')
        else:
            return(results.stdout)
    except Exception as e:
        return(str(e))