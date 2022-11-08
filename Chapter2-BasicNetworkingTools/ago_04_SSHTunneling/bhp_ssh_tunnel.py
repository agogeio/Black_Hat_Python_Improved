import ago_execute_cmd

while True:
    cmd = input('enter a command: ')
    cmd = cmd.strip()

    if cmd != 'exit':
        results = ago_execute_cmd.execute_cmd(cmd)
        print(results)
    elif cmd == 'exit':
        break